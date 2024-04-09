/*
Menu System Code.

Author: Davis Rippon
Version: 1.0
Date Last Edited: April 9 2024
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define insertCase 6953633055386 
#define removeCase 6953974396019 
#define searchCase 6954013102811 
#define printCase 210724587794 
#define exportCase 6953488276103 
#define quit 6385632776 

unsigned long hash(const char *str) {
    unsigned long hash = 5381;  
    int c;

    while ((c = *str++))
        hash = ((hash << 5) + hash) + c;
    return hash;
}

unsigned long generateID(char * name, int value, char * units) {
    long ID = hash(name) + hash(units) + value;
    return ID;
}

int main() {

    int userQuit = 0;
    
    while (userQuit == 0) {

        char usrInput[400];
        fgets(usrInput,400,stdin);

        char menuChoice[10];
        sscanf(usrInput,"%s ", menuChoice);

        switch (hash(menuChoice)) {
            case insertCase: 
                break;

            case removeCase:
                break;

            case searchCase:
                break;

            case printCase:
                break;
    
            case exportCase:
                break;

            case quit:
                break;
        }

    }
    
}