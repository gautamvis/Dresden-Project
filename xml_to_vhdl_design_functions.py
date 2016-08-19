#xml to vhdl helper functions - design

#These functions are each used to print a different aspect of the design file
#(port map, signal declarations, etc)

import sys

#Create a class to store the name, width, and type of a port
#These are used multiple times, both when creating the design and testbench file
class port:

    def __init__(self, name, width, type):
        self.name = name
        self.width = width
        self.type = type

#Create an array of ports(port_list) used in both design file and testbench file
def store_ports(root, port_list):

    cxn_list = root.findall('connection')
    in_list = {}
    out_list = {}
    
    #Go through each port of each block
    for block in root.findall('block'):
        for prt in block:
            continue_p = False
            
            #Search through list of connections, known ins, and known outs to determine if
            #there is a connection involving the port. If so, do nothing (known inputs/outputs are added later on)
            #If signal is found, bool allows loop to continue
            for input in root.findall('input'):
                if sig_exists(input, block.get('name'), prt.get('name')):
                    in_list[input.get('buffer')] = int(input.get('srcWidth'))
                    continue_p = True
                    break
            if continue_p:
                continue
            
            for output in root.findall('output'):
                if sig_exists(output, block.get('name'), prt.get('name')):
                    out_list[output.get('buffer')] = int(output.get('srcWidth'))
                    continue_p = True
                    break
            if continue_p:
                continue
            
            for cxn in cxn_list:
                if sig_exists(cxn, block.get('name'), prt.get('name')):
                    continue_p = True
                    break
            if continue_p:
                continue
                
            #Dont add clock ports to the portlist
            if prt.get('name') == 'clk':
                continue
            
            #Add port to the port list
            port_list.append(port(block.get('name') + '_' + prt.get('name'),
                                  int(prt.get('width')),
                                  prt.get('type'))
            )

    #Add known input/output ports to the port list
    for buffer, width in in_list.items():
        port_list.append(port(buffer, width, 'in'))
    for buffer, width in out_list.items():
        port_list.append(port(buffer, width, 'out'))


#Print inputs and outputs (print generic info, and then run the print ports function above)
def print_ins_outs(port_list, entity_name):

    print("entity " + entity_name + " is \n\n    port( ")

    print_ports(port_list, entity_name)


#Print each signal specified in the xml
def print_signals(root, entity_name):

    print('''architecture structural of {entity} is
          
          --Signal Declarations--
                                        '''
          .format(entity = entity_name),
    )
    
    
    #Dictionary of signals - this prevents repeating signals from being printed
    #If two signals com from the same port, the signal is only printed once
    signal_dict ={}
    
    #Get the ports involved in each connection
    for cxn in root.iter('connection'):
        
        #Store source blk, port, width of signal, mainly to make code below more legible
        src_blk = str(cxn.get('srcBlk'))
        src_port = str(cxn.get('srcPort'))
        signal_name = src_blk + "_" + src_port
        
        #Error check - if a port specified in xml input file doesn't match up to the list of connections
        if root.find(".*[@name='"+src_blk+"']/*[@name='"+src_port+"']") is None:
            sys.exit('Error: Connection requires port ' + src_port + ' in block ' + src_blk
                     + '. No such port exists')
                    
        #Find each signal with root.find, and add to the dictionary each signal_name, width pair
        signal_dict[signal_name] = int(root.find(".*[@name='"+src_blk+"']/*[@name='"+src_port+"']").get('width'))

    #Include signals for known outputs
    for output in root.findall('output'):
        signal_dict[output.get('buffer')] = int(output.get('srcWidth'))

    #Print each signal in the dictionary of signals
    print("\n".join(get_sig(signal,width) for signal, width in signal_dict.items()))


def print_blocks(root, port_list, clockreset):
    
    print('\nbegin')
    
    #Print a process to connect the output port to a buffer
    #This is done so that the output can easily be accessed/printed in the test bench file
    out_port = find_output_port(port_list)
    for output in root.findall('output'):
        if out_port == output.get('buffer'):
            print('''
         process ({outport}_buffer) begin
         {buffer} <= {outport}_buffer;
         end process;
                '''
                .format(outport = out_port,
                        buffer = output.get('buffer'))
            )
    
    #Find the list of connections, constants, inputs and outputs from the xml file
    #Used when determining the line to print for each port in the list of blocks
    cxn_list = root.findall('connection')
    const_list = root.findall('constant')
    input_list  = root.findall('input')
    output_list  = root.findall('output')

    #For each block in the xml file
    for block in root.findall('block'):

        #Print name and type of block
        print("{blockname} : entity work.{blocktype} \n"
              "port map("
              .format(blockname = block.get('name'), blocktype = block.get('instance_type')),
        )
        
        #Include clock and reset ports, if enabled
        if(clockreset == 'on'):
        
            print("    clk => clk_in,\n"+
                  "    reset => reset_in,")

        #Print the port + formatting
        print(",\n".join(get_port_in_block(root, cxn_list, const_list, input_list, output_list, block.get('name'),port.get('name'),
        int(port.get('width')), port.get('type')) for port in block), "\n    );\n")

    print("end structural;\n")

