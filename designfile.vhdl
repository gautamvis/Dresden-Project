library ieee; 
use ieee.std_logic_1164.all; 
use ieee.numeric_std.all; 

entity biquad is 

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

end biquad;

architecture structural of biquad is
          
          --Signal Declarations--
                                        
signal add1_stg0_C_out_buffer : std_logic;
signal delay_a0_stg0_A_output_buffer : std_logic_vector(15 downto 0);
signal add3_stg0_Sum_buffer : std_logic_vector(31 downto 0);
signal delay_b0_stg0_A_output_buffer : std_logic_vector(15 downto 0);
signal mul_b2_stg0_Z_buffer : std_logic_vector(31 downto 0);
signal delay_b1_stg0_A_output_buffer : std_logic_vector(15 downto 0);
signal delay_a1_stg0_A_output_buffer : std_logic_vector(15 downto 0);
signal mul_b0_stg0_Z_buffer : std_logic_vector(31 downto 0);
signal add1_stg0_Sum_buffer : std_logic_vector(31 downto 0);
signal add2_stg0_Sum_buffer : std_logic_vector(31 downto 0);
signal mul_a1_stg0_Z_buffer : std_logic_vector(31 downto 0);
signal mul_a0_stg0_Z_buffer : std_logic_vector(31 downto 0);
signal add2_stg0_C_out_buffer : std_logic;
signal add3_stg0_C_out_buffer : std_logic;
signal add0_stg0_Sum_buffer : std_logic_vector(31 downto 0);
signal mul_b1_stg0_Z_buffer : std_logic_vector(31 downto 0);

begin

process (add0_stg0_Sum_buffer) begin
add0_stg0_Sum <= add0_stg0_Sum_buffer;
end process;



add0_stg0 : entity work.generic_add 
port map(
    A_input => add1_stg0_Sum_buffer,
    B_input => mul_b0_stg0_Z_buffer,
    C_in => add1_stg0_C_out_buffer,
    C_out => add0_stg0_C_out,
    Sum => add0_stg0_Sum_buffer 
    );

add1_stg0 : entity work.generic_add 
port map(
    A_input => mul_a0_stg0_Z_buffer,
    B_input => add2_stg0_Sum_buffer,
    C_in => add2_stg0_C_out_buffer,
    C_out => add1_stg0_C_out_buffer,
    Sum => add1_stg0_Sum_buffer 
    );

add2_stg0 : entity work.generic_add 
port map(
    A_input => add3_stg0_Sum_buffer,
    B_input => mul_b1_stg0_Z_buffer,
    C_in => add3_stg0_C_out_buffer,
    C_out => add2_stg0_C_out_buffer,
    Sum => add2_stg0_Sum_buffer 
    );

add3_stg0 : entity work.generic_add 
port map(
    A_input => mul_a1_stg0_Z_buffer,
    B_input => mul_b2_stg0_Z_buffer,
    C_in => add3_stg0_C_in,
    C_out => add3_stg0_C_out_buffer,
    Sum => add3_stg0_Sum_buffer 
    );

mul_a0_stg0 : entity work.generic_mul 
port map(
    A_input => delay_a0_stg0_A_output_buffer,
    B_input => mul_a0_stg0_B_input,
    Z => mul_a0_stg0_Z_buffer 
    );

mul_a1_stg0 : entity work.generic_mul 
port map(
    A_input => delay_a1_stg0_A_output_buffer,
    B_input => mul_a1_stg0_B_input,
    Z => mul_a1_stg0_Z_buffer 
    );

mul_b0_stg0 : entity work.generic_mul 
port map(
    A_input => mul_b0_stg0_A_input,
    B_input => mul_b0_stg0_B_input,
    Z => mul_b0_stg0_Z_buffer 
    );

mul_b1_stg0 : entity work.generic_mul 
port map(
    A_input => delay_b0_stg0_A_output_buffer,
    B_input => mul_b1_stg0_B_input,
    Z => mul_b1_stg0_Z_buffer 
    );

mul_b2_stg0 : entity work.generic_mul 
port map(
    A_input => delay_b1_stg0_A_output_buffer,
    B_input => mul_b2_stg0_B_input,
    Z => mul_b2_stg0_Z_buffer 
    );

delay_a0_stg0 : entity work.generic_delay 
port map(
    A_input => add0_stg0_Sum_buffer(31 downto 16),
    clk => clk_in,
    A_output => delay_a0_stg0_A_output_buffer 
    );

delay_a1_stg0 : entity work.generic_delay 
port map(
    A_input => delay_a0_stg0_A_output_buffer,
    clk => clk_in,
    A_output => delay_a1_stg0_A_output_buffer 
    );

delay_b0_stg0 : entity work.generic_delay 
port map(
    A_input => delay_b0_stg0_A_input,
    clk => clk_in,
    A_output => delay_b0_stg0_A_output_buffer 
    );

delay_b1_stg0 : entity work.generic_delay 
port map(
    A_input => delay_b0_stg0_A_output_buffer,
    clk => clk_in,
    A_output => delay_b1_stg0_A_output_buffer 
    );

end structural;
