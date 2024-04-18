# wakfu-game-analysis-and-model
A set of code in relation with the MMORP Wakfu Ankama.

The list of files and their purpose:

  - harvest_data.txt:
    - Text file that contains the experimental data of how mutch did I gather when I am harvesting. Each columns correspond to a buff value.

  - farming_modelisation.py:
    - Python script to model the production of farming plants ressources.
      - **planting_stage**: simulates trying to fill a N-box card with plants.
      - **harvest_plants_stage**: simulate the harvest stage with a map fill with N_plants.
      - **crop_cycle**: simulate the farm of plants ressources.
      - **harvest_tree_stage**: simulates the gathering of a (partialy) filled box of n cells with trees.
      - **forestery_cycle**: simulate the farm of trees ressources.

  - Other.py:
    - **kama_production**: calculate how much would give the craft recipes of kamas.
