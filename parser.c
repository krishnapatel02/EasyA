
/*
Written by Peter Nelson
Intended to parse json file from Daily Emerald grade data into easily searchable format

Created: 1/18/23
Modified: 2/3/23

Instructions for use:
    copy json file contents to a textfile named gradedata.txt
    delete line 1 and all code at the bottom of the file, leaving only data
    move gradedata.txt to the same directory as parser.c
    compile parser.c with "gcc parser.c" on linux terminal
    execute with "./a.out"
    parsed data will be output to a file named parsedData.txt
*/



#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>


int main(int argc, char* argv[]) {

    //open gradedata file
    FILE *f1 = fopen("gradedata.txt", "r");
    //open file for formatted output
    FILE *f2 = fopen("temp.txt", "w");

    char buff[255];
    char readchar;

    //for every character in gradedata.txt
    while(!feof(f1)) {
        readchar = fgetc(f1);
        //if character is not alphabetic, a digit or a newline, print to temp.txt
        if(isalpha(readchar) != 0 || isdigit(readchar) != 0 || readchar == '\n') {
            fprintf(f2, "%c", readchar);
        }
    }

    //close previous files
    fclose(f1);
    fclose(f2);

    //open temp.txt for reading and parsedData.txt for writing
    FILE *f3 = fopen("temp.txt", "r");
    FILE *f4 = fopen("parsedData.txt", "w");

    char className[10];
    char lastName[30];
    char firstName[30];
    char level[5];

    int storedClass = 0;
    int nameSeparated = 0;

    //for each line of temp.txt
    while(fscanf(f3, "%s", buff) == 1) {
        //if line starts with T, c, or b, then ignore
        if(!(buff[0] == 'T') && !(buff[0] == 'c') && !(buff[0] == 'b')) {
            //if first character of line is capital, must be class name
            if(isupper(buff[0]) != 0) {
                strcpy(className, buff);
                //for each character in the class name, look for first digit
                for(int i = 0; i < strlen(buff); i++) {
                    if(isdigit(buff[i])) {
                        level[0] = buff[i];
                        break;
                    }
                }
                //create level number from above search
                level[1] = '0'; level[2] = '0'; level[3] = '\0';
                storedClass = 1;
            }
            //write out classname and level to parsedData.txt
            if(storedClass == 0 && buff[0] == 'a') {
                fprintf(f4, "%s, ", className);
                fprintf(f4, "%s, ", level);
            }
            nameSeparated = 0;
            //if line starts with i, must be instructor name
            if(buff[0] == 'i') {
                //ignore 'instructor' word, separate name by a comma between last and first name
                for(int i = 10; i < strlen(buff); i++) {
                    if(i > 11 && nameSeparated == 0 && isupper(buff[i]) != 0) {
                        fprintf(f4, "%c ", ',');
                        nameSeparated = 1;
                    }
                    fprintf(f4, "%c", buff[i]);
                }
                fprintf(f4, "%c", '\n');
                storedClass = 0;
            }
            //write out line and level
            else fprintf(f4, "%s, ", buff);
            if(isupper(buff[0]) != 0) {
                fprintf(f4, "%s, ", level);
            }
        }
    }

    //close files
    fclose(f3);
    fclose(f4);
    return 0;
}