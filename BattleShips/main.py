import random
from random import randint

class BoardException(Exception):  # задаем исключения
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):  # необходимое исключение для того, чтобы компьютер смог разместить корабли на поле
    pass


class Dot:  # задаем систему координат
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):  # зададим метод, сравнивающий точки и проверяющий их вхождение в список точек корабля
        return self.x == other.x and self.y == other.y

    def __repr__(self):  # зададим метод, выводящий координаты точки в консоль
        return f"Dot({self.x}, {self.y})"


class Ship:  # задаем координаты корабля
    def __init__(self, bow, l, o):
        self.bow = bow  # положение носа корабля
        self.l = l  # длина корабля в клетках
        self.o = o  # ориентация корабля (вертикально/горизонтально)
        self.lives = l  # количество жизней корабля приравнено к длине корабля

    @property
    def dots(self):
        ship_dots = []  # задаем список, в который войдут все координаты корабля
        for i in range(self.l):  # перебираем точки на протяжении всей длины корабля, чтобы задать
            cur_x = self.bow.x  # координаты положения носа корабля
            cur_y = self.bow.y

            if self.o == 0:  # координаты точек для ориентации корабля
                cur_x += i
            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots



class Board:  # задаем игровое поле вместе со всеми параметрами и обозначениями
    def __init__(self, hid=False, size=6):
        self.hid = hid  # скрываем корабли
        self.size = size
        self.count = 0  # устанавливаем счетчик подбитых кораблей
        self.field = [["0"] * size for _ in range(size)]  # рисуем матрицу
        self.busy = []  # задаем список занятых точек (подбитые корабли или точки, в которые уже стреляли)
        self.ships = []  # задаем список всехх кораблей доски

    def __str__(self):  # задаем нумерацию строк и столбцов
        res = ""
        res += " |1|2|3|4|5|6|"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1}|" + "|".join(row) + "|"

        if self.hid:
            res = res.replace("■", "0")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))  # будем проверять, находится ли точка за пределами доски

    def contour(self, ship, verb=False):  # зададим контур корабля и его отображение на доске
        near = [
            (-1, 1), (0, 1), (1, 1),  # зададим координаты сдвигов точек от центральной
            (-1, 0), (0, 0), (1, 0),
            (-1, -1), (0, -1), (1, -1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:  # если точка не за пределами поля и не занята,
                    if verb:
                        self.field[cur.x][cur.y] = "."  # то помечаем ее точкой и вносим в список занятых
                self.busy.append(cur)

    def add_ship(self, ship):  # добавим корабль на поле
        for d in ship.dots:
            if self.out(d) or d in self.busy:    # если координаты точек заняты или за пределами поля,
                raise BoardWrongShipException()  # то вызываем ошибку
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)


    def shot(self, d):  # добавим отображение уничтоженных и поврежденных кораблей на поле
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль поврежден!")
                    return True

        self.field[d.x][d.y] = "."
        print("Вы промахнулись!")
        return False


    def begin(self):  # обнуляем список занятых точек, чтобы можно было начать игру
        self.busy = []


class Player:  # задаем родительский класс игрока
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        return True

    def turn(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class User(Player):  # задаем дочерний класс игрока-человека
    def ask(self):
        while True:
            cords = input("Введите координаты выстрела: ").split()

            if len(cords) != 2:
                 print(" Введите 2 координаты!")
                 continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                 print(" Введите числа!")
                 continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class AI(Player):  # задаем дочерний класс игрока-компьютера
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Координаты выстрела компьютера: {d.x + 1} {d.y + 1}")
        return d


class Main:  # задаем генерацию игрового поля
    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board


    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board


    def __init__(self, size=6):  # задаем работу конструктора игровых полей для игрока и компьютера
        self.size = size
        pl_board = self.random_board()
        ai_board = self.random_board()
        ai_board.hid = True

        self.ai = AI(ai_board, pl_board)
        self.us = User(pl_board, ai_board)


    def greet(self):  # задаем приветствие для игрока
        print("------------------")
        print(" Добро пожаловать ")
        print("      в игру      ")
        print("   'Морcкой бой'  ")
        print("------------------")
        print("формат ввода: x y ")
        print("x - номер строки  ")
        print("y - номер столбца ")


    def loop(self):  # задаем основной игровой цикл
        num = 0
        gift_list = ["Священный якорь", "Сабля божественного адмирала", "Штурвал покорителя морей", "Гром-пушка"]
        while True:
            print("-" * 20)
            print("Доска человека:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-" * 20)
            if num % 2 == 0:
                print("Ход человека!")
                repeat = self.us.turn()
            else:
                print("Ход компьютера!")
                repeat = self.ai.turn()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Человек выиграл!")
                print("Ваша награда за победу: ", random.choice(gift_list))
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):  # задаем запуск игры
        self.greet()
        self.loop()


# Запускаем игру
g = Main()
g.start()