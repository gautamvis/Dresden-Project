#xml to vhdl converter

#Import the files containing helper functions, and ElementTree, a library used to help parsing xml files
import xml_to_vhdl_design_functions
import xml_to_vhdl_tb_functions
from argparse import ArgumentParser
import xml.etree.ElementTree as el_tree


#Parsing the command line is currently commented out, while testing. Uncomment later

#Parse command line, to get the names of input file, design file, testbench file
#And enable clock/reset mode, to prints blocks with clock and reset ports

##parser = ArgumentParser()
##parser.add_argument("-i", "--inputfile", help="XML file name")
##parser.add_argument("-d", "--designfile", help="Name of file containing design")
##parser.add_argument("-t", "--tbfile", help="Name of file containing testbench")
##parser.add_argument("-c", "--clockreset",help="To create blocks with clock/reset ports, type 'on'")
##
##args = parser.parse_args()
##infile = args.inputfile
##designfile = args.designfile
##tbfile = args.tbfile
##clockreset = 'off' #off by default
##clockreset = args.clockreset


#FIXME - these vars are set to avoid parsing while testing. Remove later
infile = 'sample_input.xml'
designfile = "newdesignfile.vhdl"
tbfile = "tbfile.vhdl"
clockreset = "off"

#Set up ElementTree, to parse the xml file
tree = el_tree.parse(infile)
root = tree.getroot() 

#FIXME parse these when these names are added to the source file (currently are not)
temparchname = "structural"
tempentityname = "ser_add"

#Store certain ports (name, type, width) that are repeatedly used in an array
port_list = []
xml_to_vhdl_design_functions.store_ports(root, port_list)

#Print all output to the design file
with open(designfile, 'w+') as outfile:

    #Print the VHDL Libraries used
    print(
          'library ieee; \n'
          'use ieee.std_logic_1164.all; \n'
          'use ieee.numeric_std.all; \n'
          ,file=outfile
    )

    #Run the set of functions which print blocks with clock and reset mode, if enabled
    #These helper functions are found in 'xml_to_vhdl_design_functions'
    #Separate functions to print in/out ports, to print the connections, and to print the blocks
    if clockreset == 'on':
    
        xml_to_vhdl_design_functions.print_ins_outs_clockreset(root, port_list, outfile)
        xml_to_vhdl_design_functions.print_signals(root, outfile)
        xml_to_vhdl_design_functions.print_blocks_clockreset(root, outfile)

    #If not, run the set of functions without clock/reset ports
    else:
    
        xml_to_vhdl_design_functions.print_ins_outs(port_list, outfile)
        xml_to_vhdl_design_functions.print_signals(root, outfile)
        xml_to_vhdl_design_functions.print_blocks(root, outfile)

#Print all output to the testbench file
with open(tbfile, 'w+') as outfile:

    #Print VHDL Libraries used, and the entity name of the testbench
    print(
          'library ieee; \n'
          'use ieee.std_logic_1164.all; \n'
          'use ieee.numeric_std.all; \n'
          'use std.textio.all; \n'
          'use work.all; \n\n'
          'entity {ent}_tb is \n'
          'end entity {ent}_tb; \n'
    
        .format(ent = tempentityname, arch = temparchname)
        ,file=outfile
    )



    #Run the set of helper functions to create the testbench
    #These helper functions are found in 'xml_to_vhdl_tb_functions'
    #Separate functions to print the component, print pre-written functions to convert
    #  a string to a std_vec and vice versa in vhdl, to print the signals, to print the
    #  the port map, and to print the process

    xml_to_vhdl_tb_functions.print_component(root, port_list, outfile)
    xml_to_vhdl_tb_functions.print_string_to_stdvec_fxns(outfile)
    xml_to_vhdl_tb_functions.print_signals_tb(port_list, outfile)
    xml_to_vhdl_tb_functions.print_port_map_tb(port_list, outfile)
    xml_to_vhdl_tb_functions.print_test_process(root, port_list, outfile)















