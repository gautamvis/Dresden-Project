--VHDL code for Full Adder

library ieee;
use ieee.std_logic_1164.all;

entity full_add is
	port(
		a: in std_ulogic;
		b: in std_ulogic;
		c_in : in std_ulogic;
		sum : out std_ulogic;
		c_out : out std_ulogic);
end full_add;


architecture arch of full_add is

begin
	sum <= a xor b xor c_in;
	c_out <= (a and b) or (a and c_in) or (b and c_in);
end arch;
