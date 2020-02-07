import sys

# Dictionary of all the valid tags and their corresponding level
tags = {
    "INDI": "0", "NAME": "1", "SEX": "1", "BIRT": "1", "DEAT": "1", "FAMC": "1", "FAMS": "1", "FAM": "0", "MARR": "1",
    "HUSB": "1", "WIFE": "1", "CHIL": "1", "DIV": "1", "DATE": "2", "HEAD": "0", "TRLR": "0", "NOTE": "0"
}
f = open(sys.argv[1], "r")
while True:
    # Get one line of the GEDCOM file at a time
    inp = f.readline().strip()

    # If input is empty then break
    if not inp:
        break

    print("--> " + inp)

    # Splits the current line by spaces and puts it into an array
    line = inp.split()

    # Build output string little by little
    out = "<-- " + line[0] + "|"
    arg = ""
    valid = False

    # For every word in the current line, checks if it is in the dictionary of tags.
    # If it is in the dictionary and it is at the right level, build the output with Y
    # If it is in the dictionary but isn't at the right levle, build the output with N
    for arg in line:
        if arg in tags.keys() and tags[arg] == line[0]:
            valid = True
            out += arg + "|Y|"
            break
        elif arg in tags.keys():
            valid = True
            out += arg + "|N|"
            break
    
    # Check the two special cases where the tag comes after the argument.
    if (arg == "INDI" or arg == "FAM") and line[2] != arg:
        out = "<-- " + line[0] + "|" + arg + "|N|"
    
    # Gets rid of the tag from the array
    if arg in tags.keys():
        line.remove(arg)

    # Accounts for the other possible tags that aren't in the dictionary of valid tags
    if not valid and len(line) > 1 and (line[1].isupper() or "_" in line[1]):
        out = "<-- " + line[0] + "|" + line[1] + "|N|"
        del line[1]

    # Deletes the level from the array
    del line[0]

    # Adds the arguments to the output string
    for x in line:
        out += x + " "
    print(out.strip())

f.close()