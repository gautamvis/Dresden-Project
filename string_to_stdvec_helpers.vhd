library ieee; 
use ieee.std_logic_1164.all; 
use ieee.numeric_std.all; 
use std.textio.all; 

package str_to_stdvec_helpers is 

	function str_to_stdvec(inp: string) return std_logic_VECTOR;
	function stdvec_to_str(inp: std_logic_VECTOR) return string;

end;

package body str_to_stdvec_helpers is

	function str_to_stdvec(inp: string) return std_logic_VECTOR is

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

end package body;

