#Scraper.py
#Author: Peter Nelson

#Created 1/19/23
#Modified 2/3/23

#This code parses scraped html files sourced from web archive University of Oregon department urls.
#Output is a new formatted text file containing a list of scraped faculty members.
#To run, enter 'python3 scraper.py' in terminal
    #enter html file name
    #enter format specifier: 'a' for abbreviated, 'f' for full names


#import beautiful soup for html scraping
from bs4 import BeautifulSoup

#import re for regular expressions
import re

#import sys for sys.exit()
import sys

#import os for so.getcwd()
import os

#get html file name from input
print("Input HTML file name:")
fileName = input()

#store path of designated html file
currentDir = os.getcwd()
path = currentDir + "/faculty_htmls/" + fileName

#get user choice of abbreviated or full name list
print("Input name format: ('f' for full/ 'a' for abreviated")
fileType = input()

#if input does not match 'a' for abbreviated or 'f' for full
#exit program with error message
if fileType != "a" and fileType != "f":
    sys.exit("Incorrect name format entered")

#open specified html file
with open(path, "r") as f:
    #open html file with bs4 using html parser tool
    doc = BeautifulSoup(f, "html.parser")

#find all html objects tagged with 'facultylist'
tags = doc.find_all(["p"], class_ = "facultylist")
#delete final object because it is always a text line and not a name
del tags[-1]

#create new text file name to store name list
d = fileName.split(".")
e = d[0] + ".txt"

#open new text file
f = open(e, "w")

#if the specified file type is 'f' for full
if fileType == "f":
    #for all faculty name lines in search list
    for tag in tags:
        #create string from bs4 object
        text = str(tag)
        #trim name line to only include full name
        x = re.search(">([a-zA-Z.’\s])*\w+", text)
        n = x[0].split(">")
        #write the full name to the new file
        f.write(n[1])
        f.write("\n")


#if the specified file type is 'a' for abbreviated
elif fileType == "a":
    ##for all faculty name lines in search list
    for tag in tags:
        ##create string from bs4 object
        text = str(tag)
        #trim name line to only include full name
        x = re.search(">([a-zA-Z.’\s])*\w+", text)
        n = x[0].split(">")
        #split the name by spaces into list 'words'
        words = n[1].split(" ")
        #set regular expression compilation to filter middle initials
        regex = re.compile('^[A-Z][a-z]*[.]$')
        filtered = [i for i in words if not regex.match(i)]
        #if the first filtered word is 'The', then the line is not needed
        if(filtered[0] != "The"):
            #write first name to file
            f.write(filtered[0])
            #write comma to file
            f.write(",")
            #write last name to file
            f.write(filtered[1])
            #if there are more than two words, then there must be more to the last name
            if(filtered.__len__() > 2):
                #if the last word is 'Jr' then skip
                if(filtered[2] != "Jr"):
                    f.write(" ")
                    #write second last name
                    f.write(filtered[2])
            f.write("\n")
        
    
print("Text file written")
#close html file
f.close()