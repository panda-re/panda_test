# replaymoviecommon.py
# Code common to multiple replaymovie tests.
#
# Created:  22-AUG-2019

import glob
import os

INDENT_SPACES = "                 "

def delete_ppms():
    '''
    Delete all the *.ppm files in the folder the test was run from.
    '''
    ppmlist = glob.glob("*.ppm")
    for filepath in ppmlist:
        try:
            os.remove(filepath)
        except:
            print(INDENT_SPACES + "***** ERROR DELETING PPM FILE *****")
            