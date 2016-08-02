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
    dualcxn_list = root.findall('dualconnection')
    
    #Go through each port of each block
    for block in root.findall('block'):
        for prt in block:
            continue_p = False
            for cxn in cxn_list:
            #Search through list of connections, to determine if
            #there is a connection involving the port. If so, do nothing
            #If signal is found, bool allows loop to continue
                if sig_exists(cxn, block.get('name'), prt.get('name')):
                    continue_p = True
                    break
            if continue_p:
                continue
            
            #Search through dualconnections - continue if found
            for dualcxn in dualcxn_list:
                if dualsig_exists(dualcxn, block.get('name'), prt.get('name')):
                    continue_p = True
                    break
            if continue_p:
                continue

            #Dont add clock ports to the portlist
            if prt.get('name') == 'clk':
                continue
            
            port_list.append(port(block.get('name') + '_' + prt.get('name'),
                                  int(prt.get('width')),
                                  prt.get('type'))
            )

#Print inputs and outputs (print generic info, and then run the print ports function above)
def print_ins_outs(root, port_list, clockreset, entity_name):

    #Print entity name + formatting
    print("entity " + entity_name + " is \n\n    port( ")
    
    #Print clock/reset ports
    print("    clk_in : in std_logic;\n" +
          "    reset_in : in std_logic;")
    
    #Print ports + end formatting
    print(";\n".join(get_port_in_entity(port.name, port.width, port.type) for port in port_list)
          + "\n    );\n\nend " + entity_name + ";\n")


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
    for cxn in root.iter('connection'):
    
        src_blk = str(cxn.get('srcBlk'))
        src_port = str(cxn.get('srcPort'))
        signal_name = src_blk + "_" + src_port
        
        #Error check - if ports specified in xml input file don't match connections
        if root.find(".*[@name='"+src_blk+"']/*[@name='"+src_port+"']") is None:
            sys.exit('Error: Connection requires port ' + src_port + ' in block ' + src_blk
                     + '. No such port exists')
                    
        #Find each signal with root.find, and add to the dictionary each signal_name, width pair
        signal_dict[signal_name] = int(root.find(".*[@name='"+src_blk+"']/*[@name='"+src_port+"']").get('width'))

    #Add dualsignals to the dictionary of signals
    for dualcxn in root.iter('dualconnection'):
        src_blk = str(dualcxn.get('srcBlk'))
        src_port = str(dualcxn.get('srcPort'))
        signal_name = src_blk + "_" + src_port
    
        signal_dict[signal_name] = int(root.find(".*[@name='"+src_blk+"']/*[@name='"+src_port+"']").get('width'))

    
    #Print each signal in the dictionary of signals
    print("\n".join(get_sig(signal,width) for signal, width in signal_dict.items()))


def print_blocks(root, port_list, clockreset, arch_name):
    
    print('\nbegin')
    
    #Print the following process for testbench to function
    output_port = find_output_port(port_list)
    print('''
    process ({outport}_buffer) begin
    {outport} <= {outport}_buffer;
    end process;
          '''
        .format(outport = output_port)
    )
   
    #List of connections and constants from xml file
    cxn_list = root.findall('connection')
    dualcxn_list = root.findall('dualconnection')
    const_list = root.findall('constant')

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
        print(",\n".join(get_port_in_block(cxn_list, dualcxn_list, const_list, block.get('name'),port.get('name'),
        int(port.get('width')), port.get('type')) for port in block), "\n    );\n")

    print("end {arch};" .format(arch=arch_name))

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
def get_port_in_block(cxn_list, dualcxn_list, const_list, blockname, portname, width, type):

    #If connection exists, retun the line to print
    for cxn in cxn_list:
        if sig_exists(cxn, blockname, portname):
            return "    " + portname + " => " + cxn.get('srcBlk') + "_" + cxn.get('srcPort') + "_buffer"

    #If dual connection exists, return line to print
    for dualcxn in dualcxn_list:
        if sig_exists(dualcxn, blockname, portname):
            return ("    " + portname + " => " + dualcxn.get('srcBlk') + "_"
                   + dualcxn.get('srcPort') + "_buffer(" + str(int(dualcxn.get('srcWidth'))-1) + " downto "
                   + str(int(dualcxn.get('srcWidth')) - width) + ")")


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

    #Multiple bit signal vs single bit
    if width > 1:
        return "signal " + signal + "_buffer : std_logic_vector(" + str(width-1) + " downto 0);"
        
    return "signal " + signal + "_buffer : std_logic;"


#Check to see if port has constant
#If it does, return the value of the constant, converted to binary
#Fullname feature is needed because in some functions, blockname and portname are joined

#NOTE: assumes 'value' of each constant is given in decimal
def const_exists(const_list, blockname, portname, width, fullname):

    for const in const_list:
        if ((blockname == const.get('destBlk') and portname == const.get('destPort')) or
            (fullname == const.get('destBlk') + "_" + const.get('destPort'))):
            #convert value to binary, and pad with 0's depending on port width
            return bin(int(const.get('value')))[2:].zfill(int(width))

    return -1

#Checks if there is a dualsignal associated with the port
#Dual signal = port is used both as an input/output buffer and an internal connection
def dualsig_exists(dualcxn, blockname, portname):
    
    if dualcxn.get('destBlk') == blockname and dualcxn.get('destPort') == portname:
        return True
        
    return False

#Returns output port (the largest, by default)
#This is required for filters in which the output port serves as a signal also
def find_output_port(port_list):

    temp_port = port_list[0]
    
    for port in port_list:
        if port.type == 'out' and port.width > temp_port.width:
            temp_port = port

    return temp_port.name






