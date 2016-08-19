from argparse import ArgumentParser
import sys

#Parse command line to determine name of outputfile, type of filter, number of stages,
#And name of the text file from which coefficients for the multipliers are inputted

parser = ArgumentParser()
parser.add_argument("-o", "--outputfile", help="Name of .txt file (to create)")
parser.add_argument("-i", "--inputfile", help="Name of .txt file with 32bit input")


args = parser.parse_args()
outfile = args.outputfile
infile = args.inputfile

#Convert 32 bit .txt output file to .txt decimal file
with open(outfile, 'w+') as outie:

    with open(infile, 'r') as innie:

        for line in innie:

            bintemp = int(line, 2)
            print(bintemp, file=outie)


