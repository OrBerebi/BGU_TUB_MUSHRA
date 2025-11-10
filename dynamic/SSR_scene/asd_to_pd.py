import xml.etree.ElementTree as ET

def xml_to_pd(xml_file, pd_file="scene.pd"):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Pd header
    pd_lines = [
        "#N canvas 50 50 1000 800 10;\n"
    ]

    y_offset = 50
    obj_id = 0

    for i, src in enumerate(root.findall(".//source")):
        name = src.get("name")
        file_path = src.find("file").text
        src_id = src.get("id")

        # Only take left channel (L) since readsf~ 2 handles stereo
        if name.endswith("_L"):
            # Pd object positions
            x = 50
            y = y_offset + i * 120

            # Objects
            readsf = f"#X obj {x} {y} readsf~ 2;\n"
            r_play = f"#X obj {x} {y-30} r play_{src_id};\n"
            msg_open = f"#X msg {x} {y+30} open \"{file_path}\" , 1;\n"
            dac = f"#X obj {x} {y+60} dac~ 1 2;\n"

            # Connections (line numbers = sequential obj_id)
            pd_lines.extend([readsf, r_play, msg_open, dac])
            pd_lines.append(f"#X connect {obj_id+1} 0 {obj_id+2} 0;\n")
            pd_lines.append(f"#X connect {obj_id+2} 0 {obj_id} 0;\n")
            pd_lines.append(f"#X connect {obj_id} 0 {obj_id+3} 0;\n")
            pd_lines.append(f"#X connect {obj_id} 1 {obj_id+3} 1;\n")

            obj_id += 4

    # Write Pd patch
    with open(pd_file, "w") as f:
        f.writelines(pd_lines)

    print(f"✅ Pd patch generated: {pd_file}")


# Usage
xml_to_pd("demo2.asd", "demo2.pd")
