# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 23:11:46 2022

@author: Matthieu Nougaret

This script groups together different functions that are not related to
specific subject as the other.
"""

def KamaProduction(minerai_inf, quanti):
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
	Kamas : int
		Quantity of kama producted.

	"""
	Minerals = {'Iron_2':150, 'Copper':240, 'Silex':330, 'Zinc':420,
				'Korail':510, 'Sandstone':600, 'Titan_S':9000, 'Saphire':690,
				'Carbone_S':9800, 'Mercury_S':16000, 'Carbone':780,
				'Obsidienne':11400}
	if minerai_inf == 'Iron':
		Kamas = quanti*50

	elif minerai_inf != 'Fer' :
		minerai_use = Minerals[minerai_inf]
		Kamas = int(quanti/5)*minerai_use

	else :
		Kamas = 0
		print("This  does not exist or is not implemented yet")

	return Kamas




