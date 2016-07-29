library ieee; 
use ieee.std_logic_1164.all; 
use ieee.numeric_std.all; 
use std.textio.all; 
use work.all; 
use work.str_to_stdvec_helpers.all; 

entity biquad_tb is 
end entity biquad_tb; 

architecture test of biquad_tb is 
    
    component biquad is
    
    port(
    add0_stg0_C_out : out std_logic;
    add3_stg0_C_in : in std_logic;
    mul_a0_stg0_B_input : in std_logic_vector(15 downto 0);
    mul_a1_stg0_B_input : in std_logic_vector(15 downto 0);
    mul_b0_stg0_A_input : in std_logic_vector(15 downto 0);
    mul_b0_stg0_B_input : in std_logic_vector(15 downto 0);
    mul_b1_stg0_B_input : in std_logic_vector(15 downto 0);
    mul_b2_stg0_B_input : in std_logic_vector(15 downto 0);
    delay_b0_stg0_A_input : in std_logic_vector(15 downto 0);
    add0_stg0_Sum : out std_logic_vector(31 downto 0);
    clk_in : in std_logic

    );

   end component;

    signal add0_stg0_C_out_buffer : std_logic;
    signal add3_stg0_C_in_buffer : std_logic;
    signal mul_a0_stg0_B_input_buffer : std_logic_vector(15 downto 0);
    signal mul_a1_stg0_B_input_buffer : std_logic_vector(15 downto 0);
    signal mul_b0_stg0_A_input_buffer : std_logic_vector(15 downto 0);
    signal mul_b0_stg0_B_input_buffer : std_logic_vector(15 downto 0);
    signal mul_b1_stg0_B_input_buffer : std_logic_vector(15 downto 0);
    signal mul_b2_stg0_B_input_buffer : std_logic_vector(15 downto 0);
    signal delay_b0_stg0_A_input_buffer : std_logic_vector(15 downto 0);
    signal add0_stg0_Sum_buffer : std_logic_vector(31 downto 0);

    signal done : std_logic := '0';
    signal clock : std_logic := '0'; 

begin 

DUT : biquad 

    port map( 

    add0_stg0_C_out => add0_stg0_C_out_buffer,
    add3_stg0_C_in => add3_stg0_C_in_buffer,
    mul_a0_stg0_B_input => mul_a0_stg0_B_input_buffer(15 downto 0),
    mul_a1_stg0_B_input => mul_a1_stg0_B_input_buffer(15 downto 0),
    mul_b0_stg0_A_input => mul_b0_stg0_A_input_buffer(15 downto 0),
    mul_b0_stg0_B_input => mul_b0_stg0_B_input_buffer(15 downto 0),
    mul_b1_stg0_B_input => mul_b1_stg0_B_input_buffer(15 downto 0),
    mul_b2_stg0_B_input => mul_b2_stg0_B_input_buffer(15 downto 0),
    delay_b0_stg0_A_input => delay_b0_stg0_A_input_buffer(15 downto 0),
    add0_stg0_Sum => add0_stg0_Sum_buffer(31 downto 0),
    clk_in => clock

    );

clk_process : process
                    begin --clock
                    wait for 2 ns;
                      while true loop
                      -- begin
                         clock <= '0';
                         wait for 1 ns;
                         clock <= '1';
                         wait for 1 ns;
                      end loop;
                    end process clk_process; 




    Read_input : process
        file vector_file : text;
        file output_file : text;

        variable stimulus_in : std_logic_VECTOR(15 downto 0);
        variable str_stimulus_in : string(16 downto 1);
        variable str_stimulus_out : string(32 downto 1);
        
        variable file_line_in : line;
        variable file_line_out : line;
        
        begin
        
        file_open(vector_file, "32bit_input.txt", READ_MODE);
        file_open(output_file, "32bit_output.txt", WRITE_MODE);
        
        while not endfile(vector_file) loop
            readline(vector_file, file_line_in);
            read(file_line_in, str_stimulus_in);
            stimulus_in := str_to_stdvec(str_stimulus_in);
                
            add3_stg0_C_in_buffer <= '0'; 
            mul_a0_stg0_B_input_buffer <= x"00F0"; 
            mul_a1_stg0_B_input_buffer <= x"009B"; 
            mul_b0_stg0_A_input_buffer <= stimulus_in(15 downto 0); 
            mul_b0_stg0_B_input_buffer <= x"0164";
            mul_b1_stg0_B_input_buffer <= x"0136";
            mul_b2_stg0_B_input_buffer <= x"009B" ;
            delay_b0_stg0_A_input_buffer <= stimulus_in(15 downto 0); 

                    wait for 2 ns;
                    
                    if(add0_stg0_C_out_buffer = '1') then
                        write(file_line_out, bit'('1'));
                    elsif(add0_stg0_C_out_buffer = '0') then
                        write(file_line_out, bit'('0'));
                    end if;
                    
                    str_stimulus_out := stdvec_to_str(add0_stg0_Sum_buffer);
                    
                    write(file_line_out, str_stimulus_out);
                    writeline(output_file, file_line_out);
                    end loop;
                    wait;
                file_close(vector_file);
                file_close(output_file);

        end process Read_input;

end test;
