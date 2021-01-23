class NaiveBayes:
    def __init__(self):
        self.table = []
        self.probabilitiesOfClass = {}
        self.probabilitiesAll = {}
    
    #csv files only, or list
    #table is name or path of archive
    # 1 to extArq for csv files
    #pt = 1 -> for print table
    def load(self, table, extArq = 0, pt = 0):
        if extArq == 0:
            self.table = table
        elif extArq == 1:
            try:
                self.table = CsvToTable().ArqToTable(table)
            except:
                raise("Csv File is Required")
        if pt == 1:
            print("------------ table ------------")
            print(self.table)
            print('-------------------------------')
            print('\n')
        
    def start(self):
        self.generatedClassProbabilities()
        self.generatedAllProbabilities()
    
    def generatedClassProbabilities(self, pt = 0):
        p = {}
        total = 0
        positionClass = len(self.table[0]) -1
        for n in range(1,len(self.table)):
            result = self.table[n][positionClass]
            if result in p:
                p[result] += 1
                total += 1
            else:
                p[result] = 1
                total += 1
        for k in p.keys():
            self.probabilitiesOfClass[k] = (p[k], p[k]/total)
        
        if pt == 1:
            print("--------probabiliti of class--------")
            print(self.probabilitiesOfClass)
            print("------------------------------------")
            print('\n')

    def generatedAllProbabilities(self, pt = 0):
        p = {}
        for n in range(1, len(self.table)):
            for i in range(0, len(self.table[0])):
                if self.table[n][i] in p:
                    if self.table[n][len(self.table[0]) -1] not in p[self.table[n][i]]:
                        p[self.table[n][i]][self.table[n][len(self.table[0]) -1]] = 1
                    else:
                        p[self.table[n][i]][self.table[n][len(self.table[0]) -1]] += 1
                else:
                    p[self.table[n][i]] = {self.table[n][len(self.table[0]) -1]: 1}

        for k in p.keys():
            flag = {}
            for k1 in p[k].keys():
                flag[k1] = p[k][k1]
                flag[k1 + "Probability"] = p[k][k1]/self.probabilitiesOfClass[k1][0]
            self.probabilitiesAll[k] = flag
        if pt == 1:
            print("-------- probabilities all --------")
            print(self.probabilitiesAll)
            print("---------------------------------")
            print('\n')
    
    def checkProbability(self, line):
        #line = 'sunny,hot,high,FALSE'
        string = line.split(",")
        probs = {}
        for k in self.probabilitiesOfClass.keys():
            calculo = self.probabilitiesOfClass[k][1]
            cont = 0
            for i in string:
                try:
                    calculo = calculo * self.probabilitiesAll[i+str(cont)][k + 'Probability']
                except:
                    calculo = calculo * 0
                cont += 1
            probs[k] = calculo
        
        print("-------------- Result --------------")
        maior = 0
        name = ''
        for k in probs.keys():
            if probs[k] > maior:
                maior = probs[k]
                name = k
        n = len(self.table[0])-1
        name = name.replace(str(n),'')
        print(name + " : " + str(maior))
        print('-------------------------------------')
        print('\n')


class CsvToTable:
    def __init__(self):
        pass
        
    def ArqToTable(self, NameArq):
        with open(NameArq) as f:
            l1 , l2 = [], []
            string = ''
            for piece in self.read_in_chunks(f):
                if piece != '\n' and piece != ',':
                    string += piece
                elif piece == ',':
                    l1.append(string + str(len(l1)))
                    string = ''
                else:
                    l1.append(string + str(len(l1)))
                    l2.append(l1)
                    l1 = []
                    string = ''
        return l2

    def read_in_chunks(self, file_object, chunk_size=1):
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data


if __name__ == "__main__":
    n = NaiveBayes()
    n.load('insurance.csv', 1)
    n.start()
    n.checkProbability('FALSE,Adult,Prole,Adventurous,Older,Moderate,EggShell,Economy,Poor,TwentyThou,FALSE,SubStandard,FALSE,TenThou,FALSE,FiveThou,City,FALSE,TenThou,Thousand,TRUE,Thousand,Poor,FALSE,Thousand,Many')
    n.checkProbability('FALSE,Senior,Prole,Cautious,Current,None,Football,Economy,Normal,TwentyThou,FALSE,Normal,TRUE,Thousand,FALSE,TenThou,City,TRUE,Thousand,Thousand,TRUE,Thousand,Good,TRUE,Thousand,Zero')
    n.checkProbability('FALSE,Senior,UpperMiddle,Psychopath,Current,None,Football,FamilySedan,Excellent,Domino,TRUE,Normal,FALSE,Thousand,FALSE,TwentyThou,City,FALSE,Thousand,Thousand,FALSE,Thousand,Good,TRUE,Thousand,One')
    n.checkProbability('FALSE,Adolescent,Middle,Normal,Older,None,EggShell,Economy,Normal,FiftyThou,FALSE,Normal,FALSE,Thousand,FALSE,FiveThou,Suburb,FALSE,Thousand,Thousand,TRUE,Thousand,Fair,FALSE,Thousand,Zero')
    n.checkProbability('FALSE,Adolescent,Prole,Normal,Older,Moderate,Football,Economy,Poor,FiftyThou,FALSE,SubStandard,FALSE,TenThou,FALSE,FiveThou,City,FALSE,TenThou,Thousand,FALSE,Thousand,Fair,FALSE,Thousand,Many')