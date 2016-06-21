#xml to vhdl converter

#Get filename (xtml file)
filename = input('Enter filename: ')

#Set up to parse
import xml.etree.ElementTree as my_el_tree
tree = my_el_tree.parse(filename)
#root = tree.getroot()

#Parse xml file
with open('outfile.vhdl', 'w+') as outfile:

    #Write libraries used
    print(
        'library ieee;\n'
        'use ieee.std_logic_1164.all;\n'
        'use ieee.numeric_std.all;\n'
        ,file=outfile
    )

    #Write data from each block in xml
    print('begin\n', file=outfile)
    for block in tree.iter(tag='block'):

        print("{blockname} : {blocktype}"
              .format(blockname = block.get('name'), blocktype = block.get('instance_type')),
              "\n port map( ", file=outfile
        )                                                 

        #Write data for each port in a block
        for port in block:
            print( "  {portname} => "
                   .format(portname = port.get('name')),
                   file=outfile
            )
            
        print("\n", file=outfile)

    print("end structural;\n", file=outfile)
    
