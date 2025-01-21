# -*- coding: utf-8 -*-
"""
Compiler backend targeting the Hack processor.
Translates from a stack-based intermediate representation language for the virtual machine to Hack assembly code.

Author: Naga Kandasamy
Date modified: November 7, 2024

Student name(s): Ricky Chen, Phong Nguyen 
Date modified: 11/13/24
"""
import os
import sys


def generate_exit_code():
    """Generate some epilogue code that places the program, upon completion, into 
    an infinite loop. 
    """
    s = []
    s.append('@ALL_DONE')
    s.append('(ALL_DONE)')
    s.append('0;JMP')
    return s


def generate_push_code(segment, index):
    """Generate assembly code to push value into the stack.
    Variable is read from the specified memory segment using (base + index) addressing.
    """
    s = [] 
    segment_dict = {
        'local': '@LCL',
        'argument' : '@ARG',
        'this' : '@THIS',
        'that' : '@THAT',
        'temp' : '@5',
        'pointer' : '@3', 
        'static' : '@16'
    }

    # FIXME: complete implmentation for local, argument, this, that, temp, pointer, and static segments.
    if segment == 'constant':
        # FIXME: complete the implementation 
        s.append('@' + index)
        s.append("D = A")
    else:
        s.append(segment_dict[segment])
        if segment in list(segment_dict)[:4]:
            s.append("D = M")
        else:
            s.append("D = A")
        s.append("@" + index)
        s.append("A = D + A")
        s.append("D = M")
    s.append("@SP")
    s.append("A = M")
    s.append("M = D")
    s.append("@SP")
    s.append("M = M + 1")

    return s
    

def generate_pop_code(segment, index):
    """Generate assembly code to pop value from the stack.
    The popped value is stored in the specified memory segment using (base + index) 
    addressing.
    """
    s = []
    segment_dict = {
        'local': '@LCL',
        'argument' : '@ARG',
        'this' : '@THIS',
        'that' : '@THAT',
        'temp' : '@5',
        'pointer' : '@3', 
        'static' : '@16'
    }

    # FIXME: complete implmentation for local, argument, this, that, temp, pointer, and static segments.
    s.append(segment_dict[segment])
    if segment in list(segment_dict)[:4]:
        s.append("D = M")
    else:
        s.append("D = A")
    s.append("@" + index)
    s.append("D = D + A")
    s.append("@R13")
    s.append("M = D")
    s.append("@SP")
    s.append("M = M - 1")
    s.append("A = M")
    s.append("D = M")
    s.append("@R13")
    s.append("A = M")
    s.append("M = D")  

    return s


def generate_arithmetic_or_logic_code(operation):
    """Generate assembly code to perform the specified ALU operation. 
    The two operands are popped from the stack and the result of the operation 
    placed back in the stack.
    """
    s = []
    operation_dict = {
        'add': 'D = M + D',
        'sub' : 'D = M - D',
        'or' : 'D = M | D',
        'and' : 'D = M & D'
    }

    # FIXME: complete implementation for + , - , | , and & operators
    s.append("@SP")
    s.append("M = M - 1")
    s.append("A = M")
    s.append("D = M")
    s.append("@SP")
    s.append("M = M - 1")
    s.append("A = M")
    s.append(operation_dict[operation])
    s.append("@SP")
    s.append("A = M")
    s.append("M = D")
    s.append("@SP")
    s.append("M = M + 1")        
            
    return s


def generate_unary_operation_code(operation):
    """Generate assembly code to perform the specified unary operation. 
    The operand is popped from the stack and the result of the operation 
    placed back in the stack.
    """
    s = []
    operation_dict = {
        'not': 'D = !M',
        'neg' : 'D = -M'
    }
    
    # FIXME: complete implementation for bit-wise not (!) and negation (-) operatiors
    s.append("@SP")
    s.append("M = M - 1")
    s.append("A = M")
    s.append(operation_dict[operation])
    s.append("@SP")
    s.append("A = M")
    s.append("M = D")
    s.append("@SP")
    s.append("M = M + 1")
    
    return s


