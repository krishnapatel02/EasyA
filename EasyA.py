"""
EasyA.py
--------
Authors: Joey Le, Andrew Liu
Created: 1/19/2023
Last Modified: 2/5/2023

Purpose: This file serves as a device driver for the other modules in the system. 
It activates the other modules wihin the system to do their intended functionality.

Revision History (Date | Author | Modifications)
----------------------------------------------
1/19/2023 | Joey Le | Create initial file and added rough descriptions for each interacted module
1/19/2023 | Andrew Liu | Reformatting and adding a test call to GUI initialization
1/28/2023 | Joey Le | Incorporated GraphGen.py into this file
2/5/2023 | Joey Le | Removed all unneccessary placeholder functions and comments.
"""

''' Access the Student Graphic User Interface (StudentInterface.py)'''
import StudentInterface

''' Run the GUI with gui() '''
def gui():
    # The function from StudentInterface.py to activate the GUI.
    StudentInterface.initGui()

''' Run main() to start the GUI. '''
def main():
    """
    IMPORTANT! 
    tkinter windows runs in their own mainloop which MUST BE RUN IN THE MAIN THREAD and is NOT THREADSAFE!
    This means that all modules must be callable from the GUI.
    """
    gui()

''' Check for it being main. '''
if __name__ == '__main__':
    # Run the main function.
    main()
