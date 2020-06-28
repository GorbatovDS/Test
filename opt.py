# -*- coding: UTF-8 -*-
import numpy as np


# Функция нахождения минимального элемента, исключая текущий элемент
def Min(lst, myindex):
    return min(x for idx, x in enumerate(lst) if idx != myindex)


# функция удаления нужной строки и столбцах
def Delete(matrix, index1, index2):
    del matrix[index1]
    for i in matrix:
        del i[index2]
    return matrix


# Функция вывода матрицы
def PrintMatrix(matrix):
    print("---------------")
    for i in range(len(matrix)):
        print(matrix[i])
    print("---------------")


# Вычитаем минимальный элемент из строк и столбцов
# Считаем нижнюю границу
def Reducing(matrix, H):
    for i in range(len(matrix)):
        temp = min(matrix[i])
        H += temp
        for j in range(len(matrix)):
            matrix[i][j] -= temp

    for i in range(len(matrix)):
        temp = min(row[i] for row in matrix)
        H += temp
        for j in range(len(matrix)):
            matrix[j][i] -= temp
    return matrix, H


def Little2(matrix, flag=None):
    NullMax = 0
    index1 = 0
    index2 = 0
    tmp = 0
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 0:
                tmp = Min(matrix[i], j) + Min((row[j] for row in matrix), i)
                if tmp >= NullMax:
                    NullMax = tmp
                    index1 = i
                    index2 = j
    return index1, index2


def Cikl(matrix, H, flag=None):
    # print("---------------")
    # print(Str)
    # print(Stb)
    # PrintMatrix(matrix)
    # print("---------------")
    if (len(matrix) == 2) or (len(matrix) == 1):
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                try:
                    if matrix[i][j] != float('inf'):
                        res.append(Str[i] + 1)
                        res.append(Stb[j] + 1)
                        del Str[i]
                        del Stb[j]
                        Delete(matrix, i, j)
                        res.append(Str[0] + 1)
                        res.append(Stb[0] + 1)
                        del Str[0]
                        del Stb[0]
                        return
                except:
                    break

        if len(matrix) == 1:
            res.append(Str[0] + 1)
            res.append(Stb[0] + 1)
            del Str[0]
            del Stb[0]
            return
    id1, id2, = Little2(matrix, flag)
    MatrixWo = []
    for i in range(len(matrix)):
        MatrixWo.append(matrix[i].copy())
    MatrixWo[id1][id2] = float('inf')
    oldIndex1 = Str[id1]
    oldIndex2 = Stb[id2]
    if oldIndex2 in Str and oldIndex1 in Stb:
        NewIndex1 = Str.index(oldIndex2)
        NewIndex2 = Stb.index(oldIndex1)
    elif oldIndex1 not in Stb and oldIndex2 in Str:
        while oldIndex1 not in Stb:
            for i in range(1,len(res),2):

                if oldIndex1 == res[i]-1:
                    oldIndex1 = res[i-1]-1
        NewIndex1 = Str.index(oldIndex2)
        NewIndex2 = Stb.index(oldIndex1)
    elif oldIndex2 not in Str and oldIndex1 in Stb:
        while oldIndex2 not in Str:
            for i in range(0,len(res), 2):
                if oldIndex2 == res[i]-1:
                    oldIndex2 = res[i+1]-1
        NewIndex1 = Str.index(oldIndex2)
        NewIndex2 = Stb.index(oldIndex1)
    elif oldIndex2 not in Str and oldIndex1 not in Stb:
        while oldIndex2 not in Str:
            for i in range(0, len(res), 2):
                if oldIndex2 == res[i] - 1:
                    oldIndex2 = res[i + 1] - 1
        while oldIndex1 not in Stb:
            for i in range(1,len(res),2):

                if oldIndex1 == res[i]-1:
                    oldIndex1 = res[i-1]-1
        NewIndex1 = Str.index(oldIndex2)
        NewIndex2 = Stb.index(oldIndex1)
    Hy = H+9999999
    matrix[NewIndex1][NewIndex2] = float('inf')
    matrix = Delete(matrix, id1, id2)
    matrix, H = Reducing(matrix, H)
    MatrixWo, Hy = Reducing(MatrixWo, Hy)
    if Hy < H:
        matrix = []
        for i in range(len(MatrixWo)):
            matrix.append(MatrixWo[i].copy())

        return Cikl(matrix, Hy)
    elif Hy >= H:
        res.append(Str[id1] + 1)
        res.append(Stb[id2] + 1)
        del Str[id1]
        del Stb[id2]

        return Cikl(matrix, H)


