FILENAME_IN 		= './trainers.csv'
FILENAME_OUT 		= './trainers.txt'
DATASTARTLINENUM = 3

def load_data():
	fin = open(FILENAME_IN, mode='r', encoding='utf-8')
	linenum = 0

	data_dict = {}
	errors = []

	curr_name = ''
	curr_battleno = 0
	for line in fin:
		linenum += 1 # first line of CSV is line 1, so we can add to linenum here
		if linenum < DATASTARTLINENUM:
			continue

		spline = line.split(',')
		spline[-1] = spline[-1].strip('\n')
		data_line = []
		for col in spline:
			col = col.replace('\\\\', '\\')
			if col != '' and col[-1] == '"':
				data_line[-1] += col
				data_line[-1] = data_line[-1].strip('"')
			else:
				data_line.append(col)
		
		if data_line[0] == 'TRAINER':
			curr_name = data_line[4]
			curr_battleno = int(data_line[5]) if data_line[5] != '' else 0
			if not curr_name in data_dict:
				data_dict[curr_name] = {}
			data_dict[curr_name][curr_battleno] = dict( # one entry per battle #
				trainer_type 	= data_line[3],
				lose_text 		= data_line[6],
				items 			= data_line[7], # in the form "item|item|item" or just "item"
				skill 			= data_line[8],
				pokemon 		= []
			)

			if data_line[3] == '' or data_line[6] == '':
				errors.append((linenum, 'trainer without type or lose text'))

		elif data_line[0] == 'POKEMON':
			data_dict[curr_name][curr_battleno]['pokemon'].append(dict(
				species 		= data_line[10],
				level 			= data_line[11],
				moves 			= data_line[12], # in the form "move|move|move" or just "move"
				ability 		= data_line[13],
				item 			= data_line[14],
				ivs 			= data_line[15], # in the form 0|0|0|0|0|0
				ball 			= data_line[16]
			))

			if data_line[10] == '' or data_line[11] == '':
				errors.append((linenum, 'pokemon without species/name or level'))

		else:
			errors.append((linenum, 'column A not trainer or pokemon'))

	fin.close()

	return data_dict, errors


def export_data(data_dict):
	BATTLE_DELIM = '#-------------------------------\n'

	fin = open(FILENAME_OUT, mode='w')

	for name in data_dict:
		for battle_no in data_dict[name]:
			fin.write(BATTLE_DELIM)

			battle_data = data_dict[name][battle_no]

			if battle_no == 0:
				fin.write('[%s,%s]\n' % (battle_data['trainer_type'], name))
			else:
				fin.write('[%s,%s,%s]\n' % (battle_data['trainer_type'], name, battle_no))
			if battle_data['items'] != '':
				fin.write('Items = %s\n' % (','.join(battle_data['items'].split('|'))))
			fin.write('LoseText = %s\n' % battle_data['lose_text'])
			if battle_data['skill'] != '':
				fin.write('SkillLevel = %s\n' % battle_data['skill'])

			for pokemon in battle_data['pokemon']:
				fin.write('Pokemon = %s,%s\n' % (pokemon['species'], pokemon['level']))
				if pokemon['moves'] != '':
					fin.write('    Moves = %s\n' % (','.join(pokemon['moves'].split('|'))))
				if pokemon['ability'] != '':
					fin.write('    AbilityIndex = %s\n' % pokemon['ability'])
				if pokemon['item'] != '':
					fin.write('    Item = %s\n' % pokemon['item'])
				if pokemon['ball'] != '':
					fin.write('    Ball = %s\n' % pokemon['ball'])
				if pokemon['ivs'] != '':
					fin.write('    IV = %s\n' % (','.join(pokemon['ivs'].split('|'))))

	fin.close()



if __name__=='__main__':
	data_dict, errors = load_data()
	if len(errors) > 0:
		print('---- Errors ----')
		for line in errors:
			print(line)
		quit()
	else:
		export_data(data_dict)
		print('exporting complete -> %s' % FILENAME_OUT)