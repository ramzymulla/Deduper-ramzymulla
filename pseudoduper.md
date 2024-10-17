# Deduper Part 1:

### Problem:
Need to take in a SAM file (sorted by chromosome) and retain only the first read 
of each molecule in the original sample. This is based on
4 attributes: ```chromosome #```, ```5' start position```, ```strand```, and ```UMI```
(unique molecular identifier located in the QNAME).

### Pseudocode:
```
for read in SAM file:

    get UMI, chromosome from QNAME,RNAME
    skip if UMI is invalid (go to next read)

    if new chromosome:
        empty the set of written molecules (clear memory)
        update chromosome

    determine strand from bitflag

    adjust 5' start position using CIGAR string

    molecule <- (UMI,strand,pos)
    skip if molecule has already written (go to next read)
    otherwise, write current read to output file
    update set of written molecules
```

### High Level Functions:

```py
def calculate_pos(POS, CIGAR, reverse = False)->int:
    '''
    Determines the 5' starting position based on the recorded position, the CIGAR string, and which strand it's on
    '''
    return pos
# INPUT: POS = 7891, CIGAR = 5S66M, reverse=False
# OUTPUT: 7891+5

# INPUT: POS = 7891, CIGAR = 5S66M, reverse=True
# OUTPUT: 7891+71

# INPUT: POS = 7891, CIGAR = 66M5S, reverse=True
# OUTPUT: 7891+66
```


```py
def get_cols(line)->dict:
    '''
    Extracts SAM columns into a dictionary
    '''
    return cols
# INPUT: Line from SAM file (non- header)
# OUTPUT: Dictionary of <column name>:<column value> (i.e., 'QNAME':$1, 'BITFLAG':$2, 'RNAME':$3, etc.)
```

```py
def is_reverse(BITFLAG) -> bool:
    '''
    Parses bitflag to determine whether it is on the reverse strand
    '''
    return is_it_reverse

# INPUT: 16
# OUTPUT: True
```

```py
def get_UMI(QNAME) -> str:
    '''
    Extracts UMI from the QNAME
    '''
    return umi
# INPUT: NS500451:154:HWKTMBGXX:1:11101:13546:46364:TCAGGACT
# OUTPUT: TCAGGACT
```

