##########################################################
## parser.py by Krishna Patel (kp)
## Created 1/19/23
## Last Modified: 2/2/23
##########################################################

"""
Purpose: This file will look through the JSON file and generate a CSV file usable by the EasyA program. 
================ Revision History ================
File created                         kp    1/19/23
Data parsing implementation          kp    1/19/23
completed                         
Update to exclude middle names of    kp    1/21/23
instructors                  
Update to write to file instead      kp    2/02/23
of to terminal.       
Clean up code                        kp    2/04/23
==================================================

"""
import json
import re


def formatLine(dataEntry, className):
    CSV_line = "" #initialize an empty string
        #all important data elements will be seperated with a comma to stay consistent with a CSV data format
    course = re.split('(\d+)', className) #split course name (ex. CS210) to seperate subject code and class number (ex. [CS, 210])
    CSV_line += course[0] + "," + course[1] + "," #add course subject and number to string
    CSV_line += dataEntry["TERM_DESC"]+ "," #add the term the course was offered to string
    CSV_line +=dataEntry["aprec"]+ "," #add percentage of A's to string
    CSV_line +=dataEntry["bprec"]+ "," #add percentage of B's to string
    CSV_line +=dataEntry["cprec"]+ "," #add percentage of C's to string
    CSV_line +=dataEntry["crn"]+ ","   #add course CRN to string
    CSV_line +=dataEntry["dprec"]+ "," #add percentage of D's to string
    CSV_line +=dataEntry["fprec"]+ "," #add percentage of F's to string
    if(len(dataEntry["instructor"])): #If the instructor name is valid it will be added to the string
        name = dataEntry["instructor"].split(",") #split instructor name at the ","
        CSV_line += name[0] + "," + name[1].split()[0] #add name to string, but split first and middle name at comma 
        #and only add first name to string
    else:
        """
        There was one course that had no instructor assigned, to handle this case the name assigned
        will be NULL for both the first and last name.
        """
        CSV_line += "NULL" + "," +"NULL"

    return CSV_line

def processFile(inputFile, outFile):
    """
    This function will open the input and output file, and will write the parsed data to the output file.
    """
    try:
        JSONfile = open(inputFile, "r") #open JSONfile in read mode and assign filestream to variable "JSONFile"
    except IOError: #if the file does not exist we will exit the program after printing an error
        print("Data file does not exist, please execute program again with real file.")
        exit()
    outputFile = open(outFile, "w") #open output file with filename "parsed_data.csv" in write mode
    #and assign filestream to variable "outputFile"
    data = json.load(JSONfile) #loads all data from JSONFile into a dictionary for easy lookup
    outputFile.write("subject, course number, term, aprec, bprec, cprec, crn, dprec, fprec, last, first\n") #write a CSV header to the output file
    for className in data: #Go through each class in the dataset
        for i in range(len(data[className])):
            """
            The JSON file grouped the same courses into one dictionary index, so we will go through each instance
            to ensure every time a course was offered is recorded.
            """
            dataEntry = data[className][i]
            CSV_line = formatLine(dataEntry, className)
            outputFile.write(CSV_line + "\n") #Write the line of data to the file.
    JSONfile.close() #close the JSON file
    outputFile.close() #close the output file
    return 0

if __name__ == "__main__":
    processFile("gradedata.js", "parsed_data.csv")