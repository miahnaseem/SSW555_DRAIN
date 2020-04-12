import sys
import datetime
import collections
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

fakeDates = ""


# formats the date into YYYY-MM-DD
def formatDate(date):
    newDate = date.split()
    newDate[1] = str(months[newDate[1]])
    return newDate[2] + "-" + newDate[1] + "-" + newDate[0]

# Checks to make sure all dates are before current date
def checkUS01():
    result = ""
    for row in indiTable:
        # removes headers and borders
        row.border = False
        row.header = False
        currID = row.get_string(fields=["ID"]).strip()
        currDate = datetime.datetime.today().date()
        # convert all individual dates from string to date type
        birthDate = datetime.datetime.strptime(row.get_string(fields = ["Birthday"]).strip(), '%Y-%m-%d').date()
        # compares birth date with current date
        if birthDate > currDate:
            result += "ERROR: INDIVIDUAL: US01: " + currID + ": Birth date " +str(birthDate) + " is after current date " + str(currDate) + "\n"
        # if the individual had died, compare the death date with current date
        if row.get_string(fields = ["Death"]).strip() != "NA":
            deathDate = datetime.datetime.strptime(row.get_string(fields = ["Death"]).strip(), '%Y-%m-%d').date()
            if deathDate > currDate:
                 result += "ERROR: INDIVIDUAL: US01: " + currID + ": Death date " +str(deathDate) + " is after current date " + str(currDate) + "\n"
    for row in famTable:
        # removes headers and borders
        row.border = False
        row.header = False
        # convert all family dates from string to date type
        marriageDate = datetime.datetime.strptime(row.get_string(fields = ["Married"]).strip(), '%Y-%m-%d').date()
        # compares marriage date with current date
        if marriageDate > currDate:
            result += "ERROR: INDIVIDUAL: US01: " + currID + ": Marriage date " +str(marriageDate) + " is after current date " + str(currDate) + "\n"
        # if the family had divorced, compare the divorce date with current date
        if row.get_string(fields = ["Divorced"]).strip() != "NA":
            divorceDate = datetime.datetime.strptime(row.get_string(fields = ["Divorced"]).strip(), '%Y-%m-%d').date()
            if divorceDate > currDate:
                result += "ERROR: INDIVIDUAL: US01: " + currID + ": Divorce date " +str(divorceDate) + " is after current date " + str(currDate) + "\n"
    return result

# Checks to make sure birth was before marriage
def checkUS02():
    result = ""
    for row in famTable:
        # removes headers and borders
        row.border = False
        row.header = False
        # converts marriageDate from string to date type
        marriageDate = datetime.datetime.strptime(row.get_string(fields = ["Married"]).strip(), '%Y-%m-%d').date()
        # gets husband and wife IDs
        husbID = row.get_string(fields = ["Husband ID"]).strip()
        wifeID = row.get_string(fields = ["Wife ID"]).strip()
        # gets birth date and converts from string to date type
        if 'BIRT' in indi[husbID]:
            husbBirth = datetime.datetime.strptime(formatDate(indi[husbID]["BIRT"]),'%Y-%m-%d').date()
        if 'BIRT' in indi[wifeID]:
            wifeBirth = datetime.datetime.strptime(formatDate(indi[wifeID]["BIRT"]),'%Y-%m-%d').date()      
        #compares birth date with marriage date
        if husbBirth > marriageDate:
            result += "ERROR: INDIVIDUAL: US02: " + husbID + ": Marriage date " +str(marriageDate) + " is before Birth date " + str(husbBirth) + "\n"   
        if wifeBirth > marriageDate:
            result += "ERROR: INDIVIDUAL: US02: " + wifeID + ": Marriage date " +str(marriageDate)+ " is before Birth date " + str(wifeBirth) + "\n"  
    return result 

# Checks to make sure birth occurs before death
def checkUS03():
    result = ""
    for row in indiTable:
        # removes headers and borders
        row.border = False
        row.header = False
        # converts birth date from string to date type
        birthDate = datetime.datetime.strptime(row.get_string(fields = ["Birthday"]).strip(), '%Y-%m-%d').date()
        currID = row.get_string(fields=["ID"]).strip() 
        if 'DEAT' in indi[currID]:
            deathDate = datetime.datetime.strptime(row.get_string(fields = ["Death"]).strip(), '%Y-%m-%d').date()
            if birthDate > deathDate:
                result += "ERROR: INDIVIDUAL: US03: " + currID + ": Death date " +str(deathDate) + " is before Birth date " + str(birthDate) + "\n"   
    return result   

# Checks to make sure marriage occurs before divorce
def checkUS04():
    result = ""
    for row in famTable:
        # strips borders and headers
        row.border = False
        row.header = False
        # checks if divorce occured
        if row.get_string(fields = ["Divorced"]).strip() != "NA" and row.get_string(fields = ["Married"]).strip() != "NA":
            marriageDate = datetime.datetime.strptime(row.get_string(fields = ["Married"]).strip(), '%Y-%m-%d').date()
            divorceDate = datetime.datetime.strptime(row.get_string(fields = ["Divorced"]).strip(), '%Y-%m-%d').date()
            # compares marriage and divorce date
            if divorceDate < marriageDate:
                result += "ERROR: FAMILY: US04: " + row.get_string(fields=["ID"]).strip() + ": Divorce date "+ str(divorceDate) + " is before marriage date " + str(marriageDate) + "\n"
    return result


# Checks to make sure marriages occur before deaths
def checkUS05():
    result = ""
    for row in famTable:
        # strips borders and headers
        row.border = False
        row.header = False
        if row.get_string(fields = ["Married"]).strip() != "NA":
            marriageDate = datetime.datetime.strptime(row.get_string(fields = ["Married"]).strip(), '%Y-%m-%d').date()
            # stores married couple's IDs
            husbID = row.get_string(fields = ["Husband ID"]).strip()
            wifeID = row.get_string(fields = ["Wife ID"]).strip()
            # if table has a record of the husband's death, compares the death date to the marriage date
            if 'DEAT' in indi[husbID]:
                husbDeath = datetime.datetime.strptime(formatDate(indi[husbID]["DEAT_DATE"]),'%Y-%m-%d').date()
                if marriageDate > husbDeath:
                    result += "ERROR: INDIVIDUAL: US05: " + husbID + ": Death date " +str(husbDeath) + " is before marriage date " + str(marriageDate) + "\n"
            # if table has a record of the wife's death, compares the death date to the marriage date
            if 'DEAT' in indi[wifeID]:
                wifeDeath = datetime.datetime.strptime(formatDate(indi[wifeID]["DEAT_DATE"]),'%Y-%m-%d').date()
                if marriageDate > wifeDeath:
                    result += "ERROR: INDIVIDUAL: US05: " + husbID + ": Death date " +str(wifeDeath) + " is before marriage date " + str(marriageDate) + "\n"  
    return result

