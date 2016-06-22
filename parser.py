#xml to vhdl converter

#Get filename (xtml file)
#FIXME
#filename = input('Enter filename: ')
filename = 'sample_input.xml'

#Set up ElementTree
import xml.etree.ElementTree as my_el_tree
tree = my_el_tree.parse(filename)
root = tree.getroot() 

blk = 'block'
prt = 'port'
addone = 'add1'
porta = 'a'
#test
for block in root.iter('block'):
    if block.get('name') == addone:
        for port in block.iter('port'):
            if port.get('name') == porta:
                print(port.get('width'))

        

#FIXME make outfile more general
with open('outfile.vhdl', 'w+') as outfile:

    #Write libraries used
    print(
          'library ieee;\n'
          'use ieee.std_logic_1164.all;\n'
          'use ieee.numeric_std.all;\n'
          ,file=outfile
          )

        

    #Write signals
    print("architecture {arch} of {entity} is \n"
          "--Signal Declarations-- \n"
          .format(arch = "arch_name", entity = "entity_name"),
          file=outfile
    )

    for connection in tree.iter(tag='connection'):
        
        #Each signal requires 3 pieces of data(source, destination, width)
        temp_src_blk = str(connection.get('srcBlk'))
        temp_src_port = str(connection.get('srcPort'))
        
        for block in root.iter('block'):
            if block.get('name') == temp_src_blk:
                for port in block.iter('port'):
                    if port.get('name') == temp_src_port:
                        temp_width = port.get('width')

        print("signal {srcBlk}_{srcPrt}_buffer : std_logic_vector({width} downto 0);"
              .format(srcBlk = temp_src_blk,
                      srcPrt = temp_src_blk,
                      width = temp_width),
                      file=outfile
        )
                    
    
    #Write data from each block in xml
    print('\nbegin\n', file=outfile

    )
          
    #FIXME
    for block in root.findall('block'):
##        
        print("{blockname} : {blocktype}"
              .format(blockname = block.get('name'), blocktype = block.get('instance_type')),
              "\n port map( ",
              file=outfile
        )                                                 

        #Write data for each port in a block
        for port in block:
            print( "  {portname} => "
                   .format(portname = port.get('name')),
                   file=outfile
            )
            
        print("\n", file=outfile
        )

    print("end {arch};\n" .format(arch="arch_name") ,file=outfile

    )





          
          



