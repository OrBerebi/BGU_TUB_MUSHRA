import sys
import numpy as np
import ast
from PyQt5 import QtCore, QtWidgets
from listening_experiment_py import SSRhandler
from listening_experiment_py.GUI import breeze_resources
from listening_experiment_py.BGU.main_window \
    import MushraMainWindow
from listening_experiment_py.BGU.experiment import Handler
import pprint

def load_new_config(filename="config.txt"):
    """
    Loads the new, block-based configuration file.

    Parses the file and returns a config dictionary with the keys
    'stimuli_ssr_ids', 'hidden_references_ids', and 'attributes',
    matching the data structure of the original load_config function.
    """
    config = {}
    stimuli_ssr_ids = []
    hidden_references_ids = []
    attributes = []
    attribute_map = {}
    
    window_id = -1  # Will be incremented to 0 for the first block
    current_attribute_id = -1

    try:
        with open(filename, "r") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()

            if not line:
                # Skip empty lines
                continue

            if line.startswith("Qualities:"):
                # This is the attributes definition line
                try:
                    attr_string = line.split(":", 1)[1].strip()
                    # FIX: Split by comma to support multi-word attributes
                    attributes = [attr.strip() for attr in attr_string.split(',')]
                    attribute_map = {name: i for i, name in enumerate(attributes)}
                    
                    if not attributes or attributes == ['']:
                        print("Error: 'Qualities' line is empty or malformed.")
                        sys.exit(1)
                        
                except Exception as e:
                    print(f"Error parsing 'Qualities' line: {e}")
                    sys.exit(1)
            
            elif line.startswith("reference:"):
                # This is a hidden reference ID
                try:
                    source_id = int(line.split(":", 1)[1].strip())
                    if window_id == -1 or current_attribute_id == -1:
                        print(f"Error: 'reference' found before an attribute block: {line}")
                        sys.exit(1)
                    hidden_references_ids.append([source_id, window_id, current_attribute_id])
                except Exception as e:
                    print(f"Error parsing 'reference' line: {e}")
                    sys.exit(1)

            elif line.startswith("evaluated signal:"):
                # This is a stimulus (SSR) ID
                try:
                    source_id = int(line.split(":", 1)[1].strip())
                    if window_id == -1 or current_attribute_id == -1:
                        print(f"Error: 'evaluated signal' found before an attribute block: {line}")
                        sys.exit(1)
                    stimuli_ssr_ids.append([source_id, window_id, current_attribute_id])
                except Exception as e:
                    print(f"Error parsing 'evaluated signal' line: {e}")
                    sys.exit(1)
            
            else:
                # This line must be an attribute header, starting a new block
                attr_name = line
                if attr_name in attribute_map:
                    # This is the start of a new window/block
                    window_id += 1
                    current_attribute_id = attribute_map[attr_name]
                else:
                    # Error: The line is not a known command or a defined attribute
                    # We ignore this if attributes haven't been loaded yet.
                    if attribute_map:
                        print(f"Error: Unrecognized line or unknown attribute: '{line}'")
                        print("Please check two things:")
                        print(f"  1. Is '{line}' spelled correctly?")
                        print("  2. Is it listed in the 'Qualities:' line at the top of the file, with commas separating it?")
                        sys.exit(1)
                    else:
                        print("Error: File must start with 'Qualities:' line.")
                        sys.exit(1)

        # Assign the parsed lists to the config dictionary
        config["stimuli_ssr_ids"] = stimuli_ssr_ids
        config["hidden_references_ids"] = hidden_references_ids
        config["attributes"] = attributes
        
        return config

    except Exception as e:
        print(f"Error reading config file '{filename}': {e}")
        sys.exit(1)



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
    config = load_new_config("config.txt")
    stimuli_ssr_ids = config.get("stimuli_ssr_ids", [])
    hidden_references_ids = config.get("hidden_references_ids", [])
    attributes = config.get("attributes", [])

    print(stimuli_ssr_ids)
    print(hidden_references_ids)
    print(attributes)
    #gifs_paths = config.get("gifs_paths", [])

    
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
                          hidden_references=hidden_references_ids)

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
    gui_comp.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
