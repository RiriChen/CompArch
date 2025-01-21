@256
D=A
@SP
M=D
@300
D=A
@LCL
M=D
@50
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
@150
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
@LCL
D = M
@0
A = D + A
D = M
@SP
A = M
M = D
@SP
M = M + 1
@LCL
D = M
@1
A = D + A
D = M
@SP
A = M
M = D
@SP
M = M + 1
@SP
M = M - 1
A = M
D = M
@SP
M = M - 1
A = M
D = M + D
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
@LCL
D = M
@2
A = D + A
D = M
@SP
A = M
M = D
@SP
M = M + 1
@LCL
D = M
@1
A = D + A
D = M
@SP
A = M
M = D
@SP
M = M + 1
@SP
M = M - 1
A = M
D = M
@SP
M = M - 1
A = M
D = M - D
@SP
A = M
M = D
@SP
M = M + 1
@LCL
D = M
@3
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
