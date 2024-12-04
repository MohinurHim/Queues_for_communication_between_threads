# Задача "Потоки гостей в кафе":
import queue
import time
from random import randint
from threading import Thread

class Table:
    def __init__(self, number):
        self.number = number #  номер стола
        self.guest = None #  гость, который сидит за этим столом

class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name #  имя гостя
    def run(self):
        time.sleep(randint(3, 10)) # ожидание случайным образом от 3 до 10 секунд

class Cafe:
    def __init__(self, *tables):
        self.queue = queue.Queue() # очередь (объект класса Queue)
        self.tables = tables # столы в этом кафе
    def guest_arrival(self, *guests): # прибытие гостей
        for guest in guests:  # добавляем в очередь гостей
            que = False  # есть ли гости в очереди
            for table in self.tables:  # проверяем все столы в очереди
                if table.guest is None:  # если стол свободен
                    table.guest = guest  # сажаем гостя
                    guest.start()  # запускаем гостя в отдельном потоке
                    print(f"{guest.name} сел(-а) за стол номер {table.number}")
                    que = True  # стол свободен
                    break
            if not que: # если же свободных столов для посадки не осталось, то помещаем гостя в очередь
                self.queue.put(guest)
                print(f"{guest.name} в очереди")
    def discuss_guests(self): # обслужить гостей
        for table in self.tables:
            if table.guest is not None and not table.guest.is_alive(): # Если за столом есть гость(поток) и гость(поток) закончил приём пищи
                print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                print(f"Стол номер {table.number} свободен")
                table.guest = None # текущий стол освобождается
                if not self.queue.empty(): # Если очередь ещё не пуста
                    next_guest = self.queue.get() # следующий гость из очереди
                    table.guest = next_guest  # текущему столу присваивается гость взятый из очереди
                    next_guest.start()
                    print(f"{next_guest} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")



# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()

  
                  
