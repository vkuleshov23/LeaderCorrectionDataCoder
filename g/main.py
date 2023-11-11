import numpy as np
import math

class lineCode():
    def __init__(self, n, k):
        self.k = k
        self.n = n
        
        self.keyMatrix = None  
        self.GMatrix = None
        self.HMatrix = None
        
        self.wordCount = 2 ** k
        self.words = None
        self.codeWords = None
    
    def launch(self):
        self.genGeneralMatrix()    
        print("G:")
        print(self.GMatrix, "\n")
        
        self.genWords()
        print("words:",self.wordCount, "\n")
        # print(self.words)

        self.genCodeWords()
        for i in range(self.wordCount):
            print(self.words[i], "->", self.codeWords[i])
        print()

        d = self.minCodeDistance()
        print("d =", d)
        t = math.floor((d-1)/2)
        print("correcting capability:", t, "\n")
        
        hamming = self.boundaryHamming(t)
        vagi = self.borderVarshamovGilbert(d)
        singleton = self.borderSingleton(d)

        print("Hamming boundary:", hamming)
        print("delta Hamming:", hamming - (2 ** self.k))
        print()

        print("Varshamov-Gilbert border:", vagi)
        print("delta Varshamov-Gilbert:", vagi - (2 ** self.k))
        print()

        print("Singleton border:", singleton)
        print("delta Singleton:", singleton - (2 ** self.k))
        print()


        self.genCheckMatrix()
        # print("H:")
        # print(self.HMatrix)
        
    def genGeneralMatrix(self):
        ar1 = np.eye(self.k, dtype=int)
        self.keyMatrix = np.random.randint(0,2,(self.k,self.n-self.k))
        self.GMatrix = np.hstack([ar1, self.keyMatrix])
    
    def genCheckMatrix(self):
        ar1 = self.keyMatrix.transpose()
        ar2 = np.eye(len(ar1), dtype=int)
        self.HMatrix = np.hstack([ar1, ar2])
        
    def genWords(self):
        res = np.zeros((self.wordCount, self.k), 'int')

        for i in range(self.wordCount):
            b = np.zeros(self.k)
            for j in range(self.k):
                b[j] = self.getBit(i,j)
            res[i] = b
        self.words = res
    
    def getBit(self, num, i):
        if (num & (1 << i)) == 0 :
            return 0
        else:
            return 1

    def genCodeWords(self):
        self.codeWords = np.zeros((self.wordCount, self.n), 'int')

        for i in range(len(self.codeWords)):
            # print(self.GMatrix)
            self.codeWords[i] = np.matmul(self.words[i], self.GMatrix) % 2

    def minCodeDistance(self):
        mind = self.n
        for i in range(self.wordCount):
            d = 0
            for j in range(len(self.codeWords[0])):
                if(self.codeWords[i][j] == 1):
                    d += 1
            if(d < mind and d != 0):
                mind = d
        return mind

    def getPowerCode(self, d):
        powerCode = 0
        if d == 0:
            powerCode = math.comb(self.n, d)
        else:
            for i in range(d+1):
                powerCode += math.comb(self.n, i)  
        return powerCode

    def boundaryHamming(self, t):
        return (2 ** self.n) / self.getPowerCode(t)

    def borderVarshamovGilbert(self, d):
        return (2 ** self.n) / self.getPowerCode(d - 1)

    def borderSingleton(self, d):
        return 2 ** (self.n - d + 1)

# n = int(input('n = '))
# k = int(input('k = '))
n = 9
k = 4

ex = lineCode(n, k)
ex.launch()

m = Matrix(k,n)
m.start()
# powerCode = 0
# for i in range(2):
#     powerCode += math.comb(12, i)
# print(powerCode)