"""
GraphGen.py
--------
Authors: Joey Le, Andrew Liu
Created: 1/22/2023
Last Modified: 2/5/2023

Purpose: This file develops the graphs to be displayed for the user. 
It uses the data found by search.py to compile the graphs then sends the graphs to the GUI.

Revision History (Date | Author | Modifications)
----------------------------------------------
1/22/2023 | Joey Le | Create initial file, sample data and options, and functions to display graphs in Tkinter.
1/23/2023 | Joey Le | Made X-axis labels display vertically instead of horizontally and added more clear comments on the code.
1/24/2023 | Joey Le | Modified data lists to be dictionaries and adjusted how the names of instructors/levels are acquired.
1/24/2023 | Joey Le | Updated comments to be more thorough and clear and updated sample test case to cover edge cases.
1/28/2023 | Joey Le | Reorganized functions and updated some comments; also began integrating these functions to the GUI.
1/30/2023 | Joey Le | Restructured GraphGen to omit Tkinter usage in graphGen(); GUI will use Tkinter features instead.
1/31/2023 | Joey Le | Restructured graphGen() to work on one graph at a time instead of two.
2/1/2023  | Joey Le | Added option to view only faculty and added different options to test.
2/3/2023 | Joey Le | Added comments to every line.
2/4/2023 | Joey Le | Last minute revisions to comments.
2/4/2023 | Andrew Liu | Small change to graph generator parameters - pass label instead of fixed label.
2/5/2023 | Joey Le | Minor comment adjustments and function names use camel case. 
"""

"""
Requirments to run GraphGen.py
------------------------------
The program receives a total of two dictionaries and two lists from Search.py. 

Each graph uses a one dictionary and one list: the data dictionary and options list.
    Data Dictionary: This is a dictionary containing all the necessary data for one graph.
        Key: Instructor's full name in {last_name, first_name} or class level
        Value:  A tuple of float percents as index zero and instructor count as index one
            [0] = List of five float elements of different percentages for the different letter grades : list
                [0][0] = A's
                [0][1] = B's
                [0][2] = C's
                [0][3] = D's
                [0][4] = F's
            [1] = Number of classes that by the instructor or level : int
            [2] = Whether the instructor or class level is considered faculty
        example: [Le, Joey : ([20.0, 10.0, 10.0, 30.0, 30.0], 3, True), ...]

    Options List: This is a list containing the different choices to view the graph based on the user's options
        [0] = Title of the Graph : str
        [1] = View Levels Instead of Instructor Names : bool
        [2] = View the Percent of A's : bool
        [3] = View the Instructor Count : bool

"""

