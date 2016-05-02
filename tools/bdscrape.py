#!/usr/bin/env python3

import requests
import re
import html.parser
import roman
import collections

s = requests.session()
s.headers.update({
	'User-Agent': ''	
})

parser = html.parser.HTMLParser()

bold_pattern = re.compile('<b>(.+)</b>')
skill_number_pattern = re.compile('_(\d+|M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))$')

def main():
	classes = {
		'Warrior': 'warrior',
		'Ranger': 'ranger',
		'Sorceress': 'sorcerer',
		'Berserker': 'giant',
		'Tamer': 'tamer',
		'Musa': 'blademaster',
		'Valkyrie': 'valkyrie',
		'Witch': 'wizard',
		'Ninja': 'ninja',
		'All': 'common',
	}
	classes = collections.OrderedDict(sorted(classes.items()))

	f = open('Skills.lua', 'w')
	f.write('EdanSkills.RegisterSkills({\n\n')

	idToLevel = {}
	for cls,bdcls in classes.items():
		data = get_skills(bdcls)
		skillsToList = {}

		for name, name_without_skill_number, id, skillnumber in reversed(data):
			skills = skillsToList.get(name_without_skill_number)
			if skills is None:
				skillsToList[name_without_skill_number] = [str(id)]
			else:
				skillsToList[name_without_skill_number].append(str(id))
			idToLevel[id] = skillnumber

		skillsToList = collections.OrderedDict(sorted(skillsToList.items()))
		for k,v in skillsToList.items():
			f.write('{"%s_%s", {%s}},\n' % (cls.upper(), k,','.join(v)))
		f.write('\n')

	f.write('})\n\n')

	f.write('EdanSkills.IdLevels = {\n')
	for id,level in idToLevel.items():
		f.write('[%i] = %i,\n' % (id, level or 1))
	f.write('}\n')

	f.close()

def get_skills(cls):
	r = s.get('http://bddatabase.net/query.php?a=skills&type=%s&l=us' % cls)
	
	data = []
	for entry in r.json()['aaData']:
		id = int(entry[0])
		original_name = bold_pattern.search(entry[2]).group(1)
		level = int(entry[3])

		name = parser.unescape(original_name).strip()
		name = name \
			.replace(': ', '_') \
			.replace(' - ', "_") \
			.replace("'", "") \
			.replace(' ', "_") \
			.upper()

		name = re.sub(r'[^a-zA-Z\d\s_]', '', name)

		skill_number_match = skill_number_pattern.search(name)
		if skill_number_match:
			skill_number = skill_number_match.group()[1:]
			try:
				skill_number = int(skill_number)
			except:
				try:
					skill_number = roman.fromRoman(skill_number)
				except:
					print(repr(original_name))
					raise
			name_without_skill_number = name[:-(skill_number_match.end() - skill_number_match.start())]
		else:
			skill_number = None
			name_without_skill_number = name

		print('%s id %i skillnumber %s' % (name_without_skill_number.encode('cp850', errors='replace'), id, skill_number))
		data.append([name, name_without_skill_number, id, skill_number])

	return data

main()