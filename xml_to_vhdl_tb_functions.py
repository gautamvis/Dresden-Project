#xml to vhdl helper functions - testbench

#This file contains helper functions to create the testbench file
#Includes printing the in/out ports of the component, printing out some VHDL functions to use,
#Printing the signals, the port map, and finally the test process

import xml_to_vhdl_design_functions

#Print architecture and entity, followed by ports
def print_component(root, port_list, arch_name, entity_name):

    print('''architecture {arch} of {ent}_tb is 
    
    component {ent} is
    
    port('''
    .format(arch = arch_name, ent = entity_name)
    )
    
    #Print ports + end formatting
    print("    " + ";\n    ".join(get_port(port.name, port.width, port.type) for port in port_list)
          + "\n    );\n\n   end component;\n")

#Print the signals
def print_signals_tb(port_list):

    print("    " + "\n    ".join(get_signal_tb(port.name, port.width) for port in port_list)
          + "\n    signal done : std_logic := '0';"
          + "\n    signal clock : std_logic := '0'; \n")

#Print the port map + formatting
def print_port_map_tb(port_list, entity_name):

    print ("begin \n\nDUT : " + entity_name + " \n\n    port map( \n\n    "
           +",\n    ".join(get_port_in_port_map(port.name, port.width) for port in port_list)
           + "\n    );\n")

#Print the entire testing process
def print_test_process(root, port_list):

    #Used to determine length of strings provided in input files,
    #and written to the output file
    in_width, out_width = find_input_output_width(root)
    
    #Get the input from file and convert to vectors
    #Currently reading in test values from text file named 'sample_input.txt'
    print('''\n Read_input : process
        file vector_file : text;
        file output_file : text;

        variable stimulus_in : std_logic_VECTOR({in_w_minusone} downto 0);
        variable str_stimulus_in : string({in_w} downto 1);
        variable str_stimulus_out : string({out_w} downto 1);
        
        variable file_line_in : line;
        variable file_line_out : line;
        
        begin
        
        file_open(vector_file, "32bit_input.txt", READ_MODE);
        file_open(output_file, "32bit_output.txt", WRITE_MODE);
        
        while not endfile(vector_file) loop
            readline(vector_file, file_line_in);
            read(file_line_in, str_stimulus_in);
            stimulus_in := str_to_stdvec(str_stimulus_in);
    
            '''
            .format(in_w_minusone = in_width - 1, in_w = in_width, out_w = out_width)
    )

    #Divide the inputs
    #Variable to keep track of input numbers
    input_width_tracker = 0
    #Variables to keep track of which output ports will be written to outfile
    out_port_name = ""; out_buffer_name = "";
    #List of constants
    const_list = root.findall('constant')
    
    for port in port_list:
        #If port has a constant connection, print it and continue
        temp_const = xml_to_vhdl_design_functions.const_exists(const_list,"","",port.width, port.name)
        if temp_const != -1:
            #Print with single(') or double quotes("), based on width of port (VHDL syntax)
            if port.width == 1:
                print("     " + port.name + "_buffer <= '" + temp_const + "';")
            else:
                print("     " + port.name + '_buffer <= "' + temp_const + '";')
    
        #Connect clk signals to clock
        elif port.name[-3:] == "clk":
            print("     {sname}_buffer <= clock; "
                  .format(sname = port.name)
            )
    
        #FIMXE? - As of now, only taking non-carry bits from input
        #Carry bits are set to 0 by default
        elif port.width > 1 and port.type == 'in':

            print("     {sname}_buffer <= stimulus_in({num1} downto {num2}); "
                  .format(sname = port.name,
                          num1 = input_width_tracker + port.width - 1,
                          num2 = input_width_tracker)
            )
            input_width_tracker += port.width

        #Set carry bits to 0 instead of inputting
        elif port.type == 'in':
        
            print("     {sname}_buffer <= '0'; "
                  .format(sname = port.name)
            )
        
        #These next two lines determine the port whose
        #   contents will be written to output file
        #This is determined by taking the output port mentioned
        #   which has the largest output width (specified in the xml)

        elif port.width == out_width:
            
            out_port_name = port.name
        
        else :
            out_buffer_name = port.name + "_buffer"

    #Print the sum/product obtained from each different input value
    #   to the output file(currently named 'sample_output.txt'

    print('''
                    wait for 2 ns;
                    
                    if({outbuffer} = '1') then
                        write(file_line_out, bit'('1'));
                    elsif({outbuffer} = '0') then
                        write(file_line_out, bit'('0'));
                    end if;
                    
                    str_stimulus_out := stdvec_to_str({outport}_buffer);
                    
                    write(file_line_out, str_stimulus_out);
                    writeline(output_file, file_line_out);
                    end loop;
                    wait;
                file_close(vector_file);
                file_close(output_file);

            end process Read_input;

    end test;'''
        .format(outport = out_port_name
                ,outbuffer = out_buffer_name)
        )

#Helper function needed when reading in lines from input text file and when outputting
#Determines total width of all the inputs (ex. if 3 32 bit inputs, total width = 96
#   this number is used to divide the inputs in the test process
#Also determines the width of the output(assuming there is only one final output value)
def find_input_output_width(root):

    input_width = 0
    output_width = 0
    #Go through each port of each block
    cxn_list = root.findall('connection')
    const_list = root.findall('constant')
    
    for block in root.findall('block'):
        for port in block:
            continue_p = False
            for cxn in cxn_list:
            #Search through list of connections, to determine if
            #port has an internal connection. If so, continue
                if xml_to_vhdl_design_functions.sig_exists(cxn, block.get('name'), port.get('name')):
                    continue_p = True
            
            if continue_p:
                continue
            
            #If port doesn't have a cxn, it is an input/output port
            
            #If port has a constant input, ignore it
            temp_int = xml_to_vhdl_design_functions.const_exists(const_list,
                         block.get('name'), port.get('name'), port.get('width'), "")
            if temp_int != -1:
                continue
            
            #FIXME? - Currently not considering inputting carry bits
            if port.get('type') == 'in' and int(port.get('width')) > 1:
                input_width += int(port.get('width'))
            
            elif port.get('type') == 'out' and int(port.get('width')) > output_width:
                output_width = int(port.get('width'))
    
    return input_width, output_width

#Returns a string containing the line to print, given a port
def get_port(name, width, type):

    #Port with multiple bit input/output (std_logic_vector)
    if width > 1:
        return name + " : " + type + " std_logic_vector(" + str(width - 1) + " downto 0)"
    
    #Port with single bit input/output (std_logic)
    return name + " : " + type + " std_logic"

#Returns a string containing the line to print, given a port:
def get_signal_tb(name, width):

    #Port with multiple bit input/output (std_logic_vector)
    if width > 1:
        return 'signal ' + name + '_buffer : std_logic_vector(' + str(width - 1) + ' downto 0);'
    
    #Port with single bit input/output (std_logic)
    return 'signal ' + name + '_buffer : std_logic;'

#Returns a string containing the line to print, given a port (in port map declaration)
def get_port_in_port_map(name, width):

    #Port with multiple bit input/output
    if width > 1:
        return name + " => " + name + "_buffer(" + str(width-1) + " downto 0)"
    
    #Port with single bit input/output
    return name + " => " + name + "_buffer"