''' Module needed to generate graphs '''
import matplotlib.pyplot as plt                                                     # Use matplotlib to generate graphs
#########################################################################################################################################
"""
compileBarData: a helper function to take a provided dictionary and convert it to two lists to be used for a single graph

Parameters
    data: the dictionary of different percents for each instructor/level with each instructor/level being the key.
    view_levels: a boolean that determines if the graph is to display the instructors' last names or class levels;
        this is used to decide if the keys need to be formatted to keep only the instructors' last name. 
    view_as: a boolean that factors in whether the user wants to see the percent of A's (True) or failing grades (False)
    view_count: a boolean that includes the amount of classes for the particular instructor or level if it equals True.

Returns:
    bar_data[]: a list containing two different lists where bar_data[0] contains the list of instructor or level names to place 
        along the X-axis and bar_data[1] contains the percent values to plot for each instructor on the bar graph.
"""
def compileBarData(data:dict, view_levels:bool, view_as:bool, view_count:bool, view_only_faculty:bool):
    ''' 
    Store the x-values and y-values in lists 
    '''
    x_values = []               # Contains the different instructor names or levels
    y_values = []               # Contains the different percent values for each instructor or level
    bar_data = []               # Stores mentioned lists in [x_values, y_values] and this is returned

    ''' 
    Go through the dictionary to sort out the instructors/levels and their percent values, and add them to their respective lists;
    their indices must be align. 
    '''
    # Start by creating access to all the keys and their values '''
    key_list = list(data.keys())
    # Loop through all the key values
    for i in range(len(key_list)):
        ''' Next, seperate the key and its values to be items in the x-axis and y axis respectively. '''
        # Seperate the keys, which will be the x-axis values.
        name = key_list[i]
        # Seperate the values, where index zero will be used for the y-axis values.
        number_data = data[name]
        # Specify that the key value will be the instructor's last name, if it is a class number, this will not be altered.
        last_name = name

        ''' If faculty only option is selected, then check if instructor or class level is faculty'''
        # Verify that faculty only was specified and if the data is a part of faculty
        if (view_only_faculty == True and number_data[2] == False):
            # Skip incorporating the data if its is not part of faculty
            continue

        ''' If the keys are instructors' full name, then the string needs to be adjusted to contain only the last name. '''
        # Class numbers do not need to get adjusted.
        if (view_levels == False):
            # Format the instructor key value to keep only the last name.
            last_name = formatName(name)

        ''' 
        Include the count of instructors/classes if specified by the user's options (view_count = True). 
        This information is stored in index one of the list value of the instructor/level key.
        '''
        # Check if the request wanted to see the number of instructors or classes.
        if (view_count):
            # Add the instructor count when requested.
            last_name = last_name + f" ({number_data[1]})"

        # Add the adjusted instructor key value or level key value into the list for x-values.
        x_values.append(last_name)

        ''' Determine if the information request is for the percent of A's or failing grades, then add that to the list for y-values. '''
        # Check if request wanted to the percent of A's.
        if (view_as):
            # Add the percent of A's to the data for display.
            y_values.append(number_data[0][0])
        # When the percent of A's is not requested, then the percent of D's and F's are selected.
        else:
            # Add the combined values of D's and F's to the data for display.
            y_values.append(number_data[0][3] + number_data[0][4])
        

    ''' Store the x and y lists into bar_data to return. '''
    # Add the x-list first.
    bar_data.append(x_values)
    # Then add the y-list.
    bar_data.append(y_values)
    # Return the list containing both sets of information for a graph.
    return bar_data
#########################################################################################################################################
"""
formatName(name): a helper function that formats an instructor key to provide just the last name.

Parameters:
    name: a string of the full name of an instructor in <last_name, first_name>.

Return:
    result: a string of an instructor's last name.
"""

def formatName(name:str):
    ''' 
    Start by dividing the first and last name based on the comma used to seperate them. 
    '''
    result = ""                             # The variable to store and return the last name.
    last_name = name.split(", ")            # An initial variable to divide the name between the last and first name.
    last_name = last_name[0]                # Keep the last name in the initial variable.
    
    ''' 
    Next, capitalize the first letter of each word within the last name.
    If there are more than one word in a last name, capitalize those as well
    and incorporate all words within the last name.
    The complete last name then gets stored in the result variable.
    '''
    # Seperate the different words in a last name.
    last_name = last_name.split(" ")
    # Go through each word in that last name.
    for i in range (len(last_name)):
        # Capitalize the first letter of each word and add it to the formatted last name.
        result = result + last_name[i][0].upper() + last_name[i][1:]
        # Check if there are still more words to add.
        if (i + 1 < len(last_name)):
            # Put a space for the next word.
            result = result + " "
            
    '''
    Afterwards, check for specific cases where a non-first character of last name would be capitalize.
    Update the result variable to capitlize the following character after one of these cases.
    '''
    ''' First, check for apostrophes in last names like O'Bryan. '''
    punctuation_index = result.find("\'" , 0, len(result))      # Indicate found index for last names with apostrophe.
    # Iterate through the last name to account of every instance of an apstrophe.
    while (punctuation_index != -1 and punctuation_index != len(result) - 1):
        # Upper case the first letter past the apostrophe. 
        result = result[0:punctuation_index + 1] + result[punctuation_index + 1].upper() + result[punctuation_index + 2:]
        # Check for another apostrophe.
        punctuation_index = result.find("\'", punctuation_index + 1, len(result))

    ''' Second, check for hyphens in last names like Dexter-Enriquez. '''
    punctuation_index = result.find("-" , 0, len(result))       # Indicate found index for last names with hypens.
    # Iterate through the last name to account of every instance of a hyphen.
    while (punctuation_index != -1 and punctuation_index != len(result) - 1):
        # Upper case the first letter past the hyphen.
        result = result[0:punctuation_index + 1] + result[punctuation_index + 1].upper() + result[punctuation_index + 2:]
        # Check for another hyphen.
        punctuation_index = result.find("-", punctuation_index + 1, len(result))
        
    ''' Third, check for "Mc" at the beginning of last names like McDonald. '''
    # Check for "Mc" in a last name.
    if (result[0:2] == "Mc" and len(result) > 2):
       # Upper case the first letter after "Mc".
       result = result[0:2] + result[2].upper() + result[3:]

    ''' Return the properly formatted last name '''
    return result
