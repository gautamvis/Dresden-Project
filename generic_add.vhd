	library ieee;
	use ieee.std_logic_1164.all;
	use IEEE.NUMERIC_STD.ALL;

entity generic_add is
	generic(width: integer := 32);
	port(
		A_input : in std_logic_vector(width-1 downto 0);
		B_input : in std_logic_vector(width-1 downto 0);
		C_in : in std_logic;
		C_out : out std_logic;
		Sum : out std_logic_vector(width-1 downto 0)
		);
end entity generic_add;


architecture behavioral of generic_add is
  signal temp: std_logic_vector(width downto 0);
  signal zeros: std_logic_vector(width downto 1) := (others => '0');
begin
  temp <= std_logic_vector(unsigned('0' & A_input) + unsigned('0' & B_input) + unsigned(zeros & C_in));
  Sum <= temp(width-1 downto 0);
  C_out <= temp(width);
end behavioral;

  