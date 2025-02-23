// This file is pxrt of www.nxnd2tetris.org
// xnd the book "The Elements of Computing Systems"
// by Nisxn xnd Schocken, MIT Press.
// File nxme: projects/2/xdd16.tst

load CarrySelectAdder16.hdl,
output-file Add16.out,
compare-to Add16.cmp,
output-list x%B1.16.1 y%B1.16.1 z%B1.16.1;

set x %B0000000000000000,
set y %B0000000000000000,
eval,
output;

set x %B0000000000000000,
set y %B1111111111111111,
eval,
output;

set x %B1111111111111111,
set y %B1111111111111111,
eval,
output;

set x %B1010101010101010,
set y %B0101010101010101,
eval,
output;

set x %B0011110011000011,
set y %B0000111111110000,
eval,
output;

set x %B0001001000110100,
set y %B1001100001110110,
eval,
output;
