#Gen filter helpers

#These functions are used to print an FIR or biquad filter, based on what was specified in command line
#Functions are called in 'gen_filter_xml.py' file

#Prints a biquad filter with the designated number of stages
def print_biquad_one(num_stages):

    for stage in range(num_stages):
    
        #Print blocks (4 add, 5 mult, 2 delay per stage)
        #Current defaults are generic_add and generic_mul
        print_blocks('add_in', 'add', 'generic_add', 2, stage)
        print_blocks('add_out', 'add', 'generic_add', 2, stage)
        print_blocks('mul_a', 'mul', 'generic_mul', 2, stage)
        print_blocks('mul_b', 'mul', 'generic_mul', 3, stage)
        print_blocks('delay', 'reg', 'generic_delay', 2, stage)

        #Print the all connections for this stage in the filter
        print_cxn('add_in0', 'Sum', 'delay0', 'A_input', stage)
        print_cxn('add_in0', 'Sum', 'mul_b0', 'A_input', stage)
        print_cxn('add_in1', 'Sum', 'add_in0', 'B_input', stage)
        print_cxn('add_out1', 'Sum', 'add_out0', 'B_input', stage)
        
        print_cxn('delay0', 'A_output', 'mul_a1', 'A_input', stage)
        print_cxn('delay0', 'A_output', 'mul_b1', 'A_input', stage)
        print_cxn('delay0', 'A_output', 'delay1', 'A_input', stage)

        print_cxn('delay1', 'A_output', 'mul_a2', 'A_input', stage)
        print_cxn('delay1', 'A_output', 'mul_b2', 'A_input', stage)


        print_cxn('mul_b0', 'Z', 'add_out0', 'A_input', stage)
        print_cxn('mul_a0', 'Z', 'add_in1', 'A_input', stage)
        print_cxn('mul_b1', 'Z', 'add_out1', 'B_input', stage)
        print_cxn('mul_a1', 'Z', 'add_in1', 'B_input', stage)
        print_cxn('mul_b2', 'Z', 'add_out1', 'A_input', stage)
        
        print_cxn('add_in0', 'C_in', 'add_in1', 'C_out', stage)
        print_cxn('add_out0', 'C_in', 'add_out1', 'C_out', stage)

        
        #Connecting output of one stage to input of next
        #For the first stage, add_in0's 'b' port connected to input
        if stage > 0:
            print_cxn('add_out0', 'sum', 'add_in0', 'b', stage, "nextstage")


        print('\n\n')

def print_biquad_two(num_stages):

     for stage in range(num_stages):
    
        #Print blocks (4 add, 6 mult, 4 delay per stage)
        #Current defaults are generic_add and generic_mul
        print_blocks('add', 'add', 'generic_add', 4, stage)
        print_blocks('mul_a', 'mul', 'generic_mul', 2, stage)
        print_blocks('mul_b', 'mul', 'generic_mul', 3, stage)
        print_blocks('delay_a', 'reg', 'generic_delay', 2, stage)
        print_blocks('delay_b', 'reg', 'generic_delay', 2, stage)

        #Print internal signals
        print_cxn('delay_b0', 'A_output', 'delay_b1', 'A_input', stage)
        print_cxn('delay_b0', 'A_output', 'mul_b1', 'A_input', stage)
        print_cxn('delay_b1', 'A_output', 'mul_b2', 'A_input', stage)

        print_cxn('delay_a0', 'A_output', 'delay_a2', 'A_input', stage)
        print_cxn('delay_a0', 'A_output', 'mul_a0', 'A_input', stage)
        print_cxn('delay_a1', 'A_output', 'mul_a1', 'A_input', stage)
        
        print_cxn('mul_b2', 'Z', 'add3', 'B_input', stage)
        print_cxn('mul_a1', 'Z', 'add3', 'A_input', stage)

        print_cxn('mul_b1', 'Z', 'add2', 'B_input', stage)
        print_cxn('add3', 'Sum', 'add2', 'A_input', stage)
        print_cxn('add3', 'C_out', 'add2', 'C_in', stage)
        
        print_cxn('add2', 'Sum', 'add1', 'B_input', stage)
        print_cxn('mul_a0', 'Z', 'add1', 'A_input', stage)
        print_cxn('add2', 'C_out', 'add1', 'C_in', stage)
        
        
        print_cxn('mul_b0', 'Z', 'add0', 'B_input', stage)
        print_cxn('add1', 'Sum', 'add0', 'A_input', stage)
        print_cxn('add1', 'C_out', 'add0', 'C_in', stage)

        print_cxn('add0', 'Sum', 'delay_a0', 'A_input', stage)
        

        #Connecting output of one stage to input of next
        #For the first stage, add_in0's 'b' port connected to input
        if stage > 0:

            print_cxn('add0', 'Sum', 'delay0', 'A_input', stage, "nextstage")
            print_cxn('add0', 'Sum', 'mul_b0', 'A_input', stage, "nextstage")

        
        print('\n\n')



#Print an FIR filter
def print_fir(num_stages):

    #First mul block
    print_blocks('mul', 'mul', 'generic_mul', 1, -1)

    #Print blocks (1 add, 1 mul, 1 delay per stage)
    for stage in range(num_stages):

        print_blocks('mul', 'mul', 'generic_mul', 1, stage)
        print_blocks('add', 'add', 'generic_add', 1, stage)
        print_blocks('delay', 'reg', 'generic_delay', 1, stage)


        if stage == 0:
            print_cxn_next_stage('mul', 'r', 'add', 'a', stage)
            print_cxn('mul', 'r', 'add', 'b', stage)
            print_cxn('delay', 'q', 'mul', 'a', stage)

        #Connecting output of one stage to input of next
        #For the first stage, add_in0's 'b' port connected to input
        else:
            print_cxn('add', 'sum', 'add', 'b', stage, "nextstage")
            print_cxn('delay', 'd', 'delay', 'q', stage, "nextstage")
            print_cxn('delay', 'q', 'mul', 'a', stage)


        print('\n\n')


#General template to print all blocks of an xml
def print_blocks(block_name, block_type, instance_type, num_blocks, stage_num):

    #For each block in the filter, print the block info and corresponding ports
    for block in range(num_blocks):
        
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
def print_cxn(srcBlk, srcPort, destBlk, destPort, stage, cxntype = "internal"):

    #If the connection is internal, the stage of the source and dest port are the same
    #If the connection is external, the stage of the source is one less than the destination
    stagenum1 = stage if cxntype == "internal" else int(stage)-1
    stagenum2 = stage
    
    #Print the cxn
    print('  <connection srcBlk="{sb}_stg{num}" srcPort="{sp}" destBlk="{db}_stg{num2}" destPort="{dp}"/>'
          .format(sb=srcBlk, sp=srcPort, num = stagenum1,
                  num2 = stagenum2, db=destBlk, dp=destPort)
          )

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

    print_port("A_input", "in", "32")
    print_port("clk", "in", "1")
    print_port("A_output", "out", "32")
    

def get_coefficients(sourcefile):

    with open(sourcefile, 'w+') as source:

        coeff_list = source.readlines()

    return coeff_list


