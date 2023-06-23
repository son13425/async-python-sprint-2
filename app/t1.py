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


 from threading import Timer
 import datetime
 import random


def f():
    print("Executing f1 at", datetime.datetime.now().time())
    result = f2()
    timer = Timer(5, f3)
    timer.start()
    if(result > 5):
        print("Cancelling f3 since f2 resulted in", result)
        timer.cancel()


def f2():
    print("Executing f2 at", datetime.datetime.now().time())
    return random.randint(1, 10)


def f3():
    print("Executing f3 at", datetime.datetime.now().time())


f()
