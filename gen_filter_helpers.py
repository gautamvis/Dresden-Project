#Gen filter helpers

#These functions are used to print an FIR or biquad filter, based on what was specified in command line
#Functions are called in 'gen_filter_xml.py' file

#Prints a biquad filter with the designated number of stages
def print_biquad_one(num_stages, coeff_file):

    for stage in range(num_stages):
    
        #Print blocks (4 add, 5 mult, 2 delay per stage)
        #Current defaults are generic_add and generic_mul
        print_blocks('add_a', 'add', 'generic_add', 2, stage)
        print_blocks('add_b', 'add', 'generic_add', 2, stage)
        print_blocks('mul_a', 'mul', 'generic_mul', 2, stage)
        print_blocks('mul_b', 'mul', 'generic_mul', 3, stage)
        print_blocks('delay', 'reg', 'generic_delay', 2, stage)

        #Print the all connections for this stage in the filter
        print_cxn('add_a0', 'Sum', 'delay0', 'A_input', stage)
        print_cxn('add_a0', 'Sum', 'mul_b0', 'A_input', stage)
        print_cxn('add_a1', 'Sum', 'add_a0', 'B_input', stage)
        print_cxn('add_b1', 'Sum', 'add_b0', 'B_input', stage)
        
        print_cxn('delay0', 'A_output', 'mul_a0', 'A_input', stage)
        print_cxn('delay0', 'A_output', 'mul_b1', 'A_input', stage)
        print_cxn('delay0', 'A_output', 'delay1', 'A_input', stage)

        print_cxn('delay1', 'A_output', 'mul_a1', 'A_input', stage)
        print_cxn('delay1', 'A_output', 'mul_b2', 'A_input', stage)


        print_cxn('mul_b0', 'Z', 'add_b0', 'A_input', stage)
        print_cxn('mul_a0', 'Z', 'add_a1', 'A_input', stage)
        print_cxn('mul_b1', 'Z', 'add_b1', 'B_input', stage)
        print_cxn('mul_a1', 'Z', 'add_a1', 'B_input', stage)
        print_cxn('mul_b2', 'Z', 'add_b1', 'A_input', stage)
        
        print_cxn('add_a1', 'C_out', 'add_a0', 'C_in', stage)
        print_cxn('add_b1', 'C_out', 'add_b0', 'C_in', stage)
        
        #Print constant C_in inputs of 0 for certain adders each stage
        print('  <constant destBlk="add_a1_stg' + str(stage) + '" destPort="C_in" value="0"/>')
        print('  <constant destBlk="add_a0_stg' + str(stage) + '" destPort="C_in" value="0"/>')
        print('  <constant destBlk="add_b1_stg' + str(stage) + '" destPort="C_in" value="0"/>')


        #Connecting output of one stage to input of next
        #For the first stage, add_in0's 'b' port connected to input
        if stage > 0:
            print_cxn('add_out0', 'sum', 'add_in0', 'b', stage, "nextstage")

    #Filter consists of 3 'b' multipliers and 2 'a' multipliers
    #Feed this info into function below, to print coefficient blocks
    num_b_muls = 3
    num_a_muls = 2
    print_coeffs(coeff_file, num_stages, num_b_muls, num_a_muls)
    

    print('\n\n')

