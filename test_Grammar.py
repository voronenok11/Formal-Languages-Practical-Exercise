import Grammar


def test_Grammar():
    # Грамматика правильной скобочной последовательности
    MyGrammar = Grammar.Grammar(['(', ')'],
                                ['S', 'A', 'B', 'C', 'D'],
                                'S',
                                [('S', ['EPS']),
                                 ('S', ['A', 'A']),
                                 ('S', ['B', 'C']),
                                 ('A', ['A', 'A']),
                                 ('A', ['B', 'C']),
                                 ('B', ['(']),
                                 ('C', ['A', 'D']),
                                 ('C', [')']),
                                 ('D', [')'])])
    assert MyGrammar.CYK(['EPS']) == True
    assert MyGrammar.CYK(['(']) == False
    assert MyGrammar.CYK([')']) == False
    assert MyGrammar.CYK(['(', ')']) == True
    assert MyGrammar.CYK(['(', ')', ')']) == False
    assert MyGrammar.CYK([')', '(']) == False
    assert MyGrammar.CYK(list('(()())')) == True
    assert MyGrammar.CYK(list('(((())()())(()))')) == True
    assert MyGrammar.CYK(list('(((())()()))(()))')) == False
    assert MyGrammar.CYK(list('(()))(')) == False
