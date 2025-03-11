Glycan Design Antigen Pipeline
This pipeline is designed to modify antigens by placing glycans at specified positions and generating multiple antigen structures using custom computational tools. The script leverages the single_glycan module for processing and utilizes Python’s file handling capabilities to manage antigen files and directories.

Overview
The main objective of this script is to automate the process of modifying antigens by glycan attachment at specific amino acid positions. The script supports batch processing, making it suitable for generating large numbers of glycan-modified structures in parallel.

The script takes in a CSV file containing antigen-related information and uses it to copy antigen files into a working directory where glycan modifications are performed. The final output consists of modified antigen structures, stored in separate folders for each glycan position.

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

python sequence_pos_run.py <start_pos> <end_pos> <n_struct> <antigens_csv>
<start_pos>: The starting position (1-based index) for glycan placement.
<end_pos>: The ending position (1-based index) for glycan placement.
<n_struct>: The number of antigen structures to generate for each glycan modification.
<antigens_csv>: The path to the CSV file containing the antigen information.

Example Usage
python sequence_pos_run.py 1 10 100 antigens.csv
This command will:

Process glycan positions from 1 to 10.
Generate 100 antigen structures for each position.
Use antigens.csv to locate antigen files for modification.
CSV File Format
The CSV file should have the following columns:

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
Directory Setup: For each antigen, the script creates a new folder to store glycan-modified structures at each specified glycan position.
File Copying: It copies the antigen PDB and FASTA files from the source directories to the new folders.
Glycan Processing: The script runs the glycan modification process for each glycan position using the single_glycan module.
Result Storage: Each glycan-modified structure is stored in a subfolder corresponding to the glycan position.

Script Flow
Copy Antigen Files: The copy_antigen_files function copies the antigen PDB and FASTA files into a working folder for each glycan position.
Run Glycan Modification: For each glycan position (from start_pos to end_pos), the script creates a new folder and runs the glycan design workflow.
Main Workflow: The script loops over each antigen in the CSV file, processes the glycan positions, and calls the single_glycan module for structure generation.

Notes
The script assumes that the necessary template_files and antigens directories exist in the current working directory.
The single_glycan module must be correctly installed or placed in the working directory for the script to function properly.
If the antigen has a native glycan, its position can be specified in the CSV file. If not, the script uses a default value (-1).

