// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(OUT)
@KBD
D = M
@BLACKEN
D; JGT
@WHITEN
D; JEQ


(BLACKEN)
	
	@8192
	D = A
	@n
	M = D
	
	@SCREEN
	D = A
	@addr1
	M = D
	@i
	M = 0

	(LOOP1)
	@i
	D = M
	@n
	D = D-M
	@OUT
	D; JGE

	@addr1
	A = M 
	M = -1 //set all 111...

	@addr1
	M = M+1

	@i
	M = M+1

	@LOOP1
	0; JMP

(WHITEN)
	
	@8192
	D = A
	@n
	M = D
	
	@SCREEN
	D = A
	@addr2
	M = D
	@j
	M = 0

	(LOOP2)
	@j
	D = M
	@n
	D = D-M
	@OUT
	D; JGE

	@addr2
	A = M 
	M = 0 //set all 111...

	@addr2
	M = M+1

	@j
	M = M+1

	@LOOP2
	0; JMP