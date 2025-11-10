import numpy as np
import socket
import os.path
import os
import sys
import scipy.io as scyio
import rtmidi
import threading
import time
import xml.etree.ElementTree as ET
import re
import wave
from PyQt5 import QtCore
from pythonosc.udp_client import SimpleUDPClient
from pythonosc import dispatcher, osc_server



class ExperimentHandler():
    def __init__(self, ssr_ids, base_path='listening_experiment',
                 debug=False, test_signal_list=None,
                 binaural_playback_mode=False):
        self.ssr_ids = np.asarray(ssr_ids)
        self._overall_id_cnt = 0
        self._base_path = base_path
        self._debug = debug
        self._result_file_name = []

        if test_signal_list is None:
            self.binaural_playback_mode = True
        else:
            self.binaural_playback_mode = binaural_playback_mode

        self.test_signal_list = test_signal_list

    def _init(self, reset):
        # check and prepare path for results
        if not self._debug:
            # check if directory exists
            if not os.path.isdir(self._base_path):
                try:
                    os.mkdir(self._base_path)
                except Warning:
                    print(f'Could not create dir {self._base_path}!',
                          file=sys.stderr)

            # check if participant counter exists
            if not os.path.isfile(f'{self._base_path}/overall_id_cnt.mat') or reset:
                scyio.savemat(f'{self._base_path}/overall_id_cnt.mat',
                              {'overall_id_cnt': self._overall_id_cnt})
            else:
                self._overall_id_cnt = int(scyio.loadmat(
                    f'{self._base_path}/overall_id_cnt.mat')['overall_id_cnt'][0] + 1)
                scyio.savemat(f'{self._base_path}/overall_id_cnt.mat',
                              {'overall_id_cnt': self._overall_id_cnt})

            # create result file
            if not os.path.isdir(f'{self._base_path}/results'):
                try:
                    os.mkdir(f'{self._base_path}/results')
                except Warning:
                    print(f'Could not create dir {self._base_path}/results!',
                          file=sys.stderr)
            self._result_file_name = f'{self._base_path}/results/results_subj{self._overall_id_cnt}'
        self._randomize()
        print('finish setting up experiment')

    def _randomize(self):
        pass

    def set_participant_infos(self, infos):
        pass

    def next_trial(self):
        pass

    def write_results(self):
        pass