# Checks to make sure all divorces happened before deaths
def checkUS06():
    result = ""
    for row in famTable:
        # removes headers and borders
        row.border = False
        row.header = False
        # if family has been divorced, converts divorce date from string to date type
        if row.get_string(fields = ["Divorced"]).strip() != "NA":
            divorceDate = datetime.datetime.strptime(row.get_string(fields = ["Divorced"]).strip(), '%Y-%m-%d').date()
            # Get divorced hubsand and wife ID
            husbID = row.get_string(fields = ["Husband ID"]).strip()
            wifeID = row.get_string(fields = ["Wife ID"]).strip()
            # if indi table has death record for husband, check if husband's death date is after divorce date
            if 'DEAT' in indi[husbID]:
                husbDeath = datetime.datetime.strptime(formatDate(indi[husbID]["DEAT_DATE"]),'%Y-%m-%d').date()
                if divorceDate > husbDeath:
                    result += "ERROR: INDIVIDUAL: US06: " + husbID + ": Death date " +str(husbDeath) + " is before divorce date " + str(divorceDate) + "\n"
            # if indi table has death record for wife, check if wife's death date is after divorce date
            if 'DEAT' in indi[wifeID]:
                wifeDeath = datetime.datetime.strptime(formatDate(indi[wifeID]["DEAT_DATE"]),'%Y-%m-%d').date()
                if divorceDate > wifeDeath:
                    result += "ERROR: INDIVIDUAL: US06: " + husbID + ": Death date " +str(wifeDeath) + " is before divorce date " + str(divorceDate) + "\n"  
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
            children = list(row.get_string(fields = ["Children"]).replace("[","").replace("]", "").replace(" ","").replace("'", "").strip().split(","))
            # loops through indiTable
            for rowI in indiTable:
                # removes headers and borders 
                rowI.border = False
                rowI.header = False
                # loops through children 
                for i in children:
                    iD = rowI.get_string(fields=["ID"]).strip()
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
            children = list(row.get_string(fields = ["Children"]).replace("['","").replace("']", "").replace(" ","").strip().split(","))
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

# Checks if there is any bigamy
def checkUS11():
    result = ""
    famTable.border = False
    famTable.header = False

    # Get a list of the husband and wife ids
    hCol = famTable.get_string(fields=["Husband ID"])
    wCol = famTable.get_string(fields=["Wife ID"])
    hCol = list(hCol.replace(" ", "").strip().split("\n"))
    wCol = list(wCol.replace(" ", "").strip().split("\n"))
    countH = []
    countW = []

    # Makes a list of people with 2 or more marriages
    for i in hCol:
        if i not in countH and hCol.count(i) > 1:
            countH.append(i)
    for i in wCol:
        if i not in countW and wCol.count(i) > 1:
            countW.append(i)

    # Find husbands that are committing bigamy
    for i in countH:
        mardates = {}
        divdates = {}
        deathdates = {}
        # Get the marriage, divorce, and death dates of the wives married to the husband committing bigamy
        for row in famTable:
            husbID = row.get_string(fields = ["Husband ID"]).replace(" ", "").strip()
            wifeID = row.get_string(fields = ["Wife ID"]).replace(" ", "").strip()
            if husbID == i:
                mardates[wifeID] = datetime.datetime.strptime(row.get_string(fields = ["Married"]).replace(" ", "").strip(), '%Y-%m-%d').date()
                if row.get_string(fields = ["Divorced"]).replace(" ", "").strip() != "NA":
                    divdates[wifeID] = datetime.datetime.strptime(row.get_string(fields = ["Divorced"]).replace(" ", "").strip(), '%Y-%m-%d').date()
                if "DEAT" in indi[husbID]:
                    deathdates[wifeID] = datetime.datetime.strptime(formatDate(indi[wifeID]["DEAT_DATE"]), '%Y-%m-%d').date()
        # Creates sorted lists of marriage dates and death/divorce dates in order to compare the dates
        marsort = list(mardates.values())
        marsort.sort()
        divsort = list(divdates.values())
        deathsort = list(deathdates.values())
        divdeath = divsort + deathsort
        divdeath.sort()
        # If there are no deaths or divorces, that means that the husband is married to multiple wives at the same time
        if len(divdeath) == 0:
            result += "ANOMALY: INDIVIDUAL: US11: Individual (" + i + ") married to multiple people at the same time\n"
        # If there are deaths and/or divorces, that means that the husband was widowed or divorced and then remarried
        # So you need to check whether there were two or more marriages that occurred at the same time frame
        else:
            j = 0
            k = 1
            while j < len(divdeath) and k < len(marsort):
                if divdeath[j] > marsort[k]:
                    result += "ANOMALY: INDIVIDUAL: US11: Individual (" + i + ") married to multiple people at the same time\n"
                    break
                j += 1
                k += 1

    # Find wives that are committting bigamy
    for i in countW:
        mardates = {}
        divdates = {}
        deathdates = {}
        # Get the marriage, divorce, and death dates of the husbands married to the wife committing bigamy
        for row in famTable:
            husbID = row.get_string(fields = ["Husband ID"]).replace(" ", "").strip()
            wifeID = row.get_string(fields = ["Wife ID"]).replace(" ", "").strip()
            if wifeID == i:
                mardates[husbID] = datetime.datetime.strptime(row.get_string(fields = ["Married"]).replace(" ", "").strip(), '%Y-%m-%d').date()
                if row.get_string(fields = ["Divorced"]).replace(" ", "").strip() != "NA":
                    divdates[husbID] = datetime.datetime.strptime(row.get_string(fields = ["Divorced"]).replace(" ", "").strip(), '%Y-%m-%d').date()
                if "DEAT" in indi[husbID]:
                    deathdates[husbID] = datetime.datetime.strptime(formatDate(indi[husbID]["DEAT_DATE"]), '%Y-%m-%d').date()
        # Creates sorted lists of marriage dates and death/divorce dates in order to compare the dates
        marsort = list(mardates.values())
        marsort.sort()
        divsort = list(divdates.values())
        deathsort = list(deathdates.values())
        divdeath = divsort + deathsort
        divdeath.sort()
        # If there are no deaths or divorces, that means that the wife is married to multiple husbands at the same time
        if len(divdeath) == 0:
            result += "ANOMALY: INDIVIDUAL: US11: Individual (" + i + ") married to multiple people at the same time\n"
        # If there are deaths and/or divorces, that means that the husband was widowed or divorced and then remarried
        # So you need to check whether there were two or more marriages that occurred at the same time frame
        else:
            j = 0
            k = 1
            while j < len(divdeath) and k < len(marsort):
                if divdeath[j] > marsort[k]:
                    result += "ANOMALY: INDIVIDUAL: US11: Individual (" + i + ") married to multiple people at the same time\n"
                    break
                j += 1
                k += 1
    return result
