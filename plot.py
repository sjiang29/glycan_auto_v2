import matplotlib.pyplot as plt
import os
import sys
import statistics
import numpy as np

def get_top_n(top_n, sc_file):
    #print(sc_file)
    
    file = open(sc_file) 
    line = file.readline()
    
    cnt = 1
    scores = []
    
    while line:
        if cnt >= 3 and cnt<=102:
            parts = line.split(":")[1].split()
            score = parts[0].strip()
            
            try:
                score = float(score)
                
            except ValueError:
                #print(parts[4])
                pass
                       
            scores.append(score)
            
        line = file.readline()
        cnt = cnt +1
    file.close()
    
    scores_100 = scores[0:100]
    scores_100.sort()
    scores.sort()
    #print(scores)   
    return scores[0:top_n], scores_100[0:50],scores

def get_top_n_for_all(working_dir, sc_file, top_n, start, end):
    
    pos_and_scores = {}
    pos_and_scores_50 = {}
    pos_and_avg_score = {}
    for filename in os.listdir(working_dir):
        f = os.path.join(working_dir, filename)
        # checking if it is a file
        print(f)
        if os.path.isdir(f) and f.find("pos_")!= -1:
            score_file_path = os.path.join(f, sc_file)
            if os.path.exists(score_file_path):
                
                #top_n_scores = get_top_n(top_n, score_file_path)
                
                pos = f.split("/")[-1]
                pos = pos.split("_")[-1]

                top_n_scores, scores_50, scores = get_top_n(top_n, score_file_path)
                avg_score = statistics.mean(scores)
                pos_and_avg_score[int(pos)] = avg_score
               
                if int(pos) >= start and int(pos) <= end:
                    #top_n_scores, scores_50 = get_top_n(top_n, score_file_path)
                    
                    pos_and_scores[int(pos)] = top_n_scores
                    pos_and_scores_50[int(pos)] = scores_50
    # sort the dict by the keys in ascending order               
    ordered_all = dict(sorted(pos_and_scores.items()))
    ordered_50 = dict(sorted(pos_and_scores_50.items()))
                    
    return ordered_all, ordered_50, pos_and_avg_score

def compare_top75_and_top50from100(working_dir, sc_file):

    ordered_all, ordered_50, pos_and_avg_score = get_top_n_for_all(working_dir, sc_file, 75, 1, 268)

    for k, v in ordered_all.items():
        v = statistics.mean(v)
        ordered_all[k] = v

    for k,v in ordered_50.items():
        v = statistics.mean(v)
        ordered_50[k] = v
    x1,y1 = ordered_all.keys(), ordered_all.values()
    x2,y2 = ordered_50.keys(), ordered_50.values()

    fig = plt.figure()

    ax = fig.add_subplot(111)
    #ax.scatter(x1, y1, c = 'b', marker = 's', label = "top 75 from 150")
    #ax.scatter(x2, y2, c = 'r', marker = 'o', label = 'top 50 from 100')
    plt.scatter(x=y1, y=y2)
    plt.xlabel("Average_Rosetta_score \n of top 75 from 150", fontsize = 16)
    plt.ylabel("Average_Rosetta_score \n of top 50 from 100", fontsize = 16)
    
    #plt.legend(loc='upper left')
    plt.figure(figsize=(10,10))
    plt.show()
            

def make_box_plot(pos_and_scores, dict_name):
    vals = list(pos_and_scores.values())

    # Create the box plot
    labels = pos_and_scores.keys()
    plt.figure(figsize = (15, 6))
    plt.boxplot(vals, labels=labels)
    plt.title(dict_name, fontsize = 16)
    #plt.figure(figsize = (15, 6))
    plt.xlabel('Amino_acid_position', fontsize = 16)
    #plt.xticks(np.arange(101, 150, 10))
    plt.xticks(rotation=90)
    plt.tick_params(labelsize = 12)
    plt.ylim(np.min(vals), np.max(vals))
    plt.ylabel('Rosetta_score', fontsize = 16)
    plt.show()


