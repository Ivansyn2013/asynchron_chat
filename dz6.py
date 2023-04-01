from chardet import detect

words = ['сетевое программирование', 'сокет', 'декоратор']

with open('tmp.txt', 'w') as file:
    for word in words:
        file.write(word + '\n')

with open('tmp.txt', 'rb') as file:
    ENCODING =detect(file.readline())['encoding']
    print('Кодировка по цмолчанию ' + ENCODING)
    data = file.read()
    data = data.decode(ENCODING)

with open('tmp.txt', 'w', encoding='utf-8') as file:
    file.write(data)

with  open('tmp.txt', 'r', encoding='utf-8') as file:
    print(file.read())
    pass
