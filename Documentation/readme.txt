Description: This system is intended to be an improved version of the Emerald Grade Tracker. (https://emeraldmediagroup.github.io/grade-data/)
The EasyA program is a tool meant for students to look at grade data for both classes and instructors by subject, level, and course number.
The data, line in The Emerald's system will display data in bar graphs but will allow side by side viewing. There is also an option to filter by 
classes taught by all instructors or only faculty. The data set is the same as The Emerald's and contains data up to 2016. 
The data is not complete as some courses were redacted by the University of Oregon for data privacy reasons. 
However, this system can be updated with new data using the addData.py file.

Authors: Spike Chen, Joey Le, Andrew Liu, Peter Nelson, Krishna Patel

Date Created: 1/13/2023

Why project was created: This project is created for CS 422 at University of Oregon and is taught by Anthony Hornof. The purpose of this 
project is to build a system that allows students to have a side by side view of grade data and to allow an administrator to 
update the data.

How to compile and run program:
    1. Unzip the file once it is done downloading, into a folder called 422-EasyA.
    2. Open the terminal on your computer (Powershell/CMD on Windows, Terminal on Mac).
    3. Navigate to the directory where the file was downloaded to. In most cases, this can be done by typing “cd Downloads/422-EasyA” 
    in the terminal and pressing enter unless the directory was changed. If the file is in a different directory type “cd <directory path>/422-EasyA/”.
    4. To replace the included data and faculty list, type and run “python3 addData.py.” The program will guide you through updating the data. 
    See section 4 of the user documentation for more info on file format requirements.
    5. To run the program, type “python3 EasyA.py” in the same directory and the program will start.

Software Dependencies: Python3, Tkinter, matplotlib, bs4(beautifulsoup4)

Directory Structure:
    1. "422-EasyA": Contains all python files to run program (EasyA.py, addData.py, GraphGen.py, parser.py, scraper.py. search.py),
    data files (faculty.txt, parsed_data.csv), and the subdirectories.
    2. "Documentation":Contains all the required documentation such as the Project Plan, User Documentation, Programmer Documentation, SDS, and readme.txt.
    3. "faculty_htmls": Contains all html files used by scraper.py to build a list of faculty.
    4. "test": Contains all test files.
