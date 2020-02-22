import sys
import datetime
from prettytable import PrettyTable
# Dictionary of all the valid tags and their corresponding level
tags = {
    "INDI": "0", "NAME": "1", "SEX": "1", "BIRT": "1", "DEAT": "1", "FAMC": "1", "FAMS": "1", "FAM": "0", "MARR": "1",
    "HUSB": "1", "WIFE": "1", "CHIL": "1", "DIV": "1", "DATE": "2", "HEAD": "0", "TRLR": "0", "NOTE": "0"
}

# Dictionary of the months for easy conversion from name to number
months = {
    "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6, "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12
}

# Dictionaries to save information about individuals or families
indi = {}

fam = {}

# formats the date into YYYY-MM-DD
def formatDate(date):
    newDate = date.split()
    newDate[1] = str(months[newDate[1]])
    return newDate[2] + "-" + newDate[1] + "-" + newDate[0]

# Checks to make sure birth was before marriage
def checkUS02():
    result = ""
    for row in famTable:
        # removes headers and borders
        row.border = False
        row.header = False
        # converts marriageDate from string to date type
        marriageDate = datetime.datetime.strptime(row.get_string(fields = ["Married"]).strip(), '%Y-%m-%d').date()
        husbID = row.get_string(fields = ["Husband ID"]).strip()
        wifeID = row.get_string(fields = ["Wife ID"]).strip()
        if 'BIRT' in indi[husbID]:
            husbBirth = datetime.datetime.strptime(formatDate(indi[husbID]["BIRT_DATE"]),'%Y-%m-%d').date()
        if 'BIRT' in indi[wifeID]:
            wifeBirth = datetime.datetime.strptime(formatDate(indi[wifeID]["BIRT_DATE"]),'%Y-%m-%d').date()      
        if husbBirth > marriageDate:
            result += "ERROR: INDIVIDUAL: US02: " + husbID + ": Marriage is before Birth date " + husbBirth + "\n"   
        if wifeBirth > marriageDate:
            result += "ERROR: INDIVIDUAL: US02: " + wifeID + ": Marriage is before Birth date " + wifeBirth + "\n"  
    return result    

# Checks if anyone was or is more than 150 years old
def checkUS07():
    result = ""
    for row in indiTable:
        # Get rid of the border and header of the pretty table
        row.border = False
        row.header = False
        # Get each relevant data from the pretty table
        currID = row.get_string(fields=["ID"]).strip()
        currAge = int(row.get_string(fields=["Age"]).strip(), 10)
        currBirth = row.get_string(fields=["Birthday"]).strip()
        currDeath = row.get_string(fields=["Death"]).strip()
        # Check age and death status
        if currAge >= 150:
            if currDeath == "NA":
                result += "ERROR: INDIVIDUAL: US07: " + currID + ": More than 150 years old - Birth date " + currBirth + "\n"
            else:
                result += "ERROR: INDIVIDUAL: US07: " + currID + ": More than 150 years old at death - Birth " + currBirth + ": Death " + currDeath + "\n"
    return result

#checks to see if couple has children before they are married
def checkUS08():
    result = ""
    # loops through famTable
    for row in famTable:
        # removes headers and borders
        row.border = False
        row.header = False
        # converts marriageDate from string to date type
        marriageDate = datetime.datetime.strptime(row.get_string(fields = ["Married"]).strip(), '%Y-%m-%d').date()
        # checks if they have children
        if row.get_string(fields = ["Children"]).strip() != "NA":
            # moves all children into a list
            children = list(row.get_string(fields = ["Children"]).replace("[","").replace("]", "").strip().split(","))
            # loops through indiTable
            for rowI in indiTable:
                # removes headers and borders 
                rowI.border = False
                rowI.header = False
                # loops through children 
                for i in children:
                    iD = "\'" + rowI.get_string(fields=["ID"]).strip() + "\'"
                    if iD == i:
                        # compares marriage and birth date
                        birthDate = datetime.datetime.strptime(rowI.get_string(fields = ["Birthday"]).strip(), '%Y-%m-%d').date()
                        if birthDate < marriageDate:
                            result += "ANOMALY: FAMILY: US08: " + row.get_string(fields=["ID"]) + ": Child (" + iD.replace("'","") + ") born " + rowI.get_string(fields = ["Birthday"]).strip() + " before marriage on " + row.get_string(fields = ["Married"]).strip() + "\n"
    return result
