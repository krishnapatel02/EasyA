##########################################################
## search.py by Krishna Patel (kp)
## Created 1/21/23
## Last Modified: 2/5/23
##########################################################

"""
Purpose: This file provides the search implementation to allow the student interface to find the 
relavant information needed to generate a graph. This file is expected to receive a CSV file
through the buildMaps function to return a dictionary lookup table tiered in order by subject,
course level, course number, last name of instructor, first name of instructor. 
The instructorSearch function will receive the parameters subject, level, and course number. If level or course
number are negative they will be ignored in the search. 


================ Revision History ================
File created                         kp    1/21/23
Dictionary building added            kp    1/21/23
Search implementation written        kp    1/21/23
Bug where counter variables not      kp    1/21/23
reset in search loops fixed
More error handling added and        kp    1/25/23
keyError in dictionary fixed
Added a filter for faculty           kp    1/30/23
Added more descriptive error         kp    1/31/23
constants
Added looking at grades by class     kp    1/31/23
number
Added more comments                  kp    2/04/23
Added error checking for a course    kp    2/05/23
level that is empty.
==================================================

"""

import csv

subjectMap = {}  # map[subject][last][first] = number of courses taught
instructorMap = {}  # map[subject][level][course #][last][first] = [[grades], [grades], ..., [grades]]
# subject map will keep track of the grades
# instructor map will keep track of classes taught per professor by subject

SUBJECT_ERROR = -1 #Will be returned if a subject cannot be found
LEVEL_ERROR = -2 #Will be returned if a level cannot be found in a subject
CLASSNUM_ERROR = -3 #Will be returned if a course number cannot be found in a subject level



