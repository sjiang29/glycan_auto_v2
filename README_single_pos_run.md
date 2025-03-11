Glycan Design Pipeline for Single Antigen Position
This pipeline allows for glycan modification at a single specified position on antigens and generates multiple antigen structures. The script processes antigen data provided in a CSV file, creates the necessary directories, and runs the glycan design process using the single_glycan module.

Overview
This script is used to modify antigens by placing glycans at a specified amino acid position. The modification is performed for one glycan position at a time, and multiple antigen structures are generated for each modification. The script automates this process, making it suitable for batch processing antigen datasets.

Requirements
Python 3.x
Required Python packages:
single_glycan (custom module)
sys
csv
os
shutil


Usage
Command-Line Arguments
To run the script, you must provide the following arguments:
python single_pos_run.py <glycan_pos> <n_struct> <antigens_csv>
<glycan_pos>: The specific amino acid position (1-based index) where the glycan will be placed.
<n_struct>: The number of antigen structures to generate for the glycan modification.
<antigens_csv>: The path to the CSV file containing antigen information.

Example Usage
python single_pos_run.py 1 100 antigens.csv

This command will:

Modify the antigen at glycan position 1.
Generate 100 antigen structures.
Use antigens.csv to locate antigen files for modification.
CSV File Format
The CSV file (antigens.csv) should contain the following columns:

pdb: Path to the antigen PDB file.
fasta: Path to the antigen FASTA file.
antigen: The name of the antigen.
native_glycan_pos: The position of the native glycan (if any) on the antigen.

Example antigens.csv:
pdb,fasta,antigen,native_glycan_pos
antigen1.pdb,antigen1.fasta,antigen1,3
antigen2.pdb,antigen2.fasta,antigen2,

How It Works
Input Files: The script reads the antigen files listed in the CSV (pdb, fasta, native_glycan_pos).
Directory Setup: For the specified glycan position, the script creates a new folder and stores the modified antigen structure files.
File Copying: The antigen PDB and FASTA files are copied into the new folder for the glycan modification.
Glycan Processing: The script uses the single_glycan module to place the glycan at the specified position and generate the antigen structure.
Result Storage: The glycan-modified structures are stored in the corresponding folder for the glycan position.

Script Flow
Copy Antigen Files: The copy_antigen_files function copies the antigen PDB and FASTA files into a folder specific to the glycan position.
Run Glycan Modification: The script creates the folder for the glycan position and runs the glycan design workflow using the single_glycan module.
Main Workflow: The script loops over the antigen data from the CSV file, processes the specified glycan position, and generates the required number of modified antigen structures.

Notes
The script assumes that the necessary template_files and antigens directories exist in the current working directory.
The single_glycan module must be correctly installed or placed in the working directory for the script to function properly.
If the antigen has a native glycan, its position can be specified in the CSV file. If not, the script uses a default value of -1.

