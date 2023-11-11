import numpy as np
import numpy.random as random


def getbit(num, index):
	if (num & (1 << index)) == 0:
		return 0
	else:
		return 1

def getMsgs(l):
	msgs = []
	for num in range(2**l):
		msgs.append(getMsg(l, num))
	return np.array(msgs)

def getMsg(l, num):
	msg = []
	for x in range(l):
		msg.insert(0,getbit(num, x))
	return np.array(msg)

def getWeight(word):
	d = 0
	for i in range(len(word)):
		if (int(word[i]) == 1):
			d += 1
	return d

def sum2(word1, word2):
	word = []
	for i in range(len(word1)):
		word.append((word1[i] + word2[i])%2)
	return np.array(word)

def getAllD(words):
	d = []
	for i in range(len(words)):
		if False == isNull(words[i]):
			d.append(getWeight(words[i]))
	return np.array(d)


def calculateD(l):
	words = getMsgs(l)
	d = getAllD(words)
	return np.min(d)


def calcD(words):
	# words = getMsgs(l)
	d = getAllD(words)
	return np.min(d)

def createI(k):
	matrix = np.zeros((k,k))
	for i in range(k):
		for j in range(k):
			if i == j:
				matrix[i][j] = 1
	return matrix 

def createC(k, n):
	matrix = np.zeros((k,n-k))
	for i in range(k):
		for j in range(n-k):
			if random.random() > 0.5:
				matrix[i][j] = 1
			else:
				matrix[i][j] = 0
	return matrix

def createG(k, n, C):
	I = createI(k)
	return np.hstack((I, C))

def createH(k, n, C_):
	I = createI(n-k)
	C = np.transpose(C_)
	return np.hstack((C, I))

def isNull(word):
	for i in range(len(word)):
		if word[i] == 1:
			return False
	return True

def getBitCode(msg, G):
	code = np.matmul(msg, G)%2
	return code

def getCodeWords(G, msgs, k, n):
	codeWords = []
	for msg in msgs:
		bit_code = getBitCode(msg, G)
		codeWords.append(bit_code)
	return np.array(codeWords)

def getDecodeMsgs(H, words):
	codeWords = []
	for word in words:
		bit_code = getBitCode(word, np.transpose(H))
		codeWords.append(bit_code)
	return np.array(codeWords)

def correcting(d):
	return np.floor((d-1)/2)

def inputWord():
	word = []
	row = True
	while row:
		row = input()
		if row:
			numbers = map(int, row.split())
			word.append(list(numbers))
			break
	return word[0]

def check(liders1, liders2):
	for i in range(len(liders1)):
		if np.array_equal(liders1[i],liders2[i]):
			print("BAD")
			break
	# print("GOOD")

def find_leader_index(s, S):
	for i in range(len(S)):
		if np.array_equal(s, S[i]):
			return i
	return -1

def decodeByLeaders(word, leaders, H, S, codeWords, msgs):
	s = getBitCode(word, np.transpose(H))
	# print("S:", s)
	leader_index = find_leader_index(s, S)
	# print("leader_index:", leader_index)
	cword = sum2(word, leaders[leader_index])
	print(cword)
	for i in range(len(codeWords)):
		if np.array_equal(cword, codeWords[i]):
			return msgs[i]

	# if leader_index >= 0:
	# 	return sum2(word, leaders[leader_index])
	# else:
	# 	return np.array([])

def findl(codeWord):
	i = 0
	while True:
		if 2**i > len(codeWord):
			return int(i)
		i += 1

def notExist(codeWords, v):
	for word in codeWords:
		if np.array_equal(v, word):
			return False
	return True

def findMin(words):
	minimum = 999
	index = -1
	for i in range(len(words)):
		d = getWeight(words[i])
		if d < minimum:
			minimum = d
			index = i
	return index

def findAllLiders(codeWords, H):
	h = np.transpose(H)
	table = []
	S = []
	S.append(getBitCode(codeWords[0], h))
	table.append(codeWords[0])
	msgs = getMsgs(len(codeWords[0]))
	i = 0
	# print("S[0]:",2**len(S[0]))
	while i < (2**len(S[0])-1):
		# word = np.copy(codeWords[0])
		# word[i] = (word[i]+1)%2
		index = findMin(msgs)
		word = msgs[index]
		# print("word", word)
		msgs = np.delete(msgs, index, axis=0)
		if notExist(codeWords, word):
			s = getBitCode(word, h)
			# print("s", s)
			if notExist(S, s):
				S.append(s)
				table.append(word)
				# print("APPEND word", word)
				# print("APPEND s", s)
				i += 1
		# print("i:", i)
	return np.array(table), np.array(S)


# k = 6
# n = 10

k = int(input('введите k: '))
n = int(input('введите n: '))
if n <= 0 or k <= 0 or n < k:
    print('[X] Invalid data')
    exit()

N = 2**k

C = createC(k, n)
G = createG(k, n, C)
H = createH(k, n, C)
msgs = getMsgs(k)
minD = calcD(msgs)
codeWords = getCodeWords(G, msgs, k, n)
wordsD = calcD(codeWords)
print("Количество слов в коде:")
print(2**k)
print()
print("G:")
print(G)
print()
print("H:")
print(H)
print()
print("Messages:")
print(msgs)
print()
# print("d:", minD)
# print()
print("Кодовые слова:")
print(codeWords)
print()
print("d:", wordsD)
print()
print("Корректирующая способность:", correcting(wordsD))
print()
# decodeMsgs = getDecodeMsgs(H, codeWords)
# print(decodeMsgs)
# print()
leaders, S = findAllLiders(codeWords, H)
print("leaders:")
print(leaders)
print()
print("S:")
print(S)
print()

while True:
	print("Input word:")
	word = inputWord()
	# res = getBitCode(word, np.transpose(H))
	print("It'is word:", decodeByLeaders(word, leaders, H, S, codeWords, msgs))
	# if isNull(res[0]):
	# 	print("It is a code word")
	# 	print(res[0])
	# else:
	# 	print("It is not a code word")
	# 	print(res[0])
	print()


# for i in range(len(aliders)):
# 	for j in range(len(aliders)):
# 		if i != j:
# 			check(aliders[i], aliders[j])
