import typing


class Grammar:
    Terminals: typing.List[str]
    NonTerminals: typing.List[str]
    StartSymbol: str
    Rules: typing.List[typing.Tuple[str, typing.List[str]]]
    # Правила передаются в формате списка tuple, где первый элемент -
    # нетерминальный символ, а второй - список элементов, на которые
    # происходит замена

    def __init__(self, GrTerminals: typing.List[str], GrNonTerminals: typing.List[str],
                 GrStartSymbol: str, GrRules: typing.List[typing.Tuple[str, typing.List[str]]]):
        self.Terminals = GrTerminals
        self.NonTerminals = GrNonTerminals
        self.StartSymbol = GrStartSymbol
        self.Rules = GrRules

    def CYK(self, word: typing.List[str]):
        len_word = len(word)
        dp = dict()
        for non_terminal in self.NonTerminals:
            dp[non_terminal] = []
            for i in range(len_word):
                dp[non_terminal].append([])
                for j in range(len_word):
                    dp[non_terminal][i].append(False)
        for rule in self.Rules:
            if len(rule[1]) > 1:
                continue
            for i in range(len_word):
                if rule[1][0] == word[i]:
                    dp[rule[0]][i][i] = True
        for l in range(2, len_word + 1):
            for i in range(0, len_word + 1 - l):
                j = i + l - 1
                for rule in self.Rules:
                    if len(rule[1]) == 1:
                        continue
                    for k in range(i, j):
                        dp[rule[0]][i][j] |= (
                            dp[rule[1][0]][i][k] & dp[rule[1][1]][k + 1][j])
        return dp[self.StartSymbol][0][len_word - 1]

    def scan(self, D: typing.List[typing.Tuple[typing.List[typing.Tuple[str,
                                                                        typing.List[str]]], int, int]], j: int, word: typing.List[str]):
        if j == 0:
            return
        for rule, i, pos in D[j - 1]:
            if pos + 1 <= len(rule[1]) and rule[1][pos] == word[j - 1]:
                if (rule, i, pos + 1) not in D[j]:
                    D[j].append((rule, i, pos + 1))

    def complete(
            self, D: typing.List[typing.Tuple[typing.List[typing.Tuple[str, typing.List[str]]], int, int]], j: int):
        for rule1, i, pos in D[j]:
            if pos < len(rule1[1]):
                continue
            for rule2, j2, pos2 in D[i]:
                if pos2 == len(rule2[1]) or rule2[1][pos2] != rule1[0]:
                    continue
                if (rule2, j2, pos2 + 1) not in D[j]:
                    D[j].append((rule2, j2, pos2 + 1))

    def predict(
            self, D: typing.List[typing.Tuple[typing.List[typing.Tuple[str, typing.List[str]]], int, int]], j: int):
        for rule1, i, pos in D[j]:
            if pos == len(rule1[1]):
                continue
            for rule2 in self.Rules:
                if rule2[0] != rule1[1][pos]:
                    continue
                if (rule2, j, 0) not in D[j]:
                    D[j].append((rule2, j, 0))

    def Earley(self, word: typing.List[str]):
        len_word = len(word)
        fic_symbol = max(self.NonTerminals)
        fic_symbol += '\''
        self.NonTerminals.append(fic_symbol)
        self.Rules.append((fic_symbol, [self.StartSymbol]))

        # Конфигурация: (rule, i, pos), где pos - позиция точки
        D = [[] for i in range(len_word + 1)]
        D[0].append((self.Rules[-1], 0, 0))

        for j in range(len_word + 1):
            self.scan(D, j, word)
            last_length = -1
            while len(D[j]) != last_length:
                last_length = len(D[j])
                self.complete(D, j)
                self.predict(D, j)

        self.NonTerminals.pop(len(self.NonTerminals) - 1)
        self.Rules.pop(len(self.Rules) - 1)
        return ((fic_symbol, [self.StartSymbol]), 0, 1) in D[len_word]
