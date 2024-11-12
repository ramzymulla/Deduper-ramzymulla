#!/usr/bin/env python

import argparse as arp
import re


SAMCOLS = ['qname','flag','rname',
           'pos','mapq','cigar','rnext',
           'pnext','tlen','seq','qual']

qnameind = 0
flagind = 1
rnameind = 2
posind = 3
cigarind = 5

def get_args():
    '''Parses user inputs from command line'''
    parser = arp.ArgumentParser(description="arg parser") 
    parser.add_argument("-f","--file", help="absolute path to input SAM file",
                        required=True)
    parser.add_argument("-o","--outfile", help="absolute path to sorted output SAM file",
                        required=True)
    parser.add_argument("-u","--umi", help="absolute path to UMI file",
                        required=True)
    # parser.add_argument("-h","--help", help="")
    return parser.parse_args()


def calculate_pos(POS:int, CIGAR: str, reverse = False)->int:
    '''
    Determines the 5' starting position based on the recorded position, 
    the CIGAR string, and which strand it's on
    '''
    cigar = re.findall(r"(\d+\D)",CIGAR)

    pos = POS
    consumes_ref = set(['M','D','N','X','='])

    if reverse:
        for cig in cigar:
            if cig[-1] in consumes_ref:
                pos += int(cig.strip(cig[-1]))
        
        if "S" in cigar[-1]:
            pos += int(cigar[-1].strip("S"))

    elif "S" in cigar[0]:
        pos -= int(cigar[0].strip("S"))

    return pos

def get_SAM_cols(line: str)->dict:
    '''
    Extracts SAM columns into a dictionary
    '''
    return {SAMCOLS[i]:line.split()[i] for i in range(len(SAMCOLS))}

def is_reverse(BITFLAG: str) -> bool:
    '''
    Parses bitflag to determine whether it is on the reverse strand
    '''
    return int(BITFLAG)&16 > 0

def get_UMI(QNAME: str) -> str:
    '''
    Extracts UMI from the QNAME
    '''
    return QNAME.split(':')[-1]

def get_UMIlist(file) -> list:
    with open(file,'r') as f:
        UMIlist = [line.strip() for line in f]

    return UMIlist

args = get_args()

SAMfile = args.file
OUTfile = args.outfile
UMIfile = args.umi

# parse known UMIs file
UMIs = set(get_UMIlist(UMIfile))

# initialize written molecules set
written_molecules = set()

# initialize previous chromosome variable
prev_chrom = '1'

chrom_read_counts = {}
unique_reads = 0
wrong_umis = 0
duplicates_removed = 0
header_lines = 1

with open(SAMfile,'r') as fin, open(OUTfile,'w') as fout:
    # write header lines
    line = fin.readline().strip()
    fout.write(line)
    line= fin.readline().strip()
    while line[0] == "@":
        header_lines += 1
        fout.write("\n"+line)
        line = fin.readline().strip()

    while line:
        cols = line.split()

        # get UMI, chromosome from QNAME,RNAME
        umi, chrom = get_UMI(cols[qnameind]),cols[rnameind]

        # skip if UMI is invalid (go to next read)
        if umi not in UMIs:
            wrong_umis += 1
        else:
            if chrom != prev_chrom:
                # update accumulators
                n_reads = len(written_molecules)
                chrom_read_counts[prev_chrom] = n_reads

                # update chromosome
                prev_chrom = chrom

                # empty the set of written molecules (clear memory)
                written_molecules.clear()

            # determine strand from bitflag
            isrev = is_reverse(cols[flagind])

            # adjust 5' start position using CIGAR string
            position = calculate_pos(int(cols[posind]),cols[cigarind],isrev)

            molecule = (umi,isrev,position)

            # only write if not already in written_molecules
            if molecule not in written_molecules:
                unique_reads += 1
                written_molecules.add(molecule)
                fout.write("\n"+line)
            else:
                duplicates_removed += 1

        line = fin.readline().strip()

with open("deduper_stats.txt",'w') as f:
    f.write(f"Header lines: {header_lines}\n")
    f.write(f"Unique reads: {unique_reads}")
    f.write(f"\nWrong UMIS: {wrong_umis}")
    f.write(f"\nDuplicates Removed: {duplicates_removed}")
    f.write(f"\nReads per Chromosome:")
    for chrom in chrom_read_counts:
        f.write(f"\n{chrom}\t{chrom_read_counts[chrom]}")