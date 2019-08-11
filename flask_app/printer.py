import subprocess
from string import Template


# Handles printing requests and label format
def print_label(printitem, printsize, batchratio):

	(name, expdate, credate) = printitem

	batchbar = credate

	destination = ''

	# Format for how everything is displayed on the label, different cases available for different situations - 's' for small label format, 'm' for medium label format, acquiry can be purchased 'p' (all info except name required on label) or made 'm' (all info required on label)
	TEMPLATES = {}
	if printsize == 's':
		destination = 'tgh_bbp12_circle'
		TEMPLATES['LABEL_TEMPLATE_TGH_CIRCLE'] = ''''^XA
			^PW600^LL0300^LS00
			^FT360,35,0^A0N,18.75,15^FB325,1,0,L^FH\^FD${name}^FS
			^FT360,60,0^A0N,18.75,15^FB325,1,0,L^FH\^FD${expdate}^FS
			^FT360,85,0^A0N,18.75,15^FB325,1,0,L^FH\^FD${credate}^FS
			^FT360,110,0^A0N,18.75,15^FB325,1,0,L^FH\^FD${batchratio}^FS
			^FT350,25^BXI,5,200,,,,,^FD${batchbar}^FS
			^FT175,15^BXI,4,200,,,,,^FD${batchbar}^FS
			^XZ
			'''
	elif printsize == 'm':
		destination = 'tgh_bbp12'
		TEMPLATES['LABEL_TEMPLATE_TGH_CIRCLE'] = '''^XA
			^PW600^LL0300^LS00
			^FT160,85,0^A0N,31.25,25^FB325,1,0,L^FH\^FD${name}^FS
			^FT1 60,130,0^A0N,31.25,25^FB325,1,0,L^FH\^FD${expdate}^FS
			^FT160,175,0^A0N,31.25,25^FB325,1,0,L^FH\^FD${credate}^FS
			^FT160,225,0^A0N,31.25,25^FB325,1,0,L^FH\^FD${batchratio}^FS
			^FT140,80^BXI,7,200,,,,,^FD${batchbar}^FS
			^XZ
			'''

	label = Template(TEMPLATES['LABEL_TEMPLATE_TGH_CIRCLE'])

	if len(name) > 21:
		name = name[:18] + '...'

	label = label.substitute(name=name, expdate=expdate, credate=credate, batchbar=batchbar, batchratio=batchratio)

	# Here you need to know the name of the printer queue, and the text for the label, and this does the actual printing: 'lp' is a command line program (line
	# printer), on my system it is /usr/bin/lp and on the PATH

	lp_args = ["lp"]
	if destination:
		lp_args += ["-d", destination]
	lp_args.append("-")
	sp = subprocess.Popen(lp_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	label_formatted = '\n' + label
	sp.stdin.write(label_formatted.encode('utf-8'))
	stdout, stderr = sp.communicate()
	sp.stdin.close()