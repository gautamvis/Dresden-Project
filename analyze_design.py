#Design analyzer

#Produces the power, area, error, and delay of a design

#Take in command line input, to get the name of input file(.xml)
#and the intended names of the output file(.txt)

#Import the files containing helper functions, ElementTree, a library used to help parsing xml files
#the sys library, used to redirect output to files
from argparse import ArgumentParser
import xml.etree.ElementTree as el_tree
import sys

#Parse the command line
parser = ArgumentParser()
parser.add_argument("-i", "--inputfile", help="Filename of design (.xml)")
parser.add_argument("-o", "--outputfile",
                    help="Intended name of output file containing results of analysis")
args = parser.parse_args()

#Set up ElementTree, to parse the xml input file, and the xml file containing add/mul info
tree = el_tree.parse(args.inputfile)
root = tree.getroot()
add_mul_tree = el_tree.parse("add_mul_data.xml")
add_mul_data = add_mul_tree.getroot()


#Class to store a design - contains name, list of modules, area, power, error, and delay
class design:

    def __init__(self, modlist, area, power, error, delay):
        self.modlist = []
        self.area = area
        self.power = power
        self.error = error
        self.delay = delay

#Store the adders/muls in the design, based on position they appear in the xml file
#Ex. if xml file lists generic_add, generic_add0_10, generic_mul1, in that order,
#    function will store in generic list [add, add, mul]
def store_types(root, generic_modlist):

    for block in root.findall('block'):
        if block.get('type') == 'add':
            generic_modlist.append('add')

        elif block.get('type') == 'mul':
            generic_modlist.append('mul')

#Recursively generate all possible combinations, and add them to a list
def gen_combinations(generic_modlist, temp_modlist, add_mul_data, counter, design_list):

    #Once the temporary design has the correct number of modules, append a copy of the design
    #   to the list of all possible designs
    if counter == len(generic_modlist):
        temp_design = design([], -1, -1, -1, -1)
        temp_design.modlist = list(temp_modlist)
        design_list.append(temp_design)
        return


    #TODO: could insert some code here to disregard certain designs, if not Pareto optimal
    #To prevent genenerating all possible combinations


    #If next element in design is an adder, run through all possible adders
    if generic_modlist[counter] == 'add':
    
        for add in add_mul_data.findall (".*[@type='add']"):

            temp_modlist.append(add.get('name'))
            gen_combinations(generic_modlist, temp_modlist, add_mul_data, counter+1, design_list)
            temp_modlist.pop()

    #If next element is mul, run through all possible muls
    elif generic_modlist[counter] == 'mul':
    
        for mul in add_mul_data.findall (".*[@type='mul']"):

            temp_modlist.append(mul.get('name'))
            gen_combinations(generic_modlist, temp_modlist, add_mul_data, counter+1, design_list)
            temp_modlist.pop()


#Returns the area and power of the design given
def get_area_power(des, add_mul_data):

    #Variables to return
    area = 0; power = 0; error = 0; delay = 0;

    #Go through each module in the list
    for mod_name in des.modlist:

        #Determine the type of module it is
        for mod in add_mul_data.findall('mod'):
                
            if mod_name == mod.get('name'):
                
                #Area and power are cumulative
                area += float(mod.get('area'))
                power += float(mod.get('power'))

    des.area = area
    des.power = power

#TODO: Return error of design
def get_error(des, add_mul_data):
    return -1

#TODO: Return delay of design
def get_delay(des, add_mul_data):
    return -1

#Main block of code to run helper functions above
#Print all output to the output file
with open(args.outputfile, 'w+') as outfile:

    #Redirect standard output to print to designfile
    sys.stdout = outfile

    #List of add/muls used in design
    generic_modlist = []
    store_types(root, generic_modlist)
    
    #Generate data for all possible combinations of adders/multipliers in the design
    design_list = []
    temp_modlist = []
    counter = 0
    gen_combinations(generic_modlist, temp_modlist, add_mul_data, counter, design_list)
    
    #Derive area, power, error, delay for each potential design
    for des in design_list:
        get_area_power(des, add_mul_data)
        get_error(des, add_mul_data)
        get_delay(des, add_mul_data)

    #FIXME - print for testing
    for des in design_list:
        print(des.modlist, des.area, des.power, des.error, des.delay)


    #TODO: Determine Pareto optimal points from these combinations

    #TODO: Print data for Pareto optimal points


