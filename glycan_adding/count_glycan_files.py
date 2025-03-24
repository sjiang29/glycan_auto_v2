import os

# Get the current working directory
current_dir = os.getcwd()

# List all the subfolders in the current directory
subfolders = [f.path for f in os.scandir(current_dir) if f.is_dir()]

pos_dir_count = 0
dirs_with_zero = []
dirs_less_100 = {}
# Loop through each subfolder and count the files with the target filename
for subfolder in subfolders:
    if "pos_" in subfolder:
        pos_dir_count = pos_dir_count + 1
        file_count = len([f for f in os.scandir(subfolder) if f.is_file() and ("Glyc_Des_Rfn_P62_monomer_A_0001" in f.name)])
        if file_count == 0:
            dirs_with_zero.append(subfolder)
        elif file_count < 100:
            dirs_less_100[subfolder] = file_count

print(f"-------There are {pos_dir_count} pos_ folders generated--------")
for d in dirs_with_zero:
    print(f"Folder: {d} has 0 files")
for key, value in dirs_less_100.items():
    print(f"{key}: {value} glycaned files")
