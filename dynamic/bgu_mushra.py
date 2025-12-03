import sys
import os
import numpy as np
import ast
from PyQt5 import QtCore, QtWidgets
from listening_experiment_py import SSRhandler
from listening_experiment_py.GUI import breeze_resources
from listening_experiment_py.BGU.main_window \
    import MushraMainWindow
from listening_experiment_py.BGU.experiment import Handler

def load_config(filename="config.txt"):
    config = {}
    try:
        with open(filename, "r") as f:
            for line in f:
                key, value = line.strip().split("=", 1)
                config[key.strip()] = ast.literal_eval(value.strip())  # Safely evaluate lists
    except Exception as e:
        print(f"Error reading config file: {e}")
        sys.exit(1)
    return config

def main():

    debug = 0
    language = 'english'
    base_path = 'bgu_results'
    do_reset = 0
    if len(sys.argv) > 1:
        for idx, arg in enumerate(sys.argv[1:]):
            if arg == '--debug':
                debug = 1

            if arg == '--language':
                print(sys.argv[idx+2])
                if sys.argv[idx+2] == 'en':
                    language = 'english'
                elif sys.argv[idx+2] == 'ger':
                    language = 'german'
                else:
                    print('Unknown language, chose english version')
            if arg == '--base_path':
                print(sys.argv[idx+2])
                base_path = sys.argv[idx+2]
            if arg == '--reset':
                print(sys.argv[idx+2])
                do_reset = sys.argv[idx+2]
    if debug:
        print("DEBUG MODE - No results will be printed!")
    else:
        print("Start listening experiment!")

    print(f'Language: {language}')

    # Read config file
    config = load_config()
    stimuli_ssr_ids = config.get("stimuli_ssr_ids", [])
    hidden_references_ids = config.get("hidden_references_ids", [])
    attributes = config.get("attributes", [])
    gifs_paths = config.get("gifs_paths", [])
    gifs_paths = [os.path.abspath(path) for path in gifs_paths]

    sample_lengths = config.get("sample_lengths", [])

    print(gifs_paths)


    
    # init app
    app = QtWidgets.QApplication(sys.argv)

    # init handlers
    num_available_src = np.max(np.max(stimuli_ssr_ids))
    ssr_handler = SSRhandler(num_available_src)
    #exp_handler = Handler(ssr_ids =stimuli_ssr_ids,
    #                      num_stimuli_per_page=5,
    #                      attributes=attributes,
    #                      base_path=base_path,
    #                      debug=debug,
    #                      do_reset=do_reset,
    #                      hidden_references=hidden_references_ids,
    #                      groups = [3,7,11,15])

    exp_handler = Handler(ssr_ids =stimuli_ssr_ids,
                          num_stimuli_per_page=4,
                          attributes=attributes,
                          base_path=base_path,
                          debug=debug,
                          do_reset=do_reset,
                          hidden_references=hidden_references_ids,
                          gifs_paths = gifs_paths,sample_lengths= sample_lengths)

    # init main gui component
    gui_comp = MushraMainWindow(ssr_handler=ssr_handler,
                                 experiment_handler=exp_handler,
                                 debug=debug)

    # set style sheet
    file = QtCore.QFile(":/dark.qss")
    file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    stream = QtCore.QTextStream(file)
    app.setStyleSheet(stream.readAll())
    app.aboutToQuit.connect(gui_comp.close_app)

    # define monitor
    display_monitor = 2
    monitor = QtWidgets.QDesktopWidget().screenGeometry(display_monitor)
    gui_comp.move(monitor.left(), monitor.top())
    # Gui_main_comp.showFullScreen()

    # show GUI
    #gui_comp.show()
    gui_comp.showFullScreen()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
