#Generate xml file for filter

#Function takes in command line input(.xml file to create, type of filter,
# number of stages, and name of the .txt file with coefficients for multipliers
#Run program with the '-h' flag only to see help

#Import helper functions from file 'gen_filter_helpers.py', command line parser, sys
import gen_filter_helpers
from argparse import ArgumentParser
import sys

#Parse command line to determine name of outputfile, type of filter, number of stages,
#And name of the text file from which coefficients for the multipliers are inputted
parser = ArgumentParser()
parser.add_argument("-o", "--outputfile", help="Name of .xml (to create)")
parser.add_argument("-t", "--type", help="Type of filter to create (biquad or FIR")
parser.add_argument("-s", "--stages", help="Number of stages in filter")
parser.add_argument("-c", "--coefficients", help="Name of .txt file containing coefficients")

args = parser.parse_args()
my_outfile = args.outputfile
filter_type = args.type
num_stages = int(args.stages)
coeff_file = args.coefficients


with open(my_outfile, 'w+') as outfile:
    
    sys.stdout = outfile
    
    #Print some generic xml stuff
    print('<?xml version="1.0" encoding="UTF-8"?> \n'
          '<network> \n'
    )
    
    #Run helper functions to print the filter's blocks, ports, connections, known inputs/outputs
    
    #Biquad v1
    if filter_type == "biquad1":
        gen_filter_helpers.print_biquad_one(num_stages, coeff_file)
    
    #Biquad v2
    if filter_type == "biquad2":
        gen_filter_helpers.print_biquad_two(num_stages, coeff_file)
    
    #FIR
    if filter_type == "FIR":
        gen_filter_helpers.print_fir(num_stages, coeff_file)


    print('\n</network>')
