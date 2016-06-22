#xml to vhdl converter

#Get input and output file names
filename = input('Enter filename: ')
my_outfile = input('Enter desired vdhl filename: ')

#for testing
#filename = 'sample_input.xml'
#my_outfile = 'outfile.vhdl'

#Set up ElementTree
import xml.etree.ElementTree as my_el_tree
tree = my_el_tree.parse(filename)
root = tree.getroot() 

#FIXME when names are added to source file
temparchname = "\'arch_name\'"
tempentityname = "\'entity_name\'"

#Write all output to file       
with open(my_outfile, 'w+') as outfile:

    #Print libraries used
    print(
          'library ieee;\n'
          'use ieee.std_logic_1164.all;\n'
          'use ieee.numeric_std.all;\n'
          ,file=outfile
    )

    #Print names of inputs/outputs
    print(
          "entity {entity} is \n"
          "  port( \n"

          "\nPRINT INPUTS/OUTPUTS HERE \n\n"
          
          "  ); \n\n"
          "end {entity} \n"
          .format(entity = tempentityname)
          ,file=outfile
    )

    #Print signals
    print("architecture {arch} of {entity} is \n\n"
          "--Signal Declarations-- \n"
          .format(arch = temparchname, entity = tempentityname),
          file=outfile
    )

    for connection in tree.iter(tag='connection'):
        
        #Each signal requires source, destination, width
        
        temp_src_blk = str(connection.get('srcBlk')) #source
        temp_src_port = str(connection.get('srcPort')) #destination
        
        for block in root.iter('block'):
            if block.get('name') == temp_src_blk:
                for port in block.iter('port'):
                    if port.get('name') == temp_src_port:
                        temp_width = port.get('width') #width

        print("signal {srcBlk}_{srcPrt}_buffer : std_logic_vector({width} downto 0);"
              .format(srcBlk = temp_src_blk,
                      srcPrt = temp_src_port,
                      width = temp_width),
                      file=outfile
        )
                    
    
    #Write data from each block in xml
    print('\nbegin\n', file=outfile
    )
    for block in root.findall('block'):
        
        print("{blockname} : {blocktype}"
              .format(blockname = block.get('name'), blocktype = block.get('instance_type')),
              "\n  port map( ",
              file=outfile
        )                                                 

        #Write data for each port in a block
        for port in block:
            print( "\t{portname} => "
                   .format(portname = port.get('name')),
                   file=outfile
            )
            
        print("\n   ); \n", file=outfile
        )

    print("end {arch};\n" .format(arch=temparchname) ,file=outfile

    )





          
          



