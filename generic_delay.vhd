	library ieee;
	use ieee.std_logic_1164.all;
	use IEEE.NUMERIC_STD.ALL;

entity generic_delay is
	generic(width: integer := 16);
	port(
		A_input : in std_logic_vector(width-1 downto 0);
		clk	: in std_logic;
--		rst : in std_logic ;
		A_output : out std_logic_vector(width-1 downto 0)
		);
end entity generic_delay;


architecture behavioral of generic_delay is
  signal temp: std_logic_vector(width-1 downto 0) := (others => '0');
begin
 
process(clk)
    begin
    if rising_edge(clk) then
      temp <= A_input;
    end if;
end process;

A_output <= temp;
end behavioral;

    