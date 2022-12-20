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

    def build_graph(self, start_rule: typing.Tuple[str, typing.List[str]]):
        vertexs_queue = [0]
        vertexs = {
            0: (start_rule, 0),
        }

        number_vertex = 1
        edges = []
        while len(vertexs_queue) > 0:
            vertex = vertexs_queue[0]
            vertexs_queue = vertexs_queue[1:]
            rule, pos = vertexs[vertex]
            if pos < len(rule[1]) and rule[1][pos] in self.NonTerminals:
                for next_rule in self.Rules:
                    if next_rule[0] != rule[1][pos] or next_rule == rule:
                        continue
                    next_config = (next_rule, 0)
                    if next_config in list(vertexs.values()):
                        for number, config in vertexs.items():
                            if config == next_config:
                                next_vertex = number
                                break
                        edges.append((vertex, next_vertex, 'EPS'))
                    else:
                        vertexs[number_vertex] = next_config
                        edges.append((vertex, number_vertex, 'EPS'))
                        vertexs_queue.append(number_vertex)
                        number_vertex += 1
            if pos < len(rule[1]):
                next_config = (rule, pos + 1)
                if next_config in list(vertexs.values()):
                    for number, config in vertexs.items():
                        if config == next_config:
                            next_vertex = number
                            break
                    edges.append((vertex, next_vertex, rule[1][pos]))
                else:
                    vertexs[number_vertex] = next_config
                    edges.append((vertex, number_vertex, rule[1][pos]))
                    vertexs_queue.append(number_vertex)
                    number_vertex += 1

        return vertexs, edges

    def build_compressed_graph(
            self, vertexs: typing.Dict[int, typing.Tuple[typing.Tuple[str, typing.List[str]], int]], edges: typing.List[typing.Tuple[int, int, str]]):
        new_vertexs = {}
        new_edges = []
        start_mask = set([0])
        eps_queue = [0]
        while len(eps_queue) > 0:
            vertex = eps_queue[0]
            eps_queue = eps_queue[1:]
            for edge in edges:
                if edge[2] != 'EPS' or edge[0] != vertex or edge[1] in start_mask:
                    continue
                eps_queue.append(edge[1])
                start_mask.add(edge[1])
        masks = [start_mask]
        queue = [0]
        while len(queue) > 0:
            mask_id = queue[0]
            next_masks = {}
            queue = queue[1:]

            for edge in edges:
                if edge[0] in masks[mask_id]:
                    if edge[2] == 'EPS':
                        continue
                    next_masks.setdefault(edge[2], set())
                    next_masks[edge[2]].add(edge[1])
                    eps_queue = [edge[1]]
                    while len(eps_queue) > 0:
                        vertex = eps_queue[0]
                        eps_queue = eps_queue[1:]
                        for edge2 in edges:
                            if edge2[2] != 'EPS' or edge2[0] != vertex or edge2[1] in next_masks[edge[2]]:
                                continue
                            eps_queue.append(edge2[1])
                            next_masks[edge[2]].add(edge2[1])

            for char, next_mask in next_masks.items():
                if next_mask in masks:
                    for ind in range(len(masks)):
                        if masks[ind] == next_mask:
                            next_mask_id = ind
                            break
                    new_edges.append((mask_id, next_mask_id, char))
                else:
                    new_edges.append((mask_id, len(masks), char))
                    queue.append(len(masks))
                    masks.append(next_mask)

        for ind in range(len(masks)):
            for number in masks[ind]:
                new_vertexs.setdefault(ind, [])
                new_vertexs[ind].append(vertexs[number])

        for ind1 in range(len(masks)):
            for ind2 in range(len(masks)):
                for char in self.NonTerminals:
                    is_new_edge = True
                    for vertex in masks[ind2]:
                        find_edge = False
                        for edge in edges:
                            if edge[2] == char and edge[1] == vertex and edge[0] in masks[ind1]:
                                find_edge = True
                                break
                        if not find_edge:
                            is_new_edge = False
                            break
                    if is_new_edge:
                        new_edges.append((ind1, ind2, char))
        return new_vertexs, list(set(new_edges))

    def build_table(self, vertexs: typing.Dict[int, typing.List[typing.Tuple[typing.Tuple[str,
                                                                                          typing.List[str]], int]]], edges: typing.List[typing.Tuple[int, int, str]]):
        table = [{} for i in range(len(vertexs))]
        for edge in edges:
            if edge[2] in self.NonTerminals:
                table[edge[0]][edge[2]] = ('#', edge[1])
            else:
                table[edge[0]][edge[2]] = ('s', edge[1])

        for vertex, configs_in_vertex in vertexs.items():
            for char in self.Terminals:
                for config in configs_in_vertex:
                    rule, pos = config
                    if pos == len(rule[1]):
                        for rule_number in range(len(self.Rules)):
                            if self.Rules[rule_number] == rule:
                                if char not in table[vertex]:
                                    table[vertex][char] = ('r', rule_number)
                                break
        return table

    def LR0(self, word: typing.List[str]):
        len_word = len(word)

        new_nonterminal = max(max(self.NonTerminals), max(self.Terminals))
        new_nonterminal += '\''
        self.NonTerminals.append(new_nonterminal)
        self.Rules.append((new_nonterminal, [self.StartSymbol]))

        new_terminal = max(max(self.NonTerminals), max(self.Terminals))
        new_terminal += '\''
        self.Terminals.append(new_terminal)

        vertexs, edges = self.build_graph(self.Rules[-1])

        vertexs, edges = self.build_compressed_graph(vertexs, edges)

        table = self.build_table(vertexs, edges)

        word.append(new_terminal)

        InLanguage = False
        ptr = 0
        stack = [0]
        while not InLanguage and ptr < len(word) and len(stack) > 0:
            word_char = word[ptr]
            stage = stack[-1]
            if word_char not in table[stage]:
                break
            type_edge, next_stage = table[stage][word_char]
            if type_edge == '#':
                break
            elif type_edge == 's':
                ptr += 1
                stack.append(word_char)
                stack.append(next_stage)
            elif next_stage == len(self.Rules) - 1:
                InLanguage = True
                break
            else:
                rule = self.Rules[next_stage]
                stack = stack[: len(stack) - 2 * len(rule[1])]
                stage = stack[-1]
                stack.append(rule[0])
                stack.append(table[stage][rule[0]][1])

        self.NonTerminals.pop(len(self.NonTerminals) - 1)
        self.Terminals.pop(len(self.Terminals) - 1)
        self.Rules.pop(len(self.Rules) - 1)
        return InLanguage