#Checks that parents are not too old
def checkUS12():
    result = ""
    # loops through famTable
    for row in famTable:
        # removes headers and borders
        row.border = False
        row.header = False
        # checks if they have children
        if row.get_string(fields = ["Children"]).strip() != "NA":
            # moves all children into a list
            children = list(row.get_string(fields = ["Children"]).replace("[","").replace("]", "").replace(" ","").replace("'", "").strip().split(","))
            # loops through indiTable
            for rowI in indiTable:
                # removes headers and borders 
                rowI.border = False
                rowI.header = False
                currAge = int(rowI.get_string(fields=["Age"]).strip(), 10)
                # loops through children 
                for i in children:
                    iD = rowI.get_string(fields=["ID"]).strip()
                    if iD == i:
                        childAge = int(rowI.get_string(fields=["Age"]).strip(), 10)
                        if childAge - currAge < 60:
                            result += "ANOMALY: FAMILY: US12: " + row.get_string(fields=["ID"]).strip() + " Parent is too old to have (" + iD + ")\n"
    return result

# Checks the siblings spacing
def checkUS13():
    result = ""
    i = 0
    for row in indiTable[:-1]:
        row.header = False
        row.border = False
        # sees what family the current individual is a child in
        childin = row.get_string(fields = ["Child"]).strip()
        # gets id of current individual
        childID = row.get_string(fields = ["ID"]).strip()
        # get birthday of current
        birthDate = datetime.datetime.strptime(row.get_string(fields = ["Birthday"]).strip(), '%Y-%m-%d').date()
        # loops through rest of the table
        for rw in indiTable[i+1:]:
            rw.header = False
            rw.border = False
            # sees what family the next individual is a child in
            nextchildin = rw.get_string(fields = ["Child"]).strip()
            # sees what family the next individual is a spouse in 
            nextDate = datetime.datetime.strptime(rw.get_string(fields = ["Birthday"]).strip(), '%Y-%m-%d').date()
            nextID = rw.get_string(fields = ["ID"]).strip()
            # sees if the the two individuals are children and spouses in the same family
            if childin != "NA" and childin == nextchildin and birthDate > nextDate:
                result += "ANOMALY: FAMILY: US13: " + childin + " Individual (" + childID + ") spacing is too large from sibling (" + nextID + ")\n"
        i += 1
    return result

# Checks to make sure no more than 5 children are born at a time
def checkUS14():
    result = ""
    famTable.header = False
    famTable.border = False
    for row in famTable:
        # Get the list of children
        children = children = row.get_string(fields = ["Children"]).replace(" ", "").replace("'", "").replace("[", "").replace("]", "").strip().split(",")
        # print(children)
        birthdays = {}
        for child in children:
            if child != "NA":
                bday = datetime.datetime.strptime(formatDate(indi[child]["BIRT"]), '%Y-%m-%d').date()
                if str(bday) in birthdays:
                    birthdays[str(bday)]+=1
                else:
                    birthdays[str(bday)] = 1

        for day in birthdays:
            if birthdays[day]>=5:
                result += "ANOMALY: FAMILY: US14: Family ("+row.get_string(fields=["ID"])+") has 5 or more children born on "+day +"\n"
    return result

# Checks to make sure no more than 15 children are in a family
def checkUS15():
    result = ""
    result = ""
    famTable.header = False
    famTable.border = False
    for row in famTable:
        # Get the list of children
        children = row.get_string(fields = ["Children"]).replace(" ", "").replace("'", "").replace("[", "").replace("]", "").strip().split(",")
        if len(children)>=15:
            result += "ANOMALY: FAMILY: US15: Family (" + row.get_string(fields=["ID"]) + ") has 15 or more children\n"
    return result

# Checks that all the males have the same last name in their family
def checkUS16():
    result = ""
    famTable.header = False
    famTable.border = False
    for row in famTable:
        # Get the husband's name to extract the last name
        husbName = row.get_string(fields = ["Husband Name"]).replace(" ", "").strip()
        # Get the list of children
        children = row.get_string(fields = ["Children"]).replace(" ", "").replace("'", "").replace("[", "").replace("]", "").strip().split(",")
        # Get the family last name
        lastName = husbName[husbName.index("/") + 1:-1]
        # Loops through each male child and check the last name
        for x in children:
            if x != "NA":
                if indi[x]["SEX"] == "M":
                    if indi[x]["NAME"][indi[x]["NAME"].index("/") + 1:-1] != lastName:
                        result += "ANOMALY: INDIVIDUAL: US16: Individual (" + str(x) + ") does not have a matching family last name\n"
    return result

