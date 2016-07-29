#Generates a testcase with random 32 bit numbers

from argparse import ArgumentParser
import sys
import random

#Parse the command line
parser = ArgumentParser()
parser.add_argument("-o", "--outputfile", help=".txt output file name")
parser.add_argument("-s", "--size",
                    help="Total number of digits per single test case"
                    "For example, if each case requires 2 32 bit inputs and one 16 bit input, s = 80")


args = parser.parse_args()
outfile = args.outputfile
size = int(args.size)

with open(outfile, 'w+') as outf:

    for i in range(0,100):

        tempint = random.randint(0, 2**size)
        tempint2 = bin(tempint)[2:].zfill(size)
        print(tempint2, file=outf)