# checks to see if child's birth occurs after death of at least one parent
def checkUS09():
    result = ""
    #loops through famTable
    for row in famTable:
        #removes headers and borders
        row.border = False
        row.header = False
        #gets husband and wife id
        husbID = row.get_string(fields = ["Husband ID"]).strip()
        wifeID = row.get_string(fields = ["Wife ID"]).strip()
        husbDeath = ""
        wifeDeath = ""
        # checks and defines husband and wife death
        if 'DEAT' in indi[husbID]:
            husbDeath = datetime.datetime.strptime(formatDate(indi[husbID]["DEAT_DATE"]),'%Y-%m-%d').date()
        if 'DEAT' in indi[wifeID]:
            wifeDeath = datetime.datetime.strptime(formatDate(indi[wifeID]["DEAT_DATE"]),'%Y-%m-%d').date()
        if row.get_string(fields = ["Children"]).strip() != "NA":
            # moves all children into a list
            children = list(row.get_string(fields = ["Children"]).replace("[","").replace("]", "").strip().split(","))
            for i in children:
                j = i.replace("'","")
                # gets child's birth date
                birth = datetime.datetime.strptime(formatDate(indi[j]["BIRT"]), '%Y-%m-%d').date()
                # checks to see if birth occurs after death of parent
                if wifeDeath != "" and husbDeath != "" and birth > wifeDeath and birth > husbDeath:
                    result += "ERROR: FAMILY: US09: " + row.get_string(fields = ["ID"]).strip() + ": Birthday of (" + j + ") on " + str(birth) + " after husband's (" + husbID + ") death on " + str(husbDeath) + " and wife's (" + wifeID + ") death on " + str(wifeDeath) + "\n"
                elif wifeDeath != "" and birth > wifeDeath:
                    result += "ERROR: FAMILY: US09: " + row.get_string(fields = ["ID"]).strip() + ": Birthday of (" + j + ") on " + str(birth) + " after wife's (" + wifeID + ") death on " + str(wifeDeath) + "\n"
                elif husbDeath != "" and birth > husbDeath:
                    result += "ERROR: FAMILY: US09: " + row.get_string(fields = ["ID"]).strip() + ": Birthday of (" + j + ") on " + str(birth) + " after husband's (" + husbID + ") death on " + str(husbDeath) + "\n"
    return result

# Checks if anyone was married before they were 14 years old 
def checkUS10():
    result = ""
    for row in famTable:
        # Get rid of the border and header of the pretty table
        row.border = False
        row.header = False

        # Gets the relevant data from the pretty table
        marriageDate = datetime.datetime.strptime(row.get_string(fields = ["Married"]).strip(), '%Y-%m-%d').date()
        husbID = row.get_string(fields = ["Husband ID"]).strip()
        wifeID = row.get_string(fields = ["Wife ID"]).strip()
        husbDate = datetime.datetime.strptime(formatDate(indi[husbID]["BIRT"]), '%Y-%m-%d').date()
        wifeDate = datetime.datetime.strptime(formatDate(indi[wifeID]["BIRT"]), '%Y-%m-%d').date()

        # Calculates the age when the husband and wife got married
        husbAge = (marriageDate - husbDate).days // 365
        wifeAge = (marriageDate - wifeDate).days // 365

        # Checks if either the husband and wife married before they were 14 years old
        if husbAge < 14 and wifeAge < 14:
            result += "ANOMALY: FAMILY: US10: " + row.get_string(fields = ["ID"]).strip() + ": Husband (" + husbID + ") and Wife (" + wifeID + ") married before the age of 14\n"
        elif husbAge < 14:
            result += "ANOMALY: FAMILY: US10: " + row.get_string(fields = ["ID"]).strip() + ": Husband (" + husbID + ") married before the age of 14\n"
        elif wifeAge < 14:
            result +=  "ANOMALY: FAMILY: US10: " + row.get_string(fields = ["ID"]).strip() + ": Wife (" + wifeID + ") married before the age of 14\n"
    return result

