import sys

# Dictionary of all the valid tags and their corresponding level
tags = {
    "INDI": "0", "NAME": "1", "SEX": "1", "BIRT": "1", "DEAT": "1", "FAMC": "1", "FAMS": "1", "FAM": "0", "MARR": "1",
    "HUSB": "1", "WIFE": "1", "CHIL": "1", "DIV": "1", "DATE": "2", "HEAD": "0", "TRLR": "0", "NOTE": "0"
}
# Dictionaries to save information about individuals or families
indi = {}

fam = {}

# Flags help select which dict and where to input data
current = ""
which_dict = ""
dated_event = ""
date = False

f = open(sys.argv[1], "r")
while True:
    # Get one line of the GEDCOM file at a time
    inp = f.readline().strip()

    # If input is empty then break
    if not inp:
        break

    # Splits the current line by spaces and puts it into an array
    line = inp.split()

    # Initialize Variables
    arg = ""
    tag = ""
    valid = False
    # For every word in the current line, checks if
    # it is in the dictionary of tags.
    # If tag is in the dictionary and it is at the right level, tag is valid
    # If tag is in the dictionary but isn't at the right level, tag is invalid
    for arg in line:
        if arg in tags.keys() and tags[arg] == line[0]:
            valid = True
            break
        elif arg in tags.keys():
            valid = False
            break

    # Check the two special cases where the we add indi or fam dictionary entry
    if line[0] == "0":
        if arg == "INDI":
            current = line[1]
            which_dict = "INDI"
            indi[current] = {}

        if arg == "FAM":
            current = line[1]
            which_dict = "FAM"
            fam[current] = {}
    # Gets rid of the tag from the array
    if arg in tags.keys():
        line.remove(arg)

    # Deletes the level from the array
    del line[0]

    if which_dict == "INDI" and arg != "INDI" and valid is True:
        if date is True:
            indi[current][dated_event] = ' '.join(line)
            date = False
        elif arg == "BIRT":
            date = True
            dated_event = arg
        else:
            indi[current][arg] = ' '.join(line)

    if which_dict == "FAM" and arg != "FAM" and valid is True:
        if date is True:
            fam[current][dated_event] = ' '.join(line)
            date = False
        if arg == "MARR" or arg == "DIV":
            date = True
            dated_event = arg
        else:
            fam[current][arg] = ' '.join(line)

    # Accounts for the other possible tags that aren't in the dictionary
    # of valid tags
    # if not valid and len(line) > 1 and (line[1].isupper() or "_" in line[1]):

        # del line[1]

    # Adds the arguments to the output string
    # for x in line:
    #     out += x + " "

print(indi)
print(fam)
f.close()
