	library ieee;
	use ieee.std_logic_1164.all;
	use IEEE.NUMERIC_STD.ALL;

entity generic_mul is
	generic(width: integer := 16);
	port(
		A_input : in std_logic_vector(width-1 downto 0);
		B_input : in std_logic_vector(width-1 downto 0);
		Z : out std_logic_vector(2*width-1 downto 0)
		);
end entity generic_mul;


architecture behavioral of generic_mul is
  signal temp: std_logic_vector(width downto 0);
  signal zeros: std_logic_vector(width downto 1) := (others => '0');
begin
  Z <= std_logic_vector(unsigned(A_input) * unsigned(B_input));
end behavioral;

  
