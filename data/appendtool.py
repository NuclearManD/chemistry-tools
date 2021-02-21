
import json

with open("reactions.json") as f:
	reactions = json.load(f)

with open("chemicals.json") as f:
	chemicals = json.load(f)


def getList(text):
	li = []
	while True:
		inp = input(text + ' (empty line to end list) > ')
		if inp == '':
			break
		else:
			li.append(inp)

	return li

def getFloatOrNone(text):
	inp = input(text + ' (or blank if none or unknown) > ')
	if inp == '':
		return None
	else:
		return float(inp)

def chemLookup(query):
	oquery = query
	query = query.lower()

	for k, v in chemicals.items():
		name = v['name'].lower()
		form = v['formula'].lower()

		if name == query:
			return k

		if form == query:
			return k

	raise KeyError(f"No chemical matches '{oquery}'")

def getChemOrNone(text):
	inp = input(text + ' (or blank if none or unknown) > ')
	if inp == '':
		return None
	return chemLookup(inp)

def processChemList(chemlist):
	outli = {}

	for text in chemlist:
		split = [i.strip() for i in text.split(',')]
		if len(split) < 2:
			raise Exception("Need at least 2 items in each reactant and each product: (name,quantity)")

		qty = int(split[1])
		if len(split) >= 3:
			state = split[2]
		else:
			state = ''

		# Look up the chemical.  Check formulas and CAS numbers too
		cas_number = chemLookup(split[0])

		# YES, this will add a space potentially between a quantity and an empty state.
		# This will make parsing the file easier later when we do [some str].split(' ')
		# because we will be expecting a space to be present.
		outli[cas_number] = str(qty) + ' ' + state

	return outli


if __name__ == '__main__':
	# This simple program allows easier addition of reactions to the list of reactions

	try:
		while True:
			reactants = getList("reactant: name,qty,state")
			products = getList("product: name,qty,state")

			min_temp = getFloatOrNone('Minimum temperature (C)')
			max_temp = getFloatOrNone('Maximum temperature (C)')
			energy = getFloatOrNone('Energy released, Joules')
			catalyst = getChemOrNone('Catalyst')
			voltage = getFloatOrNone('Electrolysis Voltage')

			obj = {
				'reactants': processChemList(reactants),
				'products': processChemList(products),
				'min_temperature': min_temp,
				'max_temperature': max_temp,
				'energy_delta_joules': energy
			}

			if catalyst is not None:
				obj['catalyst'] = catalyst

			if voltage is not None:
				obj['voltage'] = voltage

			reactions.append(obj)

			print("Added to cache.  Kill program by typing Ctrl-C to write to disk.")
			print()

	except KeyboardInterrupt:
		print("[Interrupted]")

	if not input("Save data? [Y/n]").lower().startswith('n'):

		# Serialize the data first, so we can avoid overwriting the file before discovering a problem
		reactions_data = json.dumps(reactions, indent='\t')
		with open("reactions.json", 'w') as f:
			f.write(reactions_data)
