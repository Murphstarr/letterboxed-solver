from Dictionary import Dictionary

class Node:
    # node holds the tree of word prefixes

    def __init__(self, game, par, side, word, letter):
        self.childs = []
        self.side = side
        self.ltr = letter
        self.game = game
        self.parent = par
        self.word = word
        self.fullWord = False
        if par is None:
            self.level = 0
        else:
            self.level = par.level + 1
            self.parent.childs.append(self)

    def show(self):
        # print the node tree
        sp = ' ' * self.level * 2
        print(self.level, sp, "[", self.word, "] ltr:", self.ltr, "side:",
              self.side, "<=============" if self.fullWord else "")
        for c in self.childs:
            c.show()

    def explore(self, word):
        # recursively explore the word tree building word prefixes
        if self.level > 16:
            return
        for s in range(len(self.game.sides)):
            if s == self.side:
                continue
            for ltr in self.game.sides[s]:
                newWord = self.word + ltr
                if newWord in self.game.dict.word_dict:
                    n = Node(self.game, self, s, newWord, ltr)
                    full = self.game.dict.word_dict[newWord]
                    if full:
                        self.game.validWords.append(newWord)
                        n.fullWord = True

                    n.explore(self.word)


class WordSet:
    # a solution set of words

    def __init__(self):
        self.words = []


class Game:
    # A LetterBoxed game
    ltrs = set()
    firstLtr = None
    entry = 0
    soln = []

    def sortLenc(self, w):
        # sort the solution set by number of words and then word length
        if self.firstLtr is None:
            s = len(self.ltrs - set(w))
        else:
            if w[0] == self.firstLtr:
                s = len(self.ltrs - set(w))
            else:
                s = 1000000
        return s

    def solve(self, lvl, par, nodeWord, remaingLtrs):
        # search the word tree recursively looking for word matches
        self.entry += 1
        if self.entry % 1000000 == 0:
            print(self.entry, len(self.soln))
        if lvl >= 3:  # >= n means n is h emax number of words to try
            return

        n = Node(self, par, None, nodeWord, None)
        for word in self.validWords:
            if word == nodeWord:
                continue
            if not nodeWord is None and word[0] != nodeWord[-1]:
                continue
            nextParent = par
            already = False
            while nextParent is not None:
                if nextParent.word == word:
                    already = True
                    break
                nextParent = nextParent.parent
            if already:
                continue
            remain = remaingLtrs - set(word)
            if len(remain) == 0:
                wordSet = WordSet()
                wordSet.words.append(word)
                wordSet.words.append(nodeWord)
                nextParent = n.parent
                while nextParent is not None:
                    if not nextParent.word is None:
                        wordSet.words.append(nextParent.word)
                    nextParent = nextParent.parent
                self.soln.append(wordSet)
                if False:
                    print("====== found, entry:", self.entry)
                    for w in wordSet.words:
                        print(w, end=' ')
                    print()
            else:
                self.solve(lvl + 1, n, word, remain)

    def __init__(self, dict):
        # Play a game

        self.validWords = []
        self.sides = []
        self.dict = dict
        self.sides.append(['n', 'o', 'a'])
        self.sides.append(['c', 'y', 'l'])
        self.sides.append(['j', 'i', 'e'])
        self.sides.append(['d', 'g', 'k'])

        self.root = Node(self, None, None, "", "")
        self.root.explore("")

        remainingLtrs = set()
        for side in self.sides:
            for ltr in side:
                remainingLtrs.add(ltr)

        self.solve(0, None, None, remainingLtrs)

        slns = sorted(self.soln, key=self.score)
        cnt = 0
        last = 0
        for ws in slns:
            wordCnt = len(ws.words)
            if not wordCnt == last:
                cnt = 0
                print("-----", wordCnt)
                last = wordCnt

            score = self.score(ws)
            print(cnt, "score:", score, end=' ')
            for w in reversed(range(len(ws.words))):
                print(ws.words[w], end=' ')
            print()
            cnt += 1
            if cnt > 10:
                break

    def score(self, ws):
        # score a solution set
        score = len(ws.words) * 10000
        for w in ws.words:
            score += len(w)
        return score


d = Dictionary()
g = Game(d)