#Prints a biquad filter with 4 add, 5 mul, and 4 delay blocks per stage
def print_biquad_two(num_stages, coeff_file):

    for stage in range(num_stages):
    
        #Current defaults are generic_add, generic_mul, generic_delay
        print_blocks('add', 'add', 'generic_add', 4, stage)
        print_blocks('mul_a', 'mul', 'generic_mul', 3, stage)
        print_blocks('mul_b', 'mul', 'generic_mul', 3, stage)
        print_blocks('delay_a', 'reg', 'generic_delay', 2, stage)
        print_blocks('delay_b', 'reg', 'generic_delay', 2, stage)


        #Print internal signals
        print_cxn('delay_b0', 'A_output', 'delay_b1', 'A_input', stage)
        print_cxn('delay_b0', 'A_output', 'mul_b1', 'A_input', stage)
        print_cxn('delay_b1', 'A_output', 'mul_b2', 'A_input', stage)

        print_cxn('delay_a0', 'A_output', 'delay_a1', 'A_input', stage)
        print_cxn('delay_a0', 'A_output', 'mul_a1', 'A_input', stage)
        print_cxn('delay_a1', 'A_output', 'mul_a2', 'A_input', stage)
        
        print_cxn('mul_b0', 'Z', 'add0', 'B_input', stage)
        print_cxn('mul_a1', 'Z', 'add2', 'A_input', stage)
        print_cxn('mul_b1', 'Z', 'add2', 'B_input', stage)
        print_cxn('mul_a2', 'Z', 'add3', 'A_input', stage)
        print_cxn('mul_b2', 'Z', 'add3', 'B_input', stage)

        print_cxn('add3', 'Sum', 'add1', 'A_input', stage)
        print_cxn('add3', 'C_out', 'add2', 'C_in', stage)
        
        print_cxn('add2', 'Sum', 'add1', 'B_input', stage)
        print_cxn('add2', 'C_out', 'add1', 'C_in', stage)
        
        print_cxn('add1', 'Sum', 'add0', 'A_input', stage)
        print_cxn('add1', 'C_out', 'add0', 'C_in', stage)
        
        print_cxn('add0', 'Sum', 'mul_a0', 'A_input', stage)
        
        if stage != num_stages:
            print_cxn('mul_a0', 'Z', 'delay_a0', 'A_input', stage)


        #Connecting output of one stage to input of next
        #For the first stage, add_in0's 'b' port connected to input
        if stage > 0:

            print_cxn('mul_a0', 'Z', 'delay_b0', 'A_input', stage, "nextstage")
            print_cxn('mul_a0', 'Z', 'mul_b0', 'A_input', stage, "nextstage")
            

        #Print a constant input of 0 for the C_in input of all add3 blocks
        print('  <constant destBlk="add3_stg' + str(stage) + '" destPort="C_in" value="0"/>')


    #Filter consists of 3 'b' multipliers and 2 'a' multipliers
    #Feed this info into function below, to print coefficient blocks
    num_b_muls = 3
    num_a_muls = 3
    print_coeffs(coeff_file, num_stages, num_b_muls, num_a_muls, 'biquad')

    #Print specified input and output ports
    print_input_output('input', 'mul_b0', 'A_input', 'Input', 16, 0)
    print_input_output('input', 'delay_b0', 'A_input', 'Input', 16, 0)
    print_input_output('output', 'mul_a0', 'Z', 'Sum_output', 32, num_stages-1)
    print_input_output('output', 'delay_a0', 'A_input', 'Sum_output', 32, num_stages-1)



#Print an FIR filter
def print_fir(num_stages, coeff_file):

    #First mul block
    print_blocks('mul_b', 'mul', 'generic_mul', 1, 0, 'fir')
    print_cxn('mul_b', 'Z', 'add', 'A_input', 1, "nextstage", "fir")
    print('\n')

    #Print blocks (1 add, 1 mul, 1 delay per stage)
    for stage in range(1, num_stages+1):

        print_blocks('mul_b', 'mul', 'generic_mul', 1, stage, 'fir')
        print_blocks('add', 'add', 'generic_add', 1, stage, 'fir')
        print_blocks('delay', 'reg', 'generic_delay', 1, stage, 'fir')
        
        print_cxn('delay', 'A_output', 'mul_b', 'A_input', stage, "internal", "fir")
        print_cxn('mul_b', 'Z', 'add', 'B_input', stage, "internal", "fir")
        
        #Connecting output of one stage to input of next
        if stage < num_stages:
            print_cxn('add', 'Sum', 'add', 'A_input', stage+1, "nextstage", "fir")
            print_cxn('add', 'C_out', 'add', 'C_in', stage+1, "nextstage", "fir")
            print_cxn('delay', 'A_output', 'delay', 'A_input', stage+1, "nextstage", "fir")

    #Print coefficients
    num_b_muls = 1
    num_a_muls = 0
    print_coeffs(coeff_file, num_stages+1, num_b_muls, num_a_muls, 'fir')

    #Print specified input/output ports
    print_input_output('input', 'mul_b', 'A_input', 'Input', 16, 0, 'fir')
    print_input_output('input', 'delay', 'A_input', 'Input', 16, 1, 'fir')
    print_input_output('output', 'add', 'Sum', 'Sum_output', 32, num_stages, 'fir')

    #Print a constant input of 0 for the C_in input of first add block
    print('  <constant destBlk="add1" destPort="C_in" value="0"/>')



