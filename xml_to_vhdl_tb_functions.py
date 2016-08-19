#xml to vhdl helper functions - testbench

#This file contains helper functions to create the testbench file
#Includes printing the in/out ports of the component, printing out some VHDL functions to use,
#Printing the signals, the port map, and finally the test process

import xml_to_vhdl_design_functions

#Print architecture and entity, followed by ports
def print_component(root, port_list, entity_name):

    print('''architecture test of {ent}_tb is
    
    component {ent} is
    
    port('''
    .format(ent = entity_name)
    )
    
    #This port list is the same as the one printed in the design file
    xml_to_vhdl_design_functions.print_ports(port_list, "component")

#Print the signals
def print_signals_tb(root, port_list):
    
    #Only need to find the output width in this case (for sum_buffer)
    junk, out_width = find_input_output_width(root, port_list)
    
    #Get and print the signal associated with each port in the list, along with default clock, rst, sum_buffer signals
    print("    " + "\n    ".join(xml_to_vhdl_design_functions.get_sig(port.name, port.width) for port in port_list)
          + "\n    signal clock : std_logic := '0';"
          + "\n    signal rst : std_logic := '0'; \n"
          + "\n    signal sum_buffer : std_logic_vector({ow} downto 0); \n"
          .format(ow = str(int(out_width-1))))

#Print the port map + formatting
def print_port_map_tb(port_list, entity_name):

    print ("begin \n\nDUT : " + entity_name + " \n\n    port map( \n"
           + "    clk_in => clock, \n"
           + "    reset_in => rst, \n    "
           +",\n    ".join(get_port_in_port_map(port.name, port.width) for port in port_list)
           + "\n    );\n")

#Print clock and reset processes
def print_clock_and_rst_process(port_list):

    print('''
    clk_process : process
      begin --clock
      wait for 2 ns;
        while true loop
           clock <= '0';
           wait for 1 ns;
           clock <= '1';
           wait for 1 ns;
        end loop;
    end process clk_process; 
    
    seq: process (clock,rst)
       begin
         if (clock'event and clock = '1') then
            if (rst = '1') then     
                sum_buffer  <= (others => '0');
            else
                sum_buffer  <= {sum_out}_buffer;
            end if;
         end if;        
    end process;
    '''
    .format(sum_out = xml_to_vhdl_design_functions.find_output_port(port_list))
    )


#Print the entire testing process
def print_test_process(root, port_list, test_file_in, test_file_out):

    #Used to determine length of strings provided in input files,
    #and written to the output file
    in_width, out_width = find_input_output_width(root, port_list)
    
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
        
            file_open(vector_file, "{t_in}", READ_MODE);
            file_open(output_file, "{t_out}", WRITE_MODE);
        
            rst <= '1';
            wait for 2 ns;
            rst <= '0';

        
            while not endfile(vector_file) loop
                readline(vector_file, file_line_in);
                read(file_line_in, str_stimulus_in);
                stimulus_in := str_to_stdvec(str_stimulus_in);
    
            '''
            .format(in_w_minusone = in_width - 1, in_w = in_width, out_w = out_width,
            t_in = test_file_in, t_out = test_file_out)
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
    
        #Multiple bit input
        elif port.type == 'in' and port.width > 1:

            print("     {sname}_buffer <= stimulus_in({num1} downto {num2}); "
                  .format(sname = port.name,
                          num1 = input_width_tracker + port.width - 1,
                          num2 = input_width_tracker)
            )
            input_width_tracker += port.width

        #Single bit input
        elif port.type == 'in':
        
            print("     {sname}_buffer <= stimulus_in({num1}); "
                  .format(sname = port.name, num1 = input_width_tracker)
            )
            input_width_tracker += 1

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
                    
                    str_stimulus_out := stdvec_to_str(sum_buffer);
                    
                    write(file_line_out, str_stimulus_out);
                    writeline(output_file, file_line_out);
                    end loop;
                    wait;
                file_close(vector_file);
                file_close(output_file);

            end process Read_input;

    end test;'''
        .format(outbuffer = out_buffer_name)
        )

#Helper function needed when reading in lines from input text file and when outputting
#Determines total width of all the inputs (ex. if 3 32 bit inputs, total width = 96
#   this number is used to divide the inputs in the test process
#Also determines the width of the output(assuming there is only one final output value)
def find_input_output_width(root, port_list):

    input_width = 0
    output_width = 0
    const_list = root.findall('constant')
    
    #Check each input/output port, ensuring that input ports are not constant
    for port in port_list:
        
        #If port has a constant input, ignore it
        if xml_to_vhdl_design_functions.const_exists(const_list,
                     "","", port.width, port.name) != -1:
            continue
        
        #If port is an input add its width to total
        if port.type == 'in':
            input_width += port.width
    
        #Else store the value of the largest output port
        elif port.type == 'out' and port.width > output_width:
            output_width = port.width
    
    return input_width, output_width

#Returns a string containing the line to print, given a port (in port map declaration)
def get_port_in_port_map(name, width):

    #Port with multiple bit input/output
    if width > 1:
        return name + " => " + name + "_buffer(" + str(width-1) + " downto 0)"
    
    #Port with single bit input/output
    return name + " => " + name + "_buffer"