class SSRhandler():
    def __init__(self, num_sources=3, tcp_ip='127.0.0.1', tcp_port=4711,
                 pd_port=6672, verbose=True):
        """
        Listening Experiment Py: SSR handler with Pd fallback
        """

        self._tcp_ip = tcp_ip
        self._tcp_port = tcp_port
        self._pd_port = pd_port
        self._connection_state = False
        self._connection_state_pd = False
        self._is_calibrated = 0
        self._verbose = verbose
        self._stop_timer = None
        self._s = None
        self._osc_client = None
        self._num_sources = num_sources

        self.stopGifSignal   = None
        self.rewindGifSignal = None
        self.playGifSignal   = None
        self.playing_label   = None

        try:
            # Try TCP connection to SSR
            self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._s.connect((self._tcp_ip, self._tcp_port))
            print("✅ Connected to SSR at {}:{}".format(self._tcp_ip, self._tcp_port))
            self._connection_state = True

            # SSR init sequence
            self.processing_start()
            self.transport_stop()
            self.transport_rewind()
            self._source_durations = self.get_durr_list()
            self.transport_stop()
            self.transport_rewind()
            self.transport_start()
            self._num_sources = int(len(self._source_durations)/2)

        except (ConnectionRefusedError, OSError) as e:
            print("⚠️ Could not connect to SSR at {}:{} ({})".format(self._tcp_ip, self._tcp_port, e))
            print("👉 Falling back to Pd on port", self._pd_port)

            # Fallback: UDP OSC client for Pd
            try:
                self.init_pd_listener()

            except Exception as e2:
                print("❌ Failed to connect to Pd as well:", e2)
                self._connection_state_pd = False
            
            
            

            #self.pd_send_play()


    def init_pd_listener(self):
        self._osc_client = SimpleUDPClient("127.0.0.1", self._pd_port)
        self._connection_state_pd = True
        print(f"✅ Connected to Pd via UDP OSC at 127.0.0.1:{self._pd_port}")

        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/bang", self.bang_handler)

        ip = "127.0.0.1"
        port = 5005
        self.server = osc_server.ThreadingOSCUDPServer((ip, port), self.dispatcher)
        print(f"Listening on {ip}:{port} to PD for bangs")

        # Run server in background thread
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

    def pd_send_sel(self,file_id: int):
        """Select a file (like file1, file2)."""
        self._osc_client.send_message("/stop", "stop")
        sel_str = f"id_{file_id}"
        self._osc_client.send_message("/sel", sel_str)
        print(f"sent: /sel {sel_str}")

    def pd_send_play(self):
        """Send play command."""
        self._osc_client.send_message("/play", "play")
        print("sent: /play play")

    def pd_send_stop(self):
        """Send stop command."""
        self._osc_client.send_message("/stop", "stop")
        print("sent: /stop stop")

    def bang_handler(self,address, *args):
        if address != "/bang":
            return  # ignore other OSC messages

        if not args:
            print("⚠ Received /bang with no content")
            return

        bang_type = args[0]  # first argument sent by Pd

        if bang_type == "bang_1":
            print("Got bang_1 from Pd!")
            if self.stopGifSignal and self.rewindGifSignal and self.playGifSignal and self.playing_label:
                self.playing_label.setText("Playing Src")
                self.stopGifSignal.emit()
                self.rewindGifSignal.emit()
                self.playGifSignal.emit()

        elif bang_type == "bang_2":
            print("Got bang_2 from Pd!")
            if self.stopGifSignal and self.rewindGifSignal and self.playGifSignal and self.playing_label:
                self.playing_label.setText("Playing Non")
                self.stopGifSignal.emit()
                self.rewindGifSignal.emit()

        else:
            print("Unknown bang content:", bang_type)




    def destroy_handler(self):
        try:
            self._s.close()
        except:
            print('No SSR TCP connection running, nothing to stop')


    def def_ssr_handler_gui_link(ui_label):
        self.ui = ui_label


    def get_durr_list(self):
        # Gets a list of signal length in seconds for each source. (helps with reseting the playback)
        def parse_source_lengths_regex(xml_response, sample_rate=48000):
            lengths = {}
            # Matches: id="1" ... length="323307"
            pattern = r'id="(\d+)"[^>]*length="(\d+)"'
            for match in re.finditer(pattern, xml_response):
                src_id = int(match.group(1))
                length_samples = int(match.group(2))
                lengths[src_id] = length_samples / sample_rate
            return lengths

        # Ensure SSR is ready
        self._send_xml('<request><source id="1" mute="true"/></request>')
        resp = self._recv_xml_response()
        list_durr = parse_source_lengths_regex(resp)
        print(list_durr)
        return list_durr

    # ---------------- xml utilities ----------------
    def _send_xml(self, xml):
        """Send one XML request, terminated with binary zero as required by SSR."""
        try:
            self._s.send((xml + '\0').encode('utf-8'))
        except Exception as e:
            if self._verbose:
                print(f'No SSR TCP connection running! ({e})')

    def _recv_xml_response(self, timeout=0.5):
        """
        Read a single SSR XML response (terminated by \0). Non-blocking-ish:
        returns whatever arrived before timeout (empty string if none).
        """
        if not self._connection_state:
            return ''
        old_to = None
        try:
            old_to = self._s.gettimeout()
            self._s.settimeout(timeout)
        except:
            old_to = None

        chunks = []
        try:
            while True:
                data = self._s.recv(4096)
                if not data:
                    break
                if b'\0' in data:
                    before, _, _ = data.partition(b'\0')
                    chunks.append(before)
                    break
                chunks.append(data)
        except socket.timeout:
            pass
        except Exception as e:
            if self._verbose:
                print(f'Error receiving SSR response: {e}')
        finally:
            try:
                self._s.settimeout(old_to)
            except:
                pass

        try:
            return b''.join(chunks).decode('utf-8', errors='ignore')
        except:
            return ''


    # ---------------- timer utilities ----------------
    def _cancel_stop_timer(self):
        """Stop and clear any pending stop timer."""
        if getattr(self, '_stop_timer', None) is not None:
            try:
                self._stop_timer.cancel()
            except:
                pass
            self._stop_timer = None

    def _on_stop_timer(self):
        """Called by the Timer when playback should end."""
        if self._verbose:
            print('Stop timer expired — stopping transport')
        try:
            self.transport_stop()
        finally:
            self._cancel_stop_timer()

    # ---------- transport & processing ----------
    def processing_start(self):
        self._send_xml('<request><state processing="start"/></request>')  # start DSP

    def processing_stop(self):
        self._send_xml('<request><state processing="stop"/></request>')  # start DSP

    def transport_stop(self):
        self._send_xml('<request><state transport="stop"/></request>')    # pause

    def transport_rewind(self):
        # Either rewind or seek to 0; both are valid:
        # self._send_xml('<request><state seek="0"/></request>')
        self._send_xml('<request><state transport="rewind"/></request>')  # go to 0

    def transport_start(self):
        self._send_xml('<request><state transport="start"/></request>')   # play
    

    def play_source_once(self, src_id, playing_label, playGifSignal, stopGifSignal, rewindGifSignal):
        """
        Play a pair of sources sequentially: [reference_id, selected_id].
        Each is played from start to finish, with automatic stop after the last source.
        GIF playback is synced with each source.
        """
        safety_buffer = 0.1
        self.playGifSignal = playGifSignal
        self.stopGifSignal = stopGifSignal
        self.rewindGifSignal = rewindGifSignal
        self.playing_label = playing_label

        # --- Helper to start a stereo source ---
        def _start_source(s_id, delay_gif=False):
            real_id_L = (s_id - 1) * 2 + 1
            real_id_R = (s_id - 1) * 2 + 2

            self._send_xml(f'<request><source id="{real_id_L}" mute="false"/></request>')
            self._send_xml(f'<request><source id="{real_id_R}" mute="false"/></request>')
            self.transport_start()

            if delay_gif:
                # Apply 400 ms GIF delay only if requested
                QtCore.QTimer.singleShot(400, lambda: self.playGifSignal.emit())
            else:
                # start GIF immediately
                self.playGifSignal.emit()

            if self._verbose:
                print(f'▶️ Playing source: L_{real_id_L} and R_{real_id_R}')

        # --- Helper to stop all sources ---
        def _stop_all():
            if self._verbose:
                print(f'⏹️ Auto-stopping sources')
            self.transport_stop()
            self.transport_rewind()
            self.mute_all(self.stopGifSignal, self.rewindGifSignal)
            self.processing_stop()
            playing_label.setText("Playing Non")

        def _play_selected():
            # Stop/mute reference
            self.transport_stop()
            self.transport_rewind()
            self.mute_all(self.stopGifSignal, self.rewindGifSignal)

            # Start selected without GIF delay
            _start_source(sel_id, delay_gif=True)
            playing_label.setText("Playing Src")

            # Schedule stop after selected finishes
            QtCore.QTimer.singleShot(total_sel_ms-200, _stop_all)


        if not isinstance(src_id, (list, tuple)) or len(src_id) != 2:
            raise ValueError("src_id must be a list or tuple of two source IDs: [ref, selected]")

        ref_id, sel_id = src_id

        for s_id in src_id:
            if not (1 <= s_id <= self._num_sources):
                raise ValueError(f'Source {s_id} does not exist')

        if self._verbose:
            print(f'▶️ Play sources sequentially: {ref_id} → {sel_id}')

        if self._connection_state_pd:
            self.stopGifSignal.emit()
            self.rewindGifSignal.emit()
            self.playGifSignal.emit()
            playing_label.setText("Playing Ref")
            self.pd_send_sel(sel_id)
            

        else:
            # Cancel any pending stop timers
            self._cancel_stop_timer()

            # Ensure engine running, reset timeline, mute all
            self.processing_start()
            self.transport_stop()
            self.transport_rewind()
            self.mute_all(self.stopGifSignal, self.rewindGifSignal)

            # Get durations from cached dictionary
            dur_ref = self._source_durations[(ref_id - 1) * 2 + 1]
            dur_sel = self._source_durations[(sel_id - 1) * 2 + 1]

            if self._verbose:
                print(f'  -> durations: ref={dur_ref:.3f}s, sel={dur_sel:.3f}s')

            # --- Play reference first ---
            _start_source(ref_id, delay_gif=True)
            playing_label.setText("Playing Ref")

            # Schedule selected source after reference finishes
            total_ref_ms = int((dur_ref + safety_buffer) * 1000)
            total_sel_ms = int((dur_sel + safety_buffer) * 1000)

            # Schedule selected source
            QtCore.QTimer.singleShot(total_ref_ms, _play_selected)


    def select_source(self, src_id):
        print('Activate Source ', src_id)

        if src_id > self._num_sources + 1:
            raise ValueError('Source does not exist')
        else:
            cmd = '<request><source id="{:01d}" mute="true"/></request>\0'
            for idx in range(1, self._num_sources + 1):
                msg = cmd.format(idx)
                try:
                    self._s.send(msg.encode('utf-8'))
                except:
                    if self._verbose:
                        print('No SSR TCP connection running!')


            cmd = '<request><source id="{:01d}" mute="false"/></request>\0'
            msg = cmd.format(src_id)
            try:
                self._s.send(msg.encode('utf-8'))
            except:
                if self._verbose:
                    print('No SSR TCP connection running!')



    def calibrate_tracker(self):
        # Set internal flag
        self._is_calibrated = 1

        try:
            midiout = rtmidi.MidiOut()
            available_ports = midiout.get_ports()

            # Attempt to find the head tracker MIDI port
            for idx, port_name in enumerate(available_ports):
                if "Bridge" in port_name or "Head Tracker" in port_name:
                    midiout.open_port(idx)
                    break
            else:
                print("⚠️  Bridgehead MIDI device not found in ports:")
                for p in available_ports:
                    print(f" - {p}")
                return

            # SysEx message = F0 00 21 42 01 00 01 F7 (as in ZERO button)
            sysex_message = [0xF0, 0x00, 0x21, 0x42, 0x01, 0x00, 0x01, 0xF7]
            midiout.send_message(sysex_message)
            print("✅ Headtracker calibrated via MIDI (ZERO message sent).")

            del midiout

        except Exception as e:
            if self._verbose:
                print(f"❌ Failed to calibrate tracker via MIDI: {e}")
            try:
                self._s.send(b'<request><state tracker="reset"/></request>\0')
                print("🔁 Fallback: Sent reset over TCP to SSR.")
            except:
                if self._verbose:
                    print("⚠️  No SSR TCP connection running!")
        

    """
    def mute_all(self):
        if self._verbose:
            print('Mute all sources')
        else:
            pass

        cmd = '<request><source id="{:01d}" mute="true"/></request>\0'
        for idx in range(1, self._num_sources + 1):
            msg = cmd.format(idx)
            try:
                self._s.send(msg.encode('utf-8'))
            except:
                if self._verbose:
                    print('No SSR TCP connection running!')
    """

    def mute_all(self, stopGifSignal, rewindGifSignal):
        """Mute all sources, stop playback, rewind, and reset any pending timers."""
        if self._verbose:
            print('Mute all sources and reset playback')
        
        # Stop the gif
        stopGifSignal.emit()
        rewindGifSignal.emit()

        if self._connection_state_pd:
            self.pd_send_stop()
        else:
            # Cancel any pending stop timers
            self._cancel_stop_timer()
            # Stop transport and rewind timeline
            self.transport_stop()
            self.transport_rewind()
            # Send mute commands for all sources
            cmd = '<request><source id="{:01d}" mute="true"/></request>\0'
            for idx in range(1, (self._num_sources)*2 +1):
                msg = cmd.format(idx)
                try:
                    self._s.send(msg.encode('utf-8'))
                except:
                    if self._verbose:
                        print('No SSR TCP connection running!')

    def get_connection_state(self):
        cmd = '<request><source id="{:01d}" mute="true"/></request>\0'
        msg = cmd.format(1)
        connection_state = True
        try:
            self._s.send(msg.encode('utf-8'))
        except:
            connection_state = False

        return connection_state

    def reconnect(self):
        self._is_calibrated = 0
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._s.connect((self._tcp_ip, self._tcp_port))
            print('TCP connection to SSR initialized')
        except:
            print('Could not establish TCP connection to SSR, run GUI without SSR')

    def clear_scene(self):
        if self._connection_state:
            if self._verbose:
                print('try clearing ASD scene')

            # clear old scene
            cmd = '<request> <scene clear = "true" /> </request>\0'
            try:
                self._s.send(cmd.encode('utf-8'))
            except:
                if self._verbose:
                    print('No SSR TCP connection running!')
                else:
                    pass

    def load_new_scene(self, fullfilename):
        # clear old scene
        self.clear_scene()

        if self._connection_state:
            if self._verbose:
                print(f'try loading new ASD scene: {fullfilename}')

            # load new scene
            cmd = '<request> <scene load = "{:s}" /> </request>\0'.format(
                fullfilename)
            try:
                self._s.send(cmd.encode('utf-8'))
            except:
                if self._verbose:
                    print('No SSR TCP connection running!')
                else:
                    pass

    

