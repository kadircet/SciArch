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
REG1-24	General Purpose Registers
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
ADD		r += r/m/imm
SUB		r += r/m/imm
MUL		r *= r/m/imm
DIV		r /= r/m/imm	REM = r % (r/m/imm)
TEST	r & r/m/imm	(Sets SF to MSB of the result) (Sets ZF to 1 if both operands are 0, otherwise 0)
CMP		r, r/m/imm	Subtracts(signed) operand2 from operand1 and Sets SF to MSB of the result, ZF to 1 if result is 0, otherwise 0
JMP		IP += r/m/imm
JMPL	IP = r/m/imm
JE		IP += r/m/imm iff ZF==1
JNE		IP += r/m/imm iff ZF==0
JL		IP += r/m/imm iff SF==1
JLE		IP += r/m/imm iff (SF==1 | ZF==0)
JG		IP += r/m/imm iff SF==0
JGE		IP += r/m/imm iff (SF==0 | ZF==0)
JZ		IP += r/m/imm iff ZF==1
JNZ		IP += r/m/imm iff ZF==0
JS		IP += r/m/imm iff SF==1
JNS		IP += r/m/imm iff SF==0
MOV		r/imm, m	r/imm/m, r	(MOV SRC, DEST)
"""

"""
Each opcode is 6bits(2 bytes with operands)
0x0000	HLT
0x0001	NOP
0x0002	AND	(r1(5bits) | r2(5bits))
0x0002	AND (r1(5bits) | 11110(5bits) | immediate value (ARCHBITS bits))
0x0002	AND	(r1(5bits) | 11111(5bits) | memory address (ARCHBITS bits))
0x0002	AND (11111(5bits) | 11111(5bits) | memory address (ARCHBITS bits) | immediate value (ARCHBITS bits))
0x0003	OR	(r1(5bits) | r2(5bits))
0x0003	OR	(r1(5bits) | 11110(5bits) | immediate value (ARCHBITS bits))
0x0003	OR	(r1(5bits) | 11111(5bits) | memory address (ARCHBITS bits))
0x0004	XOR	(r1(5bits) | r2(5bits))
0x0004	XOR	(r1(5bits) | 11110(5bits) | immediate value (ARCHBITS bits))
0x0004	XOR	(r1(5bits) | 11111(5bits) | memory address (ARCHBITS bits))
0x0005	NOT	(r1(5bits))
0x0006	XCHG(r1(5bits) | r2(5bits))
0x0006	XCHG(r1(5bits) | 11111(5bits) | memory address (ARCHBITS bits))
0x0007	SHL	(r1(5bits) | r2(5bits))
0x0007	SHL	(r1(5bits) | 11110(5bits) | immediate value(ARCHBITS bits))
0x0008	SHR	(r1(5bits) | r2(5bits))
0x0008	SHR	(r1(5bits) | 11110(5bits) | immediate value(ARCHBITS bits))
0x0009	ROL	(r1(5bits) | r2(5bits))
0x0009	ROL	(r1(5bits) | 11110(5bits) | immediate value(ARCHBITS bits))
0x000A	ROR	(r1(5bits) | r2(5bits))
0x000A	ROR	(r1(5bits) | 11110(5bits) | immediate value(ARCHBITS bits))
0x000B	NEG	(r1(5bits))
0x000C	ADD	(r1(5bits) | r2(5bits))
0x000C	ADD	(r1(5bits) | 11111(5bits) | memory address (ARCHBITS bits))
0x000C	ADD	(r1(5bits) | 11110(5bits) | immediate value (ARCHBITS bits))
0x000D	SUB	(r1(5bits) | r2(5bits))
0x000D	SUB	(r1(5bits) | 11111(5bits) | memory address (ARCHBITS bits))
0x000D	SUB	(r1(5bits) | 11110(5bits) | immediate value (ARCHBITS bits))
0x000E	MUL	(r1(5bits) | r2(5bits))
0x000E	MUL	(r1(5bits) | 11111(5bits) | memory address (ARCHBITS bits))
0x000E	MUL	(r1(5bits) | 11110(5bits) | immediate value (ARCHBITS bits))
0x000F	DIV	(r1(5bits) | r2(5bits))
0x000F	DIV	(r1(5bits) | 11111(5bits) | memory address (ARCHBITS bits))
0x000F	DIV	(r1(5bits) | 11110(5bits) | immediate value (ARCHBITS bits))
0x0010	TEST(r1(5bits) | r2(5bits))
0x0010	TEST(r1(5bits) | 11111(5bits) | memory address (ARCHBITS bits))
0x0010	TEST(r1(5bits) | 11110(5bits) | immediate value (ARCHBITS bits))
0x0011	CMP	(r1(5bits) | r2(5bits))
0x0011	CMP	(r1(5bits) | 11111(5bits) | memory address (ARCHBITS bits))
0x0011	CMP	(r1(5bits) | 11110(5bits) | immediate value (ARCHBITS bits))
0x0012	JMP	(r1(5bits))
0x0012	JMP	(11111(5bits) | memory address (ARCHBITS bits))
0x0012	JMP	(11110(5bits) | immediate value (ARCHBITS bits))
0x0013	JMPL(r1(5bits))
0x0013	JMPL(11111(5bits) | memory address (ARCHBITS bits))
0x0013	JMPL(11110(5bits) | immediate value (ARCHBITS bits))
0x0014	JE	(r1(5bits))
0x0014	JE	(11111(5bits) | memory address (ARCHBITS bits))
0x0014	JE	(11110(5bits) | immediate value (ARCHBITS bits))
0x0015	JNE	(r1(5bits))
0x0015	JNE	(11111(5bits) | memory address (ARCHBITS bits))
0x0015	JNE	(11110(5bits) | immediate value (ARCHBITS bits))JL		IP = r/m/imm iff SF==1
0x0016	JL	(r1(5bits))
0x0016	JL	(11111(5bits) | memory address (ARCHBITS bits))
0x0016	JL	(11110(5bits) | immediate value (ARCHBITS bits))JG		IP = r/m/imm iff SF==0
0x0017	JG	(r1(5bits))
0x0017	JG	(11111(5bits) | memory address (ARCHBITS bits))
0x0017	JG	(11110(5bits) | immediate value (ARCHBITS bits))JG		IP = r/m/imm iff SF==0
0x0018	JLE	(r1(5bits))
0x0018	JLE	(11111(5bits) | memory address (ARCHBITS bits))
0x0018	JLE	(11110(5bits) | immediate value (ARCHBITS bits))JG		IP = r/m/imm iff SF==0
0x0019	JGE	(r1(5bits))
0x0019	JGE	(11111(5bits) | memory address (ARCHBITS bits))
0x0019	JGE	(11110(5bits) | immediate value (ARCHBITS bits))JZ		IP = r/m/imm iff ZF==1
0x001A	JZ	(r1(5bits))
0x001A	JZ	(11111(5bits) | memory address (ARCHBITS bits))
0x001A	JZ	(11110(5bits) | immediate value (ARCHBITS bits))JS		IP = r/m/imm iff SF==1
0x001B	JNZ	(r1(5bits))
0x001B	JNZ	(11111(5bits) | memory address (ARCHBITS bits))
0x001B	JNZ	(11110(5bits) | immediate value (ARCHBITS bits))JS		IP = r/m/imm iff SF==1
0x001C	JS	(r1(5bits))
0x001C	JS	(11111(5bits) | memory address (ARCHBITS bits))
0x001C	JS	(11110(5bits) | immediate value (ARCHBITS bits))JS		IP = r/m/imm iff SF==1
0x001D	JNS	(r1(5bits))
0x001D	JNS	(11111(5bits) | memory address (ARCHBITS bits))
0x001D	JNS	(11110(5bits) | immediate value (ARCHBITS bits))MOV		r/imm, m	r/imm/m, r	(MOV SRC, DEST)
0x001E	MOV	(r1(5bits) | r2(5bits))
0x001E	MOV	(r1(5bits) | 11111(5bits) | memory address (ARCHBITS bits))
0x001E	MOV	(11110(5bits) | r1(5bits) | immediate value (ARCHBITS bits))
0x001E	MOV	(11110(5bits) | 11111(5bits) | immediate value (ARCHBITS bits) | memory address (ARCHBITS bits))
0x001E	MOV (11111(5bits) | r1(5bits) | memory address (ARCHBITS bits))
"""

import sys

memory = {}
IP = 0
REM= 0
SP = 0
BP = 0
SI = 0
DI = 0
CS = 0
DS = 0
SS = 0
Flags=0
reg = []
for i in range(24):
	reg.append(0)
	
instruction = 0
instructions =
{
	0x00: HALT,
	0x01: NOP,
	0x02: AND,
	0x03: OR,
	0x04: XOR,
	0x05: NOT,
	0x06: XCHG,
	0x07: SHL,
	0x08: SHR,
	0x09: ROL,
	0x0A: ROR,
	0x0B: NEG,
	0x0C: ADD,
	0x0D: SUB,
	0x0E: MUL,
	0x0F: DIV,
	0x10: TEST,
	0x11: CMP,
	0x12: JMP
	0x13: JMPL
	0x14: JE,
	0x15: JNE,
	0x16: JL,
	0x17: JG,
	0x18: JLE,
	0x19: JGE,
	0x1A: JZ,
	0x1B: JNZ,
	0x1C: JS,
	0x1D: JNS,
	0x1E: MOV
}

commandSize = 2
def HALT():
	dumpMemory()
	sys.exit()

def NOP():
	#
	return

def AND():
	r1 = (instruction>>5) & 0x1F
	r2 = instruction & 0x1F
	
	if(r2>=0x1E)
		commandSize += ARCHBITS/8
		if(r2==0x1E)
			r2 = getBytes(IP+2, 4)
		else
			r2 = getBytes(getBytes(IP+2, 4), 4)
	else
		r2 = reg[r2]
		
	reg[r1] &= r2
	return

def OR():
	r1 = (instruction>>5) & 0x1F
	r2 = instruction & 0x1F
	
	if(r2>=0x1E)
		commandSize += ARCHBITS/8
		if(r2==0x1E)
			r2 = getBytes(IP+2, 4)
		else
			r2 = getBytes(getBytes(IP+2, 4), 4)
	else
		r2 = reg[r2]
		
	reg[r1] |= r2
	return

def XOR():
	r1 = (instruction>>5) & 0x1F
	r2 = instruction & 0x1F
	
	if(r2>=0x1E)
		commandSize += ARCHBITS/8
		if(r2==0x1E)
			r2 = getBytes(IP+2, 4)
		else
			r2 = getBytes(getBytes(IP+2, 4), 4)
	else
		r2 = reg[r2]
		
	reg[r1] ^= r2
	return

def NOT():
	r1 = (instruction>>5) & 0x1F
	
	reg[r1] = ~reg[r1]
	return

def XCHG():
	r1 = (instruction>>5) & 0x1F
	r2 = instruction & 0x1F
	tmp = reg[r1]
	
	if(r2==0x1F)
		commandSize += ARCHBITS/8
		r2 = getBytes(IP+2, 4)
		reg[r1] = getBytes(r2, 4)
		memory[r2] = tmp
	else
		reg[r1] = reg[r2]
		reg[r2] = tmp
		
	return

def SHL():
	r1 = (instruction>>5) & 0x1F
	r2 = instruction & 0x1F
	
	if(r2==0x1E)
		commandSize += ARCHBITS/8
		r2 = getBytes(IP+2, 4)
	else
		r2 = reg[r2]
		
	reg[r1] <<= r2
	return

def SHR():
	r1 = (instruction>>5) & 0x1F
	r2 = instruction & 0x1F
	
	if(r2==0x1E)
		commandSize += ARCHBITS/8
		r2 = getBytes(IP+2, 4)
	else
		r2 = reg[r2]
		
	reg[r1] >>= r2
	return

def ROL():
	r1 = (instruction>>5) & 0x1F
	r2 = instruction & 0x1F
	
	if(r2==0x1E)
		commandSize += ARCHBITS/8
		r2 = getBytes(IP+2, 4)
	else
		r2 = reg[r2]
	
	MSB = reg[r1] & (1<<(ARCHBITS-1))
	reg[r1] <<= r2
	reg[r1] += MSB>0?1:0
	return

def ROR():
	r1 = (instruction>>5) & 0x1F
	r2 = instruction & 0x1F
	
	if(r2==0x1E)
		commandSize += ARCHBITS/8
		r2 = getBytes(IP+2, 4)
	else
		r2 = reg[r2]
	
	LSB = reg[r1] & 0x01
	reg[r1] >>= r2
	reg[r1] |= LSB<<(ARCHBITS-1)
	return

def NEG():
	r1 = (instruction>>5) & 0x1F
	
	reg[r1] = ((~reg[r1])+1) & 0xFFFFFFFF
	return
	
