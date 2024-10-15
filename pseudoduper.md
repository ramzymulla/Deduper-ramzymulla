# Deduper Part 1:

### Problem:
Need to take in a SAM file and retain only the first read 
of each molecule in the original sample. This is based on
4 attributes: ```chromosome #```, ```5' start position```, ```strand```, and ```UMI```
(unique molecular identifier located in the QNAME).


### Pseudocode:
```
written <- set of written molecules
knownUMIs <- set of known UMIs
chr <- string identifying the current chromosome
numread <- counter for total number of reads
numwritten <- counter for number of reads written to output

fill knownUMIs using UMI text file

for line in SAM file:

    extract columns

    get UMI, chr from QNAME,RNAME

    if new chr:
        empty the set of written mols
        update chr

    eval bitflag:
        skip if unmapped (go to next line)
        determine strand

    calculate 5' start position
    get UMI, chr from QNAME,RNAME

    skip if UMI is invalid (go to next line)

    mol <- (UMI,strand,pos)
    skip if mol in written (go to next line)
    add to written
    write to output file

```