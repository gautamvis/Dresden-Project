#xml to vhdl helper functions - design

#These functions are each used to print a different aspect of the design file
#(port map, signal declarations, etc)

#FIXME when these names are added to source file
temparchname = "structural"
tempentityname = "ser_add"


#Create a class to store the name, width, and type of a port
#These are used multiple times, both when creating the design and testbench file
class port:

    def __init__(self, name, width, type):
        self.name = name
        self.width = width
        self.type = type

#Create an array of ports(port_list) used in both design file and testbench file
def store_ports(root, port_list):

    #Go through each port of each block
    cxn_list = root.findall('connection')
    
    for block in root.findall('block'):
        for prt in block:
            
            #Search through list of connections, to determine if
            #there is a connection onvolving the port. If so, do nothing
            #If signal is found, bool allows loop to continue
            continue_bool = 0;

            for cxn in cxn_list:

                if ( (cxn.get('srcBlk') == block.get('name') and
                    cxn.get('srcPort') == prt.get('name') ) or
                     
                     (cxn.get('destBlk') == block.get('name') and
                    cxn.get('destPort') == prt.get('name') ) ):

                        continue_bool = 1;
                        break;
            if continue_bool == 1:
                continue

            #If no connection found, then add this port to the array
            temp_name = block.get('name') + '_' + prt.get('name')
            temp_width = int(prt.get('width'))
            temp_type = prt.get('type')
            temp_port = port(temp_name, temp_width, temp_type)
            
            port_list.append(temp_port)


#Function to print all the ports in the design
def print_ports(port_list, outfile):

    #Prevent extra semicolon at the end
    iteration_counter = 0
    
    
    total_num_ports = len(port_list)
   
    for port in port_list:

        iteration_counter += 1
        
        #Print port with multiple bit input/output
        if port.width > 1:
            print("    {sname} : {ptype} std_logic_vector({width} downto 0)"
                  .format(sname = port.name,
                        ptype = port.type,
                        width = port.width-1)
                  ,file=outfile
                  ,end=""
                  
            )
        #Print port with single bit input/output
        else:
            print("    {sname} : {ptype} std_logic"
                  .format(sname = port.name,
                        ptype = port.type)
                  ,file=outfile
                  ,end=""
                  
            )

        #Don't print semicolon for last port
        if iteration_counter < total_num_ports:
            print(";", file=outfile)

#Print inputs and outputs (print generic info, and then run the print ports function above)
def print_ins_outs(port_list, outfile):
    print(
          "entity {entity} is \n"
          "  port( \n"
          .format(entity = tempentityname)
          ,file=outfile

    )
    
    
    print_ports(port_list, outfile)
    
    print('''
          
          
);

end {entity};

          '''
          .format(entity = tempentityname)
          ,file=outfile
    )

#Print each signal specified in the xml
def print_signals(root, outfile):

    print('''architecture {arch} of {entity} is
          
          --Signal Declarations--
                                        '''
          .format(arch = temparchname, entity = tempentityname),
          file=outfile
    )
    #Print a signal for every connection
    #Get source block, source port, and width to do this
    
    #Dictionary of signals - this prevents repeating signals from being printed
    #If two signals com from the same port, the signal is only printed once
    signal_dict ={}
    
    #Get the ports involved in each connection
    for connection in root.iter('connection'):
        temp_src_blk = str(connection.get('srcBlk'))
        temp_src_port = str(connection.get('srcPort'))
        signal_name = temp_src_blk + "_" + temp_src_port
        
        #Locate which port in which block this connection involves
        for block in root.iter('block'):
            if block.get('name') == temp_src_blk:
                for port in block.iter('port'):
                    if port.get('name') == temp_src_port:
                        temp_width = int(port.get('width'))

                        #If signal name already exists in the dictionary, it is overwritten
                        #This prevents repeat signals
                        signal_dict[signal_name] = temp_width


    #Print each signal in the dictionary of signals
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
    #to ensure no extra comma is printed after the last port
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
            #If it does, connect the port to a buffer
            #If not, the port by default is set to have an external input/output
            temp_bool = 0
            for cxn in temp_cxn_list:
                
                #If connection exists:
                if ( (cxn.get('srcBlk') == block.get('name') and
                    cxn.get('srcPort') == port.get('name') ) or
                     
                     (cxn.get('destBlk') == block.get('name') and
                    cxn.get('destPort') == port.get('name') ) ):

                   print("{srcBlk}_{srcPort}_buffer"
                         .format(srcBlk = cxn.get('srcBlk'), srcPort = cxn.get('srcPort'))
                         ,file=outfile
                         ,end=""
                   )
                   
                   #Don't print a comma after last port
                   if iteration_counter < num_ports:
                       print (", ", file=outfile)
                   
                   temp_bool = 1
                   break;
        
            #If a connection was printed, continue with the loop
            if temp_bool == 1:
                   continue
               
               
            #If no connection found, the port is either an input or output port
            #The following lines deal with each of these cases
        
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


#Logic for these functions is exactly the same as above,
#With slight changes due to addition of clock and reset

#Print inputs and outputs
def print_ins_outs_clockreset(root, port_list, outfile):
    print(
          "entity {entity} is \n"
          "  port( \n"
          .format(entity = tempentityname)
          ,file=outfile
          
    )
    
    iteration_counter = 0
    
    total_num_blocks = len(root.findall(name='block'))
   
    for port in port_list:
    
        iteration_counter += 1
        
        #Print port with multiple bit input/output
        if port.width > 1:
            print("    {sname} : {ptype} std_logic_vector({width} downto 0)"
                  .format(sname = port.name,
                        ptype = port.type,
                        width = port.width - 1)
                  ,file=outfile
                  ,end=""
                  
            )
        #Print port with single bit input/output
        else:
            print("    {sname} : {ptype} std_logic"
                  .format(sname = port.name,
                        ptype = port.type)
                  ,file=outfile
                  ,end=""
                  
            )
    
    print("\n    {blockname}_clk : in std_logic;"
          "\n    {blockname}_reset : in std_logic"
          .format(blockname = port.name)
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