def main(name: str):
    matrix = []
    # Вводим размерность и матрицу
    with open(name, 'r') as f:
        n = int(f.readline())
        for i in range(n):
            matrix.append(list(map(int, f.readline().strip().split())))
        day = f.readline().strip()
        reindex = eval(f.readline())
    H = 0
    Hy = 0
    PathLenght = 0
    global Str
    global Stb
    global res
    Str=[]
    Stb=[]
    res = []
    result = []
    StartMatrix = []
    flag = 1

    # Инициализируем массивы для сохранения индексов
    for i in range(n):
        Str.append(i)
        Stb.append(i)

    # Сохраняем изначальную матрицу
    for i in range(n):
        StartMatrix.append(matrix[i].copy())

    # Присваеваем главной диагонали float(inf)
    for i in range(n):
        matrix[i][i] = float('inf')
    # PrintMatrix(matrix)

    matrix, H = Reducing(matrix, H)
    Cikl(matrix, H, flag)

    for i in range(0, len(res) - 1, 2):
        if res[i] == 1:
            result.append(res[i])
            result.append(res[i+1])
    while len(result) < len(res) and result[len(result)-1] !=1:
        for i in range(0, len(res) - 1, 2):
            if res[i] == result[len(result)-1] and result[len(result)-1] != 1:
                result.append(res[i])
                result.append(res[i+1])
            elif result[len(result)-1] == 1:
                break
    # print(result)

    # Считаем длину пути
    for i in range(0, len(result) - 1, 2):
        if i == len(result) - 2:
            PathLenght += StartMatrix[result[i]-1][result[i+1]-1]
        else:
            PathLenght += StartMatrix[result[i] - 1][result[i + 1] - 1]

    # print(PathLenght)
    tuple_result = list()
    for r in np.arange(0, len(result) - 1, step=2):
        tuple_result.append((result[r], result[r + 1]))

    return tuple_result, PathLenght, day, reindex


if __name__ == '__main__':
    # print('>>>>>>>>>begin<<<<<<<<<<<<<<<<')
    print(main('buffer.txt'))
    # print('>>>>>>>>>end<<<<<<<<<<<<<<<<<<')

