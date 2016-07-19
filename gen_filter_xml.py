#Generate xml file for filter

#Function takes in command line input and outputs an xml file detailing a biquad or fir filter
#Run program with the '-h' flag only to see help

#Import helper functions from file 'gen_filter_helpers.py' and command line parser
import gen_filter_helpers
from argparse import ArgumentParser

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


with open(my_outfile, 'w+') as outfile:
    
    #Print some generic xml stuff
    print('<?xml version="1.0" encoding="UTF-8"?> \n'
          '<network> \n'
          ,file=outfile
    )
    
    #Run helper functions to print the filter based on the type of filter
    
    #Biquad
    if filter_type == "biquad":
        gen_filter_helpers.print_biquad(num_stages, outfile)
    
    #FIR
    if filter_type == "FIR":
        gen_filter_helpers.print_fir(num_stages, outfile)
    

    print('</network>' ,file=outfile
)