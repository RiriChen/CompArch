// 
//  Unsigned Division HACK Assembly
// 
// Student name(s): Ricky Chen, Phong Nguyen
// Date modified: October 19, 2024 
//

@18
M = 0
@16
D = M
@19
M = D

(WHILE)
@19
D = M
@17
D = D - M
@EXIT
D; JLT

@18
M = M + 1
@17
D = M
@19
M = M - D
@WHILE
0; JMP

(EXIT)
@EXIT
0; JMP