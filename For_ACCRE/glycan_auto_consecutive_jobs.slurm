#!/bin/bash

#SBATCH --account=p_csb_meiler
#SBATCH --partition=production 
#SBATCH --mail-type=ALL
#SBATCH --mail-user=shan.jiang@vanderbilt.edu
#SBATCH --job-name=Glyc_
#SBATCH --output=Accre/GlycTest_%A_job_%a.out
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=1G
#SBATCH --time=95:30:00
#SBATCH --array=3-5    #Define the task aarray index range, both number are included

export LD_LIBRARY_PATH="/gpfs51/dors2/meilerlab/apps/Linux2/x86_64/lib64:/dors/meilerlab/apps/Linux2/x86_64/lib"

cd /dors/meilerlab/home/jians15/Desktop/glycan_arph/glycan_automation_v2


# Dynamically use SLURM_ARRAY_TASK_ID as the job ID
JOB_ID=$SLURM_ARRAY_TASK_ID

#Run the Python script with the specific job ID: python single_pos_run.py [aa_index] [number_of_struct] ["antigens.csv"], here JOB_ID is the amino acid index(1-based)
python3 single_pos_run.py $JOB_ID 1 antigens.csv

