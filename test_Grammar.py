import Grammar


def test_Grammar_for_CYK():
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


def test_Grammar_for_Earley():
    # Грамматика арифметики с переменной a, сложением, умножением и круглыми
    # скобками
    MyGrammar = Grammar.Grammar(['(', ')', 'a'],
                                ['S', 'T', 'F'],
                                'S',
                                [('S', ['T', '+', 'S']),
                                 ('S', ['T']),
                                 ('T', ['F', '*', 'T']),
                                 ('T', ['F']),
                                 ('F', ['(', 'S', ')']),
                                 ('F', ['a'])])
    assert MyGrammar.Earley(['EPS']) == False
    assert MyGrammar.Earley(list('(a+a)')) == True
    assert MyGrammar.Earley(list('a*(a+a)*a')) == True
    assert MyGrammar.Earley(list('a*a)')) == False
    assert MyGrammar.Earley(list('a*a+a')) == True
    assert MyGrammar.Earley(list('aa')) == False
