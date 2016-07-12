#xml to vhdl converter
import xml_to_vhdl_design_functions
import xml_to_vhdl_tb_functions
from argparse import ArgumentParser
import xml.etree.ElementTree as el_tree

#FIXME - need to get entity name and arch name from somewhere

#Parse command line

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
##clockreset = args.clockreset

#fixme test
infile = 'sample_input.xml'
designfile = "designfile.vhdl"
tbfile = "tbfile.vhdl"
clockreset = "off"

#Set up ElementTree
tree = el_tree.parse(infile)
root = tree.getroot() 

#FIXME when these names are added to source file
temparchname = "structural"
tempentityname = "ser_add"


#Class to store name, width, type of each signal
class signal:

    def __init__(self, name, width, type):
        self.name = name
        self.width = width
        self.type = type

#Store relevant info about the signals (name, size, type) in an array
#This function is used to create both design file and testbench file
def store_signals(root, sig_list):

    #Go through each port of each block
    cxn_list = root.findall('connection')
    
    for block in root.findall('block'):
        for port in block:
            
            #Search through list of connections, to determine if
            #port has an internal connection. If so, do nothing
            #If signal is found, bool allows loop to continue
            continue_bool = 0;

            for cxn in cxn_list:

                if ( (cxn.get('srcBlk') == block.get('name') and
                    cxn.get('srcPort') == port.get('name') ) or
                     
                     (cxn.get('destBlk') == block.get('name') and
                    cxn.get('destPort') == port.get('name') ) ):

                        continue_bool = 1;
                        break;
            if continue_bool == 1:
                continue

            temp_name = block.get('name') + '_' + port.get('name')
            temp_width = int(port.get('width'))
            temp_type = port.get('type')
            temp_sig = signal(temp_name, temp_width, temp_type)
            sig_list.append(temp_sig)



with open(designfile, 'w+') as outfile:

    #VHDL Libraries used
    print(
          'library ieee; \n'
          'use ieee.std_logic_1164.all; \n'
          'use ieee.numeric_std.all; \n'
          ,file=outfile
    )

    #Blocks have clock/reset ports
    if clockreset == 'on':
    
        xml_to_vhdl_design_functions.print_ins_outs_clockreset(root, outfile)
        xml_to_vhdl_design_functions.print_signals(root, outfile)
        xml_to_vhdl_design_functions.print_blocks_clockreset(root, outfile)

    #Without clock/reset ports
    else:
    
        xml_to_vhdl_design_functions.print_ins_outs(root, outfile)
        xml_to_vhdl_design_functions.print_signals(root, outfile)
        xml_to_vhdl_design_functions.print_blocks(root, outfile)


with open(tbfile, 'w+') as outfile:

    #VHDL Libraries used
    #VHDL Libraries used
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



    sig_list = []
    
    xml_to_vhdl_tb_functions.print_component(root, sig_list, outfile)
    xml_to_vhdl_tb_functions.print_string_to_stdvec_fxns(outfile)
    xml_to_vhdl_tb_functions.print_signals_tb(sig_list, outfile)
    xml_to_vhdl_tb_functions.print_port_map_tb(sig_list, outfile)
    xml_to_vhdl_tb_functions.print_test_process(root, sig_list, outfile)















