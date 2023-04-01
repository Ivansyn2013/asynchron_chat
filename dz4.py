words = ['разработка', 'администрирование', 'protocol', 'standard']

for word in words:
    word = word.encode('utf-16')
    print('Кодировано в utf16 ', word)
    word = word.decode('utf-16')
    print('Декодировано ' , word)