'''
grid of box plot, can be adjusted accordingly
'''
def make_box_plot_grid(pos_and_scores, dict_name):
    # Split data into three parts
    keys = list(pos_and_scores.keys())  # Extract amino acid positions
    values = list(pos_and_scores.values())

    # Ensure we have exactly 268 positions
    # assert len(keys) == 268, "Expected 268 positions, but got {}".format(len(keys))

    # Split data into first 100, second 100, and last 68
    keys1, values1 = keys[:87], values[:87]  # First 100
    keys2, values2 = keys[87:174], values[87:174]  # Second 100
    keys3, values3 = keys[174:], values[174:]  # Last 68

    fig, axes = plt.subplots(3, 1, figsize=(12, 12))  # 3-row, 1-column

    # Define subplots
    data_splits = [(keys1, values1, "Top 100 Positions"),
                   (keys2, values2, "Middle 100 Positions"),
                   (keys3, values3, "Bottom 68 Positions")]

    for i, (keys_split, values_split, title) in enumerate(data_splits):
        box = axes[i].boxplot(values_split, labels=keys_split, patch_artist=True)

        # Set grey color for each box
        for patch in box['boxes']:
            patch.set(facecolor='grey')

        # Formatting
        #axes[i].set_title(f"{dict_name} - {title}", fontsize=16)
        #plt.suptitle("Best 75 scores out of 100 across all positions", fontsize = 16)
        #plt.xlabel('Amino_acid_position', fontsize = 16)
        #axes[i].set_xlabel('Amino Acid Position', fontsize=14)
        axes[i].set_xticklabels(keys_split, rotation=90)
        axes[i].tick_params(labelsize=10)
        axes[i].set_ylim(-1000, 6000)
        axes[i].set_ylabel('Rosetta Score', fontsize=14)

    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.show()     

def plot_all_for_current_dir(cur_dir, top_n, start, end, sasa_file):
    pos_and_scores, pos_and_scores_50, pos_and_avg_score = get_top_n_for_all(cur_dir, "Glyc_score.sc", top_n, start, end)
   
    pos_and_sasa = read_sasa(sasa_file)
    plot_sasa_vs_score(pos_and_sasa, pos_and_avg_score)
    make_box_plot(pos_and_scores, f"Top {top_n} from 100")
    # make_box_plot(pos_and_scores_50, "Top 50 from 100 out of 150")

def read_sasa(sasa_file):
    file = open(sasa_file)
    line = file.readline()
    pos_and_sasa = {}
    while line:
        parts = line.split(":")

        pos = parts[0]
        pos = int(pos.split(" ")[0][3:])
        score = float(parts[1])
        pos_and_sasa[pos] = score

        line = file.readline()
    file.close()

    return pos_and_sasa

def plot_sasa_vs_score(pos_and_sasa, pos_and_avg_score):

    sasa_vs_score = {}

    for key,value in pos_and_avg_score.items():
        sasa_vs_score[pos_and_sasa[key]] = value

    x,y = sasa_vs_score.keys(), sasa_vs_score.values()

    #plt.figure(figsize=())
    plt.scatter(x, y)
    plt.xlabel("Solvent_Accessible_Surface_Area", fontsize = 16 )
    plt.ylabel("Average_Rosetta_score", fontsize = 16)
    plt.tick_params(labelsize = 14)
    plt.ylim(min(y), max(y))
    plt.show()

   

def main(argv):

    cur_dir = os.getcwd()
    
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    top_n = int(sys.argv[3])
    sasa_file = sys.argv[4]
    plot_all_for_current_dir(cur_dir, top_n, start, end, sasa_file)

    #compare_top75_and_top50from100(cur_dir, "Glyc_score.sc")
    
    

if __name__ == "__main__":
        main(sys.argv[1:])