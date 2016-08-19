#!/bin/bash

#Run gen_filter program(creates filter given  command line input)
#-o = output filename, -t = type of filter, -s = number of stages, -c = coefficient file
python3 gen_filter_xml.py -o "biquad2.xml" -t "biquad2" -s 1 -c "bqstage1coeffs.txt"

#Run xml to vhdl converter
#-i = input xml file, -c = clock/reset mode, -tfi = testbench file input, tfo = tesbench file output
python3 xml_to_vhdl.py -i "biquad2.xml" -c 'off' -tfi "bigtest.txt" -tfo "biquad2_binary_output.txt"

#Compile the components needed to allow the VHDL testbench to run
ghdl -a string_to_stdvec_helpers.vhd
ghdl -a full_add.vhd
ghdl -a generic_add.vhd
ghdl -a generic_mul.vhd
ghdl -a generic_delay.vhd

#Compile the VHDL design file created by 'xml_to_vhdl.py'
ghdl -a biquad2.vhd
#Compile the VHDL testbench file created by 'xml_to_vhdl.py'
ghdl -a biquad2_tb.vhd

#Elaborate the testbench
ghdl -e biquad2_tb

#Run the testbench and produce a waveform file and an output text file
#Currently set to cut off after 300ns, as big test case is very large
ghdl -r biquad2_tb --stop-time=300ns --wave="biquad2.ghw"

#Convert the binary file (testbench output) into decimal values
#-i = input filename, -o = output filename
python3 binarytodecimal.py -i biquad2_binary_output.txt -o biquad2_decimal_output.txt

echo "Done"
