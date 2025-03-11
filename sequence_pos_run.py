import single_glycan as sg
import sys
import csv
import os
import shutil

'''
    Helper function to copy target antigen related files from source folder to destination folder   
'''
def copy_antigen_files(source_dir, dest_dir, antigen_pdf, antigen_fasta):
        files = [antigen_fasta, antigen_pdf]
        for item in files:
            source_path = os.path.join(source_dir, item)
            dest_path = os.path.join(dest_dir, item)

            if os.path.isfile(source_path):
                shutil.copy2(source_path, dest_path)

'''
    Main function to run the program

    Args:
        This needs to be 4 input from user
        usage: 'python run.py <starting aa index> <end aa index> <n_struct> <name of csv file that list the interested antigesn>' in the terminal, /
        e.q. 'python run.py 1 10 100 antigens.csv'
    
'''

def main(argv):
        if len(argv) != 4:
            print("please provide starting and ending aa index for glycan(1-based), number of designed structure you want, csv_file")
            print("Example usage: python run.py 1 2 100 antigens.csv")
            sys.exit(2)
        else:
            working_dir = os.getcwd()
            start_pos = int(sys.argv[1])
            end_pos = int(sys.argv[2])
            n_struct = int(sys.argv[3])
            antigens_csv = sys.argv[4]
            template_folder = os.path.join(os.getcwd(), 'template_files')
            antigen_folder = os.path.join(os.getcwd(), 'antigens')

            with open(antigens_csv, mode ='r') as file:    
                csvFile = csv.DictReader(file)
                for lines in csvFile:
                    antigen_pdb = lines['pdb']
                    antigen_fasta = lines['fasta']
                    antigen = lines['antigen']
                    native_glycan_pos = lines['native_glycan_pos']

                    folder_for_antigen = antigen
                    path_for_antigen_folder = os.path.join(os.getcwd(), folder_for_antigen)

                    if not os.path.isdir(path_for_antigen_folder):
                         os.makedirs(folder_for_antigen)
                    # cd to the new folder for the antigen
                    os.chdir(folder_for_antigen)
                    print(">>>>>>>Current folder: {folder}".format(folder = folder_for_antigen))
          
                    for i in range(start_pos, end_pos + 1):
                  
                        glycan_pos = i 
                        

                        folder_for_pos = "pos_" + str(glycan_pos)
                        if not os.path.exists(folder_for_pos):
                            #shutil.rmtree(folder_for_pos) 
                            shutil.copytree(template_folder, folder_for_pos)

                            copy_antigen_files(source_dir=antigen_folder, dest_dir= folder_for_pos, antigen_pdf=antigen_pdb, antigen_fasta=antigen_fasta)
                        
                        # cd to the folder to a spefic pos
                        os.chdir(folder_for_pos)
                        if native_glycan_pos == "":
                            native_glycan_pos = -1
                        else:
                             native_glycan_pos = int(native_glycan_pos)
                        single_Glycan = sg.Single_Glycan(glycan_pos, n_struct, ag_fasta=antigen_fasta, ag_pdb=antigen_pdb, native_glycan_pos=native_glycan_pos)
                        single_Glycan.run_single_glycan()

                        # go back to the antigen-level folder
                        os.chdir("..")

                    # go back to the working dir
                    os.chdir("..")

                print("ALL JOBS ARE DONE. CURRENT WOKING DIR IS : {folder}".format(folder = os.getcwd()))
                os.chdir(working_dir)
                          


if __name__ == "__main__":
        main(sys.argv[1:])