# Checks to see if a parent marries a child
def checkUS17():
    result = ""
    i = 0
    for row in famTable[:-1]:
        row.header = False
        row.border = False
        # gets husbID of current row
        husbID = row.get_string(fields = ["Husband ID"]).strip()
        # gets wifeID of current row
        wifeID = row.get_string(fields = ["Wife ID"]).strip()
        # gets children from current row
        children = list(row.get_string(fields = ["Children"]).replace("['","").replace("']", "").replace(" ","").strip().split(","))
        # loops through rest of the table excluding current and previously accessed rows
        for rw in famTable[i+1:]:
            rw.header = False
            rw.border = False
            #gets husbID of next row
            nexthusbID = rw.get_string(fields = ["Husband ID"]).strip()
            #gets wifeID of next row
            nextwifeID = rw.get_string(fields = ["Wife ID"]).strip()
            # loops through children
            for iD in children:
                # checks if parent and child are married
                if husbID == nexthusbID and iD == nextwifeID:
                    result += "ANOMALY: FAMILY: US17: " + rw.get_string(fields = ["ID"]).strip() + ": Husband (" + husbID + ") marries Child (" + iD + ")\n"
                if wifeID == nextwifeID and iD == nexthusbID:
                    result += "ANOMALY: FAMILY: US17: " + rw.get_string(fields = ["ID"]).strip() + ": Wife (" + wifeID + ") marries Child (" + iD + ")\n"
        i += 1
    return result

# Checks to see if siblings marry each other
def checkUS18():
    result = ""
    i = 0
    for row in indiTable[:-1]:
        row.header = False
        row.border = False
        # sees what family the current individual is a child in
        childin = row.get_string(fields = ["Child"]).strip()
        # sees what family the current individual is a spouse in 
        spousein = row.get_string(fields = ["Spouse"]).strip()
        # gets id of current individual
        iD = row.get_string(fields = ["ID"]).strip()
        # loops through rest of the table
        for rw in indiTable[i+1:]:
            rw.header = False
            rw.border = False
            # sees what family the next individual is a child in
            nextchildin = rw.get_string(fields = ["Child"]).strip()
            # sees what family the next individual is a spouse in 
            nextspousein = rw.get_string(fields = ["Spouse"]).strip()
            nextiD = rw.get_string(fields = ["ID"]).strip()
            # sees if the the two individuals are children and spouses in the same family
            if childin == nextchildin and spousein == nextspousein and spousein != "NA" and childin != "NA":
                result += "ANOMALY: FAMILY: US18: " + nextspousein + ": Individual (" + iD + ") is married to sibling (" + nextiD + ")\n"
        i += 1
    return result

# Checks for marriages between first cousins
def checkUS19():
    result = ""
    for row in famTable:
        row.header = False
        row.border = False
        famID = row.get_string(fields = ["ID"]).strip()
        husbID = row.get_string(fields = ["Husband ID"]).strip()
        wifeID = row.get_string(fields = ["Wife ID"]).strip()
        # Check only happens if both husb and wife are children of families in GED file (need siblings for first cousins)
        if "FAMC" in indi[husbID]:
            husbFam = indi[husbID]["FAMC"]
            if "FAMC" in indi[wifeID]:
                wifeFam = indi[wifeID]["FAMC"]
                # Get id of parents of each spouse
                husbFamHusb = fam[husbFam]["HUSB"]
                husbFamWife = fam[husbFam]["WIFE"]
                wifeFamHusb = fam[wifeFam]["HUSB"]
                wifeFamWife = fam[wifeFam]["WIFE"]
                # Compare dict "FAMC" entry for each id to see if parents of each spouse are siblings (i.e. spouses are first cousins)
                # husband dad and wife dad siblings
                try:
                    if indi[husbFamHusb]["FAMC"] == indi[wifeFamHusb]["FAMC"]:
                        result += "ANOMALY: FAMILY: US19: " + famID + ": Individual (" + husbID + ") is married to first cousin (" + wifeID + ")\n"
                except:
                    pass
                # husband mom and wife mom siblings
                try:
                    if indi[husbFamWife]["FAMC"] == indi[wifeFamWife]["FAMC"]:
                        result += "ANOMALY: FAMILY: US19: " + famID + ": Individual (" + husbID + ") is married to first cousin (" + wifeID + ")\n"
                except:
                    pass
                # husband dad and wife mom siblings
                try:
                    if indi[husbFamHusb]["FAMC"] == indi[wifeFamWife]["FAMC"]:
                        result += "ANOMALY: FAMILY: US19: " + famID + ": Individual (" + husbID + ") is married to first cousin (" + wifeID + ")\n"
                except:
                    pass
                # husband mom and wife dad siblings
                try:
                    if indi[husbFamWife]["FAMC"] == indi[wifeFamHusb]["FAMC"]:
                       result += "ANOMALY: FAMILY: US19: " + famID + ": Individual (" + husbID + ") is married to first cousin (" + wifeID + ")\n"
                except:
                    pass
            else:
                pass
        else:
            pass
    return result

# Checks for marriages between aunts/uncles and nieces/nephews
def checkUS20():
    result = ""
    for row in famTable:
        row.header = False
        row.border = False
        famID = row.get_string(fields = ["ID"]).strip()
        husbID = row.get_string(fields = ["Husband ID"]).strip()
        wifeID = row.get_string(fields = ["Wife ID"]).strip()
        # Check only happens if both husb and wife are children of families in GED file (need siblings for aunts/uncles)
        if "FAMC" in indi[husbID]:
            husbFam = indi[husbID]["FAMC"]
            if "FAMC" in indi[wifeID]:
                wifeFam = indi[wifeID]["FAMC"]
                # Get id of parents of each spouse
                husbFamHusb = fam[husbFam]["HUSB"]
                husbFamWife = fam[husbFam]["WIFE"]
                wifeFamHusb = fam[wifeFam]["HUSB"]
                wifeFamWife = fam[wifeFam]["WIFE"]
                # Compare dict "FAMC" entry for each id to see if parents of spouse and spouse are siblings
                # husband dad and wife siblings
                try:
                    if indi[husbFamHusb]["FAMC"] == indi[wifeID]["FAMC"] and indi[husbFamHusb]["NAME"] != indi[wifeID]["NAME"]:
                        result += "ANOMALY: FAMILY: US20" + famID + ": Individual (" + husbID + ") is married to parent's sibling (" + wifeID + ")\n"
                except:
                    pass
                # husband mom and wife siblings
                try:
                    if indi[husbFamWife]["FAMC"] == indi[wifeID]["FAMC"] and indi[husbFamWife]["NAME"] != indi[wifeID]["NAME"]:
                        result += "ANOMALY: FAMILY: US20: " + famID + ": Individual (" + husbID + ") is married to parent's sibling (" + wifeID + ")\n"
                except:
                    pass
                # husband and wife mom siblings
                try:
                    if indi[husbID]["FAMC"] == indi[wifeFamWife]["FAMC"] and indi[husbID]["NAME"] != indi[wifeFamWife]["NAME"]:
                        result += "ANOMALY: FAMILY: US20: " + famID + ": Individual (" + husbID + ") is married to parent's sibling (" + wifeID + ")\n"
                except:
                    pass
                # husband and wife dad siblings
                try:
                    if indi[husbID]["FAMC"] == indi[wifeFamHusb]["FAMC"] and indi[husbID]["NAME"] != indi[wifeFamHusb]["NAME"]:
                       result += "ANOMALY: FAMILY: US20: " + famID + ": Individual (" + husbID + ") is married to parent's sibling (" + wifeID + ")\n"
                except:
                    pass 
    return result

