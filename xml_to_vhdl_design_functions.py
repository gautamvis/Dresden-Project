#xml to vhdl helper functions - design

#These functions are each used to print a different aspect of the design file
#(port map, signal declarations, etc)

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
            #there is a connection involving the port. If so, do nothing
            #If signal is found, bool allows loop to continue
            continue_p = false;

            for cxn in cxn_list:

                if ( (cxn.get('srcBlk') == block.get('name') and
                    cxn.get('srcPort') == prt.get('name') ) or
                     
                     (cxn.get('destBlk') == block.get('name') and
                    cxn.get('destPort') == prt.get('name') ) ):

                        continue_p = true;
                        break;
            if continue_p == true:
                continue

            port_list.append(port(block.get('name') + '_' + prt.get('name'),
                                  int(prt.get('width')),
                                  prt.get('type'))
            )

#Print inputs and outputs (print generic info, and then run the print ports function above)
def print_ins_outs(root, port_list, clockreset, entity_name):
    print(
          "entity {entity} is \n"
          "  port( \n"
          .format(entity = entity_name)

    )
    
    #Prevent extra semicolon at the end
    iteration_counter = 0
    
    total_num_ports = len(port_list)
   
    for port in port_list:

        iteration_counter += 1
        
        print_port_in_entity(port.name, port.type, port.width)
        
        #Don't print semicolon for last port
        if iteration_counter < total_num_ports:
            print(";")

    #Print clock reset ports, if enabled
    if clockreset == 'on':
    
        for block in root.findall('block'):
        
            print("\n    {blockname}_clk : in std_logic;"
                  "\n    {blockname}_reset : in std_logic"
                  .format(blockname = block.get('name'))
                  ,end=""
            )
    
    print('''
          
);

end {entity};

          '''
          .format(entity = entity_name)
    )

#Print each signal specified in the xml
def print_signals(root, arch_name, entity_name):

    print('''architecture {arch} of {entity} is
          
          --Signal Declarations--
                                        '''
          .format(arch = arch_name, entity = entity_name),
    )
    #Print a signal for every connection
    #Get source block, source port, and width to do this
    
    #Dictionary of signals - this prevents repeating signals from being printed
    #If two signals com from the same port, the signal is only printed once
    signal_dict ={}
    
    #Get the ports involved in each connection
    for connection in root.iter('connection'):
        src_blk = str(connection.get('srcBlk'))
        src_port = str(connection.get('srcPort'))
        signal_name = src_blk + "_" + src_port
        
        #Locate which port in which block this connection involves
        for block in root.iter('block'):
            if block.get('name') == src_blk:
                for port in block.iter('port'):
                    if port.get('name') == src_port:
                        temp_width = int(port.get('width'))

                        #If signal name already exists in the dictionary, it is overwritten
                        #This prevents repeat signals
                        signal_dict[signal_name] = temp_width


    #Print each signal in the dictionary of signals
    for key, value in signal_dict.items():
        
        if value > 1:
            print("signal {sig}_buffer : std_logic_vector({size} downto 0);"
                  .format(sig = key, size = value - 1),
            )
        else:
            print("signal {sig}_buffer : std_logic;"
                      .format(sig = key),
            )

def print_blocks(root, clockreset, arch_name):
    
    print('\nbegin\n')
    
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
        )

        for port in block:
            
            iteration_counter += 1;
            
            #Print the name of the port
            print( "    {portname} => "
                   .format(portname = port.get('name')),
                   end="",
            )

            #Print the input/output/connection of the port

            #Search to see if the port has a connection
            #If it does, connect the port to a buffer
            #If not, the port by default is set to have an external input/output
            continue_p = 0
            for cxn in temp_cxn_list:
                
                #If connection exists:
                if ( (cxn.get('srcBlk') == block.get('name') and
                    cxn.get('srcPort') == port.get('name') ) or
                     
                     (cxn.get('destBlk') == block.get('name') and
                    cxn.get('destPort') == port.get('name') ) ):

                   print("{srcBlk}_{srcPort}_buffer"
                         .format(srcBlk = cxn.get('srcBlk'), srcPort = cxn.get('srcPort'))
                         ,end=""
                   )
                   
                   #Don't print a comma after last port
                   if iteration_counter < num_ports:
                       print (", ")
                   
                   continue_p = 1
                   break;
        
            #If a connection was printed, continue with the loop
            if continue_p == 1:
                   continue
               
            
            #If no connection found, the port is either an input or output port
            #The following lines deal with each of these cases
        
            print_port_in_block(block.get('name'),
                                port.get('name'),
                                port.get('type'),
                                port.get('width'),
            )
            
            #To ensure no comma printed after last port
            if iteration_counter < num_ports:
                print (", ")
    
        #Include clock and reset ports, if enabled
        if(clockreset == 'on'):
        
            print(", \n"
                  "    clk => {blockname}_clk, \n"
                  "    reset => {blockname}_reset"
                  .format(blockname = block.get('name'))
                  ,end=""
            )
        
        print("\n   ); \n")

    print("end {arch};" .format(arch=arch_name))


#Prints a single port found in the overall entity declaration
def print_port_in_entity(portname, type, width):

    #Print port with multiple bit input/output
    if width > 1:
        print("    {sname} : {ptype} std_logic_vector({width} downto 0)"
              .format(sname = portname,
                    ptype = type,
                    width = width-1)
              ,end=""
        )
    #Print port with single bit input/output
    else:
        print("    {sname} : {ptype} std_logic"
              .format(sname = portname,
                    ptype = type)
              ,end=""
        )

#Prints a single port found in an adder/multiplier block
def print_port_in_block(blockname, portname, type, width):
    
    #Port has multiple bit output
    if int(width) >1 and type == 'out':
           
        print("{bname}_{pname}({width} downto 0)"
              .format(bname = blockname,
                    pname = portname,
                    width = int(width)-1)
              ,end=""
        )
    #Port has single bit output or is an input port
    else:
           
        print("{bname}_{pname}"
              .format(bname = blockname,
                    pname = portname)
              ,end=""
        )