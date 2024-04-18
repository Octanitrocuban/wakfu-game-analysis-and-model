# -*- coding: utf-8 -*-
"""
This script groups together different functions that are not related to
specific subject as the other.
"""

def kama_production(minerai_inf, quanti):
	"""
	Calculate how much would give the craft recipes of kamas.

	Parameters
	----------
	minerai_inf : str
		Name of name of the lowest ressources in level.
	quanti : int
		Number of ressources of the lowest ressources in level.

	Returns
	-------
	kamas : int
		Quantity of kama producted.

	"""
	minerals = {'Iron_2':150, 'Copper':240, 'Silex':330, 'Zinc':420,
				'Korail':510, 'Sandstone':600, 'Titan_S':9000, 'Saphire':690,
				'Carbone_S':9800, 'Mercury_S':16000, 'Carbone':780,
				'Obsidienne':11400}
	if minerai_inf == 'Iron':
		kamas = quanti*50

	elif minerai_inf != 'Fer' :
		minerai_use = minerals[minerai_inf]
		kamas = int(quanti/5)*minerai_use

	else :
		kamas = 0
		print("This  does not exist or is not implemented yet")

	return kamas




