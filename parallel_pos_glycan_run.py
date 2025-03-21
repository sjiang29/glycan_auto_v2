import single_glycan as sg
import sys
import csv
import os
import shutil
import multiprocessing
import time

# Helper function to copy antigen-related files (PDB, FASTA) from source to destination folder
def copy_antigen_files(source_dir, dest_dir, antigen_pdf, antigen_fasta):
    """
    Copies the antigen PDF and FASTA files from the source directory to the destination directory.
    
    Args:
    source_dir (str): Path to the source directory containing the antigen files.
    dest_dir (str): Path to the destination directory where the files will be copied.
    antigen_pdf (str): Filename of the antigen PDF file.
    antigen_fasta (str): Filename of the antigen FASTA file.
    """
    files = [antigen_fasta, antigen_pdf]
    for item in files:
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            shutil.copy2(source_path, dest_path)


def worker(task_queue):
    """
    Worker function to process glycan addition tasks. It handles one task at a time from the task queue.
    
    Args:
    task_queue (Queue): Queue containing tasks to be processed by the workers.
    """
    while True:
        task = task_queue.get()
        
        if task is None:  # Exit signal
            break
        
        # Unpack task arguments
        ith_pos, n_struct, antigen, antigen_pdb, antigen_fasta, native_glycan_pos, template_folder, antigen_folder = task

        print(f"Thread {ith_pos} starts to work")
                  
        glycan_pos = ith_pos
        folder_for_pos = f"pos_{glycan_pos}"

        if not os.path.exists(folder_for_pos):
            shutil.copytree(template_folder, folder_for_pos)
            copy_antigen_files(source_dir=antigen_folder, dest_dir=folder_for_pos, antigen_pdf=antigen_pdb, antigen_fasta=antigen_fasta)

        # Change to the folder corresponding to the current glycan position
        os.chdir(folder_for_pos)

        # Set native glycan position
        if native_glycan_pos == "":
            native_glycan_pos = -1
        single_Glycan = sg.Single_Glycan(glycan_pos, n_struct, ag_fasta=antigen_fasta, ag_pdb=antigen_pdb, native_glycan_pos=native_glycan_pos)
        single_Glycan.run_single_glycan()

        # Go back to the antigen-level folder
        os.chdir("..")

        return f"---------------Glycan was added to position {ith_pos} of antigen {antigen}-----------------------"
        

def convert_string_to_int_list(s):
    """
    Converts a comma-separated string or a range string (e.g., '1,3-5') to a list of integers.

    Args:
    s (str): Comma-separated string or range string representing positions.
    
    Returns:
    List[int]: List of integer positions.
    """
    int_list = []
    parts = s.split(",")

    for part in parts:
        part = part.strip()
        if part.isdigit():
            int_list.append(int(part))
        elif "-" in part:
            start, end = map(int, part.split("-"))
            int_list.extend(range(start, end + 1))
        else:
            raise ValueError("Invalid input!")
                      
    return int_list


def create_antigen_folder(antigen):
    """
    Creates a folder for the antigen if it doesn't already exist.
    
    Args:
    antigen (str): The name of the antigen.
    
    Returns:
    str: Path to the antigen folder.
    """
    folder_for_antigen = antigen
    path_for_antigen_folder = os.path.join(os.getcwd(), folder_for_antigen)

    if not os.path.isdir(path_for_antigen_folder):
        os.makedirs(folder_for_antigen)
    
    return path_for_antigen_folder


def read_antigen_csv(antigens_csv):
    """
    Reads antigen information from a CSV file.

    Args:
    antigens_csv (str): Path to the CSV file containing antigen information.
    
    Returns:
    list: A list of dictionaries with antigen information.
    """
    antigens = []
    with open(antigens_csv, mode='r') as file:
        csvFile = csv.DictReader(file)
        for lines in csvFile:
            antigens.append({
                'pdb': lines['pdb'],
                'fasta': lines['fasta'],
                'antigen': lines['antigen'],
                'native_glycan_pos': lines['native_glycan_pos']
            })
    return antigens


def start_worker_processes(task_queue, num_workers):
    """
    Starts multiple worker processes.

    Args:
    task_queue (Queue): Queue to distribute tasks to workers.
    num_workers (int): Number of worker processes to start.
    
    Returns:
    list: List of process objects.
    """
    processes = []
    for _ in range(num_workers):
        process = multiprocessing.Process(target=worker, args=(task_queue,))
        processes.append(process)
        process.start()
    
    return processes


def main(argv):
    """
    Main function to manage the glycan addition tasks, process the input arguments, and execute the worker processes.

    Args:
    argv (list): List of command-line arguments.
    """
    start_time = time.time()

    if len(argv) != 4:
        print("Please provide the number of cores, starting and ending AA index for glycan (1-based), number of designed structures, and CSV file.")
        print("Example usage: python local_multi_run.py 10 12,15 100 antigens.csv")
        sys.exit(2)
    else:
        n_cores = int(argv[0])
        positions = convert_string_to_int_list(argv[1])
        n_struct = int(argv[2])
        antigens_csv = argv[3]
        template_folder = os.path.join(os.getcwd(), 'template_files')
        antigen_folder = os.path.join(os.getcwd(), 'antigens')

        # Read antigen information from CSV file
        antigens = read_antigen_csv(antigens_csv)

        for antigen_data in antigens:
            antigen_pdb = antigen_data['pdb']
            antigen_fasta = antigen_data['fasta']
            antigen = antigen_data['antigen']
            native_glycan_pos = antigen_data['native_glycan_pos']

            # Create antigen folder
            path_for_antigen_folder = create_antigen_folder(antigen)
            os.chdir(path_for_antigen_folder)
            print(f">>>>>>> Current folder: {antigen}")

            task_queue = multiprocessing.Queue()

            # Start worker processes
            processes = start_worker_processes(task_queue, n_cores)

            # Add tasks to the queue
            for i in positions:
                task_queue.put((i, n_struct, antigen, antigen_pdb, antigen_fasta, native_glycan_pos, template_folder, antigen_folder))

            # Signal workers to exit after all tasks are done
            for _ in range(n_cores):
                task_queue.put(None)

            # Wait for all processes to finish
            for process in processes:
                process.join()

            print(f"All tasks completed for {antigen}")
            os.chdir("..")

        print("ALL JOBS ARE DONE. CURRENT WORKING DIR IS : {folder}".format(folder=os.getcwd()))

        # Calculate and print execution time
        end_time = time.time()
        execution_time = (end_time - start_time) / 60
        print(f"Execution time: {execution_time} minutes.")


if __name__ == "__main__":
    main(sys.argv[1:])
