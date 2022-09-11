# wakfu-game-analysis-and-model
A set of code in relation with the MMORP Wakfu Ankama.

The list of files and their purpose:

  - harvest_data.txt:
    - Text file that contains the experimental data of how mutch did I gather when I am harvesting. Each columns correspond to a buff value.

  - farming_modelisation.py:
    - Python script to model the production of farming plants ressources.
    planting_stage(Nbfree, NbSeed, pProb): simulates trying to fill a N-box card with plants.
    harvest_plants_stage(N_plants, HarvSeed, harvest_buf=0): simulate the harvest stage with a map fill with N_plants.
    CropCycle(NSeeds, FreeCells, NCycle, GetSeeds, pProb, harvest_buf=0): simulate the farm of plants ressources.
    harvest_tree_stage(Trees, Cuts, FreeCell, MinCuts, harvest_buf=0): simulates the gathering of a (partialy) filled box of n cells with trees.
    ForesteryCycle(Ncuts, FreeCell, NCycle, GetCuts, pProb, harvest_buf=0): simulate the farm of trees ressources.

  - Other.py:
    - KamaProduction(minerai_inf, quanti): Calculate how much would give the craft recipes of kamas.
