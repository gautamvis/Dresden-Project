# Code to test approximate Adders/Multipliers

Code is currently split in several parts:

    1. Gen filter - create an FIR or Biquad filter
    2. XML to VHDL - create a design and testbench VHDL file
    3. Run testbench - run the testbench file, convert the resulting .txt file from 32 bit binary to decimal,
       and produce waveform output file
    4. Analyze design - generate all possible designs of a given xml using the various inexact add/mul modules,
       and output the ones that match the Pareto optimal constraints
 
 Parts 1-3 are run with 'runprog.sh' script
 Part 4 is not functionally complete

## Gen filter

Takes in command line input (type of filter('biquad1', 'biquad2', 'FIR'), number of stages, and .txt filename containing coefficients for multipliers) and produces an XML file (which can then be used as input for the XML to VHDL function)
Compiled by default python compiler (version 3.5)

	* gen_filter_xml.py: Main function
	* gen_filter_helpers.py: Helper functions to generate the xml file
    * bqstage1coeffs.txt: Coefficient file for 1 stage biquad
    * bqstage2coeffs.txt: Coefficient file for 2 stage biquad
    * fircoeffs.txt: Coefficient file for FIR

           
## XML to VHDL

Takes in a given XML input file and produces a design file and a testbench file in VHDL
Compiled by default python compiler (version 3.5)

	* xml_to_vhdl.py: Main function
	* xml_to_vhdl_design_functions.py: Contains helper functions to create the design file 
	* xml_to_vhdl_tb_functions.py: Contains helper functions to create the testbench file
    * sample_xml_input.xml: File fed to the main function
     
## Testbench

Run the testbench created by XML to VHDL function 
Compiled by GHDL version 0.29

    * full_add.vhd: Component of the design created
    * generic_add.vhd: Component of the design created
    * generic_mul.vhd: Component of the design created
    * generic_delay.vhd: Component of the design created
    * string_to_stdvec_helpers.vhd: Used inside the testbench to convert input from file
    * bigtest.txt: Input test file
    * simpletest.txt: Input test file
    * 32bit_input.txt: Input test file 
    * binarytodecimal.py: Convert binary into decimal (for use with testbench output file)

## Analyze Design

Takes in an xml file with a design, and outputs the area, power and estimated error and delay 
of the Pareto optimal designs created by using inexact adders and multipliers in the design
Compiled by default python compiler (version 3.5)

    * analyze_design.py: Main function to do what is described above
    # add_mul_modules.xml: Contains relevant data about area, power, etc. of inexact add/muls
