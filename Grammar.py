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