'''
import numpy as np

# Функция нахождения минимального элемента, исключая текущий элемент
def Min(lst, myindex):
	return min(x for idx, x in enumerate(lst) if idx != myindex)


# функция удаления нужной строки и столбцах
def Delete(matrix, index1, index2):
	del matrix[index1]
	for i in matrix:
		del i[index2]
	return matrix


# Функция вывода матрицы
def PrintMatrix(matrix):
	print("---------------")
	for i in range(len(matrix)):
		print(matrix[i])
	print("---------------")


# Вычитаем минимальный элемент из строк и столбцов
# Считаем нижнюю границу
def Reducing(matrix, H):
	for i in range(len(matrix)):
		temp = min(matrix[i])
		H += temp
		for j in range(len(matrix)):
			matrix[i][j] -= temp

	for i in range(len(matrix)):
		temp = min(row[i] for row in matrix)
		H += temp
		for j in range(len(matrix)):
			matrix[j][i] -= temp
	return matrix, H


def Little2(matrix):
	NullMax = 0
	index1 = 0
	index2 = 0
	tmp = 0
	for i in range(len(matrix)):
		for j in range(len(matrix)):
			if matrix[i][j] == 0:
				tmp = Min(matrix[i], j) + Min((row[j] for row in matrix), i)
				if tmp >= NullMax:
					NullMax = tmp
					index1 = i
					index2 = j
	return index1, index2


def Cikl(matrix, H):
	if len(matrix) == 2:
		for i in range(len(matrix)):
			for j in range(len(matrix)):
				try:
					if (matrix[i][j] != float('inf')):
						res.append(Str[i] + 1)
						res.append(Stb[j] + 1)
						Delete(matrix,i,j)
				except:
					break

		# print(res)
		return
	id1, id2, = Little2(matrix)
	MatrixWo = []
	for i in range(len(matrix)):
		MatrixWo.append(matrix[i].copy())
	MatrixWo[id1][id2] = float('inf')
	oldIndex1 = Str[id1]
	oldIndex2 = Stb[id2]
	if oldIndex2 in Str and oldIndex1 in Stb:
		NewIndex1 = Str.index(oldIndex2)
		NewIndex2 = Stb.index(oldIndex1)
	elif oldIndex1 not in Stb and oldIndex2 in Str:
		while oldIndex1 not in Stb:
			for i in range(1,len(res),2):

				if oldIndex1 == res[i]-1:
					oldIndex1 = res[i-1]-1
		NewIndex1 = Str.index(oldIndex2)
		NewIndex2 = Stb.index(oldIndex1)
	elif oldIndex2 not in Str and oldIndex1 in Stb:
		while oldIndex2 not in Str:
			for i in range(0,len(res), 2):
				if oldIndex2 == res[i]-1:
					oldIndex2 = res[i+1]-1
		NewIndex1 = Str.index(oldIndex2)
		NewIndex2 = Stb.index(oldIndex1)
	elif oldIndex2 not in Str and oldIndex1 not in Stb:
		while oldIndex2 not in Str:
			for i in range(0, len(res), 2):
				if oldIndex2 == res[i] - 1:
					oldIndex2 = res[i + 1] - 1
		while oldIndex1 not in Stb:
			for i in range(1,len(res),2):

				if oldIndex1 == res[i]-1:
					oldIndex1 = res[i-1]-1
		NewIndex1 = Str.index(oldIndex2)
		NewIndex2 = Stb.index(oldIndex1)
	Hy = H+99999999
	matrix[NewIndex1][NewIndex2] = float('inf')
	matrix = Delete(matrix, id1, id2)
	matrix, H = Reducing(matrix, H)
	MatrixWo, Hy = Reducing(MatrixWo, Hy)
	if Hy < H:
		matrix = []
		for i in range(len(MatrixWo)):
			matrix.append(MatrixWo[i].copy())

		return Cikl(matrix, Hy)
	elif Hy >= H:
		res.append(Str[id1] + 1)
		res.append(Stb[id2] + 1)
		del Str[id1]
		del Stb[id2]

		return Cikl(matrix, H)


def main(fileName):
	# Вводим размерность и матрицу
	with open(fileName) as f:
		n = int(f.readline())
		matrix = [list(map(int, row.split())) for row in f.readlines()]
	H = 0
	Hy = 0
	PathLenght = 0
	global Str
	global Stb
	global res
	Str = []
	Stb = []
	res = []
	result = []
	StartMatrix = []

	# Инициализируем массивы для сохранения индексов
	for i in range(n):
		Str.append(i)
		Stb.append(i)


	# Сохраняем изначальную матрицу
	for i in range(n):
		StartMatrix.append(matrix[i].copy())

	# Присваеваем главной диагонали float(inf)
	for i in range(n):
		matrix[i][i] = float('inf')
	# PrintMatrix(matrix)

	matrix, H = Reducing(matrix, H)
	Cikl(matrix, H)

	# Формируем порядок пути
	for i in range(0, len(res) - 1, 2):
		if res.count(res[i]) < 2:
			result.append(res[i])
			result.append(res[i + 1])
	for i in range(0, len(res) - 1, 2):
		for j in range(0, len(res) - 1, 2):
			if result[len(result) - 1] == res[j]:
				result.append(res[j])
				result.append(res[j + 1])
	result.append(result[-1])
	result.append(result[0])
	# print("----------------------------------")
	# print(result)

	# Считаем длину пути
	for i in range(0, len(result) - 1, 2):
		if i == len(result) - 2:
			PathLenght += StartMatrix[result[i] - 1][result[i + 1] - 1]
		else:
			PathLenght += StartMatrix[result[i] - 1][result[i + 1] - 1]

	tuple_result = list()
	for r in np.arange(0, len(result) - 1, step=2):
		tuple_result.append((result[r], result[r + 1]))

	# tuple_result = [(5, 2), (2, 3), (3, 1), (1, 4), (4, 5)]
	path_true = list()
	tuple_result.sort(key=lambda t: t[0])
	path_true.append(tuple_result[0])

	while len(path_true) != len(tuple_result):
		for branch in tuple_result:
			if path_true[-1][-1] == branch[0]:
				path_true.append(branch)

	print(path_true)

	return path_true, PathLenght


if __name__ == '__main__':
	print(main('SampleIn_1.txt'))
'''