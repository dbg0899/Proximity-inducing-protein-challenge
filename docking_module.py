#!/usr/bin/env python3
import os
import subprocess
import re
import time
import glob
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed


# Set the working directory to where all conformers and receptors are located.
workdir = "/Users/danib/Desktop/challenge/ligand_conformers_top20"
os.chdir(workdir)
print("Current working directory:", os.getcwd())

# Create configuration files if they don't already exist.
def create_config_file(filename, contents):
    with open(filename, "w") as f:
        f.write(contents)
    print(f"Created config file: {filename}")



config_fkbp_contents = (
    "receptor = /Users/danib/Desktop/challenge/receptors/receptor_1_clean.pdbqt\n"
    "center_x = 6.61\n"
    "center_y = -3.18\n"
    "center_z = -6.90\n"
    "size_x = 20\n"
    "size_y = 20\n"
    "size_z = 20\n"
    "exhaustiveness = 8\n"
    "num_modes = 20\n"
)

config_brd4_contents = (
    "receptor = /Users/danib/Desktop/challenge/receptors/receptor_2_clean.pdbqt\n"
    "center_x = 1.53\n"
    "center_y = -9.77\n"
    "center_z = -0.70\n"
    "size_x = 20\n"
    "size_y = 20\n"
    "size_z = 20\n"
    "exhaustiveness = 8\n"
    "num_modes = 20\n"
)

create_config_file("config_brd4.txt", config_brd4_contents)
create_config_file("config_fkbp.txt", config_fkbp_contents)

# Define the path to your Vina executable.
vina_cpu_exe = "/Users/danib/Downloads/autodock_vina_1_1_2_mac_catalina_64bit/bin/vina"

def run_docking(ligand):
    """
    Runs docking for a given ligand file using AutoDock Vina.
    Includes debugging: prints the command, checks the return code, etc.
    """
    docked_out = f"{ligand[:-6]}_docked_out_2.pdbqt"
    log_file = f"log_fkbp_{os.path.basename(ligand)}.txt"
    command = [
        vina_cpu_exe,
        "--config", "config_brd4.txt",
        "--ligand", ligand,
        "--out", docked_out
    ]
    
    # Print the command for debugging
    print(f"Running command for {ligand}: {' '.join(command)}")
    
    start_time = time.time()
    with open(log_file, "w") as f:
        # Run the docking command and capture the return code.
        proc = subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)
    runtime = time.time() - start_time
    
    # Check if the docking command returned an error.
    if proc.returncode != 0:
        print(f"Error: Docking command for {ligand} returned nonzero exit code {proc.returncode}")
    
    # Extract the best docking score from the log file.
    best_score = None
    score_pattern = re.compile(r"\s+1\s+([-0-9.]+)\s+kcal/mol")
    try:
        with open(log_file, "r") as f:
            log_content = f.read()
            # Optionally, print part of the log content for debugging
            print(f"Log file {log_file} content (first 200 chars): {log_content[:200]}")
            for line in log_content.splitlines():
                match = score_pattern.search(line)
                if match:
                    best_score = float(match.group(1))
                    break
    except Exception as e:
        print(f"Error reading log file {log_file}: {e}")
    
    return {
        "ligand": ligand,
        "docked_output": docked_out,
        "log_file": log_file,
        "runtime_sec": runtime,
        "best_score": best_score
    }

if __name__ == '__main__':
    # List all ligand conformer files in the working directory.
    ligand_files = sorted(glob.glob("/Users/danib/Desktop/challenge/ligand_conformers_top20/ligand_conformer_*.pdbqt"))
    print("Found", len(ligand_files), "ligand conformer files.")
    
    # For testing, try running one ligand docking first.
    if ligand_files:
        print("Testing single ligand docking with:", ligand_files[0])
        test_result = run_docking(ligand_files[0])
        print("Test docking result:", test_result)
    
    results = []
    max_workers = 2  # Adjust as needed.
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ligand = {executor.submit(run_docking, ligand): ligand for ligand in ligand_files}
        for future in as_completed(future_to_ligand):
            try:
                res = future.result()
                print(f"Completed docking for {res['ligand']}: score={res['best_score']}, time={res['runtime_sec']:.2f}s")
                results.append(res)
            except Exception as e:
                print("Error in future:", e)
    
    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values(by="best_score")
    print("Docking Results:")
    print(df_results)