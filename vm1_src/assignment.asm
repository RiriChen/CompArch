@256
D=A
@SP
M=D
@300
D=A
@LCL
M=D
@5
D = A
@SP
A = M
M = D
@SP
M = M + 1
@LCL
D = M
@0
D = D + A
@R13
M = D
@SP
M = M - 1
A = M
D = M
@R13
A = M
M = D
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
@LCL
D = M
@1
D = D + A
@R13
M = D
@SP
M = M - 1
A = M
D = M
@R13
A = M
M = D
@10
D = A
@SP
A = M
M = D
@SP
M = M + 1
@LCL
D = M
@2
D = D + A
@R13
M = D
@SP
M = M - 1
A = M
D = M
@R13
A = M
M = D
@ALL_DONE
(ALL_DONE)
0;JMP
