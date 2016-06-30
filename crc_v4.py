from random import randrange
from binascii import hexlify

source = ''
polynomial = ''
crc_from_file = ''
brokenCRC = ''

def makeCRC(incode, inpolynomial):
	code = incode.replace('<', '').replace('>', '')
	# complete with zeros
	extended_source = code
	for i in range(0, len(inpolynomial)-1):
		extended_source += '0'

	# initiate first divident. its first nine symbols of source
	currentDividend = extended_source[0:len(inpolynomial)]
	try:
		for i in range(0, len(incode)):
			if (currentDividend[0] == '1') and (len(currentDividend)==len(inpolynomial)):
				currentDividend = str(bin(int(currentDividend, base=2) ^ int(inpolynomial, base=2)))[2:]
			currentDividend += extended_source[len(inpolynomial)+i]
			currentDividend = currentDividend[-len(inpolynomial):]
	except IndexError as e:
		itsjust = 'stop of the loop'
	return currentDividend

def breakSource(insource):
	rnd_pos = randrange(len(insource)-1)
	tmp = list(insource)
	if tmp[rnd_pos] == '1':
		tmp[rnd_pos] = '>0<'
	else:
		tmp[rnd_pos] = '>1<'
	tmp = ''.join(tmp)
	return tmp

def file_from_scheme(infile):
	tmplst = list(hexlify(open(infile).read(3 + (len(polynomial)-1)/8)[3:]))
	lst = []

	lst.append(tmplst[0])
	for x in xrange(1, len(tmplst)):
		lst[0] = lst[0] + tmplst[x]
	for x in range(0, len(lst)):
		lst[x] = str(bin(int(lst[x], base=16)))[2:]
	return lst

def random_file(infile):
	tmplst = list(hexlify(open(infile).read()))
	tmpsource = ''
	for x in tmplst:
		tmpsource = tmpsource + str(bin(int(x, base=16)))[2:]
	return tmpsource


try:
	polynomial = str(bin(int(raw_input('''Enter your polynomial: '''), base=2)))[2:]
except ValueError as e:
	print('''binary code, you're idiot''')
	exit()

print('''Enter data to code (0 and 1) or filename''')
inpt = raw_input('''(NOTE: if you want to check file from scheme type name of file with prefix 'sc_'): ''')
try:
	source = str(bin(int(inpt, base=2)))[2:]
except ValueError as e:
	try:
		print('Searching for file')
		if inpt.startswith('sc_'):
			### ---- FROM SCHEME
			source = raw_input('Enter your word to code: ')
			tmplst = file_from_scheme(inpt[3:])
			crc_from_file = tmplst[0]
			### ---- FROM SCHEME
		else:
			### ---- random file
			source = random_file(inpt)
			### ---- random file
	except IOError as ee:
		print('There is no such file or your string is not good')
		exit()

CRC_made_here = makeCRC(source, polynomial)
brokenSource = breakSource(source)
brokenCRC = makeCRC(brokenSource, polynomial)

print
print('''Word to code> ''' + source)
print('''It's CRC> ''' + CRC_made_here)

if crc_from_file != '':
	print('''CRC in file> ''' + crc_from_file)

	if (CRC_made_here == crc_from_file):
		print('''They are equal. Hooray C:''')
	else:
		print('''They are NOT equal. Not hooray :C''')

print('''Broken word> ''' + brokenSource)
print('''CRC of broken word> ''' + brokenCRC)

if (brokenSource.replace('<', '').replace('<', '') == brokenCRC):
	print('''They are equal''')
else:
	print('''They are not equal''')

raw_input('Exiting...')