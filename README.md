# 🌟 Proximity-Inducing Drugs Computation Challenge 🌟

Welcome to our submission for the **Proximity-Inducing Drugs Computation Challenge**! This repository contains our detailed, docking-based strategy to accurately predict the 3D ternary complex structure of **FKBP12 C22V**, **BRD4 BD1**, and a bifunctional **PROTAC** ligand as specified by the challenge requirements.

---

## Overview

To predict the ternary complex, we employed a systematic, docking-driven approach consisting of the following steps:

1. **Protein Structure Generation**  
   - **ColabFold/AlphaFold2** was used to generate high-confidence models for **FKBP12 C22V** (residues 2–108) and **BRD4 BD1** (residues 44–168).  
   - Out of multiple predictions, the **top-ranked Model 1** for each receptor was selected based on pLDDT scores.  
   - These PDB structures were processed with **Open Babel** and **AutoDock Tools** to add polar hydrogens and assign Gasteiger charges, then converted into the **PDBQT** format required for docking.  
   
2. **Ligand Preparation**  
   - The **PROTAC ligand** (SMILES:  
     `Cc1sc2c(c1C)C(c1ccc(C#CCNC(=O)COCCn3cc([C@H]4CN(Cc5ccccn5)C(=O)[C@@H]5CCC[C@H]4N5S(=O)(=O)c4cc(Cl)cc(Cl)c4)nn3)cc1)=N[C@@H](CC(=O)OC(C)(C)C)c1nnc(C)n1-2`) was processed using **RDKit**.  
   - An ensemble of **100 3D conformers** was generated using the **ETKDGv3 algorithm** and optimized with the **MMFF94** force field (with UFF as a fallback).  
   - The ensemble was ranked by minimized energy, and the **top 10 lowest-energy conformers** were selected.  
   - The multi-conformer SDF was then **split** into individual PDBQT files (with Gasteiger charges) using **Open Babel**.

3. **Docking Procedure**  
   - **AutoDock Vina** (version 1.1.2, Mac Catalina 64-bit binary) was used to dock the ligand conformers independently into the binding pockets of both receptors.  
   - **Grid Parameters:**  
     - For **BRD4 BD1**, the grid was centered on the acetyl-lysine binding pocket (approximately at **(1.53, –9.77, –0.70)**) with dimensions **20×20×20 Å**.  
     - For **FKBP12 C22V**, the grid was centered on its binding pocket (approximately at **(6.61, –3.18, –6.90)**) with the same dimensions.  
   - Each ligand conformer was docked against both receptors, and for each receptor, we selected the pose with the **lowest docking energy** (most negative affinity) that demonstrated chemically reasonable interactions with key residues  
     - **FKBP12:** *Phe36, Trp59, Tyr82*  
     - **BRD4:** *Asn140, Tyr97*

4. **Ternary Complex Assembly**  
   - The best docked ligand pose from the separate docking experiments was used.  
   - Using **PyMOL**, the receptor–ligand complexes were loaded, and the ligand was manually aligned so that its two binding “warheads” simultaneously occupied the active sites on **FKBP12 C22V** (assigned **chain A**) and **BRD4 BD1** (assigned **chain B**). The ligand was assigned **chain C**.  
   - A short energy minimization in PyMOL was performed to relieve steric clashes and optimize the interface.  
   - Based on our evaluations (docking scores, visual inspection of key interactions, and geometric plausibility), we selected **three candidate ternary complex structures**.

---

## Final Submission

We are submitting the following **three top candidate ternary complex structures** (in PDB format):

- **Ternary_Model_Approach1.pdb** – Derived from sequential warhead docking and manual assembly.  
- **Ternary_Model_Approach2.pdb** – Generated using ensemble docking with constrained protein–protein docking and linker sampling.  
- **Ternary_Model_Approach3.pdb** – A hybrid model refined by short molecular dynamics simulation and induced-fit adjustments.

Each model includes all three components with distinct chain IDs:  
- **Chain A:** FKBP12 C22V  
- **Chain B:** BRD4 BD1  
- **Chain C:** PROTAC

These models were selected based on their docking scores, the presence of critical interactions (e.g., with **Phe36, Trp59, Tyr82** in FKBP12 and **Asn140, Tyr97** in BRD4), and the overall structural plausibility of the PROTAC linker bridging the two proteins.

---

## Software/Tools Used

- **ColabFold/AlphaFold2:**  
  *[AlphaFold GitHub](https://github.com/deepmind/alphafold)*  
  Used for generating high-confidence protein structures.

- **Open Babel:**  
  *[Open Babel Website](http://openbabel.org/wiki/Main_Page)*  
  Used for adding hydrogens, converting file formats, and splitting ligand SDF files.

- **RDKit:**  
  *[RDKit Website](https://www.rdkit.org/)*  
  Used for generating and optimizing ligand conformers via the ETKDGv3 algorithm.

- **AutoDock Vina:**  
  *[AutoDock Vina Website](http://vina.scripps.edu/)*  
  Used for docking ligand conformers into the binding pockets.

- **PyMOL:**  
  *[PyMOL Website](https://pymol.org/)*  
  Used for visualizing, aligning, and merging receptor–ligand complexes.

- **UCSF Chimera (optional):**  
  *[Chimera Website](https://www.cgl.ucsf.edu/chimera/)*  
  Utilized for additional visualization and energy minimization.

---

## Repository

For complete details, reproducibility, and all scripts used in our workflow, please refer to our GitHub repository:  
[https://github.com/dbg0899/Protein_challenge/](https://github.com/dbg0899/Protein_challenge/)

---

Thank you for reviewing our submission! If you have any questions or require additional information, please feel free to open an issue on our GitHub repository.

✨ **We hope you find our approach both rigorous and innovative – good luck to everyone participating!** ✨
