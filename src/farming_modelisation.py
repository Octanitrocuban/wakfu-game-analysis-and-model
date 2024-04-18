# -*- coding: utf-8 -*-
"""
These functions are to be used for predicting (with error due to the random
nature of the game mechanic of the agriculture).

To get the harvest probability density fuction, I made the list of the number
of clover seed that I get at each plants. This list is saved on the file :
"harvest_data.txt". It have 240 values.
For the:
	- no buff column there is a mean of 1.99583, a median of 2, and the
	following distribution : {'1':0.35833333, '2':0.2875, '3':0.35416667}.
	- seal of the companions (+50%) column there is a mean of 3.145833, a
	median of 3, and the following distribution : {'1':0.133333, '2':0.195833,
   '3':0.291666, '4':0.15, '5':0.229166}.
Be aware that this code does not at this time include the Capt'Chat encounter.
This come frome that I still haven't found the apparition rate. What I can say
from now is that it is in game at least since the 21 april 2014 (1). I
encounter 11 of them during the making of the "harvest_data.txt" file.

In this code, 'plants' refer to the elements harvested by the herbalist and
peasant professions. It is in oppsition of 'trees' which refers to the
elements harvested by the forestry profession.

For the farm of trees, this code have a strong assumption on the map
organisation witch is that they are set in order to give the possibility for
the player to access at every tree freely.

This code does not hav any licence.

(1) https://www.wakfu.com/fr/mmorpg/actualites/maj/421463-pandora/details
"""
import numpy as np
#=============================================================================
def planting_stage(nb_free, nb_seed, proba):
	"""
	Simulates trying to fill a N-box card with plants.

	Parameters
	----------
	nb_free : int
		Number of free cards/cells on the map that we want to fill whith
		plants or trees. Nbfree have to be superior to 0.
	nb_seed : int
		Number of seeds are cuts possessed by the player.
	proba : float
		Plant succes probability in per centage (0 to 1).

	Returns
	-------
	nb_free : int
		Number of free cards/cells on the map that we want to fill whith
		plants.
	nb_seed : int
		Number of seeds or cuts possessed by the player.
	plan_reu : int
		Number of successful seedling.

	"""
	plan_reu = 0
	while (nb_free > 0)&(nb_seed > 0):
		reu = np.random.random(1)
		if reu <= proba:
			nb_free -= 1
			nb_seed -= 1
			plan_reu += 1
		else:
			nb_seed -= 1

	return nb_free, nb_seed, plan_reu

def harvest_plants_stage(n_plants, seeds, get_seeds, harvest_buf=0):
	"""
	Simulate the harvest stage with a map fill with N_plants.

	Parameters
	----------
	n_plants : int
		Number of plants on the map.
	seeds : int
		Number of seeds at start.
	get_seeds : int
		Minimum number of seeds owned. If NSeeds <= GetSeeds the seeds will
		also be gathered.
	harvest_buf : int|float, optional
		Buff that increase the harvest. The default is 0 witch mean that there
		aren't any buff.

	Returns
	-------
	seed_gather : int
		Number of seeds collected.
	ressources : int
		Number of plant collected.

	"""
	seed_gather = np.zeros(n_plants)
	ressources = np.zeros(n_plants)
	for i in range(n_plants):
		if seeds+np.sum(seed_gather) <= get_seeds:
			seed_gather[i] = int((harvest_buf+1)*np.random.uniform(1, 4))

		ressources[i] = int((harvest_buf+1)*np.random.uniform(1, 4))

	seed_gather = np.sum(seed_gather)
	ressources = np.sum(ressources)
	return seed_gather, ressources