#General template to print all blocks of an xml
def print_blocks(block_name, block_type, instance_type, num_blocks, stage_num, type='biquad'):

    #For each block in the filter, print the block info and corresponding ports
    for block in range(num_blocks):
        
        if type == 'fir':
            print('  <block name="{bname}{stage}" type="{btype}" instance_type="{ins_type}">'
                  .format(bname=block_name, stage=stage_num,
                          btype=block_type, ins_type=instance_type)
            )
        
        elif type == 'biquad':
            print('  <block name="{bname}{num}_stg{stage}" type="{btype}" instance_type="{ins_type}">'
                  .format(bname=block_name, num=block, stage=stage_num,
                          btype=block_type, ins_type=instance_type)
            )
        
        #Print ports based on what kind of block is specified
        if block_type == "add":
            print_adder_ports()
        elif block_type == "mul":
            print_mult_ports()
        elif block_type == "reg":
            print_delay_ports()

        print('  </block> \n')


#General template to print a connection
def print_cxn(srcBlk, srcPort, destBlk, destPort, stage, cxntype="internal", filtertype="biquad"):

    #If the connection is internal, the stage of the source and dest port are the same
    #If the connection is external, the stage of the source is one less than the destination
    stagenum1 = stage if cxntype == "internal" else int(stage)-1
    stagenum2 = stage
    
    #Print the cxn
    if filtertype == "biquad":
        print('  <connection srcBlk="{sb}_stg{num}" srcPort="{sp}" destBlk="{db}_stg{num2}" destPort="{dp}"/>'
              .format(sb=srcBlk, sp=srcPort, num = stagenum1,num2 = stagenum2, db=destBlk, dp=destPort))
    else:
        print('  <connection srcBlk="{sb}{num}" srcPort="{sp}" destBlk="{db}{num2}" destPort="{dp}"/>'
              .format(sb=srcBlk, sp=srcPort, num = stagenum1,num2 = stagenum2, db=destBlk, dp=destPort))


#General template to print a port
def print_port(port_name, port_type, width):

    print('    <port name="{pname}" type="{ptype}" width="{w}"/>'
          .format(pname=port_name, ptype=port_type, w=width)
    )
                  
#Print a default adder with 3 inputs 2 outputs
def print_adder_ports():

    print_port("A_input", "in", "32")
    print_port("B_input", "in", "32")
    print_port("C_in", "in", "1")
    print_port("C_out", "out", "1")
    print_port("Sum", "out", "32")


#Print a default multiplier with 2 inputs 1 outputs
def print_mult_ports():
    
    print_port("A_input", "in", "16")
    print_port("B_input", "in", "16")
    print_port("Z", "out", "32")


#Print a delay block
def print_delay_ports():

    print_port("A_input", "in", "16")
    print_port("clk", "in", "1")
    print_port("A_output", "out", "16")


#Print input/output
def print_input_output(type, srcBlk, srcPort, buffer, srcWidth, stage_num, filtertype='biquad'):

        if filtertype == 'fir':
            print(('\t<input' if type == 'input' else '\t<output') + ' srcBlk="{sb}{num}" srcPort="{sp}" srcWidth="{sw}" buffer="{b}"/>'
                  .format(sb = srcBlk, num = stage_num, sp = srcPort, sw = srcWidth, b = buffer))
        else:
            print(('\t<input' if type == 'input' else '\t<output') + ' srcBlk="{sb}_stg{num}" srcPort="{sp}" srcWidth="{sw}" buffer="{b}"/>'
                      .format(sb = srcBlk, num = stage_num, sp = srcPort, sw = srcWidth, b = buffer))


#Print the filter's constant coefficients from coefficients.txt file
#Text file contains all the coefficients for one stage of a filter on one line
def print_coeffs(coeff_file, num_stages, num_b_muls, num_a_muls, type='biquad'):

    #To keep track of line number in the input file
    total_num_muls = num_a_muls + num_b_muls
    
    with open(coeff_file) as infile:
        
        lines = infile.read().split()
        if type == 'biquad':
            for stage in range (0,num_stages):
            
                #Print constant coefficient blocks for all 'mul_b' in the stage
                print('\n'.join('  <constant destBlk="mul_b' + str(x) + '_stg' + str(stage)
                + '" destPort="B_input" value="' + lines[x+(total_num_muls*stage)] + '"/>' for x in range(0, num_b_muls)))
            
                #Print constant coefficient blocks for all 'mul_a' in the stage
                print('\n'.join('  <constant destBlk="mul_a' + str(x) + '_stg' + str(stage)
                + '" destPort="B_input" value="' + lines[x+num_b_muls+(total_num_muls*stage)] + '"/>' for x in range(0, num_a_muls)))

        elif type == 'fir':
            #Print constant coefficient blocks for all muls
            print('\n'.join('  <constant destBlk="mul_b' + str(stage) + '" destPort="B_input" value="'
                  + lines[stage] + '"/>' for stage in range(0, num_stages)))






