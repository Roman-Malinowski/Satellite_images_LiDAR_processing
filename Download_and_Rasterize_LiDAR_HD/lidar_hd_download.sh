#!/bin/bash

#SBATCH -A cars  # Run myaccounts to see which ressources you have access to

#SBATCH --array=1-42:1%42 # i-j:k%l Job de i à j avec un pas max de k et l job max en même temps 
#SBATCH --job-name=LiDAR_HD

#SBATCH -N 1 # Number of nodes
#SBATCH -n 1 # Number of tasks (processus paralleles)
#SBATCH --cpus-per-task=1
#SBATCH --time=00:30:00
#SBATCH --mem-per-cpu=4G

# #SBATCH --error=/home/mp/malinoro/slurm_jobs/out/%x_%A_%a.ERR  # %A is job array id, %a is array task id, %x is job's name 
# #SBATCH --output=/home/mp/malinoro/slurm_jobs/out/%x_%A_%a.OUT

out_folder="/path/where/laz/will/be/downloaded"
links_file="/path/to/the/liste_dalles.txt"
# Do not forget to change the number of parallel jobs so it matches the number of laz files that will be downloaded (default 42)
source /path/to/my/venv/bin/activate

link=`sed -n ${SLURM_ARRAY_TASK_ID}p ${links_file}`

current_dir=`pwd`
cd ${out_folder} 
wget $link
cd ${current_dir}

file_name=${link##*/}  # String operator: "##" is a greedy front trim, "*" matches anything, "/" until this last character appears
python compute_laz_date.py ${out_folder} ${file_name}
