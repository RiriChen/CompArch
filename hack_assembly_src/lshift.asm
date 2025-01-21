// 
//  Arithmetic Left Shift HACK Assembly
// 
// Student name(s): Ricky Chen, Phong Nguyen
// Date modified: October 19, 2024 
//

@16
D = M
@18
M = D

(LOOP_ENTRY)
@17
D = M
@EXIT
D; JEQ
@18
D = M
M = M + D
@17
M = M - 1
@LOOP_ENTRY
0; JMP

(EXIT)
@EXIT
0; JMP