#########################################################################################################################################
"""
graphGen: a function that creates a graph based on the data dictionary and options list for that graph.

Parameters
    data_dict: a dictionary for the data results found to display for the graph.
    options_list: a list of options needed to view the graph in the user's desired way.
    faculty_only: a boolean to determine if only faculty ought to be displayed.
    label: a string label for the x-axis of the graph.

Return:
    A single graph figure.
"""
def graphGen(data_dict: dict, options_list: list, faculty_only: bool, label: str):
    ''' 
    Set the bar graph data for the graph. 
    '''
    bar_data = compileBarData(data_dict, view_levels = options_list[1], view_as = options_list[2], view_count = options_list[3], view_only_faculty = faculty_only)

    ''' 
    Set the title of the graphs and default values of the x and y axis for each graph. 
    The axis labels have default values, but subject to change if the user options oppose these labels.
    '''
    title = options_list[0]                                   # The title for the graph.
    xlabel = label                                            # The x-axis label for the graph.
    ylabel = "% As"                                           # The y-axis label for the graph. 

    ''' 
    Establish what the x-axis and y-axis labels will be based on the user's options. 
    Use if-statements to update the default values if needed.
    '''
    # Change the x-axis label if user wants to see class numbers instead of instructors.
    if options_list[1]:
        # Change the x-axis label.
        xlabel = "Classes"
    # Change the y-axis label if user wants to see the percents of D's and F's instead of the percents of A's.
    if not options_list[2]:
        # Change the y-axis label.
        ylabel = "% Ds / Fs"

    # Modify the x-axis label to specify its faculty only if user wants to see only faculty data.
    if faculty_only:
        # Specify in the x-axis label that the data only refers to faculty data.
        xlabel = xlabel + " (Faculty Only)"

    ''' 
    Create a graph by putting it on a returnable figure then format the graph according to the user's options.
    '''
    fig = plt.figure()                                  # Store the graph in a variable.
    plt.bar(bar_data[0], bar_data[1])                   # Format as a bar graph and add its data.
    plt.xlabel(xlabel)                                  # Give a label to the x-axis.
    plt.ylabel(ylabel, rotation=0)                      # Give a label to the y-axis.
    plt.ylim(0, 100)                                    # Set y-axis range from 0 t0 100 inclusive.
    plt.title(title)                                    # Put a title on the graph.
    plt.tick_params(axis = 'x', rotation = -90)         # Rotate the x-axis valus to be vertically.

    ''' Return the graph as an individual figure once the graphs are properly created'''
    return fig
#########################################################################################################################################
"""IMPORTANT: Below are test functions for developers to test this individual component; this is not considered part of the system. """

