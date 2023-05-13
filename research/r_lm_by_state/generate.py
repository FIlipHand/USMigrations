import glob
import subprocess
import os

all_state_files = glob.glob('data/states_data/*.csv')


for file_name in all_state_files:
    out_name = file_name.split('\\')[1][:-4]
    f = open(f"{out_name}.txt", "w")
    subprocess.call(["Rscript.exe", "./src/R_snippets/lm_from_path.r", file_name], stdout=f)
    f.close()