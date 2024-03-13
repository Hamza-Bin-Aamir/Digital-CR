# import dependencies
import os
os.environ['DISPLAY'] = ':0' # this is needed for pyautogui, which is used by pywhatkit
import pywhatkit
import configparser

# Config data (editable)
DO_NOT_SEND = True # use this to get the code output in console instead of in the message
DEBUG = True # get debug outputs
CONFIG_FILE_LOCATION = 'Digital-CR-Config.ini' # relative path to file

# Helper functions
def yesno(IN:str):
    return str(IN)[0] == 'y'
def debug(IN):
    if(DEBUG):
        print(IN)

# Config data (DO NOT MODIFY)
# We will check if there are even exams, quizzes, assignments or lectures due
NO_EXAM = False; NO_QUIZ = False; NO_ASSIGNMENT = False; NO_LECTURE = False
# Store values from config file
Mode = ""; Announcement = ""; Announcement_Priority = ""
CURR_DATE = ""; CURR_DAY = ""; Lecture_Text = ""
Assignment_CurrentText=""; Assignment_DateText=""; Assignment_DayText=""; Assignment_TimeText = ""; Assignment_VenueText = ""
Quiz_CurrentText=""; Quiz_DateText=""; Quiz_DayText=""; Quiz_TimeText = ""; Quiz_VenueText = ""
Exam_CurrentText=""; Exam_DateText=""; Exam_DayText=""; Exam_TimeText = ""; Exam_VenueText = ""; Exam_Type = ""

# Config file
cp = configparser.ConfigParser(CONFIG_FILE_LOCATION) # read the config file from the specified location
try:
    debug("PARSING DEBUG FILE")
    # Check if there are any overrides
    if(cp['OTHER']['Override'] == 'Input'):
        DO_NOT_SEND = yesno(input("Would you like to send output to console (yes) or whatsapp (no)? (y/n): "))
        DEBUG = yesno(input("Would you like to see the debug outputs? (y/n): "))
    else:
        debug("NO OVERRIDES ACTIVE")

    # Read general config data
    Mode = cp["OTHER"]["Mode"]
    
# test for any missing information in the config file
except KeyError:
    print("KEY ERROR WHILE READING CONFIG FILE, EXITING PROGRAM")
    exit(504)
except:
    print("GENERAL ERROR WHILE READING CONFIG FILE, EXITING PROGRAM")
    exit(500)