#Gen filter helpers

#These functions are used to print an FIR or biquad filter, based on what was specified in command line
#Functions are called in 'gen_filter_xml.py' file

#Prints a biquad filter with the designated number of stages
def print_biquad(num_stages, outfile):


    for stage in range(num_stages):
    
        #Print blocks (4 add, 5 mult, 2 delay per stage)
        #Current defaults are generic_add and generic_mul
        print_blocks('add_in', 'add', 'generic_add', 2, stage, outfile)
        print_blocks('add_out', 'add', 'generic_add', 2, stage, outfile)
        print_blocks('mul_a', 'mul', 'generic_mul', 2, stage, outfile)
        print_blocks('mul_b', 'mul', 'generic_mul', 3, stage, outfile)
        print_blocks('delay', 'reg', 'register', 2, stage, outfile)

        #Print the all connections for this stage in the filter
        print_cxn('add_in0', 'sum', 'delay0', 'd', stage, outfile, "internal")
        print_cxn('add_in0', 'sum', 'mul_b0', 'a', stage, outfile, "internal")
        print_cxn('add_in1', 'sum', 'add_in0', 'b', stage, outfile, "internal")
        print_cxn('add_out1', 'sum', 'add_out0', 'b', stage, outfile, "internal")
        
        print_cxn('delay0', 'q', 'mul_a1', 'a', stage, outfile, "internal")
        print_cxn('delay0', 'q', 'mul_b1', 'a', stage, outfile, "internal")
        print_cxn('delay0', 'q', 'delay1', 'd', stage, outfile, "internal")

        print_cxn('delay1', 'q', 'mul_a2', 'a', stage, outfile, "internal")
        print_cxn('delay1', 'q', 'mul_b2', 'a', stage, outfile, "internal")


        print_cxn('mul_b0', 'r', 'add_out0', 'a', stage, outfile, "internal")
        print_cxn('mul_a1', 'r', 'add_in1', 'a', stage, outfile, "internal")
        print_cxn('mul_b1', 'r', 'add_out1', 'b', stage, outfile, "internal")
        print_cxn('mul_a2', 'r', 'add_in1', 'b', stage, outfile, "internal")
        print_cxn('mul_b2', 'r', 'add_out1', 'a', stage, outfile, "internal")
        
        print_cxn('add_in0', 'cin', 'add_in1', 'cout', stage, outfile, "internal")
        print_cxn('add_out0', 'cin', 'add_out1', 'cout', stage, outfile, "internal")

        
        #Connecting output of one stage to input of next
        #For the first stage, add_in0's 'b' port connected to input
        if stage > 0:
            print_cxn('add_out0', 'sum', 'add_in0', 'b', stage, outfile, "nextstage")


        print('\n\n', file=outfile)

#Print an FIR filter
def print_fir(num_stages, outfile):

    #First mul block
    print_blocks('mul', 'mul', 'generic_mul', 1, -1, outfile)

    #Print blocks (1 add, 1 mul, 1 delay per stage)
    for stage in range(num_stages):

        print_blocks('mul', 'mul', 'generic_mul', 1, stage, outfile)
        print_blocks('add', 'add', 'generic_add', 1, stage, outfile)
        print_blocks('delay', 'reg', 'register', 1, stage, outfile)


        if stage == 0:
            print_cxn_next_stage('mul', 'r', 'add', 'a', stage, outfile, "internal")
            print_cxn('mul', 'r', 'add', 'b', stage, outfile, "internal")
            print_cxn('delay', 'q', 'mul', 'a', stage, outfile, "internal")

        #Connecting output of one stage to input of next
        #For the first stage, add_in0's 'b' port connected to input
        else:
            print_cxn('add', 'sum', 'add', 'b', stage, outfile, "nextstage")
            print_cxn('delay', 'd', 'delay', 'q', stage, outfile, "nextstage")
            print_cxn('delay', 'q', 'mul', 'a', stage, outfile)


        print('\n\n', file=outfile)


#General template to print all blocks of an xml
def print_blocks(block_name, block_type, instance_type, num_blocks, stage_num, outfile):

    #For each block in the filter, print the block info and corresponding ports
    for block in range(num_blocks):
        
        print('  <block name="{bname}{num}_stg{stage}" type="{btype}" instance_type="{ins_type}">'
              .format(bname=block_name, num=block, stage=stage_num,
                      btype=block_type, ins_type=instance_type)
              ,file=outfile
        )
        
        #Print ports based on what kind of block is specified
        if block_type == "add":
            print_adder_ports(outfile)
        elif block_type == "mul":
            print_mult_ports(outfile)
        elif block_type == "reg":
            print_delay_ports(outfile)

        print('  </block> \n', file=outfile)


#General template to print a connection
def print_cxn(srcBlk, srcPort, destBlk, destPort, stage, outfile, cxntype):


    #Connection within a filter
    if cxntype == internal:
        print('  <connection srcBlk="{sb}_stg{num}" srcPort="{sp}" destBlk="{db}_stg{num}" destPort="{dp}"/>'
              .format(sb=srcBlk, sp=srcPort, num = stage, db=destBlk, dp=destPort)
              ,file=outfile
        )

    #Connection from output of one filter to input of another
    else:
        print('  <connection srcBlk="{sb}_stg{num}" srcPort="{sp}" destBlk="{db}_stg{num2}" destPort="{dp}"/>'
              .format(sb=srcBlk, sp=srcPort, num = int(stage) - 1,
                      num2 = stage, db=destBlk, dp=destPort)
              ,file=outfile
              )


#General template to print a port
def print_port(port_name, port_type, width, outfile):

    print('    <port name="{pname}" type="{ptype}" width="{w}"/>'
          .format(pname=port_name, ptype=port_type, w=width)
          ,file=outfile
    )
                  
#Print a default adder with 3 inputs 2 outputs
def print_adder_ports(outfile):

    print_port("a", "in", "32", outfile)
    print_port("b", "in", "32", outfile)
    print_port("sum", "out", "32", outfile)
    print_port("cin", "in", "1", outfile)
    print_port("cout", "out", "1", outfile)


#Print a default multiplier with 2 inputs 1 outputs
def print_mult_ports(outfile):
    
    print_port("a", "in", "16", outfile)
    print_port("b", "in", "16", outfile)
    print_port("r", "out", "32", outfile)


#Print a delay block
def print_delay_ports(outfile):

    print_port("d", "in", "32", outfile)
    print_port("q", "out", "32", outfile)