# Checks that each husband and wife is the appropriate gender for the role
def checkUS21():
    result = ""
    for row in famTable:
        row.header = False
        row.border = False
        husbID = row.get_string(fields = ["Husband ID"]).strip()
        wifeID = row.get_string(fields = ["Wife ID"]).strip()
        if(indi[husbID]["SEX"] != "M"):
            result+= "ANOMALY: FAMILY: US21: "+ row.get_string(fields = ["ID"]).strip() + ": Husband ("+husbID+") is not marked as male\n"
        if(indi[wifeID]["SEX"] != "F"):
            result+= "ANOMALY: FAMILY: US21: "+ row.get_string(fields = ["ID"]).strip() + ": Wife ("+wifeID+") is not marked as female\n"

    return result

# Checks that each id used is unique
def checkUS22():
    result = ""
    # Initialize two lists, one for individual ids, and another for family related ids
    indiIDs = []
    famIDs = []
    # Iterate through indiTable checking each id
    for row in indiTable:
        row.header = False
        row.border = False
        currentID = row.get_string(fields = ["ID"]).strip()
        # If individual's id is already in the list, it is a duplicate
        if currentID in indiIDs:
            result+= "ERROR: INDIVIDUAL: US22: Individual's ID," + currentID + ", is a duplicate\n"
        # Otherwise add it to list
        else:
            indiIDs.append(currentID)
    # Iterate through famTable checking each id
    for row in famTable:
        row.header = False
        row.border = False
        famID = row.get_string(fields = ["ID"]).strip()
        husbID = row.get_string(fields = ["Husband ID"]).strip()
        wifeID = row.get_string(fields = ["Wife ID"]).strip()
        # If the family ID is already in the list, it is a duplicate
        # Otherwise add respective ID to the famIDs list
        if famID in famIDs:
            result+= "ERROR: FAMILY: US22: Family ID," + famID + ", is a duplicate\n"
        else:
            famIDs.append(famID)
    return result


# Checks that each individual has a unique name and birth date
def checkUS23():
    result = ""
    names = {} # keeps track of names we have seen, along with the IDs that have that name
    for row in indiTable:
        row.header = False
        row.border = False
        currentName = row.get_string(fields = ["Name"]).strip()
        currentBday = datetime.datetime.strptime(row.get_string(fields = ["Birthday"]).strip(), '%Y-%m-%d').date()
        currentId = row.get_string(fields = ["ID"]).strip()
        # if there is a duplicate name, compares the birthdates of those individuals
        if currentName in names:
            found = False # keeps track of whether or not a duplicate name has been found
            for ID in names[currentName]:
                birt = datetime.datetime.strptime(formatDate(indi[ID]["BIRT"]),'%Y-%m-%d').date()
                if birt == currentBday:
                    if not found:
                        result += "ERROR: INDIVIDUAL: US23: "+currentId+": Individual ("+currentId+") has the same name \""+currentName+"\" and birthdate "+str(currentBday)+" as other individual(s) ("+ID
                        found = True
                    else: # if there is more than one duplicate, will list all of them
                        result += ", "+ID
            if found:
                result += ")\n"
            names[currentName] = names[currentName] + [currentId]
        # adds new names to the list
        else:
            names[currentName] = [currentId]
    return result

# Checks if families are unique by spouse name and marriage date
def checkUS24():
    result = ""
    # Dict to store key of family ID and value of list of husband name, wife name, marriage date
    famData = {}
    for row in famTable:
        row.border = False
        row.header = False
        # FamId is key for famData
        # husbName, wifeName, and marrDate in list as value for famData to be compared
        famID = row.get_string(fields = ["ID"]).strip()
        husbName = row.get_string(fields = ["Husband Name"]).strip()
        wifeName = row.get_string(fields = ["Wife Name"]).strip()
        marrDate = fam[famID]["MARR"]
        famEntry = [husbName, wifeName, marrDate]
        famInfo = list(famData.values())
        # Checks if the family's entry is already in the list of values
        if famEntry in famInfo:
            # Get's the first instance of duplicate value within the famData dict
            otherFam = list(famData.keys())[list(famData.values()).index(famEntry)]
            result += "ANOMALY: FAMILY: US24: " + famID + ": Family has same husband name, wife name, and marriage date as family " + otherFam + "\n" 
        else:
            # else make new entry for fam
            famData[famID] = famEntry
    return result

def getFirstName(name):
    firstName = name[:name.index("/")]
    return firstName

# Checks that all children have unique first names and birthdays in each family
def checkUS25():
    result = ""
    famTable.header = False
    famTable.border = False
    for row in famTable:
        firstNames = []
        # Get the list of children
        children = row.get_string(fields = ["Children"]).replace(" ", "").replace("'", "").replace("[", "").replace("]", "").strip().split(",")
        # Loops through each child and adds their first name and birthday
        for child in children:
            if child != "NA":
                names = {}
                names["name"] = getFirstName(indi[child]["NAME"].replace(" ", "").strip())
                names["DOB"] = str(datetime.datetime.strptime(formatDate(indi[child]["BIRT"]), "%Y-%m-%d").date())
                firstNames.append(names)
        # Keeps track of the duplicate first names and birthdays
        seen = {}
        dupes = []
        for x in firstNames:
            if x["name"] not in seen:
                seen[x["name"]] = 1
            else:
                if seen[x["name"]] == 1:
                    dupes.append(x)
                seen[x["name"]] += 1
        # Building the result string
        for dupe in dupes:
            result += "ERROR: FAMILY: US25: Family " + row.get_string(fields = ["ID"]).replace(" ", "").strip() + " has multiple individuals with the same first name " + dupe["name"] + " and birthday " + dupe["DOB"] + "\n"
    return result

