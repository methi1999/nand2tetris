orig = 'pong/Pong.hack'
target = orig.split('.')[0] + '_mine.hack'

with open(orig,'r') as f:
	original = f.read()
with open(target,'r') as f:
	final = f.read()

# print(len(original),len(final))

for i in range(len(original)):
	if original[i] != final[i]:
		print(i)