#xml to vhdl converter

#Get filename (xtml file)
filename = input('Enter filename: ')

#Set up to parse
import xml.etree.ElementTree as my_el_tree
tree = my_el_tree.parse(filename)
root = tree.getroot()

#Parse xml file
with open('outfile.vhdl', 'w+') as outfile:

    #Write libraries used
    print(
        'library ieee;\n'
        'use ieee.std_logic_1164.all;\n'
        'use ieee.numeric_std.all;\n'
        , file=outfile)

    #Write components of each block 
    print('begin\n', file=outfile)
    
    for tempblock in tree.iter(tag='block'):
        
        #FIXME
        print(' ',
              tempblock.get('name'), ' : ',
              tempblock.get('instance_type'),
              '\n\tport map(\n',
              file=outfile)

        for temppost in tempblock:
            print('\t', temppost.get('name'),
                  '\t', temppost.get('type'),
                  '\t', temppost.get('width'), '\n',
                  file=outfile, end="")

        print('\n', file=outfile)
        
    print('end structural\n', file=outfile)

        
        


#print(infile.read(), file=outfile)

        
