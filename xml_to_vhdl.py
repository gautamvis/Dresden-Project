#xml to vhdl converter

#Take in command line input, to get the names of input files(.xml and .txt),
#the intended names of the design file(.vhdl), and testbench file(.vhdl)
#and the name of the output file (.txt) produced when the testbench is run
#And to determine whether to enable clock/reset mode, to prints blocks with clock and reset ports

#Import the files containing helper functions, ElementTree, a library used to help parsing xml files,
#the sys library, used to redirect output to files, and the re library, to help create filenames from parsing cmd line
import xml_to_vhdl_design_functions
import xml_to_vhdl_tb_functions
from argparse import ArgumentParser
import xml.etree.ElementTree as el_tree
import sys
import re

#Parse the command line
parser = ArgumentParser()
parser.add_argument("-i", "--inputfile", help="XML file name")
parser.add_argument("-d", "--designfile", help="Name of file containing design")
parser.add_argument("-t", "--tbfile", help="Name of file containing testbench")
parser.add_argument("-c", "--clockreset",help="To create blocks with clock/reset ports, type 'on'")
parser.add_argument("-tfi", "--testbenchfilein",
                    help="Name of input file containing 32bit numbers (for testbench)")
parser.add_argument("-tfo", "--testbenchfileout",
                    help="Name of file that the testbench should output)")

args = parser.parse_args()
infile = args.inputfile

entityname = re.sub('.xml', '', infile)
designfile = re.sub('.xml', '.vhd', infile)
tbfile = re.sub('.xml', '_tb.vhd', infile)
if args.designfile is not None:
    designfile = args.designfile
if args.tbfile is not None:
    tbfile = args.tbfile

test_file_in = args.testbenchfilein
test_file_out = args.testbenchfileout
clockreset = 'off' #off by default
clockreset = args.clockreset

#Set up ElementTree, to parse the xml file
tree = el_tree.parse(infile)
root = tree.getroot() 

#Store input/output ports (name, type, width) that are repeatedly used (in design and tb)
port_list = []
xml_to_vhdl_design_functions.store_ports(root, port_list)

#Print all output to the design file
with open(designfile, 'w+') as outfile:

    #Redirect standard output to print to designfile
    sys.stdout = outfile

    #Print the VHDL Libraries used
    print(
          'library ieee; \n'
          'use ieee.std_logic_1164.all; \n'
          'use ieee.numeric_std.all; \n'
          ,file=outfile
    )

    #Run the set of functions which print blocks
    #These helper functions are found in 'xml_to_vhdl_design_functions'
    #Separate functions to print in/out ports, to print the connections, and to print the blocks
    xml_to_vhdl_design_functions.print_ins_outs(port_list, entityname)
    xml_to_vhdl_design_functions.print_signals(root, entityname)
    xml_to_vhdl_design_functions.print_blocks(root, port_list, clockreset)

#Print all output to the testbench file
with open(tbfile, 'w+') as outfile:

    #Redirect standard output to print to testbench file
    sys.stdout = outfile

    #Print VHDL Libraries used, and the entity name of the testbench
    print(
          'library ieee; \n'
          'use ieee.std_logic_1164.all; \n'
          'use ieee.numeric_std.all; \n'
          'use std.textio.all; \n'
          'use work.all; \n'
          'use work.str_to_stdvec_helpers.all; \n\n'
          'entity {ent}_tb is \n'
          'end entity {ent}_tb; \n'
    
        .format(ent = entityname)
        ,file=outfile
    )

    #Run the set of helper functions to create the testbench
    #These helper functions are found in 'xml_to_vhdl_tb_functions'
    #Separate functions to print the component, the signals,the port map, and the process
    xml_to_vhdl_tb_functions.print_component(root, port_list, entityname)
    xml_to_vhdl_tb_functions.print_signals_tb(root, port_list)
    xml_to_vhdl_tb_functions.print_port_map_tb(port_list, entityname)
    xml_to_vhdl_tb_functions.print_clock_and_rst_process(port_list)
    xml_to_vhdl_tb_functions.print_test_process(root, port_list, test_file_in, test_file_out)