# Checks for corresponding entries in the families and individuals
def checkUS26():
	result = ""
	# A dictionary which will contain all individual IDs in the file
	indis = {}

	for indiRow in indiTable:
		# Each individual is added with a value of 0 to signify that they have not been found in a family
		indiRow.header = False
		indiRow.border = False
		indis[indiRow.get_string(fields = ["ID"]).strip()] = 0

	for famRow in famTable:
		famRow.header = False
		famRow.border = False
		# Looks for the husband of a family in the individual dictionary
		husbID = famRow.get_string(fields = ["Husband ID"]).strip()
		# If found, marks as such
		if husbID in indis:
			indis[husbID] = 1
		# If not found, adds an error, provided individual exists
		elif husbID != "NA":
			result += "ERROR: INDIVIDUAL: US26: Individual " + husbID + " appears in family ("+famRow.get_string(fields = ["ID"]).strip()+") but has no individual listing.\n"
		
		# Looks for the wife of a family and does the same
		wifeID = famRow.get_string(fields = ["Wife ID"]).strip()
		if wifeID in indis:
			indis[wifeID] = 1
		elif wifeID != "NA":
			result += "ERROR: INDIVIDUAL: US26: Individual " + wifeID + " appears in family ("+famRow.get_string(fields = ["ID"]).strip()+") but has no individual listing.\n"
		
		# Looks for all children of a family in the individual dictionary and does the same
		children = famRow.get_string(fields = ["Children"]).replace(" ", "").replace("'", "").replace("[", "").replace("]", "").strip().split(",")
		for child in children:
			if child in indis:
				indis[child] = 1
			elif child != "NA":
				result += "ERROR: INDIVIDUAL: US26: Individual " + child + " appears in a family ("+famRow.get_string(fields = ["ID"]).strip()+") but has no individual listing.\n"

	# After looping through the families, adds an error for individuals not in a family
	for indi in indis:
		if indis[indi] == 0:
				result += "ERROR: INDIVIDUAL: US26: Individual " + indi + " is listed but does not appear in a family.\n"

	return result

# Checks to make sure age is listed in the table
def checkUS27():
    result = ""
    for row in indiTable:
        row.header = False
        row.border = False
        # Get each respective individual's id and age
        indiID = row.get_string(fields = ["ID"]).strip()
        indiAge = row.get_string(fields = ["Age"]).strip()
        # If the string of the indiAge variable is empty, that means age is not listed on table
        if str(indiAge) == "":
            result += "ERROR: INDIVIDUAL: US27: Individual " + indiID + "does not have age listed in table.\n"
    return result

# Orders siblings by age
def checkUS28():
    result = "US28: Siblings from oldest to youngest:\n"
    famTable.header = False
    famTable.border = False
    for row in famTable:
        # arr stores dictionaries of the id and date of birth of the siblings
        arr = []
        result += "Family " + row.get_string(fields = ["ID"]).replace(" ", "").strip() + ": "
        # Get the list of children
        children = row.get_string(fields = ["Children"]).replace(" ", "").replace("'", "").replace("[", "").replace("]", "").strip().split(",")
        # Loops through each child and adds id and date of birth
        for child in children:
            if child != "NA":
                dates = {}
                dates["id"] = child
                dates["DOB"] = indi[child]["BIRT"]
                arr.append(dates)
        # Sort arr by the date of birth from oldest to youngest
        arr.sort(key = lambda x: datetime.datetime.strptime(formatDate(x["DOB"]), "%Y-%m-%d").date())
        # Get just the ids and store them in siblings
        siblings = []
        for dicts in arr:
            siblings.append(dicts["id"])
        # Build the result string
        for sibling in siblings:
            result += sibling + ", "
        if siblings:
            result = result[:-2]
        result += "\n"
    return result

# Lists deceased individuals
def checkUS29():
    result = "US29: Deceased:\n"
    # loops through indiTable
    for row in indiTable:
        # removes headers and borders
        row.header = False
        row.border = False
        # gets the value under the Death column
        dead = row.get_string(fields = ["Death"]).strip()
        # sees if the individual is dead or not
        if dead == 'NA':
            continue
        else:
            # adds individual's id, name, and death date to result if they have a death date
            result += row.get_string(fields = ["ID"]).strip() + " " + row.get_string(fields = ["Name"]).strip() + " " + dead + "\n"
    return result

# Lists individuals that are living and married
def checkUS30():
    result = "US30: Living and Married:\n"
    # loops through IndiTable
    for row in indiTable:
        # removes headers and borders
        row.header = False
        row.border = False
        # gets the ID of the individual
        iD = row.get_string(fields = ["ID"]).strip().replace("'", "")
        # gets the FamID of the family that the individual is a spouse in
        spouse = row.get_string(fields = ["Spouse"]).strip()
        # gets the value of the individuals death date if there is one
        dead = row.get_string(fields = ["Death"]).strip()
        # if the individual is not dead and they have a spouse then their name, id, and marriage date will be added to the result
        if dead == 'NA' and spouse != 'NA':
            result += iD + " " + row.get_string(fields = ["Name"]).strip() + " " + fam[spouse]["MARR"] + "\n"
    return result

# Lists individuals that are living single
def checkUS31():
    result = "US31: Living and Single:\n"
    # loops through IndiTable
    for row in indiTable:
        # removes headers and borders
        row.header = False
        row.border = False
        # gets the ID of the individual
        iD = row.get_string(fields = ["ID"]).strip().replace("'", "")
        # gets the FamID of the family that the individual is a spouse in
        spouse = row.get_string(fields = ["Spouse"]).strip()
        # gets the value of the individuals death date if there is one
        dead = row.get_string(fields = ["Death"]).strip()
        # if the individual is not dead and they have a spouse then their name and id will be added to the result
        if dead == 'NA' and spouse == 'NA':
            result += iD + " " + row.get_string(fields = ["Name"]).strip() + "\n"
    return result
    
