#xml to vhdl helper functions - testbench
import xml_to_vhdl_design_functions

#FIXME when these details are added to the xml file
temparchname = "test"
tempentityname = "ser_add"


#Class to store name, width, type of each signal
class signal:

    def __init__(self, name, width, type):
        self.name = name
        self.width = width
        self.type = type

def print_component(root, sig_list, outfile):

    print('''architecture {arch} of {ent}_tb is 
    
    component {ent} is
    
    port('''
    
          .format(arch = temparchname, ent = tempentityname)
          ,file=outfile
    )
    
    
    store_signals(root, sig_list)
    print_ports_tb(sig_list, outfile)
    
    print('''
); 

end component;
          
          '''
          .format(entity = tempentityname)
          ,file=outfile
    )

#Store relevant info about the signals (name, size, type) in an array
def store_signals(root, sig_list):

    #Go through each port of each block
    cxn_list = root.findall('connection')
    
    for block in root.findall('block'):
        for port in block:
            
            #Search through list of connections, to determine if
            #port has an internal connection. If so, do nothing
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

            temp_name = block.get('name') + '_' + port.get('name')
            temp_width = int(port.get('width'))
            temp_type = port.get('type')
            temp_sig = signal(temp_name, temp_width, temp_type)
            sig_list.append(temp_sig)


def print_ports_tb(sig_list, outfile):

    #To make sure not to print an extra semicolon
    iteration_counter = 0
    
    for sig in sig_list:

        iteration_counter += 1
        
         #Print signal with multiple bit input/output (std_logic_vector)
        if(sig.width > 1):
            print('    {sname} : {stype} std_logic_vector({width} downto 0)'
                    .format(sname = sig.name,
                        stype = sig.type,
                        width = sig.width - 1)
                    ,file=outfile
                    ,end=""
                  
            )
            
        #Print signal with single bit input/output (std_logic)
        else :
            print('    {sname} : {stype} std_logic'
                    .format(sname = sig.name, stype = sig.type)
                    ,file=outfile
                    ,end=""
            )
            
        if iteration_counter < len(sig_list):
            print(';', file=outfile)
            
            


def print_string_to_stdvec_fxns(outfile):

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
    ,file=outfile
    )



def print_signals_tb(sig_list, outfile):


    for sig in sig_list:

        #Print signal with multiple bit input/output (std_logic_vector)
        if(sig.width > 1):
            print('    signal {sname}_buffer : std_logic_vector({width} downto 0); \n'
                    .format(sname = sig.name,
                        width = sig.width - 1)
                    ,file=outfile
                    ,end=""
                  
            )
        #Print sig with single bit input/output (std_logic)
        else:
            print('    signal {sname}_buffer : std_logic; \n'
                    .format(sname = sig.name)
                    ,file=outfile
                    ,end=""
                  
            )


    #Done signal
    print("    signal done : std_logic := '0'; \n", file=outfile)
    


def print_port_map_tb(sig_list, outfile):

    print ('begin \n', file=outfile)
    print('DUT : ser_add \n', file=outfile)
    print('    port map( \n', file=outfile)
    
    #To prevent extra semicolon
    iteration_counter = 0
    
    for sig in sig_list:
    
        iteration_counter += 1
        
        #Print port with multiple bit input/output
        if(sig.width > 1):
            print('    {sname} => {sname}_buffer({width} downto 0)'
                  .format(sname = sig.name,
                        ptype = sig.type,
                        width = sig.width -1)
                  ,file=outfile
                  ,end=""
                  )
        #Print port with single bit input/output
        else:
            print('    {sname} => {sname}_buffer'
                  .format(sname = sig.name)
                  ,file=outfile
                  ,end=""
                  
            )

        #Prevent extra semicolon
        if iteration_counter < len(sig_list):
            print(',', file=outfile)

    print('''
);
          ''', file=outfile
          )
    
    
    
def print_test_process(root, sig_list, outfile):

    #Used to determine length of strings provided in input files,
    #and written to the output file
    in_width = 0
    out_width = 0
    in_width, out_width = find_input_output_width(root, in_width, out_width)
    
    
    #Print generic test case procedure
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
            ,file=outfile
    )

    
    #Divide the inputs
    
    #Variable to keep track of input numbers
    temp_int = 0
    #Variables to keep track of which output ports will be written to outfile
    out_port_name = ""; out_buffer_name = "";
    
    for sig in sig_list:
        
        #FIMXE? - only get non-carry bits from input
        if sig.width > 1 and sig.type == 'in':
            
            print("     {sname}_buffer <= stimulus_in({num1} downto {num2}); "
                  .format(sname = sig.name,
                          num1 = temp_int + sig.width - 1,
                          num2 = temp_int)
                  ,file=outfile
            )
            temp_int += sig.width

                  
        #FIXME? carry bits are input as 0, instead of read from file
        elif sig.type == 'in':
        
            print("     {sname}_buffer <= '0'; "
                  .format(sname = sig.name)
                  ,file=outfile
            )

        #The port whose contents will be written to output file
        elif sig.width == out_width:
            out_port_name = sig.name
        
        #Sets it up so that the cout port of the last adder is the one considered
        else :
            out_buffer_name = sig.name


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
        ,file=outfile
        )

#Needed when reading in lines from input text file
#And outputting to the output file
def find_input_output_width(root, input_width, out_width):

     #Go through each port of each block
    cxn_list = root.findall('connection')
    
    for block in root.findall('block'):
        for port in block:
            
            
            #Search through list of connections, to determine if
            #port has an internal connection. If so, continue
            continue_bool = 0;

            for cxn in cxn_list:

                if ( (cxn.get('srcBlk') == block.get('name') and
                    cxn.get('srcPort') == port.get('name') ) or
                     
                     (cxn.get('destBlk') == block.get('name') and
                    cxn.get('destPort') == port.get('name') ) ):

                        continue_bool = 1
                        break
            if continue_bool == 1:
                continue
            
            #FIXME? if want to input C_in values
            if port.get('type') == 'in' and int(port.get('width')) > 1:
                input_width += int(port.get('width'))
            
            elif port.get('type') == 'out' and int(port.get('width')) > out_width:
                out_width = int(port.get('width'))
    
    return input_width, out_width

