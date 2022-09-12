# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 14:39:00 2022

@author: Matthieu Nougaret

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
def planting_stage(Nbfree, NbSeed, pProb):
	"""
	Simulates trying to fill a N-box card with plants.

	Parameters
	----------
	Nbfree : int
		Number of free cards/cells on the map that we want to fill whith
		plants or trees. Nbfree have to be superior to 0.
	NbSeed : int
		Number of seeds are cuts possessed by the player.
	pProb : float
		Plant succes probability in per centage (0 to 1).

	Returns
	-------
	Nbfree : int
		Number of free cards/cells on the map that we want to fill whith
		plants.
	NbSeed : int
		Number of seeds or cuts possessed by the player.
	planReu : int
		Number of successful seedling.

	"""
	planReu = 0
	while (Nbfree > 0)&(NbSeed > 0):
		reu = np.random.random(1)
		if reu <= pProb:
			Nbfree -= 1
			NbSeed -= 1
			planReu += 1
		else :
			NbSeed -= 1
	return Nbfree, NbSeed, planReu

def harvest_plants_stage(N_plants, seeds, GetSeeds, harvest_buf=0):
	"""
	Simulate the harvest stage with a map fill with N_plants.

	Parameters
	----------
	N_plants : int
		Number of plants on the map.
	seeds : int
		Number of seeds at start.
	GetSeeds : int
		Minimum number of seeds owned. If NSeeds <= GetSeeds the seeds will
		also be gathered.
	harvest_buf : int|float, optional
		Buff that increase the harvest. The default is 0 witch mean that there
		aren't any buff.

	Returns
	-------
	SeedGather : int
		Number of seeds collected.
	Ressources : int
		Number of plant collected.

	"""
	SeedGather = np.zeros(N_plants)
	Ressources = np.zeros(N_plants)
	for i in range(N_plants):
		if seeds+np.sum(SeedGather) <= GetSeeds:
			SeedGather[i] = int((harvest_buf+1)*np.random.uniform(1, 4))
		Ressources[i] = int((harvest_buf+1)*np.random.uniform(1, 4))
	SeedGather = np.sum(SeedGather)
	Ressources = np.sum(Ressources)
	return SeedGather, Ressources

def CropCycle(NSeeds, FreeCells, NCycle, GetSeeds, pProb, harvest_buf=0,
			  verbose=False):
	"""
	Simulate the farm of plants ressources.

	Parameters
	----------
	NSeeds : int
		Number of seeds at start.
	FreeCells : int
		Number of usable cell on the map.
	NCycle : int
		Number of crop cyle that what to be done. One crop cycle consists in
		a planting stage followed by a harvest stage.
	GetSeeds : int
		Minimum number of seeds owned. If NSeeds <= GetSeeds the seeds will
		also be gathered.
	pProb : float
		Probability of successful seeding. Must be in the interval [0, 1].
	harvest_buf : float, optional
		Yield as a percentage of the harvest rate. The default is 0. Must be
		in the interval [0, 1].
	verbose : bool
		Is the function is talkative.

	Returns
	-------
	Seeds : int
		Number of seeds in the player pocket.
	PlanteVecteur : np.ndarray
		Array that countain the plant pieces (resources) harvested at each
		harvest stage.
	cycl : int
		Number of crop cycle performed.

	"""
	PlanteVecteur = []
	TotCells = FreeCells
	FreeCells, Seeds, Plans = planting_stage(FreeCells, NSeeds, pProb)
	GatSeeds, Ressources = harvest_plants_stage(Plans, Seeds, GetSeeds,
											 harvest_buf)
	FreeCells = TotCells
	Seeds = Seeds + GatSeeds
	PlanteVecteur.append(Ressources)
	if verbose:
		print("E1 : {all ressources:", np.sum(PlanteVecteur), ". Seeds:",
		Seeds)
	cycl = 1
	while (cycl != NCycle)&(Seeds > 0):
		cycl += 1
		FreeCells, Seeds, Plans = planting_stage(FreeCells, Seeds, pProb)
		GatSeeds, Ressources = harvest_plants_stage(Plans, Seeds, GetSeeds,
											  harvest_buf)
		Plans = 0
		FreeCells = TotCells
		Seeds = Seeds + GatSeeds
		PlanteVecteur.append(Ressources)
		if verbose:
			print("E"+str(cycl)+" : {all ressources:", np.sum(PlanteVecteur),
			 ". Seeds", Seeds)
	PlanteVecteur = np.array(PlanteVecteur)
	return Seeds, PlanteVecteur, cycl