# Lists individuals that have the same birthday
def checkUS32():
    result = "US32: Multiple birthdays:\n"
    birthday_list =[]
    # loops through IndiTable
    for row in indiTable:
        # removes headers and borders
        row.header = False
        row.border = False
        # gets the ID of the individual
        iD = row.get_string(fields = ["ID"]).strip().replace("'", "")
        bday = datetime.datetime.strptime(row.get_string(fields = ["Birthday"]).strip(), '%Y-%m-%d').date()
        birthday_list.append(str(bday))          
    result += str([item for item, count in collections.Counter(birthday_list).items() if count > 1]) + "\n"
    return result

# Lists orphans (individuals under 18 with both parents deceased)
def checkUS33():
    result = "US33: Orphans:\n"
    for row in indiTable:
        row.header = False
        row.border = False
        indiID = row.get_string(fields = ["ID"]).strip().replace("'", "")
        # Only list thoes under the age of 18
        age = int(row.get_string(fields=["Age"]).strip(), 10)
        if age < 18:
            # From the FAMC tag, get family ID
            # With family ID, get husbID ("Dad" ID) and wifeID ("Mom" ID)
            famID = row.get_string(fields = ["Child"]).strip()
            husbID = fam[famID]["HUSB"]
            wifeID = fam[famID]["WIFE"]
            # If both parents have "DEAT" value in dict, child is an orpahn
            if "DEAT" in indi[husbID] and "DEAT" in indi[wifeID]:
                result += indiID + " " + row.get_string(fields = ["Name"]).strip() + " " + "\n"
    return result

#List large age differences 
def checkUS34():
    result = "US34: Large Age Differences:\n"
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

        # Checks if married when the older spouse was more than twice as old as the younger spouse
        if husbAge > (wifeAge*2) or wifeAge > (husbAge*2):
            result += husbID + ", born on " + str(husbDate) + ", married "+ wifeID + ", born on "+ str(wifeDate)+ ", on "+ str(marriageDate) + ".\n"
    return result
    
#List recent births
def checkUS35():
    result = "US35: Recent Births:\n"
    # loops through indiTable
    for row in indiTable:
        # removes headers and borders
        row.header = False
        row.border = False
        # gets the value under the Birth column
        birth = row.get_string(fields = ["Birthday"]).strip()
        # adds individual's id, name, and birth date to result
        cDate = datetime.date.today()
        birthDate = datetime.datetime.strptime(birth, '%Y-%m-%d').date()
        if (cDate - birthDate).days <= 30 and (cDate - birthDate).days >= 0:
            result += row.get_string(fields = ["ID"]).strip() + " recently born on " + birth + "\n"
    return result

def checkUS36():
    result = "US36: Recent Deaths:\n"
    # loops through indiTable
    for row in indiTable:
        # removes headers and borders
        row.header = False
        row.border = False
        # gets the value under the Death column
        dead = row.get_string(fields = ["Death"]).strip()
        # sees if the individual is dead or not
        if dead == 'NA':
            continue
        else:
            # adds individual's id, name, and death date to result if they have a death date
            cDate = datetime.date.today()
            death = datetime.datetime.strptime(dead, '%Y-%m-%d').date()
            if (cDate - death).days <= 30 and (cDate - death).days >= 0:
                result += row.get_string(fields = ["ID"]).strip() + " recently passed away on " + dead + "\n"
    return result

def checkUS37():
    result = "US36: Recent Survivors:\n"
    # list of survivor's children
    schil = []
    # loops through indiTable
    for row in indiTable:
        # removes headers and borders
        row.header = False
        row.border = False
        # gets the value under the Death column
        dead = row.get_string(fields = ["Death"]).strip()
        # sees if the individual is dead or not
        if dead == 'NA':
            continue
        else:
            # finds current date
            cDate = datetime.date.today()
            # sets death date to type date
            death = datetime.datetime.strptime(dead, '%Y-%m-%d').date()
            # check sif death date is recent
            if (cDate - death).days <= 30:
                # gets their ID
                iD = indi[row.get_string(fields=["ID"]).strip()]
                # sees what family they are a spouse in
                famID = indi[row.get_string(fields = ["ID"]).strip()]["FAMS"]
                sID = ""
                # finds the survivor's spouse's id
                if fam[famID]["HUSB"] == iD:
                    sID = fam[famID]["WIFE"]
                else:
                    sID = fam[famID]["HUSB"]
                # checks if they're alive and adds their name and ID to result
                if "DEAT" not in indi[sID]:
                    result += sID + " " + indi[sID]["NAME"]
                # gets the children in that family
                children = fam[famID]["CHIL"]
                # sees if they are alive and adds it to the list of survivor's children
                for i in children:
                    if "DEAT" not in indi[i] and i not in schil:
                        schil.append(i)
    # adds survivor's children to result
    for j in schil:
        result += j + " " + indi[j]["NAME"] + "\n"
                
    return result

# List the living people with birthdays coming up within the next 30 days
def checkUS38():
    result = "US38: Upcoming Birthdays:\n"
    for row in indiTable:
        # Remove the header and border from the row
        row.header = False
        row.border = False
        # Check whether the person is dead or alive
        alive = row.get_string(fields = ["Alive"]).strip()
        if alive == "True":
            # Get today month and day
            today = datetime.datetime.strftime(datetime.date.today(), '%m-%d')
            # Get the person's birthday
            birth = row.get_string(fields = ["Birthday"]).strip()
            # Get only the person's birthday month and day
            bday = datetime.datetime.strftime(datetime.datetime.strptime(birth, '%Y-%m-%d'), '%m-%d')
            # Convert the strings into dates for calculations
            today = datetime.datetime.strptime(today, '%m-%d').date()
            birthday = datetime.datetime.strptime(bday, '%m-%d').date()
            person = row.get_string(fields = ["ID"]).strip()
            # Check if the birthday is within 30 days from today
            if (birthday - today).days <= 30 and (birthday - today).days >= 0:
                result += person + " has an upcoming birthday on " + bday + "\n"
    return result

