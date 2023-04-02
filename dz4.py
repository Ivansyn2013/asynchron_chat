words = ['разработка', 'администрирование', 'protocol', 'standard']

for word in words:
    word = word.encode('utf-8')
    print('Кодировано в utf8 ', word)
    word = word.decode('utf-8')
    print('Декодировано ', word)
