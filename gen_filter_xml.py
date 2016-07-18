#Generate xml file for filter

import gen_filter_helpers
from argparse import ArgumentParser

#Parse command line
#parser = ArgumentParser()
#parser.add_argument("-o", "--outputfile", help="XML file name (to create)")
#parser.add_argument("-t", "--type", help="Type of filter to create")
#parser.add_argument("-s", "--stages", help="Number of stages in filter")
#parser.add_argument("-c", "--coefficients", help="Name of .txt file containing coefficients")


#args = parser.parse_args()
#my_outfile = args.outputfile
#filter_type = args.type
#num_stages = int(args.stages)

#FIXME for testing
my_outfile = "xmloutput.xml"
filter_type = "biquad"
num_stages = 1;


with open(my_outfile, 'w+') as outfile:
    
    print('<?xml version="1.0" encoding="UTF-8"?> \n'
          '<network> \n'
          ,file=outfile
    )
    
    #Biquad
    if filter_type == "biquad":
        gen_filter_helpers.print_biquad(num_stages, outfile)
    
    if filter_type == "FIR":
        gen_filter_helpers.print_fir(num_stages, outfile)
    
    #Insert other types

    print('</network>' ,file=outfile
)