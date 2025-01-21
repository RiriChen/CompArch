# -*- coding: utf-8 -*-
"""Assembler for the Hack processor.

Author: Naga Kandasamy
Date modified: October 28, 2024

Student name(s): Ricky Chen, Phong Nguyen
Date modified: 10/29/24 
"""

import os
import sys

"""The comp field is a c1 c2 c3 c4 c5 c6"""
valid_comp_patterns = {'0':'0101010', 
                       '1':'0111111',
                       '-1':'0111010',
                       'D':'0001100',
                       'A':'0110000',
                       '!D':'0001101',
                       '!A':'0110001',
                       '-D':'0001111',
                       '-A':'0110011',
                       'D+1':'0011111',
                       'A+1':'0110111',
                       'D-1':'0001110',
                       'A-1':'0110010',
                       'D+A':'0000010',
                       'D-A':'0010011',
                       'A-D':'0000111',
                       'D&A':'0000000',
                       'D|A':'0010101',
                       'M':'1110000',
                       '!M':'1110001',
                       '-M':'1110011',
                       'M+1':'1110111',
                       'M-1':'1110010',
                       'D+M':'1000010',
                       'M+D':'1000010',
                       'D-M':'1010011',
                       'M-D':'1000111',
                       'D&M':'1000000',
                       'D|M':'1010101'
                       }

"""The dest bits are d1 d2 d3"""
valid_dest_patterns = {'null':'000',
                       'M':'001',
                       'D':'010',
                       'MD':'011',
                       'A':'100',
                       'AM':'101',
                       'AD':'110',
                       'AMD':'111'
                       }

"""The jump fields are j1 j2 j3"""
valid_jmp_patterns =  {'null':'000',
                       'JGT':'001',
                       'JEQ':'010',
                       'JGE':'011',
                       'JLT':'100',
                       'JNE':'101',
                       'JLE':'110',
                       'JMP':'111'
                       }

"""Symbol table populated with predefined symbols and RAM locations"""
symbol_table = {'SP':0,
                'LCL':1,
                'ARG':2,
                'THIS':3,
                'THAT':4,
                'R0':0,
                'R1':1,
                'R2':2,
                'R3':3,
                'R4':4,
                'R5':5,
                'R6':6,
                'R7':7,
                'R8':8,
                'R9':9,
                'R10':10,
                'R11':11,
                'R12':12,
                'R13':13,
                'R14':14,
                'R15':15,
                'SCREEN':16384,
                'KBD':24576
                }

def print_intermediate_representation(ir):
    """Print intermediate representation"""
    
    for i in ir:
        print()
        for key, value in i.items():
            print(key, ':', value)

        
def print_instruction_fields(s):
    """Print fields in instruction"""
    
    print()
    for key, value in s.items():
        print(key, ':', value)


def valid_tokens(s):
    """Return True if tokens belong to valid instruction-field patterns"""
    if s['status'] == -1 :
        return True
    
    if s['instruction_type'] == 'C_INSTRUCTION' or s['instruction_type'] == 'J_INSTRUCTION':
        return s['dest'] in valid_dest_patterns and s['comp'] in valid_comp_patterns and ['jmp'] in valid_jmp_patterns
    elif s['instruction_type'] == 'A_INSTRUCTION':
        return s['value_type'] == 'SYMBOL' or ['value_type'] == 'NUMERIC'
    elif s['instruction_type'] == 'PSEUDO_INSTRUCTION':
        return s['value_type'] == 'SYMBOL'

    return False


