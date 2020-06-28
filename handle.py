# -*- coding: UTF-8 -*-
import datetime
import opt


def main(name):
	output = list()
	day_number = datetime.date.today().weekday()
	day_day = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
	file = open(name, 'r')
	matrix_source = list()
	week_workhours = list()
	places_amount = int(file.readline())
	places_done = list()
	for i in range(places_amount):
		matrix_source.append(list(map(int, file.readline().strip().split())))

	file.readline()
	for i in range(places_amount - 1):
		week_workhours.append(list(map(int, file.readline().strip().split())))

	file.close()

	# Calling Little alg for whole matrix
	with open('buffer.txt', 'w') as file:
		file.write(str(places_amount) + '\n')
		to_write = str()
		for line in matrix_source:
			to_write = str()
			for number in line:
				to_write += ' ' + str(number)
			to_write += '\n'
			file.write(to_write)

		file.write('AllToday\n')
		to_write = '{ '
		for i in range(places_amount):
			to_write += str(i + 1) + ': ' + str(i + 1) + ', '
		to_write = to_write[0:-2]
		to_write += ' }'
		file.write(to_write)

	output.append(opt.main('buffer.txt'))

	# Calling Little alg depending on working hours
	while len(places_done) != places_amount - 1:
		file = open('buffer.txt', 'w')
		buffer_matrix = list()
		works_this_day = [0]
		for i in range(places_amount - 1):
			if week_workhours[i][day_number] == 1:
				if (i + 1) not in places_done:
					works_this_day.append(i + 1)
					places_done.append(i + 1)

		works_this_day.sort()
		if len(works_this_day) > 1:
			for j in works_this_day:
				a = list()
				for k in works_this_day:
					a.append(matrix_source[j][k])
				buffer_matrix.append(a)

			file.write(str(len(works_this_day)) + '\n')

			for line in buffer_matrix:
				to_write = str()
				for number in line:
					to_write += ' ' + str(number)
				to_write += '\n'
				file.write(to_write)

			file.write(day_day[day_number] + '\n')
			to_write = '{ '
			for i in range(len(works_this_day)):
				to_write += str(i + 1) + ': ' + str(works_this_day[i] + 1) + ', '
			to_write = to_write[0:-2]
			to_write += ' }'
			file.write(to_write)
			file.close()
			output.append(opt.main('buffer.txt'))

		day_number += 1
		if day_number == 7:
			day_number = 0

	file = open('Output.txt', 'w')

	file.write(str(len(output)) + '\n')
	for line in output:
		file.write(str(line[0]) + '\n')
		file.write(str(line[1]) + '\n')
		file.write(str(line[2]) + '\n')
		file.write(str(line[3]) + '\n')

	file.close()
	# print('Output.txt must be done')
