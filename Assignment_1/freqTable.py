class FrequencyTable:
    def __init__(self):
        self.ft = {}

    def add(self, word):
        if word not in self.ft:
            self.ft[word] = 1
        else:
            self.ft[word] += 1

    def get(self, word):
        if word in self.ft:
            return self.ft[word]
        else:
            return 0

    def total(self):
        return sum(self.ft.values())

    def getCount(self, word):
        return self.get(word)

    def getWords(self):
        return self.ft.keys()