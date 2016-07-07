#xml to vhdl helper functions

#FIXME when these names are added to source file
temparchname = "arch_name"
tempentityname = "entity_name"




#Print inputs and outputs
def print_ins_outs(root, outfile):
    print(
          "entity {entity} is \n"
          "  port( \n"
          .format(entity = tempentityname)
          ,file=outfile

    )
    #Go through each port of each block
    cxn_list = root.findall('connection')
    
    #These variables count number of ports/ ports visited
    #to ensure no semicolon is printed after the last port
    total_num_ports = 0;
    for block in root.findall('block'):
        total_num_ports += len(block.findall('port'))

    iteration_counter = 0;
    
    for block in root.findall('block'):
        for port in block:
            
            iteration_counter += 1;
            
            #Search through list of connections, to determine if
            #port has an internal connection. If so, print nothing
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
            
            #Print port with multiple bit input/output
            if(int(port.get('width')) > 1):
                print("    {blockname}_{portname} : {ptype} std_logic_vector({width} downto 0)"
                      .format(blockname = block.get('name'),
                            portname = port.get('name'),
                            ptype = port.get('type'),
                            width = int(port.get('width'))-1)
                      ,file=outfile
                      ,end=""
                      
                )
            #Print port with single bit input/output
            else:
                print("    {blockname}_{portname} : {ptype} std_logic"
                      .format(blockname = block.get('name'),
                            portname = port.get('name'),
                            ptype = port.get('type'))
                      ,file=outfile
                      ,end=""
                      
                )

            #Don't print semicolon for last port
            if iteration_counter < total_num_ports:
                print(";", file=outfile)
                

    print(
          
          "\n ); \n\n"
          "end {entity}; \n"
          .format(entity = tempentityname)
          ,file=outfile
    )

def print_signals(root, outfile):

    print('''architecture {arch} of {entity} is
          
          --Signal Declarations--
                                        '''
          .format(arch = temparchname, entity = tempentityname),
          file=outfile
    )
    #Print a signal for every connection
    #Get source block, source port, and width to do this
    
    #Dictionary of signals
    signal_dict ={}
    for connection in root.iter('connection'):
        temp_src_blk = str(connection.get('srcBlk'))
        temp_src_port = str(connection.get('srcPort'))
        signal_name = temp_src_blk + "_" + temp_src_port
        
        for block in root.iter('block'):
            if block.get('name') == temp_src_blk:
                for port in block.iter('port'):
                    if port.get('name') == temp_src_port:
                        temp_width = int(port.get('width'))

        signal_dict[signal_name] = temp_width

    for signal in signal_dict:
        
        if signal_dict[signal] > 1:
            print("signal {sig}_buffer : std_logic_vector({size} downto 0);"
                  .format(sig = signal, size = signal_dict[signal] - 1),
                  file=outfile
            )
        else:
            print("signal {sig}_buffer : std_logic;"
                      .format(sig = signal),
                      file=outfile
                )
        

def print_blocks(root, outfile):
    
    print('\nbegin\n', file=outfile)
    
    #This var counts number of ports visitied
    #to ensure no comma is printed after the last port
    iteration_counter = 0;
    num_ports = 0;

    temp_cxn_list = root.findall('connection')

    #For each block in the xml file
    for block in root.findall('block'):

        num_ports = len(block.findall('port'))
        iteration_counter = 0
        
        #Print name and type of block
        print("{blockname} : entity work.{blocktype} \n"
              " port map("
              .format(blockname = block.get('name'), blocktype = block.get('instance_type')),
              file=outfile
        )                                                 


        for port in block:
            
            iteration_counter += 1;
            
            #Print the name of the port
            print( "    {portname} => "
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
                         ,end=""
                   )
                   #To ensure no comma printed after last port
                   if iteration_counter < num_ports:
                       print (", ", file=outfile)

                   
                   temp_bool = 1
                   break;


            if temp_bool == 1:
                   continue
                 
            #Port has multiple bit output
            if int(port.get('width')) >1 and port.get('type') == 'out':
                   
                print("{blockname}_{portname}({width} downto 0)"
                      .format(blockname = block.get('name'),
                            portname = port.get('name'),
                            width = int(port.get('width'))-1
                            )
                      ,file=outfile
                      ,end=""
                      
                )
            #Port has single bit output
            elif int(port.get('width')) == 1 and port.get('type') == 'out':
                   
                print("{blockname}_{portname}"
                      .format(blockname = block.get('name'),
                            portname = port.get('name')
                            )
                      ,file=outfile
                      ,end=""
                )
            #Input port
            else:
               print("{blockname}_{portname}"
                      .format(blockname = block.get('name'),
                            portname = port.get('name'),
                            ptype = port.get('type')
                            )
                      ,file=outfile
                     ,end=""
                )
    
            #To ensure no comma printed after last port
            if iteration_counter < num_ports:
                print (", ", file=outfile)
    
        print("\n   ); \n", file=outfile
        )

    print("end {arch};" .format(arch=temparchname) ,file=outfile
    )



