#xml to vhdl converter
import Helpers
from argparse import ArgumentParser
import xml.etree.ElementTree as el_tree

#Parse command line

parser = ArgumentParser()
parser.add_argument("-i", "--inputfile", help="XML file name")
parser.add_argument("-o", "--outputfile", help="VHDL file name")
           
args = parser.parse_args()
infile = args.inputfile
my_outfile = args.outputfile

#Set up ElementTree
tree = el_tree.parse(infile)
root = tree.getroot() 
treecopy = el_tree.parse(infile)
rootcopy = treecopy.getroot()

#FIXME when these names are added to source file
temparchname = "arch_name"
tempentityname = "entity_name"


with open(my_outfile, 'w+') as outfile:

    #VHDL Libraries used
    print(
          'library ieee;\n'
          'use ieee.std_logic_1164.all;\n'
          'use ieee.numeric_std.all;\n'
          ,file=outfile
    )

    Helpers.print_ins_outs(root, outfile)

    Helpers.print_signals(rootcopy, outfile)

    Helpers.print_blocks(root, outfile)

    