def generate_relation_code(operation, line_number):
    """Generate assembly code to perform the specified relational operation. 
    The two operands are popped from the stack and the result of the operation 
    placed back in the stack.
    """
    s = []
    label_1 = ''
    label_2 = ''
    relation_dict = {
        'lt': 'D;JLT',
        'gt' : 'D;JGT',
        'eq' : 'D;JEQ'
    }

    if operation == 'lt':
        label_1 = 'IF_LT_'
    elif operation == 'gt':
        label_1 = 'IF_GT_'
    elif operation == 'eq':
        label_1 = 'IF_EQ_'
    label_1 += str(line_number)
    label_2 = 'END_IF_ELSE_' + str(line_number)

    s.append('@SP')
    s.append('M=M-1')           # Adjust stack pointer
    s.append('A=M')
    s.append('D=M')             # D  = operand2
    s.append('@SP')
    s.append('M=M-1')           # Adjust stack pointer to get to operand #1
    s.append('A=M')

    # FIXME: complete implementation for eq and gt operations
    s.append('D = M - D')       # D = operand1 - operand2
    s.append('@' + label_1)
    s.append(relation_dict[operation])

    s.append('@SP')
    s.append('A = M')
    s.append('M = 0')          # Push result on stack 
    s.append('@SP')
    s.append('M = M + 1')
    s.append('@' + label_2)
    s.append('0;JMP')
    s.append('(' + label_1 + ')')
    s.append('@SP')
    s.append('A = M')
    s.append('M = -1')        # Push result on stack
    s.append('@SP')
    s.append('M = M + 1')
    s.append('(' + label_2 + ')')

    return s
  
def generate_set_code(register, value):
    """Generate assembly code for set"""
    s = []
    
    s.append('@' + value)
    s.append('D=A')
    
    if register == 'sp':
        s.append('@SP')
    
    if register == 'local':
        s.append('@LCL')
    
    if register == 'argument':
        s.append('@ARG')
        
    if register == 'this':
        s.append('@THIS')
        
    if register == 'that':
        s.append('@THAT')
        
    s.append('M=D')

    return s


def translate(tokens, line_number):
    """Translate a VM command/statement into the corresponding Hack assembly commands/statements."""
    s = []
    
    if tokens[0] == 'push':
        s = generate_push_code(tokens[1], tokens[2])    # Generate code to push into stack
        
    elif tokens[0] == 'pop':
        s = generate_pop_code(tokens[1], tokens[2])     # Generate code to pop from stack
        
    elif tokens[0] == 'add' or tokens[0] == 'sub' \
         or tokens[0] == 'mult' or tokens[0] == 'div' \
         or tokens[0] == 'or' or tokens[0] == 'and':
        s = generate_arithmetic_or_logic_code(tokens[0])  # Generate code for ALU operation
        
    elif tokens[0] == 'neg' or tokens[0] == 'not':
        s = generate_unary_operation_code(tokens[0])    # Generate code for unary operations
        
    elif tokens[0] == 'eq' or tokens[0] == 'lt' or tokens[0] == 'gt':
        s = generate_relation_code(tokens[0], line_number)
      
    elif tokens[0] == 'set':
        s = generate_set_code(tokens[1], tokens[2])
    
    elif tokens[0] == 'end':
        s = generate_exit_code()
        
    else:
        print('translate: Unknown operation')           # Unknown operation 
    
    return s

def run_vm_translator(file_name):
    """Main translator code. """
    assembly_code = []
    line_number = 1
    
    with open(file_name, 'r') as f:
        for command in f:        
            # print("Translating line:", line_number, command)
            tokens = (command.rstrip('\n')).split()
            
            # Ignore blank lines
            if not tokens:
                continue            
            
            if tokens[0] == '//':
                continue                                # Ignore comment       
            else:
                s = translate(tokens, line_number)
                line_number = line_number + 1
            
            if s:
                for i in s:
                    assembly_code.append(i)
            else:
                assembly_code = []
                return assembly_code
    
    return assembly_code


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: Python vm_translator.py file-name.vm")
        print("Example: Python vm_translator.py some-program.vm")
    else:
        print("Translating VM file:", sys.argv[1])
        print()
        file_name_minus_extension, _ = os.path.splitext(sys.argv[1])
        output_file = file_name_minus_extension + '.asm'
        assembly_code = run_vm_translator(sys.argv[1])
        if assembly_code:
            print('Assembly code generated successfully');
            print('Writing output to file:', output_file)
            f = open(output_file, 'w')
            for s in assembly_code:
                f.write('%s\n' %s)
            f.close()
        else:
            print('Error generating assembly code')