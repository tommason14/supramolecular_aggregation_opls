# Parameterisation

Adding drude particles to a standard non-polarisable forcefield allows for a
more accurate description of intermolecular interactions, but also results in 
over-estimation of the non-Coulombic interactions. As a result, we should
reduce the strength of the Lennard-Jones terms being interacting pairs of
atoms. The amount by which the interactions should be reduced is described
through a ratio of dispersion and induction, known as a k<sub>ij</sub> scaling factor, described [here](https://pubs.acs.org/doi/abs/10.1021/acs.jctc.9b00689) by Goloviznina and Padua.

This scaling factor is found through a SAPT2+ calculation of each pair of
molecules. Alternatively, the distance between the centre of masses of each molecule can be found,
and this can be used along with the molecular polarisabilities in a regression
model to find an approximate k<sub>ij</sub> factor.

Atomic polarisabilities for every atom type are also required, in order to
parameterise drude particles.
These atomic polarisabilities can be calculated as described in [this paper](https://pubs.rsc.org/en/content/articlelanding/2018/cp/c7cp08549d#!divAbstract) by Heid et al.
This involves calculating molecular dipoles whilst applying electric fields in
all directions. The molecular dipoles are then decomposed into atomic
contributions using bonding information. Atomic polarisabilities are then
determined using this bonding information.

Molecular dipole moments are required, and can be calculated at the MP2/cc-pVTZ level
of theory.

## k<sub>ij</sub> scaling factor determination

In the original paper, Goloviznina performed a SAPT0/aug-cc-pVDZ optimisation by choosing a
particular interaction and then gradually increasing the distance between each molecule. Intermolecular
interaction energies were calculated for each geometry, and the geometry with
the lowest total interaction energy was taken and a more accurate
SAPT2+/aug-cc-pVDZ calculation was performed using this geometry.

Alternatively, geometry optimisations can be performed with a reasonably
accurate method, for example SRS-MP2/aug-cc-pVDZ, instead of performing a SAPT0
geometry scan. A SAPT2+/aug-cc-pVDZ calculation should then be performed using the optimised structure.

The ratio of dispersion to dispersion and induction is then used to obtain a
k<sub>ij</sub> scaling factor. This factor is calculated, along with the
distance between the centre of masses of each molecule, by the
sapt_kij_analysis.py script.

For example:

```
$ sapt_kij_analysis.py sapt2.log
+-----------------------------------------------+
|     Name      |     k_ij      |     r_COM     |
+-----------------------------------------------+
|   sapt2.log   |    0.33194    |    5.34462    |
+-----------------------------------------------+
```

## Atomic polarisabilities

1. Using an optimised geometry for each molecule of interest, 6 calculations
should be set up. Heid recommended a field strength of 0.0008 au using
Gaussian with the M062X, functional so the following command line should be used:
`#P M062X/basis field=X+8 int=(grid=ultrafine) polar=Dipole`.

For the basis set, Heid also recommended using the SadleJ-pVTZ basis set.
This is not included in Gaussian, but can be found on
[basis set exchange](https://www.basissetexchange.org/).
Alternatively, a sufficiently large basis set such as cc-pVTZ/aug-cc-pVTZ may be used.

> Important: Make sure a checkpoint file is saved, using the `%chk` parameter.

Example files using the SadleJ basis set are shown in the polarisabilities folder.

2. After the calculations have finished, you should have checkpoint files saved.
Depending on where the calculations were run, these may be in a subfolder.
Convert these binary files to text files using the `formchk` command,
distributed with Gaussian (so `module load gaussian` beforehand). For example:
`formchk run.chk` will produce a `run.fchk` file in the same folder.

3. Andrew Stone's GDMA software is then used to produce atomic dipoles, using the
fchk files produced in the last step. Examples of this can be found in the gdma
subfolders.

4. Now we can calculate atomic polarisabilities.
Bonds between each atom are needed, and should be stored in a file named
`connected.in`. For example, 

```
bond 1 2
bond 1 3
bond 1 4
bond 1 6
bond 4 5
bond 6 7
```

describes all bonds in `polarisabilities/dhp.xyz`.

A python script, `analyse_polarisabilities.py`, is then used to calculate atomic polarisabilities. This should
be run from the folder containing the minusX, plusX directories. Provide the
correct field strength when prompted - a command of `X+8` in the gaussian files
corresponds to a field strength of 0.0008 au.
From the output written to the screen, save this section:
```
Total polarizability:
Name       a
   P    1.34 
   O    1.33 
   O    1.35 
   O    1.10 
   H    0.24 
   O    1.10 
   H    0.24 
Summed up contributions:
6.683060472566668
```
that describes atomic polarisabilities for each atom, in angstroms<sup>3</sup>.

These will be used in the next step to parameterise drude particles.

## Optional helper scripts

To help generate the files for each field strength, as well as the connectivity
file, you could install the `autochem` module, found
[here](https://www.github.com/tommason14/autochem), and then use the
`gauss_sadlej_polarisabilities.py` and `make_connected_in.py` scripts.
The `gauss_sadlej_polarisabilities.py` script should be run from the folder that
contains the xyz files.

# Molecular dipole moments

A molecular dipole moment can be found from a Gaussian calculation with the
following command line: `#P MP2/cc-pVTZ int=(grid=ultrafine) pop=(chelpg,dipole)`

The dipole will be used when either predicting k<sub>ij</sub> values in the next section.
