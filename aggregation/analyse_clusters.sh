#!/usr/bin/env bash

cwd="$(pwd)"

##################################################################
#  Making a Gromacs topology file for the indoledione molecules  #
##################################################################

cd build
$cwd/make-top.py -f mols/indoledione.xyz -n 20 -b 55 -ff ff/CLP.ff ff/indoledione_geo.ff ff/CLPol-alpha.ff -s ff/CLPol-ljscale.ff -d

###################################################################
#  Extracting only the indoledione molecules from the trajectory  #
###################################################################

cd ../nvt
mkdir analysis
cd analysis
python3 $cwd/extract_selection.py -sel 'resname indol' ../../build/conf.gro ../dump.dcd -o ind # creates ind.gro and ind.xtc

#########################
#  Clustering analysis  #
#########################

# most gromacs analysis tools require a binary file that is normally used when running a simulation,
# a .tpr file (portable run file)
# I've added a -maxwarn 1 because gromacs gives a warning when dealing with drude particles

gmx_mpi grompp -f $cwd/em.mdp -c ind.gro -p $cwd/build/topol.top -o ind.tpr -maxwarn 1

# Now perform cluster analysis for different cutoff lengths (3-6 angstroms)
mkdir -p {3..6}-angs
for i in {3..6}
do
  echo "Starting $i-angs"
  cd $i-angs
  gmx_mpi clustsize -f ../ind.xtc -s ../ind.tpr -mol -nc -mc -ac -hc -mcn -cut 0.$i >& out.log
  echo "Finished $i-angs"
  cd ..
done
cd $cwd

##################################
#  Extract data and plot graphs  #
##################################

# For this example, I only took the first 100 steps of the nvt run.
# When looking at the whole run, you'll probably want to create a rolling mean over time as the number of clusters oscillates a lot.
# Just change this 1 to 50 or 100 to average over every 50 or 100 steps
echo "Plotting data"
python3 compare_cutoffs.py 1
