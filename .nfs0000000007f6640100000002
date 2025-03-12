Glycan Design Pipeline
This pipeline is designed for glycan-based antigen structure generation using multiprocessing and parallel threading. It leverages custom modules for single glycan processing and supports concurrent execution to optimize computation for large antigen datasets.

Description
The script enables parallel processing of antigen-related files (PDB and FASTA formats) and glycan positions to design a set of antigen structures with glycan modifications. Using multiprocessing and threading, it performs glycan modification and structure generation efficiently across multiple CPU cores.

The core functionality is divided into multiple steps:

Copy antigen-related files: Antigen files are copied from source directories to specific folders.
Glycan position processing: A glycan is placed at specific positions on the antigen to design modified structures.
Parallel execution: Multiple processes are spawned to process glycan positions in parallel for efficient computation.
Requirements
Python 3.x
Required Python packages:
single_glycan (custom module)
os
sys
csv
shutil
multiprocessing
threading
concurrent.futures
time
Installation
Clone or download the repository containing the code.

Install the necessary Python packages (if not already available).

Usage
The script requires several command-line arguments to specify the number of cores to use, the range of glycan positions to process, the number of antigen structures to generate, and the CSV file containing antigen information.

Command-Line Arguments:
python local_multi_sparse_run.py <num_cores> <positions> <n_struct> <csv_file>
<num_cores>: The number of CPU cores to utilize for parallel processing.
<positions>: The positions (1-based) for glycan placement, positions should and ONLY be seperated by comma(see example)
<n_struct>: The number of structures to generate for each glycan modification.
<csv_file>: The CSV file containing antigen information (PDB, FASTA, and native glycan position).

Example:
python local_multi_sparse_run.py 10 1-5,15,20 100 antigens.csv
Where:
10 is the number of cores.
1-5 and 15 and 20 are the positions of glycan modification (1-based index), which are seperated by ",". 1-5 means all the positions from 1 to 5(inclusive).
100 is the number of structures to generate.
antigens.csv is the CSV file containing antigen information.
CSV File Format:
The CSV file (antigens.csv) should contain the following columns:

pdb: Path to the antigen PDB file.
fasta: Path to the antigen FASTA file.
antigen: The name of the antigen.
native_glycan_pos: The position of the native glycan on the antigen (optional).
Example antigens.csv:
pdb,fasta,antigen,native_glycan_pos
antigen1.pdb,antigen1.fasta,antigen1,3
antigen2.pdb,antigen2.fasta,antigen2,

How it Works
Copy Antigen Files: The copy_antigen_files function copies the antigen PDB and FASTA files from the source directory to a new folder created for each glycan position.
Worker Function: Each worker performs tasks in parallel. It sets up the antigen folders, processes glycan positions, and runs the glycan design workflow using the Single_Glycan module.
Parallel Execution: The main function uses multiprocessing to spawn multiple worker processes, each handling a specific glycan position.
Task Queue: A task queue is used to distribute tasks to workers, ensuring efficient processing of glycan modifications.
Example Output
After running the script, you will have multiple folders representing different glycan positions (pos_1, pos_2, etc.), each containing the antigen structure files and designed glycan-modified structures.

Notes
The script uses multiprocessing to run multiple tasks concurrently. Each task handles a specific glycan position and generates multiple antigen structures.
Be sure to adjust the template_files and antigens folders to match the directory structure and files available to the script.
The single_glycan module must be available for this script to work. Ensure it's properly installed or present in your working directory.