#Function to determine whether an internal signal exists for the given port
#Searches the connections given in the xml, to see if the source port
#   of the connection matches the current port
def sig_exists(cxn, blockname, portname):
    
    if ((cxn.get('srcBlk') == blockname and cxn.get('srcPort') == portname ) or
        (cxn.get('destBlk') == blockname and cxn.get('destPort') == portname)) :
                
        return True

    return False

#Returns a string containing the line to print, given a port in entity declaration
def get_port_in_entity(portname, width, type):
    
    #Port with multiple bit input/output
    if int(width) > 1:
         return "    " + portname + " : " + type + " std_logic_vector(" + str(width-1) + " downto 0)"
    
    #Port with single bit input/output
    return "    " + portname + " : " + type + " std_logic"

#Returns a string containing the line to print, given a port in block declaration
def get_port_in_block(root, cxn_list, const_list, input_list, output_list, blockname, portname, width, type):

    #If port is connected to a known input
    for input in input_list:
        if sig_exists(input, blockname, portname):
            return "    " + portname + " => " + input.get('buffer') + "(" + str(int(input.get('srcWidth'))-1) + " downto 0)" if width > 1 else "    " + portname + " => " + input.get('buffer')

    #If port is connected to a known output
    for output in output_list:
        if sig_exists(output, blockname, portname):
            return "    " + portname + " => " + output.get('buffer') + '_buffer' + "(" + str(int(output.get('srcWidth'))-1) + " downto " + str(int(output.get('srcWidth'))-width) + ")" if width > 1 else "    " + portname + " => " + output.get('buffer') + '_buffer'

    #If connection exists (as speficied in the xml)
    for cxn in cxn_list:
        if sig_exists(cxn, blockname, portname):
            if width > 1:
            
                #Ensure always using most significant bits when the source is larger than the width of the input port
                #This code, for example, will connect an input port to bits (31 downto 16) instead of bits (15 downto 0) of the source port
                srcWidth = get_width(root, cxn.get('srcBlk'), cxn.get('srcPort'))
                if srcWidth > width:
                    return "    " + portname + " => " + cxn.get('srcBlk') + "_" + cxn.get('srcPort') + "_buffer(" + str(srcWidth-1) + " downto " + str(srcWidth- width) + ")"

                return "    " + portname + " => " + cxn.get('srcBlk') + "_" + cxn.get('srcPort') + "_buffer(" + str(width-1) + " downto 0)"
        
            #If source width and current port width are equal, no need to specify which bits to take
            return "    " + portname + " => " + cxn.get('srcBlk') + "_" + cxn.get('srcPort') + "_buffer"

    #If port is a clock input
    if portname == 'clk':
        return "    " + portname + " => clk_in"

    #If port has a constant input
    temp_int = const_exists(const_list, blockname, portname, width, "")
    if temp_int != -1:
            #if single bit, return string with single quotes (') - important for VHDL syntax
            if width == 1:
                return "    " + portname + " => '" + temp_int + "'"
            
            #else return string with double quotes (")
            return "    " + portname + ' => "' + temp_int + '"'

    #Port has multiple bit output
    if width >1 and type == 'out':
        return "    " + portname + " => " + blockname + "_" + portname + "(" + str(width-1) + " downto 0)"
    
    #Port has single bit output or is an input port
    return "    " + portname + " => " + blockname + "_" + portname

#Returns a string containing the line to print, given a signal in signal declaration
def get_sig(signal, width):

    #Multiple bit signal
    if width > 1:
        return "signal " + signal + "_buffer : std_logic_vector(" + str(width-1) + " downto 0);"
    
    #Single bit signal
    return "signal " + signal + "_buffer : std_logic;"


#Check to see if port is connected to a constant
#Return the value of the constant (converted to binary), or -1 if no constant exists
#Fullname feature is needed because in some cases, blockname and portname are joined
#NOTE: assumes 'value' of each constant is given in decimal
def const_exists(const_list, blockname, portname, width, fullname):

    for const in const_list:
        if ((blockname == const.get('destBlk') and portname == const.get('destPort')) or
            (fullname == const.get('destBlk') + "_" + const.get('destPort'))):
            #convert value to binary, and pad with 0's depending on port width
            return bin(int(const.get('value')))[2:].zfill(int(width))

    return -1

#Returns output port (the largest, by default)
#This is required for designs in which the output port serves also as a signal
def find_output_port(port_list):

    #Set largest port as first port in list, by default
    temp_port = port_list[0]
    for port in port_list:
    
        #In case the default port is an input port, update it to the first output port found
        if temp_port.type == 'in':
            temp_port = port
        
        #Update the deault if width is greater than the current width
        elif port.type == 'out' and port.width >= temp_port.width:
            temp_port = port

    return temp_port.name

#Return the width of a given port, knowing only blockname and portname
def get_width(root, srcBlk, srcPort):

    for block in root.findall('block'):
        if srcBlk == block.get('name'):
            for port in block.findall('port'):
                if srcPort == port.get('name'):
                    return int(port.get('width'))

#Print all ports in port list (used in both design and tb)
def print_ports(port_list, entity_name):
    
    #Print clock/reset ports
    print("    clk_in : in std_logic;\n" +
          "    reset_in : in std_logic;")
          
    #Print ports + end formatting
    print(";\n".join(get_port_in_entity(port.name, port.width, port.type) for port in port_list)
          + "\n    );\n\nend " + entity_name + ";\n")



