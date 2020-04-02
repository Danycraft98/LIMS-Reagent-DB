import subprocess
from string import Template


# Handles printing requests and label format
def print_label(data, element_type, label_size, acquiry_met, batch_ratio):
    (name, expdate, credate) = data
    expdate = expdate.strftime("%Y-%m-%d %H:%M:%S")
    credate = credate.strftime("%Y-%m-%d %H:%M:%S")
    destination = ""

    """Format for how everything is displayed on the label, different cases available for different situations
    - 's' for small label format
    - 'm' for medium label format
    - acquiry_met can be: 
        - 'p' for purchased
        - 'm' for made"""

    templates = {}
    if label_size == "s":
        destination = "tgh_bbp12_circle"
        if element_type == "kit" or (acquiry_met and (acquiry_met == "m" or acquiry_met == "p")):
            templates["LABEL_TEMPLATE_TGH_CIRCLE"] = """"^XA
                        ^PW600^LL0300^LS00
                        ^FT360,35,0^A0N,18.75,15^FB325,1,0,L^FH\^FD${name}^FS
                        ^FT360,60,0^A0N,18.75,15^FB325,1,0,L^FH\^FD${expdate}^FS
                        ^FT360,85,0^A0N,18.75,15^FB325,1,0,L^FH\^FD${credate}^FS
                        ^FT360,110,0^A0N,18.75,15^FB325,1,0,L^FH\^FD${batch_ratio}^FS
                        ^FT350,25^BXI,5,200,,,,,^FD${credate}^FS
                        ^FT175,15^BXI,4,200,,,,,^FD${credate}^FS
                        ^XZ"""
    elif label_size == "m":
        destination = "tgh_bbp12"
        if element_type == "kit" or (acquiry_met and (acquiry_met == "m" or acquiry_met == "p")):
            templates["LABEL_TEMPLATE_TGH_CIRCLE"] = """^XA
                            ^PW600^LL0300^LS00
                            ^FT160,85,0^A0N,31.25,25^FB325,1,0,L^FH\^FD${name}^FS
                            ^FT160,130,0^A0N,31.25,25^FB325,1,0,L^FH\^FD${expdate}^FS
                            ^FT160,175,0^A0N,31.25,25^FB325,1,0,L^FH\^FD${credate}^FS
                            ^FT160,225,0^A0N,31.25,25^FB325,1,0,L^FH\^FD${batch_ratio}^FS
                            ^FT140,80^BXI,7,200,,,,,^FD${credate}^FS
                            ^XZ"""

    label = Template(templates["LABEL_TEMPLATE_TGH_CIRCLE"])

    if len(name) > 21:
        name = name[:18] + "..."

    label = label.substitute(name=name, expdate=expdate, credate=credate, batchbar=credate, batch_ratio=batch_ratio)
    print(label)

    # Here you need to know the name of the printer queue, and the text for the label, and this does the actual printing: "lp" is a command line program (line
    # printer), on my system it is /usr/bin/lp and on the PATH

    lp_args = ["lp"]
    if destination:
        lp_args += ["-d", destination]
    lp_args.append("-")
    sp = subprocess.Popen(lp_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    label_formatted = "\n" + label
    sp.stdin.write(label_formatted.encode("utf-8"))
    sp.communicate()
    sp.stdin.close()
