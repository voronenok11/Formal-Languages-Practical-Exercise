Для работы с pytest нужно выполнить две команды:
    pip install pytest
    pip install pytest-cov
Далее чтобы их запустить, нужно напасть команду pytest --cov=Grammar.py --cov-report=html
Выдастся статистика по покрытая строчкам и то, что тесты успешно работают. Все покрытые строчки можно увидеть на сайте, по которому можно перейти в html-файле htmlcov/index.html и нажать на имя файла.

Чтобы руками потестить грамматику, нужно создать экземпляр класса Grammar, где нужно передать четыре аргумента:
1) Терминальные символы - список строк
2) Нетерминальные символы - список строк
3) Начальное состояние - строка, которая присутствует в нетерминальных символах
4) Правила - список пар, где первый элемент пары - левая часть правила, а второй элемент - список строк, на что происходит замена в правиле
