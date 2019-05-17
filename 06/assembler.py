compazerokey = ['0','1','-1','D','A','!D','!A','-D','-A','D+1','A+1','D-1','A-1','D+A','D-A','A-D','D&A','D|A']
compaonekey = ['0','0','0','0','M','0','!M','0','-M','0','M+1','0','M-1','D+M','D-M','M-D','D&M','D|M']
compvalues = ['101010','111111','111010','001100','110000','001101','110001','001111','110011','011111','110111','001110','110010','000010','010011','000111','000000','010101']
compTable = {}
for i in range(18):
	compTable[compazerokey[i]] = '0'+compvalues[i]
	if compaonekey[i] != '0':
		compTable[compaonekey[i]] = '1'+compvalues[i]

destkeys = ['null','M','D','MD','A','AM','AD','AMD']
destvalues = ['000','001','010','011','100','101','110','111']
destTable = dict(zip(destkeys,destvalues))

jumpkeys = ['null','JGT','JEQ','JGE','JLT','JNE','JLE','JMP']
jumpvalues = ['000','001','010','011','100','101','110','111']
jumpTable = dict(zip(jumpkeys,jumpvalues))

class symbolTable():

	def __init__(self):
		self.symbolTable = {}
		self.counter = 16
		for i in range(16):
			self.symbolTable['R'+str(i)] = str(i)
		self.symbolTable['SCREEN'] = '16384'
		self.symbolTable['KBD'] = '24576'
		predefined = ['SP','LCL','ARG','THIS','THAT']
		for i in range(5):
			self.symbolTable[predefined[i]] = str(i)

	def addLabel(self, string, nextLineNum):
		self.symbolTable[string] = str(nextLineNum)

	def addVar(self, string):

		to_search = string[1:]
		if to_search in self.symbolTable:
			return self.symbolTable[to_search]
		else:
			self.symbolTable[to_search] = str(self.counter)
			self.counter += 1
			return self.symbolTable[to_search]


def aInstruction(instruct, padded=True):
	number = int(instruct[1:])
	if number == 0:
		return '0'*16
	mask = 1
	string = ""
	while number > 0:
		# print(number)
		if mask&number:
			string += '1'
		else:
			string += '0'
		number = number >> 1
	if padded:
		return '0'*(16-len(string)) + string[::-1]
	else:
		return string[::-1]

def CInstruction(instruct):

	final = '111'
	if '=' in instruct:
		dest,comp = instruct.split('=')[0].strip(), instruct.split('=')[1].split(';')[0].strip()
	else:
		dest,comp = 'null', instruct.split(';')[0].strip()
	if ';' in instruct:
		jump = instruct.split(';')[-1].strip()
	else:
		jump = 'null'

	final += (compTable[comp] + destTable[dest] + jumpTable[jump])
	print('Final C instruction:', final)
	return final

def readAndStrip(input_path):

	with open(input_path, 'r') as f:
		data = f.readlines()
	# print(data,len(data))
	to_return = []
	for line in data:
		if line[:2] == '//' or line[:2] == '\n':
			continue
		else:
			to_return.append(line.split('//')[0].strip())
	return to_return

# print(readAndStrip('add/Add.asm'))
def firstpass(data, table):

	lineNum = 0
	for i in range(len(data)):
		if data[i][0] == '(':
			label = data[i][1:-1]
			print("Found LABEL:",label,'       and line number is',str(lineNum))
			table.addLabel(label,lineNum)
		else:
			lineNum += 1


def driver(path='add/Add1.asm'):

	data = readAndStrip(path)
	print('Cleaned data:',data)
	final_data = []
	s = symbolTable()

	#firstpass
	firstpass(data, s)

	for line in data:
		#Label
		print("Current line:",line)
		# if line[0] == '(':
		# 	print("In label")
		# 	nextLineNum = s.symbolTable[line[1:-1]]
		# 	instruction = aInstruction('@'+nextLineNum)
		# 	print("Adding",instruction)
		# 	final_data.append(instruction)
		#Variable or A
		if line[0] == '(':
			continue
		if line[0] == '@':
			if line[1] in [str(x) for x in list(range(10))]:
				#A instruction
				print('A instruction with value',line[1:])
				final_data.append(aInstruction(line))
			else: #variable
				res = s.addVar(line)
				print("Found variable with address:",res)
				final_data.append(aInstruction('@'+res))
		#C
		else:
			print("C instruction:",line)
			final_data.append(CInstruction(line))

	return '\n'.join(final_data)+'\n'


output = driver('rect/Rect.asm')
with open('rect/Rect_mine.hack', 'w') as f:
	f.write(output)




