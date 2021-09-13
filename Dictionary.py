class Dictionary:
    def __init__(self):
        wordsFile = open('data/corncob_lowercase.txt', 'rb')
        wordLines = wordsFile.readlines()
        self.validWords = []
        cnt = 0
        for line in wordLines:
            cnt += 1
            line1 = line.decode("utf-8").lower().strip()
            if len(line1) < 3:
                continue
            word = line1.split()[0]
            if len(word) < 3:
                continue
            self.validWords.append(str(word))
        print("words list length:", len(self.validWords))
        self.word_dict = {}
        cnt = 0
        for word in self.validWords:
            for i in range(len(word)+1):
                if i == 0:
                    continue
                wrd = word[:i]
                if not wrd in self.word_dict:
                    self.word_dict[wrd] = (i == len(word))
            cnt += 1
