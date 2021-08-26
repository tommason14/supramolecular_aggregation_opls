# Clustering analysis

Uses `gmx clustsize` to compute cluster size distributions.

By placing `analyse_clusters.sh`, `compare_cutoffs.py`, `em.mdp`,
`extract_selection.py` and `make-top.py` into the parent folder and running
`bash analyse_clusters.sh`, the script will:

- create a gromacs topology file containing info of the indoledione molecules
- extract the indolediones from the trajectory
- create a gromacs run file that the clustering program reads
- run the clustering program, `gmx clustsize`
- extract data on the number of molecules in each cluster, the size of the largest cluster, and the cluster size distribution over time, then save the data to 3 csv files and plot graphs of the data

The number of molecules in each cluster might vary a lot. If the graphs aren’t smooth, you can create a rolling mean of the data by running `python3 compare_cutoffs.py N`, and it will average the data of N steps.