def crop_cycle(n_seeds, free_cells, n_cycle, get_seeds, proba, harvest_buf=0,
			  verbose=False):
	"""
	Simulate the farm of plants ressources.

	Parameters
	----------
	n_seeds : int
		Number of seeds at start.
	free_cells : int
		Number of usable cell on the map.
	n_cycle : int
		Number of crop cyle that what to be done. One crop cycle consists in
		a planting stage followed by a harvest stage.
	get_seeds : int
		Minimum number of seeds owned. If n_seeds <= get_seeds the seeds will
		also be gathered.
	proba : float
		Probability of successful seeding. Must be in the interval [0, 1].
	harvest_buf : float, optional
		Yield as a percentage of the harvest rate. The default is 0. Must be
		in the interval [0, 1].
	verbose : bool
		Is the function is talkative.

	Returns
	-------
	seeds : int
		Number of seeds in the player pocket.
	plante_vecteur : np.ndarray
		Array that countain the plant pieces (resources) harvested at each
		harvest stage.
	cycl : int
		Number of crop cycle performed.

	"""
	plante_vecteur = []
	tot_cells = free_cells
	free_cells, seeds, plantes = planting_stage(free_cells, n_seeds, proba)
	gath_seeds, ressources = harvest_plants_stage(plantes, seeds, get_seeds,
											 harvest_buf)

	free_cells = tot_cells
	seeds = seeds + gath_seeds
	plante_vecteur.append(ressources)
	if verbose:
		print("E1 : {all ressources:", np.sum(plante_vecteur), ". Seeds:",
		seeds, "}")

	cycl = 1
	while (cycl != n_cycle)&(seeds > 0):
		cycl += 1
		free_cells, seeds, plantes = planting_stage(free_cells, seeds, proba)
		gath_seeds, ressources = harvest_plants_stage(plantes, seeds, get_seeds,
											  harvest_buf)

		plantes = 0
		free_cells = tot_cells
		seeds = seeds + gath_seeds
		plante_vecteur.append(ressources)
		if verbose:
			print("E"+str(cycl)+" : {all ressources:", np.sum(plante_vecteur),
			 ". Seeds", seeds, "}")

	plante_vecteur = np.array(plante_vecteur)
	return seeds, plante_vecteur, cycl

def harvest_tree_stage(trees, cuts, free_cell, min_cuts, harvest_buf=0):
	"""
	Simulates the gathering of a (partialy) filled box of n cells with trees.

	Parameters
	----------
	trees : int
		Number of trees on the map.
	cuts : int
		Number of 'baby tree'.
	free_cell : int
		Number of free cell on the map.
	min_cuts : int
		Minimum number of 'baby tree' owned. If cuts <= min_cuts the seeds will
		also be gathered.
	harvest_buf : int|float, optional
		Yield as a percentage of the harvest rate. The default is 0. Must be
		in the interval [0, 1].

	Returns
	-------
	trees : int
		Number of trees on the map.
	cuts : int
		Number of 'baby tree'.
	free_cell : int
		Number of free cell on the map.
	ressources : int
		Number of the log of wood gathered.

	"""
	ressources = 0
	for i in range(trees):
		if cuts <= min_cuts:
			cuts += int(1+harvest_buf)*np.random.uniform(1, 4)
			if cuts <= min_cuts:
				cuts += int(1+harvest_buf)*np.random.uniform(1, 4)

		else:
			ressources += int(1+harvest_buf)*np.random.uniform(1, 4)
			trees -= 1
			free_cell += 1

	return trees, cuts, free_cell, ressources

def forestery_cycle(n_cuts, free_cell, n_cycle, GetCuts, proba, 
					harvest_buf=0, verbose=False):
	"""
	Simulate the farm of trees ressources.

	Parameters
	----------
	n_cuts : int
		Number of cutting|saplings at the start.
	free_cell : int
		Number of cell on the map that can be used for the farming.
	n_cycle : int
		Number of cyle that want to be done. One cycle consists in a planting
		stage followed by a forestery stage.
	get_cuts : int
		Minimum number of 'baby tree' owned. If cuts <= min_cuts the seeds will
		also be gathered.
	proba : int|float
		Probability of successful seeding. Must be in the interval [0, 1].
	harvest_buf : int|float, optional
		Yield as a percentage of the forestery rate. The default is 0. Must be
		in the interval [0, 1].
	verbose : bool
		Is the function is talkative.

	Returns
	-------
	cuts : int
		Number of cutting|saplings at the start.
	tree_vector : np.ndarray
		Array that countain the log of wood (resources) harvested at each
		forestery stage.
	cyc : int
		Number of crop cycle performed.

	"""
	tree_vector = []
	cyc = 1
	tot_cell = free_cell
	free_cells, cuts, trees = planting_stage(free_cell, n_cuts, proba)
	trees, cuts, free_cell, ressources = harvest_tree_stage(trees, n_cuts,
															free_cell,
															get_cuts,
															harvest_buf)

	tree_vector.append(ressources)
	if verbose:
		print("E1 : {all ressources:", np.sum(tree_vector), ". Seeds:",
			  cuts, "}")

	while (cyc < n_cycle)|((cuts <= 0)&(free_cell >= tot_cell)):
		free_cells, cuts, trees = planting_stage(free_cell, cuts, proba)
		trees, cuts, free_cell, ressources = harvest_tree_stage(trees,
													cuts, free_cell,
													get_cuts, harvest_buf)

		tree_vector.append(ressources)
		if verbose:
			print("E"+str(cyc)+" : {all ressources:", np.sum(tree_vector),
			 ". 'Baby trees'", cuts, "}")

	tree_vector = np.array(tree_vector)
	return cuts, tree_vector, cyc