def harvest_tree_stage(Trees, Cuts, FreeCell, MinCuts, harvest_buf=0):
	"""
	Simulates the gathering of a (partialy) filled box of n cells with trees.

	Parameters
	----------
	Trees : int
		Number of trees on the map.
	Cuts : int
		Number of 'baby tree'.
	FreeCell : int
		Number of free cell on the map.
	MinCuts : int
		Minimum number of 'baby tree' owned. If Cuts <= MinCuts the seeds will
		also be gathered.
	harvest_buf : int|float, optional
		Yield as a percentage of the harvest rate. The default is 0. Must be
		in the interval [0, 1].

	Returns
	-------
	Trees : int
		Number of trees on the map.
	Cuts : int
		Number of 'baby tree'.
	FreeCell : int
		Number of free cell on the map.
	Ressources : int
		Number of the log of wood gathered.

	"""
	Ressources = 0
	for i in range(Trees):
		if Cuts <= MinCuts:
			Cuts += int(1+harvest_buf)*np.random.uniform(1, 4)
			if Cuts <= MinCuts:
				Cuts += int(1+harvest_buf)*np.random.uniform(1, 4)
		else:
			Ressources += int(1+harvest_buf)*np.random.uniform(1, 4)
			Trees -= 1
			FreeCell += 1
	return Trees, Cuts, FreeCell, Ressources

def ForesteryCycle(Ncuts, FreeCell, NCycle, GetCuts, pProb, harvest_buf=0,
			  verbose=False):
	"""
	Simulate the farm of trees ressources.

	Parameters
	----------
	Ncuts : int
		Number of cutting|saplings at the start.
	FreeCell : int
		Number of cell on the map that can be used for the farming.
	NCycle : int
		Number of cyle that want to be done. One cycle consists in a planting
		stage followed by a forestery stage.
	GetCuts : int
		Minimum number of 'baby tree' owned. If Cuts <= MinCuts the seeds will
		also be gathered.
	pProb : int|float
		Probability of successful seeding. Must be in the interval [0, 1].
	harvest_buf : int|float, optional
		Yield as a percentage of the forestery rate. The default is 0. Must be
		in the interval [0, 1].
	verbose : bool
		Is the function is talkative.

	Returns
	-------
	Cuts : int
		Number of cutting|saplings at the start.
	TreeVector : np.ndarray
		Array that countain the log of wood (resources) harvested at each
		forestery stage.
	cyc : int
		Number of crop cycle performed.

	"""
	TreeVector = []
	cyc = 1
	TotCell = FreeCell
	FreeCells, Cuts, Trees = planting_stage(FreeCell, Ncuts, pProb)
	Trees, Cuts, FreeCell, Ressources = harvest_tree_stage(Trees, Ncuts,
											FreeCell, GetCuts, harvest_buf)
	TreeVector.append(Ressources)
	if verbose:
		print("E1 : {all ressources:", np.sum(TreeVector), ". Seeds:", Cuts)
	while (cyc < NCycle)|((Cuts <= 0)&(FreeCell >= TotCell)):
		FreeCells, Cuts, Trees = planting_stage(FreeCell, Cuts, pProb)
		Trees, Cuts, FreeCell, Ressources = harvest_tree_stage(Trees, Cuts,
											FreeCell, GetCuts, harvest_buf)
		TreeVector.append(Ressources)
		if verbose:
			print("E"+str(cyc)+" : {all ressources:", np.sum(TreeVector),
			 ". 'Baby trees'", Cuts)
	TreeVector = np.array(TreeVector)
	return Cuts, TreeVector, cyc
