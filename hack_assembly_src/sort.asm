// 
//  Bubble Sort HACK Assembly
// 
// Student name(s): Ricky Chen, Phong Nguyen
// Date modified: October 19, 2024 
//

@19 // continue
M = 1

(WHILE)
@19
D = M
@EXIT
D; JEQ
@19
M = 0

@18 // i
M = 0 
(FOR)
@18
D = M
@17
D = D - M
D = D + 1
@WHILE
D; JGE // Jumps to WHILE if (i - n + 1) >= 0

@16
D = M
@18
D = D + M
@20
M = D // stores temp pointer
@20
A = M
D = M // D = arr[i]
@20
A = M + 1 // M = arr[i + 1]
D = D - M // D = arr[i] - arr[i + 1]

@INC
D; JLE // Jumps to increment i if arr[i] <= arr[i +1]
@20 // starts swapping arr[i] arr[i + 1]
A = M
D = M // D = arr[i]
@21
M = D // temp_val = arr[i]
@20
A = M + 1
D = M // D = arr[i + 1]
@20
A = M
M = D // arr[i] = arr[i + 1]
@21
D = M // D = arr[i]
@20
A = M + 1
M = D // arr[i + 1] = arr[i]
@19
M = 1

(INC)
@18
M = M + 1 // i++
@FOR
0;JMP

(EXIT)
@EXIT
0; JMP