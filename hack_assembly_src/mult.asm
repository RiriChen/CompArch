// 
//  Unsigned Multiplication HACK Assembly
// 
// Student name(s): Ricky Chen, Phong Nguyen
// Date modified: October 19, 2024 
//

@18
M = 0

(LOOP_ENTRY)
@17
D = M
@LOOP_EXIT
D; JEQ

@16
D = M
@18
M = M + D
@17
M = M - 1 
@LOOP_ENTRY
0; JMP

(LOOP_EXIT)
@LOOP_EXIT
0; JMP