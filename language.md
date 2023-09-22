# Scripting language reference

Fast language for small devices with a modern Python-like syntax.
- No dynamic memory allocation
- No pointers
- No recursion
- No use of stack for passing parameters

## Problems
1.	Using functions when objects are in arrays e.g. Sprites[1].load(a_y) requires passing additional variable load( 1, a_y)
2.	Passing by reference without self-modifying code when you have multiple calls to a function

# references to other objects ---test it in practice with some codes
Access to objects just by name?

# Types
{byte, word, dword}

# Declarations of variables
Declarations are mandatory
byte a
word b,c,d

# Constants
{Binary, dec or hex}
0b01000100, 255, 0x30
- const some_constant = 0x2000

# Arrays
single dimensional
initializations

# Strings
is single-dimensional initialized array?

# Data placement
Placement of data at specific addresses is possible
- byte x at 0x2000
- byte x[100] at 0x3000

# if, else
# expressions
# arithmetic operator (+-*/%)
# comparison operators (==, !=, <, >, <=, >=)
# assignment operator =, +=, -=, *=, /=, %=
# bitwise operators (&,~,!)
# logical operators (and, or, xor)
# for loops
only for arrays of objects? For element in array.	
#procedures with params and return values

def load():
	statement
	return x
procedures can have single return value so can be used directly as expressions
parameters are always passed as reference, even for simple types? Reason � to avoid using global variables.

#comments
Python style #
#Code examples

// file test.u8b

byte x
def check(byte a_x, byte a_y):
	byte x = a_x
Missles[0].x += 1
Players[x+1].id = a_x
Sprites[x].load(a_y)
for player in Players:
	if player.x > x:
		break

Translation to C code:
byte test__x;
byte test__check_x;
byte test__check_a_x
void test__check()
{
	++missile__x[0];
	player__id[test__check_x+1] = test__check_a_x
	sprite__load(x,a_y)
}

def evasion():
	byte a,b,c,d
	check(a,b)
	check(c,d)
