#xml to vhdl helper functions - testbench
import xml_to_vhdl_design_functions

#Print some generic info, then run the 'print_ports' function

def print_component(root, port_list, arch_name, entity_name):

    print('''architecture {arch} of {ent}_tb is 
    
    component {ent} is
    
    port('''
    
          .format(arch = arch_name, ent = entity_name)
    )
    
    
    print_ports_tb(port_list)
    
    print('''
); 

end component;
          
          '''
          .format(entity = entity_name)
    )

def print_ports_tb(port_list):

    #To make sure not to print an extra semicolon
    iteration_counter = 0
    
    for port in port_list:

        iteration_counter += 1
        
        #Print port with multiple bit input/output (std_logic_vector)
        if(port.width > 1):
            print('    {sname} : {stype} std_logic_vector({width} downto 0)'
                    .format(sname = port.name,
                        stype = port.type,
                        width = port.width - 1)
                    ,end=""
                  
            )
            
        #Print port with single bit input/output (std_logic)
        else :
            print('    {sname} : {stype} std_logic'
                    .format(sname = port.name, stype = port.type)
                    ,end=""
            )
        
        #Don't print an extra semicolon at the end
        if iteration_counter < len(port_list):
            print(';')
            
            

#Print functions to convert string to std_vec and vice versa in VHDL
#Needed for the VHDL test process
def print_string_to_stdvec_fxns():

    print('''    function str_to_stdvec(inp: string) return std_logic_VECTOR is
		variable temp: std_logic_VECTOR(inp'range) := (others => 'X');
	begin
		for i in inp'range loop
			if(inp(i) = '1') then
				temp(i):= '1';
			elsif(inp(i) = '0') then
				temp(i) := '0';
			end if;
		end loop;
	return temp;
	end function str_to_stdvec;

	function stdvec_to_str(inp: std_logic_VECTOR) return string is
		variable temp: string(inp'left+1 downto 1) := (others => 'X');
	begin
		for i in inp'reverse_range loop
			if(inp(i) = '1') then
				temp(i+1) := '1';
			elsif(inp(i) = '0') then
				temp(i+1) := '0';
			end if;
		end loop;
	return temp;
	end function stdvec_to_str; 
    
    '''
    )


#Print the signals
def print_signals_tb(port_list):

    #Go through the list of ports
    for port in port_list:

        #Print port with multiple bit input/output (std_logic_vector)
        if(port.width > 1):
            print('    signal {sname}_buffer : std_logic_vector({width} downto 0); \n'
                    .format(sname = port.name,
                        width = port.width - 1)
                    ,end=""
                  
            )
        #Print port with single bit input/output (std_logic)
        else:
            print('    signal {sname}_buffer : std_logic; \n'
                    .format(sname = port.name)
                    ,end=""
                  
            )


    #Done signal
    print("    signal done : std_logic := '0'; \n")
    


def print_port_map_tb(port_list):

    print ('begin \n')
    print('DUT : ser_add \n')
    print('    port map( \n')
    
    #To prevent extra semicolon
    iteration_counter = 0
    
    for port in port_list:
    
        iteration_counter += 1
        
        #Print port with multiple bit input/output
        if(port.width > 1):
            print('    {sname} => {sname}_buffer({width} downto 0)'
                  .format(sname = port.name,
                        ptype = port.type,
                        width = port.width -1)
                  ,end=""
                  )
        #Print port with single bit input/output
        else:
            print('    {sname} => {sname}_buffer'
                  .format(sname = port.name)
                  ,end=""
                  
            )

        #Prevent extra semicolon
        if iteration_counter < len(port_list):
            print(',')

    print('''
);
          '''
          )
    
    
#Print the entire testing process
def print_test_process(root, port_list):

    #Used to determine length of strings provided in input files,
    #and written to the output file
    in_width = 0
    out_width = 0
    in_width, out_width = find_input_output_width(root, in_width, out_width)
    
    
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
        
        file_open(vector_file, "sample_input.txt", READ_MODE);
        file_open(output_file, "sample_output.txt", WRITE_MODE);
        
        while not endfile(vector_file) loop
            readline(vector_file, file_line_in);
            read(file_line_in, str_stimulus_in);
            stimulus_in := str_to_stdvec(str_stimulus_in);
    
            '''
            .format(in_w_minusone = in_width - 1, in_w = in_width, out_w = out_width)
    )

    
    #Divide the inputs
    
    #Variable to keep track of input numbers
    temp_int = 0
    #Variables to keep track of which output ports will be written to outfile
    out_port_name = ""; out_buffer_name = "";
    
    for port in port_list:
        
        #FIMXE? - As of now, only taking non-carry bits from input
        #Carry bits are set to 0 by default
        if port.width > 1 and port.type == 'in':
            
            print("     {sname}_buffer <= stimulus_in({num1} downto {num2}); "
                  .format(sname = port.name,
                          num1 = temp_int + port.width - 1,
                          num2 = temp_int)
            )
            temp_int += port.width

                  
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
#Determines the largest input and output ports
def find_input_output_width(root, input_width, out_width):

     #Go through each port of each block
    cxn_list = root.findall('connection')
    
    for block in root.findall('block'):
        for port in block:
            
            
            #Search through list of connections, to determine if
            #port has an internal connection. If so, continue
            continue_p = false;

            for cxn in cxn_list:

                if ( (cxn.get('srcBlk') == block.get('name') and
                    cxn.get('srcPort') == port.get('name') ) or
                     
                     (cxn.get('destBlk') == block.get('name') and
                    cxn.get('destPort') == port.get('name') ) ):

                        continue_p = true
                        break
            if continue_p == true:
                continue
            
            #If port doesn't have a cxn, it is an input/output port
            #FIXME? - Currently not considering inputting carry bits
            #         only considering larger input ports
            if port.get('type') == 'in' and int(port.get('width')) > 1:
                input_width += int(port.get('width'))
            
            elif port.get('type') == 'out' and int(port.get('width')) > out_width:
                out_width = int(port.get('width'))
    
    return input_width, out_width