def parse(command):
    """Implements finite automate to scan hack assembly commands and parse them.

    WHITE SPACE: Space characters are ignored. Empty lines are ignored.

    COMMENT: Text beginning with two slashes (//) and ending at the end of the line is considered 
    comment and is ignored.
 
    CONSTANTS: Must be non-negative and are written in decimal notation. 
 
    SYMBOL: A user-defined symbol can be any sequence of letters, digits, underscore (_), dot (.), 
    dollar sign ($), and colon (:) that does not begin with a digit.

    LABEL: (SYMBOL)
    """

    # Data structure to hold the parsed fields for the command
    s = {}
    s['instruction_type'] = ''
    s['value'] = ''
    s['value_type'] = ''
    s['dest'] = ''
    s['comp'] = ''
    s['jmp'] = ''
    s['status'] = 0


    # Valid operands and operations for C-type instructions
    valid_operands = '01DMA'
    valid_operations = '+-&|'
    # Valid symbols
    valid_symbols = '_.$:'


    state = 0
    # FIXME: Implement your finite automata to extract tokens from command
    for char in command:
        match state:
            case -1: # Error state
                s['status'] = -1
                
            case 0: # Initial States
                if char == ' ': # Ignore blank spaces
                    pass 
                elif char == '\n': # Ignore blank lines
                    pass 
                elif char == '/': # Maybe a comment
                    state = 1
                elif char == '@':
                    s['instruction_type'] = 'A_INSTRUCTION'
                    state = 3
                elif char in valid_operands:
                    s['dest'] = char
                    s['comp'] = char
                    state = 7
                elif char in '-!':
                    s['instruction_type'] = 'J_INSTRUCTION'
                    s['dest'] = 'null'
                    s['comp'] = char
                    state = 13
                elif char == '(':
                    s['instruction_type'] = 'PSEUDO_INSTRUCTION'
                    s['value_type'] = 'SYMBOL'
                    state = 16
                else:
                    s['status'] = -1
                    state = -1 # Not a comment

            case 1: #Check if comment
                if char == '/':
                    state = 2
                else:
                    s['status'] = -1
                    state = -1

            case 2: #Ignore comment
                pass
            
            case 3: # Check type of A-Instructions
                if char == ' ':
                    pass
                elif char.isalpha():
                    s['value'] = char
                    s['value_type'] = "SYMBOL"
                    state = 4
                elif char.isnumeric():
                    s['value'] = char
                    s['value_type'] = "NUMERIC"
                    state = 5
                else:
                    s['status'] = -1
                    state = -1

            case 4: # Symbol A-Instruction
                if char.isalnuma() or char in valid_symbols:
                    s['value'] += char
                    state = 4
                elif char == ' ':
                    state = 6
                elif char == '\n':
                    pass
                elif char == '/':
                    state = 1
                else:
                    s['status'] = -1
                    state = -1

            case 5: # Numeric A-Instruction
                if char.isnumeric():
                    s['value'] += char
                    state = 5
                elif char == ' ':
                    state = 6
                elif char == '\n':
                    pass
                elif char == '/':
                    state = 1
                else:
                    s['status'] = -1
                    state = -1

            case 6: # End of instruction checker
                if char == ' ':
                    pass
                elif char == '\n':
                    pass
                elif char == '/':
                    state = 1
                else:
                    s['status'] = -1
                    state = -1

            case 7: # Check C or J Instruction
                if char == ' ':
                    pass
                elif char in 'AMD':
                    s['dest'] += char
                    state = 7
                elif char == '=':
                    s['instruction_type'] = 'C_INSTRUCTION'
                    s['jmp'] = 'null'
                    state = 8
                elif char in valid_operations:
                    s['instruction_type'] = 'J_INSTRUCTION'
                    s['comp'] += char 
                    s['dest'] = 'null'
                    state = 13
                elif char == ';':
                    s['instruction_type'] = 'J_INSTRUCTION'
                    s['dest'] = 'null'
                    state = 15
                else:
                    s['status'] = -1
                    state = -1

            case 8: # C-Instructions State
                if char == ' ':
                    pass
                elif char in '01':
                    s['comp'] = char
                    state = 6
                elif char in 'AMD':
                    s['comp'] = char
                    state = 10
                elif char in '-!':
                    s['comp'] = char
                    state = 11
                else:
                    s['status'] = -1
                    state = -1

            case 10: # C-Instructions State (AMD or operand)
                if char == ' ':
                    pass
                elif char == '\n':
                    pass
                elif char == '/':
                    state = 1
                elif char in valid_operations:
                    s['comp'] += char
                    state = 12
                else:
                    s['status'] = -1
                    state = -1

            case 11: # C-Instructions State (- or ! then AMD or 1)
                if char == ' ':
                    pass
                elif char in 'AMD1':
                    s['comp'] += char
                    state = 6
                else:
                    s['status'] = -1
                    state = -1

            case 12: # C-Instructions State (operand)
                if char == ' ':
                    pass
                elif char in valid_operands:
                    s['comp'] += char
                    state = 6
                else:
                    s['status'] = -1
                    state = -1

            case 13:  # J-Instructions
                if char == ' ':
                    pass
                elif char in 'AMD1':
                    s['comp'] += char
                    state = 14
                else:
                    s['status'] = -1
                    state = -1

            case 14:  # Looking for ';' J-Instructions
                if char == ' ':
                    pass
                elif char == ';':
                    state = 15
                else:
                    s['status'] = -1
                    state = -1

            case 15:  # Looking JMP for J-Instructions
                if char == ' ':
                    pass
                elif char == '\n':
                    state = 0
                elif char == '/':
                    state = 1
                elif char.isalpha():
                    s['jmp'] += char
                else:
                    s['status'] = -1
                    state = -1

            case 16:  # Pseudo-instruction state
                if char.isalnum() or char in valid_symbols:
                    s['value'] += char
                    state = 16
                elif char == ')':
                    state = 6
                else:
                    s['status'] = -1
                    state = -1
            case _: # Default Error Case
                s['status'] = -1
                state = -1

    # FIXME: check if the tokens were formed correctly
    if valid_tokens(s):
        return s
    
    return 0  


# TODO
def generate_machine_code():
    """Generate machine code from intermediate data structure"""
    
    machine_code = []
    
    return machine_code
   

def print_machine_code(machine_code):
    """Print generated machine code"""
    
    rom_address = 0
    for code in machine_code:
        print(rom_address, ':', code)
        rom_address = rom_address + 1


# TODO
def run_assembler(file_name):      
    """Pass 1: Parse the assembly commands into an intermediate data structure.
    This can be a list of elements, called ir, where each element is a dictionary with the following 
    structure: 

    s['instruction_type'] = ''
    s['value'] = ''
    s['value_type'] = ''
    s['dest'] = ''
    s['comp'] = ''
    s['jmp'] = ''
    s['status'] = 0

    The symbol table is also generated in this step.    
    """

    # FIXME: Implement Pass 1 of the assembler to generate the intermediate data structures
    with open(file_name, 'r') as f:
        for command in f:  
            pass


    # FIXME: Implement Pass 2 of assembler to generate the machine code from the intermediate data structures
    machine_code = []

    return machine_code


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: Python assembler.py file-name.asm")
        print("Example: Python assembler.py series_sum.asm")
    else:
        print("Assembling file:", sys.argv[1])
        print()
        file_name_minus_extension, _ = os.path.splitext(sys.argv[1])
        output_file = file_name_minus_extension + '.hack'
        machine_code = run_assembler(sys.argv[1])
        if machine_code:
            print('Machine code was generated successfully');
            print('Writing machine code output to file:', output_file)
            f = open(output_file, 'w')
            for s in machine_code:
                f.write('%s\n' %s)
            f.close()
        else:
            print('Error generating machine code')