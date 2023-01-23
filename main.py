from math import log2
from tkinter import *

eps = 0.0000001


def separate_probability(mas_XY, num_x, num_y):
    """Ищем p(x) и p(y)"""
    sp_x = []
    for i in range(num_x):
        sum = 0
        for j in range(num_y):
                sum += mas_XY[i + j + (num_y - 1) * i]
        sp_x.append(round(sum, 4))

    sp_y = []
    for i in range(num_y):
        sum = 0
        for j in range(num_x):
            sum += mas_XY[i + j + (num_y - 1) * j]
        sp_y.append(round(sum, 4))

    return sp_x, sp_y


def probability(mas_XY, sp_x, sp_y, num_x, num_y):
    """Ищем p(x|y) и p(y|x)"""
    p_x = []
    for i in range(num_x):
        for j in range(num_y):
            p_x.append(round(mas_XY[i + j + (num_y - 1) * i] / sp_y[j], 4))

    p_y = []
    for i in range(num_y):
        for j in range(num_x):
            p_y.append(round(mas_XY[i + j + (num_y - 1) * j] / sp_x[j], 4))

    return p_x, p_y


def is_dependence(mas_XY, sp_x, sp_y, num_x, num_y):
    """Проверка на зависимость"""
    for i in range(num_x):
        for j in range(num_y):
            if abs(mas_XY[i + j + (num_y - 1) * i] - (sp_x[i] * sp_y[j])) >= eps:

                return False
    return True


def entropy_ensemble(mas_XY, sp_x, sp_y, num_x, num_y):
    """Ищем H(X), H(Y) и H(XY)"""
    entropy_X = 0.
    for i in range(num_x):
        if sp_x[i].__eq__(0) is False:
            entropy_X += sp_x[i] * log2(sp_x[i])

    entropy_Y = 0.
    for i in range(num_y):
        if sp_y[i].__eq__(0) is False:
            entropy_Y += sp_y[i] * log2(sp_y[i])

    entropy_XY = 0.
    for i in range(num_x * num_y):
        if mas_XY[i].__eq__(0) is False:
            entropy_XY += mas_XY[i] * log2(mas_XY[i])

    return round(entropy_X * (-1), 2), round(entropy_Y * (-1), 2), round(entropy_XY * (-1), 2)


def partial_conditional_entropies(sp_x, sp_y, p_x, p_y, num_x, num_y):
    """Ищем Hy(X) и Hx(Y)"""
    paren_hxy = 0
    for i in range(num_x):
        sum = 0
        for j in range(num_y):
            if p_y[j + i + (num_x - 1) * j].__eq__(0) is False:
                sum += p_y[j + i + (num_x - 1) * j] * log2(p_y[j + i + (num_x - 1) * j])
        print(f'Hx{i + 1}(Y) = {round(- sum, 2)}')
        paren_hxy -= sp_x[i] * sum

    print("-------------------------------------")

    paren_hyx = 0
    for i in range(num_y):
        sum = 0
        for j in range(num_x):
            if p_x[j + i + (num_y - 1) * j].__eq__(0) is False:
                sum += p_x[j + i + (num_y - 1) * j] * log2(p_x[j + i + (num_y - 1) * j])
        print(f'Hy{i + 1}(X) = {round(-sum, 2)}')
        paren_hyx -= sp_y[i] * sum

    print("-------------------------------------")

    return round(paren_hxy, 2), round(paren_hyx, 2)


# def read(filename):
#     with open(filename) as f:
#         mas = []
#         for row in f.readlines():
#             mas.append(list(map(float, row.split())))
#         return mas[0], mas[1]


def logical(vol_x, vol_y, massive_XY):
    # filename = input('Введите название файла: ')
    # number = int(input('Введите номер задачи: '))
    # matrix_XY, quantity_xy = read(filename)
    quantity_xy = []
    quantity_xy.append(vol_x)
    quantity_xy.append(vol_y)

    matrix_XY = list(map(float, massive_XY.split()))

    number = 2
    result = []

    sepp_x, sepp_y = separate_probability(matrix_XY, int(quantity_xy[0]), int(quantity_xy[1]))
    prob_x, prob_y = probability(matrix_XY, sepp_x, sepp_y, int(quantity_xy[0]), int(quantity_xy[1]))

    for i in range(int(quantity_xy[0])):
        result.append(f"p(x{i + 1}) = {sepp_x[i]}")

    result.append("-------------------------------------")

    for i in range(int(quantity_xy[1])):
        result.append(f"p(y{i + 1}) = {sepp_y[i]}")

    result.append("-------------------------------------")

    for i in range(int(quantity_xy[0])):
        for j in range(int(quantity_xy[1])):
            result.append(f"p(x{i + 1}|y{j + 1}) = {prob_x[i + j + (int(quantity_xy[1]) - 1) * i]}")

    result.append("-------------------------------------")

    for i in range(int(quantity_xy[1])):
        for j in range(int(quantity_xy[0])):
            result.append(f"p(y{i + 1}|x{j + 1}) = {prob_y[i + j + (int(quantity_xy[0]) - 1) * i]}")

    result.append("-------------------------------------")

    if is_dependence(matrix_XY, sepp_x, sepp_y, int(quantity_xy[0]), int(quantity_xy[1])):
        result.append('Ансамбли не зависимы')
    else:
        result.append('Ансамбли зависимы')

    result.append("-------------------------------------")

    if number == 2:
        enen_X, enen_Y, enen_XY = entropy_ensemble(matrix_XY, sepp_x, sepp_y, int(quantity_xy[0]), int(quantity_xy[1]))
        result.append(f"H(X) = {enen_X}, H(Y) = {enen_Y}, H(XY) = {enen_XY}")
        result.append("-------------------------------------")
        pce_hxy, pce_hyx = partial_conditional_entropies(sepp_x, sepp_y, prob_x, prob_y, int(quantity_xy[0]),
                                                         int(quantity_xy[1]))
        result.append(f"Hx(Y) = {pce_hxy}, Hy(X) = {pce_hyx}")

    return result


def clicked():
    lbl4 = Label(window)
    lbl4.grid(column=0, row=5)

    res = logical(int(txtX.get()), int(txtY.get()), txtXY.get())

    for i in range(len(res)):
        print(res[i])
        lbl4 = Label(window)
        lbl4.grid(column=0, row=5 + i)
        lbl4.configure(text=res[i])


if __name__ == '__main__':
    window = Tk()
    window.title("Добро пожаловать в калькулятор вероятности и энропии")
    window.geometry('700x800')

    lbl1 = Label(window, text="Введите максимальное кол-во x: ")
    lbl1.grid(column=0, row=0)
    txtX = Entry(window, width=10)
    txtX.grid(column=1, row=0)

    lbl2 = Label(window, text="Введите максимальное кол-во y: ")
    lbl2.grid(column=0, row=1)
    txtY = Entry(window, width=10)
    txtY.grid(column=1, row=1)

    lbl3 = Label(window, text="Введите значения произведения ансамбля (Пример: x1y1 x1y2 x2y1 x2y2)")
    lbl3.grid(column=0, row=2)
    txtXY = Entry(window, width=100)
    txtXY.grid(column=0, row=3)

    btn = Button(window, text="Выполнить", command=clicked)
    btn.grid(column=0, row=4)
    window.mainloop()