def buildMaps(filename, subjectMap, instructorMap):
    """                                                                                               
    This function builds the dictionaries required for the search to function. It builds two maps 
    one for subjects that keep track of how many courses an instructor has taught, and one for    
    keeping track of the grades an instructor has assigned for every course they have taught.     
    """

    fields = [] #holds header of the CSVFile
    with open(filename, "r") as csvfile:
        csvread = csv.reader(csvfile) #returns an iterator that will allow reading of the CSV file line by line
        fields = next(csvread) #To advance and skip header of csv file
        for row in csvread: #Go through every row of the data file
            if row[0] not in subjectMap: #if the subject id not in the dictionary add it
                levels = {100: {}, 200: {}, 300: {}, 400: {}, 500: {}, 600: {}, 700: {}} #create levels for each subject
                subjectMap[row[0]] = levels #map levels to the subject
                classNumber = int(row[1]) #set classNumber variable
                level = ((classNumber // 100) * 100) #generate level from the course number
                last = row[9].lower() #assign last name of instructor to variable
                first = row[10].lower() #assign first name of instructor to variable
                subjectMap[row[0]][level][classNumber] = {last: {first: [[float(row[3]), float(row[4]), float(row[5]), float(row[7]), float(row[8])]]}} #Assign instructor to a course with their grades
                instructorMap[row[0]] = {row[9]: {row[10]: 1}} #Add instructor to instuctorMap
            else: #if the subject code is in the dictionary
                subject = row[0] #set subject variable to subject code
                number = int(row[1]) #set number to course number
                grades = [float(row[3]), float(row[4]), float(row[5]), float(row[7]), float(row[8])] #make list of an instructor's grades
                last = row[9].lower() #set last name to variable
                first = row[10].lower() #set first name to variable
                level = (number // 100) * 100 #generate level from class number
                if (number in subjectMap[subject][level]): #if the course number is already in the dictionary for a subject
                    if (last in subjectMap[subject][level][number]): #if an instructor's last name is in the dictionary
                        if (first in subjectMap[subject][level][number][last]): #if instructor's last name is in the dictionary
                            #the last names and first names are in seperate tiers to account for 
                            #two instructors sharing the same last name in a particular department
                            subjectMap[subject][level][number][last][first].append(grades) #add grades to existing instructor
                        else:
                            subjectMap[subject][level][number][last].update({first: [[grades]]}) #add first name and corresponding grades
                    else:
                        subjectMap[subject][level][number].update({last: {first: [grades]}}) #add last name, first name, and corresponding grades
                else:
                    subjectMap[subject][level].update({number: {last: {first: [grades]}}}) #add course number, last name, first name, and grades

                #code below updates number of courses an instructor has taught
                if (last in instructorMap[subject]): # if an instructor's last name is in the dictionary of instructors in a particular subject
                    if (first in instructorMap[subject][last]): # if an instructor's first name is already in the dictionary 
                        instructorMap[subject][last][first] += 1 #increment by 1 to add a class taught if all conditions above are met
                    else:
                        instructorMap[subject][last].update({first: 1}) #add instructor to map and set classes taught to 1
                else:
                    instructorMap[subject].update({last: {first: 1}}) #add instructor to map and set classes taught to 1


buildMaps("parsed_data.csv", subjectMap, instructorMap) #build the maps needed for search module to function


def AddList(gradeList, data):
    """
    #Takes a list of data and adds it to the existing 
    #gradeList which will later be used for averaging.
    """
    if (len(gradeList) != len(data)):
        return -1 #we cannot add lists if they are not of the same size, so we terminate with an error
    else:
        for i in range(len(data)):
            gradeList[i] += data[i]
            #go through data list and add each index to corresponding index in gradeList


def getFacultyList(fileName="faculty.txt"):
    """
    Creates a list of all faculty members from the webscraper's output. 
    """
    f = open(fileName) #Open file with name from parameter "fileName"
    faculty = [] #initialize list of faculty
    for line in f: #go through each line in faculty file
        strippedLine = line.strip() #strip line for "\n"
        splitName = strippedLine.split(",")  # Split name into [first, last] at char ","
        fullName = splitName[1] + ", " + splitName[0] #full name is "last, first" to match data in dictionary
        faculty.append(fullName.lower()) #append lower case name to faculty list
    f.close()
    return faculty #return the populated faculty list


def isFaculty(instructorName: str, facultyList):
    """Returns whether an instructor is faculty"""
    return (instructorName in facultyList)


def avgList(gradeList, count):
    """Averages grade list by dividing each percentage by count.
    Count is the number of classes taught.
    """
    for i in range(len(gradeList)): #go through grade list
        gradeList[i] = round((gradeList[i] / count), 2) #set grade in gradeList to averaged grade


def instructorSearch(subject, level, classNum, facultyList):
    """
    Performs main search to find grade averages by instructor for a given subject, class level, or class number.
    Returns search results as a dictionary in the following form:
    {"last, first": ([%A's, %B's, %C's, %D's, %F's], courses taught, if instructor is faculty)}
    """
    level = int(level) #assign level to variable
    classNum = int(classNum) #assign course number to variable
    dictionaryIndex = None #Initialize index into dictionary
    resultList = {} #dictionary containing results initialized
    count = 0 #set count of courses taught to 0
    grades = [0.0, 0.0, 0.0, 0.0, 0.0] #initialize an array of grades[%A, %B, %C, %D, %F]
    if (subject in subjectMap):
        dictionaryIndex = subjectMap[subject] #Set index into dictionary if a subject is found 
    else:
        return SUBJECT_ERROR  # otherwise return error because subject does not exist
    if (level > 0 and classNum > 0): #if level and class number are specified do this case
        if(len(subjectMap[subject][level]) == 0): #if the level is empty in the dictionary, no classes exist
            return LEVEL_ERROR #return the error
        if(classNum not in dictionaryIndex[level]): #check if course number is valid
            return CLASSNUM_ERROR
        dictionaryIndex = dictionaryIndex[level][classNum] #If all conditions are valid set index to level and class number into a subject
        for instructorLast in dictionaryIndex: #loop through last names of professors teaching a course number
            for instructorFirst in dictionaryIndex[instructorLast]: #loop through first names of professors who share the same last name
                for classGrades in dictionaryIndex[instructorLast][instructorFirst]: #loop through grades of a professor teaching a course 
                    AddList(grades, classGrades) #add the list of grades so they can be averaged
                    count += 1 #increase the count of classes the summed grades represent
                avgList(grades, count) #average the grades in the list
                instructorName = instructorLast + ", " + instructorFirst #Concatonate name to be in the form "Last, First"
                fac = isFaculty(instructorName, facultyList) #Determine if the instructor is a faculty member
                resultList[instructorName] = (grades, instructorMap[subject][instructorLast][instructorFirst], fac) #set index into dictionary with professor's grades, courses taught, and whether or not they are a faculty member
            count = 0 #reset count for next loop iteration
            grades = [0.0, 0.0, 0.0, 0.0, 0.0] #reset count for next loop iteration
        return resultList #once all courses have been looked at return list containing all relevant grade data
    elif (level > 0):  # If only a level is specified do this case
        if(len(dictionaryIndex[level]) == 0): #if the level is empty in the dictionary, no classes exist
            return LEVEL_ERROR #return the error
        dictionaryIndex = dictionaryIndex[level] #update index if level is in a subject
        for classNum in dictionaryIndex:
            for instructorLast in dictionaryIndex[classNum]:
                for instructorFirst in dictionaryIndex[classNum][instructorLast]:
                    for classGrades in dictionaryIndex[classNum][instructorLast][instructorFirst]: #loop through all possible classes and instructors in a subject level
                        AddList(grades, classGrades) #for each instructor add up the grades of the courses they have taught
                        count += 1 #increment count 
                    avgList(grades, count) #average over the count of grades
                    instructorName = instructorLast + ", " + instructorFirst #concatenate instructor name
                    fac = isFaculty(instructorName, facultyList) #check if instructor is a faculty member
                    if (instructorName in resultList): #if the instructor is already in our result dictionary we need to update it
                        oldGrades = resultList[instructorName][0] # save the current grades 
                        AddList(grades, oldGrades) #add the old grades to the new ones
                        avgList(grades, 2) #average the grades over 2 
                        resultList[instructorName] = (grades, instructorMap[subject][instructorLast][instructorFirst], fac) # set result to updated grades
                    else:
                        resultList[instructorName] = (
                        grades, instructorMap[subject][instructorLast][instructorFirst], fac) #if it's not in the result list we just add it to the dictionary
                count = 0 #reset count
                grades = [0.0, 0.0, 0.0, 0.0, 0.0] #reset list
        return resultList #return result
    else:  # whole subject
        for levelIndex in dictionaryIndex: # go through all levels for a subject
            if (dictionaryIndex.get(levelIndex) != None): #if the level is valid look through it
                for classNum in dictionaryIndex[levelIndex]: #go through all course numbers in a level
                    for instructorLast in dictionaryIndex[levelIndex][classNum]: # go through last names of all professors 
                        for instructorFirst in dictionaryIndex[levelIndex][classNum][instructorLast]: #go through first names 
                            for classGrades in dictionaryIndex[levelIndex][classNum][instructorLast][instructorFirst]: #go through grades of specific instructor
                                AddList(grades, classGrades) #Add class grades to total grades
                                count += 1 #increment count
                            avgList(grades, count) #average grades over count
                            instructorName = instructorLast + ", " + instructorFirst #concatanate name
                            fac = isFaculty(instructorName, facultyList) #check if instructor is faculty
                            if (instructorName in resultList): #if if instructor is already in list 
                                oldGrades = resultList[instructorName][0] #copy old grades
                                AddList(grades, oldGrades) #add old grades to new ones
                                avgList(grades, 2) # average the grades 
                                resultList[instructorName] = (
                                grades, instructorMap[subject][instructorLast][instructorFirst], fac) #update result dictionary
                            else:
                                resultList[instructorName] = (
                                grades, instructorMap[subject][instructorLast][instructorFirst], fac) #add grades and instructor to result dictionary
                            count = 0 #reset count
                            grades = [0.0, 0.0, 0.0, 0.0, 0.0] #reset grades
            else:
                continue
        return resultList # return result data

def classSearch(subject, level, facultyList, facultyLookup=False):
    """
    This function will return the grade data by class level.
    For example, if you pass through the subject as MATH, and level as 200, you will get the 
    grade percentages for course numbers such as 231, 232, 251, etc.
    Returns search results as a dictionary in the following form:
    {"Course number": ([%A's, %B's, %C's, %D's, %F's], number of classes, if search was only faculty)}
    """
    resultList = {} #initialize dictionary that will be returned containing data
    count = 0 #initialize count for number of grades for a course number 
    grades = [0.0, 0.0, 0.0, 0.0, 0.0] #initialize an index of grades to 0
    if(level < 100):
        return LEVEL_ERROR
    if(subject in subjectMap): #check if the subject is valid
        if(level in subjectMap[subject]): #Check if this course level exists for a valid subject
            if(len(subjectMap[subject][level]) == 0): #if the level is empty in the dictionary, no classes exist
                return LEVEL_ERROR #return the error
            for classNum in subjectMap[subject][level]: #go through all course numbers in a particular level of a subject
                    for instructorLast in subjectMap[subject][level][classNum]: #go through all last names of instructors who teach a course
                        for instructorFirst in subjectMap[subject][level][classNum][instructorLast]: #
                            instructorName = instructorLast + ", " + instructorFirst #concatenate first and last name as "last, first"
                            for classGrades in subjectMap[subject][level][classNum][instructorLast][instructorFirst]: #go through all class grades for each instructor 
                                if(facultyLookup and instructorName not in facultyList): #if a member is not faculty and that option was specified skip this instructor
                                    continue
                                AddList(grades, classGrades) #add grades to list of grades for that course number
                                count += 1 #increment number of times class was offered 
                            if(not facultyLookup or (facultyLookup and instructorName in facultyList)):
                                 avgList(grades, count) #average the grades by the number of times the class was offered
                            if ((str(classNum)) in resultList): #if the class is already in the results the results need to be added up
                                if(not facultyLookup or (facultyLookup and instructorName in facultyList)): #
                                    avgList(grades, count) #average the grades by courses taught
                                    oldGrades = resultList[str(classNum)][0] #save old grades
                                    AddList(grades, oldGrades) #add new old grades two new ones
                                    avgList(grades, 2) #average the grades
                                    prevClassCount = resultList[str(classNum)][1] #save previous class count
                                    resultList[str(classNum)] = (grades, prevClassCount + 1, facultyLookup) #save with new grades and increment the class count
                            else:
                                if(not facultyLookup or (facultyLookup and instructorName in facultyList)):
                                    resultList[str(classNum)] = (
                                    grades, 1, facultyLookup) #add class to faculty list
                                else:
                                    resultList[str(classNum)] = (
                                    grades, 0, facultyLookup) #if a class exists but no faculty teaches it, we will set it to 0 to show that
                            count = 0
                            grades = [0.0, 0.0, 0.0, 0.0, 0.0]
            return resultList
        else: #if the level is not valid, we return an error              
            return LEVEL_ERROR
    else: #if the subject is not valid, we return an error 
        return SUBJECT_ERROR
    

if __name__ == "__main__":
    """Test code for when module is executed independently.
    Will not be called when program is run through the main module.
    """
    faculty = getFacultyList("faculty.txt")
    #print(faculty)
    print(classSearch("WR", 200, faculty, True))
    print(instructorSearch("WR", 200, -1, faculty))