# Flags help select which dict and where to input data
current = ""
which_dict = ""
dated_event = ""
date = False
ddate = False
f = open("testFile.ged", "r")
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

    # Adds tag and information in tag under respect current individual entry
    # Dated events are stored and entered when date flag raised
    if which_dict == "INDI" and arg != "INDI" and valid is True:
        if date is True:
            indi[current][dated_event] = ' '.join(line)
            date = False
        # As DEAT has argument "Y", add extra indi entry for death date
        elif ddate is True:
            indi[current]["DEAT_DATE"] = ' '.join(line)
            ddate = False
        elif arg == "DEAT":
            ddate = True
            indi[current][arg] = ' '.join(line)
        elif arg == "BIRT":
            date = True
            dated_event = arg
        else:
            indi[current][arg] = ' '.join(line)
    # Dated events are stored and entered when date flag raised
    # Adds tag and information in tag under respective current family entry
    if which_dict == "FAM" and arg != "FAM" and valid is True:
        if date is True:
            fam[current][dated_event] = ' '.join(line)
            date = False
        if arg == "MARR" or arg == "DIV":
            date = True
            dated_event = arg
        else:
            if arg == "HUSB" or arg == "WIFE" or arg == "CHIL":
                fam[current][arg] = ' '.join(line)


# gets current date
indiTable = PrettyTable()
indiTable.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
currentDate = datetime.date.today()
# Iterates through indi dict printing unique identifier and NAME in order
for key in indi:
    
    #formats birth date
    birth = datetime.datetime.strptime(formatDate(indi[key]["BIRT"]), '%Y-%m-%d').date()
    #sets the values for alive and death columns
    if "DEAT" not in indi[key]:
        alive = True
        death = "NA"
    else:
        alive = False
        death = indi[key]["DEAT_DATE"]
    #calculates age
    #if the person is alive, the age will be calculated using  current date - birth date
    if alive:
        age = (currentDate - birth).days//365
    #if they're dead, the age will be calculated using death date - birth date
    #also death date variable is made to put into table
    else:
        death = datetime.datetime.strptime(formatDate(death), '%Y-%m-%d').date()
        age = (death - birth).days//365

    if "FAMS" in indi[key]:
        spouse = indi[key]["FAMS"]
    else:
        spouse = "NA"
    if "FAMC" in indi[key]:
        child = indi[key]["FAMC"]
    else:
        child = "NA"
    indiTable.add_row([key, indi[key]["NAME"],  indi[key]["SEX"], birth, age, alive, death, child, spouse])

print(indiTable)

# Makes a prettytable with the following fields
famTable = PrettyTable()
famTable.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
# Iterates through fam dict to get the necessary information to use in the prettytable
for key in fam:
    # Gets the marriage date
    marry = datetime.datetime.strptime(formatDate(fam[key]["MARR"]), '%Y-%m-%d').date()

    # Gets the divorce date
    if "DIV" not in fam[key]:
        div = False
        divorce = "NA"
    else:
        div = True
        divorce = datetime.datetime.strptime(formatDate(fam[key]["DIV"]), '%Y-%m-%d').date()

    # Gets the children of the family
    childs = []
    for elem in fam[key]:
        if elem == "CHIL":
            childs.append(fam[key][elem])
    if not childs:
        children = "NA"
    else:
        children = childs
    
    # Makes the table
    famTable.add_row([key, marry, divorce, fam[key]["HUSB"], indi[fam[key]["HUSB"]]["NAME"], fam[key]["WIFE"], indi[fam[key]["WIFE"]]["NAME"], children])

print(famTable)

print(checkUS02(), end = "")
print(checkUS07(), end = "")
print(checkUS08(), end = "")
print(checkUS09(), end = "")
print(checkUS10(), end = "")

f.close()