# Lists the living couples who have anniversaries coming up within the next 30 days
def checkUS39():
    result = "US39: Upcoming Anniversaries:\n"
    for row in famTable:
        # Remove the header and border from the row
        row.header = False
        row.border = False
        # Check whether the couple is divorced
        divorced = row.get_string(fields = ["Divorced"]).strip()
        # Get the husband and wife IDs
        husbID = row.get_string(fields = ["Husband ID"]).strip()
        wifeID = row.get_string(fields = ["Wife ID"]).strip()
        # If they are still married and are both alive
        if divorced == "NA" and ("DEAT" not in indi[husbID]) and ("DEAT" not in indi[wifeID]):
            # Get todays month and day
            today = datetime.datetime.strftime(datetime.date.today(), '%m-%d')
            # Get the marriage date
            marriage = row.get_string(fields = ["Married"]).strip()
            mdate = datetime.datetime.strftime(datetime.datetime.strptime(marriage, '%Y-%m-%d'), '%m-%d')
            # Convert the strings into dates for calculations
            today = datetime.datetime.strptime(today, '%m-%d').date()
            anniversary = datetime.datetime.strptime(mdate, '%m-%d').date()
            family = row.get_string(fields = ["ID"]).strip()
            # Check if the anniversary is within 30 days from today
            if (anniversary - today).days <= 30 and (anniversary - today).days >= 0:
                result += family + " has an upcoming anniversary on " + mdate + "\n"
    return result

# Prints all illegitimate dates
def checkUS42():
	return fakeDates

# Flags help select which dict and where to input data
current = ""
which_dict = ""
dated_event = ""
date = False
ddate = False
children = []
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
            children.clear()
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
            if arg == "HUSB" or arg == "WIFE":
                fam[current][arg] = ' '.join(line)
            if arg == "CHIL":
                children.append(' '.join(line))
                curr_child = children[:]
                fam[current][arg] = curr_child

# gets current date
indiTable = PrettyTable()
indiTable.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
currentDate = datetime.date.today()
# Iterates through indi dict printing unique identifier and NAME in order
for key in indi:
    #formats birth date
    try:
    	birth = datetime.datetime.strptime(formatDate(indi[key]["BIRT"]), '%Y-%m-%d').date()
    except ValueError:
    	editedDate = formatDate(indi[key]["BIRT"]).split("-")
    	editedDate[2] = "1"
    	editedDate = "-".join(editedDate)
    	birth = datetime.datetime.strptime(editedDate, '%Y-%m-%d').date()
    	fakeDates+="ERROR: INDIVIDUAL: US42: "+key+" contains illegitimate birth date "+indi[key]["BIRT"]+" which may cause the date to appear incorrectly.\n"

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
        try:
        	death = datetime.datetime.strptime(formatDate(indi[key]["DEAT_DATE"]), '%Y-%m-%d').date()
        except ValueError:
        	editedDate = formatDate(indi[key]["DEAT_DATE"]).split("-")
        	editedDate[2] = "1"
        	editedDate = "-".join(editedDate)
        	death = datetime.datetime.strptime(editedDate, '%Y-%m-%d').date()
        	fakeDates+="ERROR: INDIVIDUAL: US42: "+key+" contains illegitimate death date "+indi[key]["DEAT_DATE"]+" which may cause the date to appear incorrectly.\n"
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
    try:
    	marry = datetime.datetime.strptime(formatDate(fam[key]["MARR"]), '%Y-%m-%d').date()
    except ValueError:
    	editedDate = formatDate(fam[key]["MARR"]).split("-")
    	editedDate[2] = "1"
    	editedDate = "-".join(editedDate)
    	marry = datetime.datetime.strptime(editedDate, '%Y-%m-%d').date()
    	fakeDates+="ERROR: FAMILY: US42: "+key+" contains illegitimate marriage date "+fam[key]["MARR"]+" which may cause the date to appear incorrectly.\n"

    # Gets the divorce date
    if "DIV" not in fam[key]:
        div = False
        divorce = "NA"
    else:
        div = True
        try:
        	divorce = datetime.datetime.strptime(formatDate(fam[key]["DIV"]), '%Y-%m-%d').date()
        except ValueError:
        	editedDate = formatDate(fam[key]["MARR"]).split("-")
        	editedDate[2] = "1"
        	editedDate = "-".join(editedDate)
        	divorce = datetime.datetime.strptime(editedDate, '%Y-%m-%d').date()
        	fakeDates+="ERROR: FAMILY: US42: "+key+" contains illegitimate divorce date "+fam[key]["DIV"]+" which may cause the date to appear incorrectly.\n"

    # Gets the children of the family
    childs = []
    for elem in fam[key]:
        if elem == "CHIL":
            childs = fam[key][elem]
    if not childs:
        children = "NA"
    else:
        children = childs

    # Makes the table
    famTable.add_row([key, marry, divorce, fam[key]["HUSB"], indi[fam[key]["HUSB"]]["NAME"], fam[key]["WIFE"], indi[fam[key]["WIFE"]]["NAME"], children])

print(famTable)


# print(checkUS01(), end = "")
# print(checkUS02(), end = "")
# print(checkUS03(), end = "")
# print(checkUS04(), end = "")
# print(checkUS05(), end = "")
# print(checkUS06(), end = "")
# print(checkUS07(), end = "")
# print(checkUS08(), end = "")
# print(checkUS09(), end = "")
# print(checkUS10(), end = "")
# print(checkUS11(), end = "")
# print(checkUS12(), end = "")
# print(checkUS13(), end = "")
# print(checkUS14(), end = "")
# print(checkUS15(), end = "")
# print(checkUS16(), end = "")
# print(checkUS17(), end = "")
# print(checkUS18(), end = "")
# print(checkUS19(), end = "")
# print(checkUS20(), end = "")
# print(checkUS21(), end = "")
# print(checkUS22(), end = "")
# print(checkUS23(), end = "")
# print(checkUS24(), end = "")
# print(checkUS25(), end = "")
# print(checkUS26(), end = "")
# print(checkUS27(), end = "")
# print(checkUS28(), end = "")
# print(checkUS29(), end = "")
# print(checkUS30(), end = "")
# print(checkUS31(), end = "")
# print(checkUS32(), end = "")
# print(checkUS33(), end = "")
# print(checkUS34(), end = "")
# print(checkUS35(), end = "")
# print(checkUS36(), end = "")
# print(checkUS37(), end = "")
# print(checkUS38(), end = "")
# print(checkUS39(), end = "")
# print(checkUS42(), end = "")

f.close()
