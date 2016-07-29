#Convert 32 bit .txt output file to .txt decimal file
outfile = "decimaloutput.txt"
with open(outfile, 'w+') as outie:

    with open("32bit_output.txt", 'r') as innie:

        for line in innie:

            bintemp = int(line, 2)
            print(bintemp, file=outie)


