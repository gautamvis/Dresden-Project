#xml to vhdl converter
import xml_to_vhdl_print_functions
from argparse import ArgumentParser
import xml.etree.ElementTree as el_tree

#FIXME - need to get entity name and arch name from somewhere

#Parse command line

##parser = ArgumentParser()
##parser.add_argument("-i", "--inputfile", help="XML file name")
##parser.add_argument("-o", "--outputfile", help="VHDL file name")
##parser.add_argument("-c", "--clockreset",help="To create blocks with clock/reset ports, type 'on' ")
##
##args = parser.parse_args()
##infile = args.inputfile
##my_outfile = args.outputfile
##clockreset = args.clockreset

#fixme test
infile = 'sample_input.xml'
my_outfile = "outfile.vhdl"
clockreset = "off"

#Set up ElementTree
tree = el_tree.parse(infile)
root = tree.getroot() 

#FIXME when these names are added to source file
temparchname = "arch_name"
tempentityname = "entity_name"


with open(my_outfile, 'w+') as outfile:

    #VHDL Libraries used
    print(
          'library ieee; \n'
          'use ieee.std_logic_1164.all; \n'
          'use ieee.numeric_std.all; \n'

          ,file=outfile
    )

    #Blocks have clock/reset ports
    if clockreset == 'on':
    
        xml_to_vhdl_print_functions.print_ins_outs_clockreset(root, outfile)
        xml_to_vhdl_print_functions.print_signals(root, outfile)
        xml_to_vhdl_print_functions.print_blocks_clockreset(root, outfile)

    #Without clock/reset ports
    else:
    
        xml_to_vhdl_print_functions.print_ins_outs(root, outfile)
        xml_to_vhdl_print_functions.print_signals(root, outfile)
        xml_to_vhdl_print_functions.print_blocks(root, outfile)