"""
compileSampleData(): a helper function to form data dictionary samples.

Parameters
    str_name : a bool to specify whether to create a data dictionary of instructors (True) or class levels (False).

Returns:
    sample_dict: a data dictionary of sample data.
"""
def compileSampleData(str_name:bool):
    # Return value containing the data dictionary.
    sample_dict = {}
    # Instructor Data
    ''' Specific entries into sampleDict can be adjusted to experiment with specific data examples. '''
    if (str_name):
        # Test more common examples.
        sample_dict["world, hello s."] = [(20.0, 0.0, 0.0, 20.0, 20.0), 1, True]
        # Test more common examples.
        sample_dict["joey, le"] = [(20.0, 0.0, 0.0, 20.0, 20.0), 1, False]
        # Test apostrophes in a last name.
        sample_dict["o'bear, johnny bill"] = [(25.0, 0.0, 0.0, 25.0, 25.0), 2, True]
        # Test apostrophes in a last name.
        sample_dict["y'e's', test no"] = [(25.0, 0.0, 0.0, 25.0, 25.0), 2, False]
        # Test multiple words in a last name.
        sample_dict["original name, instructor"] = [(30.0, 0.0, 0.0, 30.0, 30.0), 3, True]
        # Test multiple words in a last name.
        sample_dict["from the store, teacher"] = [(30.0, 0.0, 0.0, 30.0, 30.0), 3, False]
        # Test hypens in a last name.
        sample_dict["hypen-hyphen, punctuation s"] = [(35.0, 0.0, 0.0, 35.0, 35.0), 4, True]
        # Test hypens in a last name.
        sample_dict["minus-minus-minus-, math"] = [(35.0, 0.0, 0.0, 35.0, 35.0), 4, False]
        # Test "Mc" in a last name.
        sample_dict["mcquarter, harold"] = [(40.0, 0.0, 0.0, 40.0, 40.0), 5, True]
        # Test "Mc" in a last name.
        sample_dict["mc, mister"] = [(40.0, 0.0, 0.0, 40.0, 40.0), 5, False]
        # Test every case at once.
        sample_dict["mcev'ery-thing here, test"] = [(45.0, 0.0, 0.0, 45.0, 45.0), 6, True]
    # Class Levels
    else:
        # 100 Level Example
        sample_dict["100"] = [(20.0, 0.0, 0.0, 20.0, 20.0), 1, True]
        # 111 Level Example
        sample_dict["111"] = [(20.0, 0.0, 0.0, 20.0, 20.0), 1, False]
        # 121 Level Example
        sample_dict["121"] = [(25.0, 0.0, 0.0, 25.0, 25.0), 2, True]
        # 122 Level Example
        sample_dict["122"] = [(25.0, 0.0, 0.0, 25.0, 25.0), 2, False]
        # 131 Level Example
        sample_dict["131"] = [(30.0, 0.0, 0.0, 30.0, 30.0), 3, True]
        # 132 Level Example
        sample_dict["132"] = [(30.0, 0.0, 0.0, 30.0, 30.0), 3, False]
        # 141 Level Examplee
        sample_dict["141"] = [(35.0, 0.0, 0.0, 35.0, 35.0), 4, True]
        # 142 Level Example
        sample_dict["142"] = [(35.0, 0.0, 0.0, 35.0, 35.0), 4, False]
        # 152 Level Example
        sample_dict["151"] = [(40.0, 0.0, 0.0, 40.0, 40.0), 5, True]
        # 152 Level Example
        sample_dict["152"] = [(40.0, 0.0, 0.0, 40.0, 40.0), 5, False]
        # 161 Level Example
        sample_dict["161"] = [(45.0, 0.0, 0.0, 45.0, 45.0), 6, True]
    # Return the sample data dictionary
    return sample_dict

"""
displayGraph(): a testing function to display two graphs out of six different options.

Parameters
    None.

Returns:
    Two matplotlib graphs that get displayed.
"""
def displayGraph():
    ''' 
    Two different options can be used at a time with the two graphGen() calls; additional options or graphGen() calls can be added. 
    These sample options have an additional fifth index to specify faculty only.
    '''
    # Option A shows the percent of A's and instructor count.
    sample_optionsA = ["As/Count", False, True, True, False]
    # Options B provides a sample default with all Falses for the parameters
    sample_optionsB = ["Default", False, False, False, False]
    # Option C provides the levels instead of instructors and class count
    sample_optionsC = ["Levels/Count", True, False, True, False]
    # Option D provides just the levels without count 
    sample_optionsD = ["Levels", True, False, False, False]
    # Option E provides only faculty data of instructors
    sample_optionsE = ["Faculty", False, False, False, True]
    # Option F provides only faculty data of classes
    sample_optionsF = ["Levels/Faculty", True, False, False, True]
    # Form one graph
    graphGen(data_dict = compileSampleData(str_name = True), options_list = sample_optionsB, faculty_only = sample_optionsB[4], label = "x-label")
    # Form another graph
    graphGen(data_dict = compileSampleData(str_name = True), options_list = sample_optionsE, faculty_only = sample_optionsE[4], label = "x-label")
    # Display the test graphs
    plt.show()

''' Uncomment below to test this graph independently from entire system. '''
#displayGraph()
