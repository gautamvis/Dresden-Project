#xml to vhdl converter

#Get input and output file names
#filename = input('Enter filename: ')
#my_outfile = input('Enter desired vdhl filename: ')

#for testing remove later
filename = 'sample_input.xml'
my_outfile = 'outfile.vhdl'

#Set up ElementTree
import xml.etree.ElementTree as my_el_tree
tree = my_el_tree.parse(filename)
root = tree.getroot() 
treecopy = my_el_tree.parse(filename)
rootcopy = treecopy.getroot()

#FIXME when these names are added to source file
temparchname = "arch_name"
tempentityname = "entity_name"


#Writing output to file       
with open(my_outfile, 'w+') as outfile:

    #Print libraries used
    print(
          'library ieee;\n'
          'use ieee.std_logic_1164.all;\n'
          'use ieee.numeric_std.all;\n'
          ,file=outfile
    )

    #Print inputs and outputs
    print(
          "entity {entity} is \n"
          "  port( \n"
          .format(entity = tempentityname)
          ,file=outfile

    )
    #Go through each port of each block
    cxn_list = root.findall('connection')
    for block in root.findall('block'):
        for port in block:
            booltemp = 0;

            #Search through list of connections, to determine if
            #port has an internal connection. If so, print nothing
            for cxn in cxn_list:

                if ( (cxn.get('srcBlk') == block.get('name') and
                    cxn.get('srcPort') == port.get('name') ) or
                     
                     (cxn.get('destBlk') == block.get('name') and
                    cxn.get('destPort') == port.get('name') ) ):

                        booltemp = 1;
                        break;
            if booltemp == 1:
                continue
            
            #Print port with multiple bit input/output
            if(int(port.get('width')) > 1):
                print("{blockname}_{portname} : {ptype} std_logic_vector({width} downto 0);"
                    .format(blockname = block.get('name'),
                            portname = port.get('name'),
                            ptype = port.get('type'),
                            width = int(port.get('width'))-1)
                    ,file=outfile
                )
            #Print port with single bit input/output
            else:
                print("{blockname}_{portname} : {ptype} std_logic;"
                    .format(blockname = block.get('name'),
                            portname = port.get('name'),
                            ptype = port.get('type'))
                    ,file=outfile
                )
    print(
          
          "  ); \n\n"
          "end {entity}; \n"
          .format(entity = tempentityname)
          ,file=outfile
    )

    #End of printing inputs/outputs



    #Print signals
    print("architecture {arch} of {entity} is \n\n"
          "--Signal Declarations-- \n"
          .format(arch = temparchname, entity = tempentityname),
          file=outfile
    )

    #FIXME test
    num_connections = len(root.findall('connection'))

    while num_connections > 0:
        #Print a signal for every connection
        for connection in rootcopy.iter(tag='connection'):
                        
            temp_src_blk = str(connection.get('srcBlk')) #source block
            temp_src_port = str(connection.get('srcPort')) # source port
            
            for block in root.iter('block'):
                if block.get('name') == temp_src_blk:
                    for port in block.iter('port'):
                        if port.get('name') == temp_src_port:
                            temp_width = int(port.get('width')) #width

            if temp_width > 1:
                print("signal {srcBlk}_{srcPrt}_buffer" \
                      " : std_logic_vector({width} downto 0);"
                      .format(srcBlk = temp_src_blk,
                              srcPrt = temp_src_port,
                              width = temp_width - 1),
                              file=outfile
                )
            else:
                print("signal {srcBlk}_{srcPrt}_buffer" \
                      " : std_logic;"
                      .format(srcBlk = temp_src_blk,
                              srcPrt = temp_src_port),
                              file=outfile
                    )

            #To prevent repeating connections             
            rootcopy.remove(connection)
            num_connections -= 1
            for cxn in rootcopy.iter(tag='connection'):
                if (cxn.get('srcBlk') == temp_src_blk and
                    cxn.get('srcPort') == temp_src_port):

                    rootcopy.remove(cxn)
                    num_connections -= 1
                    
        
    #End of printing signals


        
    #Print block data:
    print('\nbegin\n', file=outfile
    )

    temp_cxn_list = root.findall('connection')

    #For each block in the xml file
    for block in root.findall('block'):

        #Print name and type of block
        print("{blockname} : {blocktype}"
              .format(blockname = block.get('name'), blocktype = block.get('instance_type')),
              "\n  port map( ",
              file=outfile
        )                                                 


        for port in block:
            #Print the name of the port
            print( "\t{portname} => "
                   .format(portname = port.get('name')),
                   end="",
                   file=outfile
            )

            #Print the input/output/connection of the port

            #Search to see if the port has a connection
            #If not, defaults to external input/output
            temp_bool = 0
            for cxn in temp_cxn_list:
                
                if ( (cxn.get('srcBlk') == block.get('name') and
                    cxn.get('srcPort') == port.get('name') ) or
                     
                     (cxn.get('destBlk') == block.get('name') and
                    cxn.get('destPort') == port.get('name') ) ):

                   print("{srcBlk}_{srcPort}_buffer"
                         .format(srcBlk = cxn.get('srcBlk'), srcPort = cxn.get('srcPort'))
                         ,file=outfile
                   )
                   temp_bool = 1
                   break;

            if temp_bool == 1:
                   continue
                 
            #Port has multiple bit output
            if int(port.get('width')) >1 and port.get('type') == 'out':
                   
                print("{blockname}_{portname}({width})"
                    .format(blockname = block.get('name'),
                            portname = port.get('name'),
                            width = int(port.get('width'))
                            )
                    ,file=outfile
                )
            #Port has single bit output
            elif int(port.get('width')) == 1 and port.get('type') == 'out':
                   
                print("{blockname}_{portname}"
                    .format(blockname = block.get('name'),
                            portname = port.get('name')
                            )
                    ,file=outfile
                )
            #Input port
            else:
               print("{blockname}_{portname}_{ptype}put"
                    .format(blockname = block.get('name'),
                            portname = port.get('name'),
                            ptype = port.get('type')
                            )
                    ,file=outfile
                ) 
                            
            
        print("\n   ); \n", file=outfile
        )

    print("end {arch};\n" .format(arch=temparchname) ,file=outfile

    )

    #End of printing block data



          
          




