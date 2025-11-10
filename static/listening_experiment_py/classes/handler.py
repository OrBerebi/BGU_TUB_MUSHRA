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

        print("Connecting to Pd on port", self._pd_port)
        try:
            self.init_pd_listener()

        except Exception as e2:
            print("❌ Failed to connect to Pd:", e2)
            self._connection_state_pd = False
            


    def init_pd_listener(self):
        self._osc_client = SimpleUDPClient("127.0.0.1", self._pd_port)
        self._connection_state_pd = True
        print(f"✅ Connected to Pd via UDP OSC at 127.0.0.1:{self._pd_port}")

        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/bang", self.bang_handler)

        ip = "127.0.0.1"
        port = 5005
        self.server = osc_server.ThreadingOSCUDPServer((ip, port), self.dispatcher)
        print(f"Listening on {ip}:{port} to PD for Bangs!")

        # Run server in background thread
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

    def pd_send_sel(self,file_id: int):
        """Select a file (like id_1, id_2,....)."""
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

        elif bang_type == "bang_2":
            print("Got bang_2 from Pd!")

        else:
            print("Unknown bang content:", bang_type)


    def select_source(self, src_id):
        print('Activate Source ', src_id)
        if src_id > self._num_sources + 1:
            raise ValueError('Source does not exist')
        else:
            if self._connection_state_pd:
                self.pd_send_play()
                self.pd_send_sel(src_id)
            else:
                print('Someting is wrong with PD')


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
        

    def mute_all(self):
        """Mute all sources, stop playback, rewind, and reset any pending timers."""
        if self._verbose:
            print('Mute all sources and reset playback')
        
        if self._connection_state_pd:
            self.pd_send_stop()
        else:
            print('Someting is wrong with PD')

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

    

