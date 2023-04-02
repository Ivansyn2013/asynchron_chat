attribute_var = 'attribute'
class_var = 'класс'
func_var = 'функция'
type_var = 'type'

vars = [attribute_var, type_var, class_var, func_var]

for el in vars:
    try:
        print(bytes(el, 'ascii'))
    except:
        print(f'Невозможно преобразовать "{el}"')
