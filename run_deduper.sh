#!/usr/bin/env bash

#SBATCH -A bgmp
#SBATCH -p bgmp
#SBATCH -t0-20
#SBATCH -c 8
#SBATCH --output=logs/run_deduper_live_%j.out
#SBATCH --error=logs/run_deduper_live_%j.err

/usr/bin/time -v python Al-Mulla_deduper.py \
-f  /projects/bgmp/rza/bioinfo/Bi624/Deduper-ramzymulla/C1_SE_uniqAlign_sorted.sam \
-o  /projects/bgmp/rza/bioinfo/Bi624/Deduper-ramzymulla/C1_SE_uniqAlign_deduped.sam \
-u /projects/bgmp/rza/bioinfo/Bi624/Deduper-ramzymulla/STL96.txt