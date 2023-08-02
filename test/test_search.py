##################################
##test_search.py by Spike Chen (SC)
##last Modified:1/31/23
##################################

import search
import unittest
class T0_search_faculty(unittest.TestCase):
    #test if the function instructorSearch is working

    def test_instructorSearch01(self):
        """test for only one professor for one class"""
        
        print("\n")
        print('test for has only one professor who is not in faculty')
        faculty = search.getFacultyList("allFacultyList_abreviated.txt")
        self.assertEqual(search.instructorSearch("CIS",100,111, faculty),
                         {'prottsman, christie': ([75.3, 10.4, 9.1, 0.0, 5.2], 1, False)})


    def test_instructorSearch02(self):
        """test for more professor for one class some of them is in the faculty"""
        
        print("\n")
        print('test the instructorSearch function which has more professor for the class')
        faculty = search.getFacultyList("allFacultyList_abreviated.txt")
        self.assertEqual(search.instructorSearch("CIS",200,210, faculty),
                         {'young, michal': ([35.93, 36.58, 15.78, 8.12, 3.62], 4, True),
                          'sventek, joseph': ([15.6, 41.3, 33.0, 6.4, 3.7], 1, False),
                          'freeman hennessy, kathleen': ([14.3, 37.8, 26.9, 12.6, 8.4], 4, True)})


class T1_search_professor_inList(unittest.TestCase):
    # this test to check that how the function instructorSearch check if the professor is the faculty
    # 1: just show the the class we search
    # 2:check that each professor's name is in the list of faculty
    # 3: if is in the list will show True or show False
    
    ## in our program the just pass will be call with the faculty list
    ## for testing just use the professor name to run the function can easy to see the result
    
    def test_instructorSearch_inList01(self):
        """test for only one professor for one class"""
        
        print("\n")
        print('test the instructorSearch function which has only one professor for the class')
        faculty = search.getFacultyList("allFacultyList_abreviated.txt")
        self.assertEqual(search.instructorSearch("CIS", 100, 111, 'prottsman, christie'),
                         {'prottsman, christie': ([75.3, 10.4, 9.1, 0.0, 5.2], 1, True)})


    def test_instructorSearch_inList02(self):
        """test for more professor for one class"""
        
        print("\n")
        print('test the instructorSearch function which has more professor for the class')
        faculty = search.getFacultyList("allFacultyList_abreviated.txt")
        self.assertEqual(search.instructorSearch("CIS",200,210, 'sventek, joseph'),
                         {'young, michal': ([35.93, 36.58, 15.78, 8.12, 3.62], 4, False),
                          'sventek, joseph': ([15.6, 41.3, 33.0, 6.4, 3.7], 1, True),
                          'freeman hennessy, kathleen': ([14.3, 37.8, 26.9, 12.6, 8.4], 4, False)})


class T2_classSearch(unittest.TestCase):
    # the classSearch function is used for searching the all the class from the user input level
    # those classes which can depend on the user input if they waht to see the faculty or not
    ## True for the faculty searching
    ## False for not

    def test_classSearch01(self):
        """test for searching the faculty class"""
        
        print("\n")
        print('test for searching the faculty class')
        faculty = search.getFacultyList("allFacultyList_abreviated.txt")
        self.assertEqual(search.classSearch("CIS", 200, faculty, True), {'210': ([25.12, 37.19, 21.34, 10.36, 6.01], 2, True)})
        
    def test_iclassSearch02(self):
        """test for searching the not faculty class"""
        
        print("\n")
        print('test for searching the not faculty class')
        faculty = search.getFacultyList("allFacultyList_abreviated.txt")
        self.assertEqual(search.classSearch("CIS", 200, faculty, False), {'210': ([20.04, 38.37, 25.64, 9.93, 6.03], 3, False)})


class T3_search_error(unittest.TestCase):
    # this part is for the error test
    # because the function instructorSearch has four input
    # one input is the faculty list so there jusr are three inputs from the user for instructorSearch
    # the classSearch just need 2 inputs and chouse is the faculty or not
    # to see if the user's three inputs is wrong

    ## instructorSearch:
    ## return the -1 means the subject name is wrong
    ## return the -2 means the level is wrong
    ## return the -3 means the class name is weong

    ## classSearch:
    ## return the -1 means the subject name is wrong
    ## return the -2 means the level is wrong

    def test_instructorSearch_error01(self):
        """test when the subject name is Wong"""
        
        print("\n")
        print('test the instructorSearch function which with wrong subject name input')
        faculty = search.getFacultyList("allFacultyList_abreviated.txt")
        self.assertEqual(search.instructorSearch("CI", 200, 210, faculty), -1)

    def test_instructorSearch_error02(self):
        """test when the level is Wong"""
        
        print("\n")
        print('test the instructorSearch function which with wrong level input')
        faculty = search.getFacultyList("allFacultyList_abreviated.txt")
        self.assertEqual(search.instructorSearch("CIS", 20, 210, faculty), -2)

    def test_instructorSearch_error03(self):
        """test when the class name is Wong"""
        
        print("\n")
        print('test the instructorSearch function which with wrong class name input')
        faculty = search.getFacultyList("allFacultyList_abreviated.txt")
        self.assertEqual(search.instructorSearch("CIS", 200, 21, faculty), -3)

    def test_instructorSearch_error04(self):
        """test when the level is different with the class level"""
        
        print("\n")
        print('test the instructorSearch function which with wrong class levle')
        faculty = search.getFacultyList("allFacultyList_abreviated.txt")
        self.assertEqual(search.instructorSearch("CIS", 200, 112, faculty), -3)

    def test_classSearch_error05(self):
        """test when the subject name is Wong"""
        
        print("\n")
        print('test the classSearch function which with wrong subject name input')
        faculty = search.getFacultyList("allFacultyList_abreviated.txt")
        self.assertEqual(search.classSearch("CS", 200, faculty, False), -1)

    def test_classSearch_error05(self):
        """test when the level is Wong"""
        
        print("\n")
        print('test the classSearch function which with wrong class level input')
        faculty = search.getFacultyList("allFacultyList_abreviated.txt")
        self.assertEqual(search.classSearch("CIS", 20, faculty, False), -2)



if __name__ == '__main__':
    unittest.main()
