# Зададим карту
maps = [1, 2, 3,
        4, 5, 6,
        7, 8, 9]

# Зададим победные комбинации
victories = [[0, 1, 2],
             [3, 4, 5],
             [6, 7, 8],
             [0, 3, 6],
             [1, 4, 7],
             [2, 5, 8],
             [0, 4, 8],
             [2, 4, 6]]

# Выведем карту на экран
def print_maps():
    print("-" * 13)
    for i in range(3):
        print("|", maps[0 + i * 3], "|", maps[1 + i * 3], "|", maps[2 + i * 3], "|")
        print("-" * 13)

# Сделаем ход в ячейку
def step_maps(step,mark):
    ind = maps.index(step)
    maps[ind] = mark

# Получим текущий результат игры
def check_result():
    win = ""
    for i in victories:
        if maps[i[0]] == "X" and maps[i[1]] == "X" and maps[i[2]] == "X":
            win = "X"
        if maps[i[0]] == "O" and maps[i[1]] == "O" and maps[i[2]] == "O":
            win = "O"
    return win

# Опишем ход игры
game_over = False
player1 = True

while game_over == False:
    print_maps()
    if player1 == True:
        mark = "X"
        step = int(input("Игрок 1, ваш ход: "))
    else:
        mark = "O"
        step = int(input("Игрок 2, ваш ход: "))

    step_maps(step, mark)
    win = check_result()
    if win != "":
        game_over = True
    else:
        game_over = False
    player1 = not player1

print_maps()
print("Победил", win)












