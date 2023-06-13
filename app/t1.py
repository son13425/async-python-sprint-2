import types


# Функция, которая возвращает имя поступающей на вход функции
# и возвращает новую функцию
# инкапсулирующию поведение исходной функции
def notify(fn, *args, **kwargs):

    def fncomposite(*args, **kwargs):
        # Обычная функциональность notify
        print("running %s" % fn.__name__)
        rt = fn(*args, **kwargs)
        return rt
    # Возвращаем сложную функцию
    return fncomposite


# Метакласс, меняющий поведение своих классов
# на новые методы, 'дополненные' поведением
# преобразователя сложной функции
class Notifies(type):

    def __new__(cls, name, bases, attr):
        # Заменим каждую функцию на выражение,
        # которое печатает имя функции
        # перед запуском вычисления с
        # предоставленными args и возвращает его результат
        for name, value in attr.items():
            if type(value) is types.FunctionType or type(value) is types.MethodType:
                attr[name] = notify(value)

        return super(Notifies, cls).__new__(cls, name, bases, attr)


# Проверим метакласс
class Math(metaclass=Notifies):
    def multiply(a, b):
        product = a * b
        print(product)
        return product


Math.multiply(5, 6)

# Запуск multiply():
# 30


class Shouter(metaclass=Notifies):
    def intro(self):
        print("I shout!")


s = Shouter()
s.intro()

# Запуск intro():
# I shout!
