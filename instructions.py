#!/usr/bin/python
"""
This code emulates a 32bit architecture it can be changed
by changing the following constant
"""
ARCHBITS=32

"""
Registers:
IP		Instruction Pointer, points to current instructions memory address
REM		Remainder Register, holds the remainder after a division operation
SP		Stack Pointer
BP		Base Pointer
SI		Source Index
DI		Destination Index
CS		Code Segment Register
DS		Data Segment Register
SS		Stack Segment Register
REG1-32	General Purpose Registers
Flags	Flags Register
"""

"""
Flags:
CF		Carry Flag
ZF		Zero Flag
SF		Sign Flag
DF		Direction Flag
OF		Overflow Flag
"""

"""
Instruction List:
HLT		Halts the cpu
NOP		Does no operation for a fetch-decode-execute cycle
AND		r/m &= r/imm - Logical ands a value stored in a register(r) or(/) memory(m) with a register(r) or immediate value(imm)
OR		r/m |= r/imm
XOR		r/m ^= r/imm
NOT		r/m ^= -1
XCHG	r :=:(swap) r/m
SHL		r<<=r/imm shift		(MSB Ignored)
SHR		r>>=r/imm shift		(LSB Ignored)
ROL		r<<=r/imm rotation	(MSB moved to LSB)
ROR		r>>=r/imm rotation	(LSB moved to MSB)
NEG		r/m *= -1	(2's complement)
ADD		r/m += r/imm	r += m/imm
SUB		r/m += r/imm	r += m/imm
MUL		r *= m/imm
DIV		r /= m/imm	REM = r % (m/imm)
TEST	r/m & r/imm 	r & m/imm	(Sets SF to MSB of the result) (Sets ZF to 1 if both operands are 0, otherwise 0)
CMP		r/m, r/imm		r, m/imm	Subtracts(signed) operand2 from operand1 and Sets SF to MSB of the result, ZF to 1 if result is 0, otherwise 0
JMP		IP += r/m/imm
JMPL	IP = r/m/imm
JE		IP = r/m/imm iff ZF==1
JNE		IP = r/m/imm iff ZF==0
JL		IP = r/m/imm iff SF==1
JLE		IP = r/m/imm iff (SF==1 | ZF==0)
JG		IP = r/m/imm iff SF==0
JGE		IP = r/m/imm iff (SF==0 | ZF==0)
JZ		IP = r/m/imm iff ZF==1
JNZ		IP = r/m/imm iff ZF==0
JS		IP = r/m/imm iff SF==1
JNS		IP = r/m/imm iff SF==0
MOV		r/imm, m	r/imm/m, r	(MOV SRC, DEST)
"""

