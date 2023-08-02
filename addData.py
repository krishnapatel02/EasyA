##########################################################
## addData.py by Krishna Patel (kp)
## Created 1/25/23
## Last Modified: 2/05/23
##########################################################

"""
Purpose: This file provides the implementation to allow a system administrator to update the
file of existing data. This file will open a new CSV file with data and add it to the 
existing CSV file. The case where a file may or may not have a file header is also handled.

================ Revision History ================
File created                         kp    1/25/23
User input and file replacement      kp    2/02/23
implemented
Added updating of faculty file       kp    2/04/23
Added clearing of terminal           kp    2/05/23
to make output easier to read
==================================================
"""
import os
clear = None
def clearTerminal():
    """
    A function to clear the terminal depending on what OS is being used.
    """
    if(os.name == "posix"):
        os.system("clear")
    else:
        os.system("cls")

def replaceData(newDataFile,currentDataFile,newFacultyFile,currentFacultyFile):
    """
    Replaces data in current files line by line.
    """
    print("Updating files") #print message indicating status
    for line in newDataFile: #go through new file
        currentDataFile.write(line) #write the lines to the existing file
    for line in newFacultyFile: #go through new file
        currentFacultyFile.write(line) #write the lines to the existing file

def userDataUpdate():
    """
    Handles user input for addData module.
    """
    clearTerminal() #clear terminal for easy readability
    newData = None #Initialize filestream to None
    newFaculty = None #initialize filestream to None
    confirmation = False #variable for confirmation of overwriting existing  data
    print("This program requires input to be in a CSV file in the following format: ")
    print("subject, course number, term, aprec, bprec, cprec, crn, dprec, fprec, last, first")
    print("The previous line must also be a header in the CSV file.")
    while(newData is None): #while the filestream is not valid we will continually loop through this block
        #ask user to input filename and strip the newline
        newFile = input("Please enter file name of new data (CSV file): ").strip()
        try:
            newData = open(newFile, "r") #try to open the file
        except IOError: #if there is an error, print an error message
            clearTerminal() #clear terminal for easy readability
            print("Filename is invalid")
    clearTerminal() #clear terminal for easy readability
    print("This program requires faculty file to be in a txt file in the following format: first,last")
    print("Separate each entry with a new line. For more information see user documentation")
    while(newFaculty is None): #while the filestream is not valid we will continually loop through this block
        #ask user to input filename and strip the newline
        newFacultyFile = input("Please enter file name of new faculty file: ").strip()
        try:
            newFaculty = open(newFacultyFile, "r") #try to open the file
        except IOError: #if there is an error, print an error message
            clearTerminal() #clear terminal for easy readability
            print("Filename is invalid, please try again")
    clearTerminal() #clear terminal for easy readability
    while(confirmation == False): #while a correct confirmation is not made loop through this block
        #receive user input and strip newline
        response = input("All data in current file and faculty file will be overwritten confirm this operation, Y to confirm, N to decline: ").strip()
        if(response == "Y"):# if  response is Y, set confirmation to true to leave loop
            confirmation = True
        elif(response == "N"): #if response is N, print message and exit program
            print("Exiting program, no changes made.")
            newData.close()
            newFaculty.close()
            exit()
        else:
            print("Response not valid.") #otherwise print a message since a valid response was not received
    data = open("parsed_data.csv", "w") #open data file to overwrite
    faculty = open("faculty.txt", "w")
    replaceData(newData, data, newFaculty, faculty) #call data to populate existing file
    newData.close() # close filestream
    data.close() #close filestream
    faculty.close() #close filestream
    newFaculty.close() #close filestream
    input("Finished. Press enter to exit.")
    return

if __name__ == "__main__":
    userDataUpdate()
    exit()