################################
#To print with clock/reset ports
################################


#Print inputs and outputs
def print_ins_outs_clockreset(root, outfile):
    print(
          "entity {entity} is \n"
          "  port( \n"
          .format(entity = tempentityname)
          ,file=outfile
          
    )
    #Go through each port of each block
    cxn_list = root.findall('connection')
  
    #These variables count number of ports/ ports visited
    #to ensure no semicolon is printed after the last port
    total_num_blocks = 0;
    for block in root.findall('block'):
      total_num_blocks += 1

    iteration_counter = 0;
    
    for block in root.findall('block'):
        for port in block:
            
            #Search through list of connections, to determine if
            #port has an internal connection. If so, print nothing
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
        
            #Print port with multiple bit input/output
            if(int(port.get('width')) > 1):
                print("\n    {blockname}_{portname} : {ptype} std_logic_vector({width} downto 0);"
                      .format(blockname = block.get('name'),
                              portname = port.get('name'),
                              ptype = port.get('type'),
                              width = int(port.get('width'))-1)
                      ,file=outfile
                      ,end=""
                      
                      )
            #Print port with single bit input/output
            else:
                print("\n    {blockname}_{portname} : {ptype} std_logic;"
                      .format(blockname = block.get('name'),
                              portname = port.get('name'),
                              ptype = port.get('type'))
                      ,file=outfile
                      ,end=""
                      
                )
        
        print("\n    {blockname}_clk : in std_logic;"
              "\n    {blockname}_reset : in std_logic"
              .format(blockname = block.get('name'))
              ,file=outfile, end=""
        )
        iteration_counter += 1
        #Don't print semicolon for last port
        if iteration_counter < total_num_blocks:
            print(";\n", file=outfile)


    print(
      
      "\n ); \n\n"
      "end {entity}; \n"
      .format(entity = tempentityname)
      ,file=outfile
      )


def print_blocks_clockreset(root, outfile):
    
    print('\nbegin\n', file=outfile)
    
    temp_cxn_list = root.findall('connection')

    #For each block in the xml file
    for block in root.findall('block'):
        
        #Print name and type of block
        print("{blockname} : entity work.{blocktype} \n"
              " port map("
              .format(blockname = block.get('name'), blocktype = block.get('instance_type')),
              file=outfile
        )                                                 


        for port in block:
            
            #Print the name of the port
            print( "    {portname} => "
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

                   print("{srcBlk}_{srcPort}_buffer, \n"
                         .format(srcBlk = cxn.get('srcBlk'), srcPort = cxn.get('srcPort'))
                         ,file=outfile
                         ,end=""
                   )
                   
                   temp_bool = 1
                   break;


            if temp_bool == 1:
                   continue
                 
            #Port has multiple bit output
            if int(port.get('width')) >1 and port.get('type') == 'out':
                   
                print("{blockname}_{portname}({width} downto 0), \n"
                      .format(blockname = block.get('name'),
                            portname = port.get('name'),
                            width = int(port.get('width'))-1
                            )
                      ,file=outfile
                      ,end=""
                      
                )
            #Port has single bit output
            elif int(port.get('width')) == 1 and port.get('type') == 'out':
                   
                print("{blockname}_{portname}, \n"
                      .format(blockname = block.get('name'),
                            portname = port.get('name')
                            )
                      ,file=outfile
                      ,end=""
                )
            #Input port
            else:
               print("{blockname}_{portname}, \n"
                      .format(blockname = block.get('name'),
                            portname = port.get('name'),
                            ptype = port.get('type')
                            )
                      ,file=outfile
                     ,end=""
                )
    
        print("    clk => {blockname}_clk, \n"
              "    reset => {blockname}_reset"
              .format(blockname = block.get('name'))
              ,file=outfile, end=""
        )
        
        print("\n   ); \n", file=outfile
        )

    print("end {arch};" .format(arch=temparchname) ,file=outfile
    )









