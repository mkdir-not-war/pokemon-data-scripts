FILENAME_IN 		= './encounters.csv'
FILENAME_OUT 		= './encounters.txt'
MAPIDS_IN			= './mapids.dat'
TERRAINFREQS_IN	 	= './terrainfreqs.dat'
DATASTARTLINENUM = 3

def load_data():
	data_dict = {}
	errors = []

	# load map ids
	fin = open(MAPIDS_IN, mode='r')
	data_dict['mapids'] = {}
	for line in fin:
		mapname, mapid = line.strip('\n').split(',')
		data_dict['mapids'][mapname] = mapid
	fin.close()

	print(data_dict)

	# load terrain encounter frequencies
	fin = open(TERRAINFREQS_IN, mode='r')
	data_dict['terrainfreqs'] = {}
	for line in fin:
		terraintag, freq = line.strip('\n').split(',')
		data_dict['terrainfreqs'][terraintag] = freq
	fin.close()

	# load pokemon encounters
	fin = open(FILENAME_IN, mode='r')
	data_dict['encounters'] = {}
	linenum = 0

	for line in fin:
		linenum += 1 # first line of CSV is line 1, so we can add to linenum here
		if linenum < DATASTARTLINENUM:
			continue

		data_line = line.strip('\n').split(',')
		route = data_line[0]
		ttag = data_line[1]

		if not route in data_dict['encounters']:
			data_dict['encounters'][route] = {}
		if not ttag in data_dict['encounters'][route]:
			data_dict['encounters'][route][ttag] = []

		data_dict['encounters'][route][ttag].append(dict(
			pokemon = data_line[3],
			percentage = data_line[2],
			minlvl = data_line[4],
			maxlvl = None if len(data_line) < 6 else data_line[5]
		))

	fin.close()

	return data_dict, errors


def export_data(data_dict):
	ROUTE_DELIM = '#-------------------------------\n'

	fin = open(FILENAME_OUT, mode='w')

	for route in data_dict['encounters']:
		fin.write(ROUTE_DELIM)
		fin.write('[%.3d] # %s\n' % (int(data_dict['mapids'][route.upper()]), route))

		for ttag in data_dict['encounters'][route]:
			if ttag in data_dict['terrainfreqs']:
				fin.write('%s,%s\n' % (ttag, data_dict['terrainfreqs'][ttag]))
			else:
				fin.write('%s\n' % ttag)

			for enc_data in data_dict['encounters'][route][ttag]:
				print(enc_data)
				if enc_data['maxlvl'] != '':
					fin.write('    %s,%s,%s,%s\n' % \
						(enc_data['percentage'], enc_data['pokemon'], enc_data['minlvl'], enc_data['maxlvl']))
				else:
					fin.write('    %s,%s,%s\n' % \
						(enc_data['percentage'], enc_data['pokemon'], enc_data['minlvl']))
			
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