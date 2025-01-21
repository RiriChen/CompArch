// 
//  Signed Multiplication HACK Assembly
// 
// Student name(s): Ricky Chen, Phong Nguyen
// Date modified: October 19, 2024 
//

@18
M = 0
@17
D = M
@PLOOP
D; JGT
@NLOOP
D; JLT
@EXIT
D; JEQ

(PLOOP)
@17
D = M
@EXIT
D; JEQ
@16
D = M
@18
M = M + D
@17
M = M - 1 
@PLOOP
0; JMP

(NLOOP)
@17
D = M
@EXIT
D; JEQ
@16
D = M
@18
M = M - D
@17
M = M + 1 
@NLOOP
0; JMP

(EXIT)
@EXIT
0; JMP