# import dependencies
import os # modify environment variables
os.environ['DISPLAY'] = ':0' # this is needed for pyautogui, which is used by pywhatkit
import pywhatkit # need this to send whatsapp messages 
import configparser # easily read config files
import re # regular expressions, a great way to interpret strings (once you understand them lol)

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
Mode = ""; Announcement = "";   Announcement_Priority = ""; Current_Date = ""; Current_Day = ""; LookupVenue = "" 
Lecture_Text = ""
Assignment_CurrentText="";      Assignment_DateText=""; Assignment_DayText="";  Assignment_TimeText = "";   Assignment_VenueText = ""
Quiz_CurrentText="";            Quiz_DateText="";       Quiz_DayText="";        Quiz_TimeText = "";         Quiz_VenueText = ""
Exam_CurrentText="";            Exam_DateText="";       Exam_DayText="";        Exam_TimeText = "";         Exam_VenueText = "";        Exam_Type = ""
CompleteSchedule = []

# Config file
cp = configparser.ConfigParser() 
cp.read(CONFIG_FILE_LOCATION) # read the config file from the specified location
try:
    debug("-------- READING DEBUG FILE --------")
    # Check if there are any overrides
    if(cp['GENERAL']['override'] == 'Input'):
        DO_NOT_SEND = yesno(input("Would you like to send output to console (yes) or whatsapp (no)? (y/n): "))
        DEBUG       = yesno(input("Would you like to see the debug outputs? (y/n): "))
    else:
        debug("NO OVERRIDES ACTIVE")

    # Read general config data
    debug("LOADING GENERAL CONFIG")
    Mode                    = cp["GENERAL"]["mode"]
    Announcement            = cp["GENERAL"]["announcement"]
    Announcement_Priority   = cp["GENERAL"]["priority"]
    Current_Date            = cp["GENERAL"]["date"]
    Current_Day             = cp["GENERAL"]["day"]
    LookupVenue             = cp["GENERAL"]["lookupvenue"]

    # Read lecture data
    debug("LOADING LECTURE CONFIG")
    Lecture_Text            = cp["Lecture"][Current_Day] # Extract timetable for THAT specific day ONLY

    # Read assignment data
    debug("LOADING ASSIGNMENT CONFIG")
    Assignment_CurrentText  = cp["Assignment"]["current"]
    Assignment_DateText     = cp["Assignment"]["date"]
    Assignment_DayText      = cp["Assignment"]["day"]
    Assignment_TimeText     = cp["Assignment"]["time"]
    Assignment_VenueText    = cp["Assignment"]["venue"]

    # Read quiz data
    debug("LOADING QUIZ CONFIG")
    Quiz_CurrentText        = cp["Quiz"]["current"]
    Quiz_DateText           = cp["Quiz"]["date"]
    Quiz_DayText            = cp["Quiz"]["day"]
    Quiz_TimeText           = cp["Quiz"]["time"]
    Quiz_VenueText          = cp["Quiz"]["venue"]

    # Read Exam data
    debug("LOADING EXAM CONFIG")
    Exam_CurrentText        = cp["Exam"]["current"]
    Exam_DateText           = cp["Exam"]["date"]
    Exam_DayText            = cp["Exam"]["day"]
    Exam_TimeText           = cp["Exam"]["time"]
    Exam_VenueText          = cp["Exam"]["venue"]
    Exam_Type               = cp["Exam"]["type"]

# test for any missing information in the config file
except KeyError as key:
    print(f"KEY ERROR (BAD KEY: {key.args[0]}) WHILE READING CONFIG FILE, EXITING PROGRAM")
    exit(504)
except:
    print("GENERAL ERROR WHILE READING CONFIG FILE, EXITING PROGRAM")
    exit(500)

# Parse the received inputs
debug("-------- PARSING DATA --------")

class ScheduleItem:
    def __init__(self, title, date, day, time, venue):
        self.date = date
        self.day = day
        self.title = title
        self.time = time
        self.venue = venue

def TextBeforeChar(IN:str, QUERY:chr):
    index = IN.find(QUERY)
    if index != -1:
        return IN[:index]
    else:
        return IN

# Parse the lectures text
def ParseLectures(IN:str):
    if(IN[0:2:] == "NA"):
        debug("NO LECTURES SCHEDULED")
        return
    # remove whitespace, except space
    whitespace = re.compile(r"[^\S *]") # selects all whitespace except space
    without_whitespace = re.sub(whitespace, '', IN)
    split = without_whitespace.split(",")
    
    debug("LECTURES")
    debug(split)

    for token in split:
        title_curr = TextBeforeChar(token, '(')
        debug(f"**{title_curr}**")

        # Find the first occurrence of text between round brackets for time
        time_curr = re.search(r"\(.+?\)", token)
        time_curr = time_curr.string[time_curr.start():time_curr.end():] # python split notation is cursed
        time_curr = time_curr[1:len(time_curr)-1:]

        debug(f"Time: {time_curr}")

        # Find the first occurrence of text between square brackets for venue
        venue_curr = re.search(r"\[.+?\]", token)
        venue_curr = venue_curr.string[venue_curr.start():venue_curr.end():] # python split notation is cursed
        venue_curr = venue_curr[1:len(venue_curr)-1:]
        if venue_curr == "LOOKUP":
            venue_curr = LookupVenue
        debug(f"Venue: {venue_curr}")

        CompleteSchedule.append(ScheduleItem(title_curr, Current_Date, Current_Day, time_curr, venue_curr))

def ParseOther(Titles:str, Dates:str, Days:str, Times:str, Venues:str):
    if(Titles[0:2:] == "NA"):
        debug("NONE FOUND")
        return
    
    # remove whitespace, except space
    whitespace = re.compile(r"[^\S *]") # selects all whitespace except space

    Titles = re.sub(whitespace, '', Titles)
    Titles = Titles.split(",")
    debug(Titles)

    Dates = re.sub(whitespace, '', Dates)
    Dates = Dates.split(",")
    debug(Dates)

    Days = re.sub(whitespace, '', Days)
    Days = Days.split(",")
    debug(Days)

    Times = re.sub(whitespace, '', Times)
    Times = Times.split(",")
    debug(Times)

    Venues = re.sub(whitespace, '', Venues)
    Venues = Venues.split(",")
    debug(Venues)

    for i in range(len(Titles)):
        CompleteSchedule.append(ScheduleItem(Titles[i], Dates[i], Days[i], Times[i], Venues[i]))

debug("Parsing exams")
ParseOther(Exam_CurrentText, Exam_DateText, Exam_DayText, Exam_TimeText, Exam_VenueText)

ParseLectures(Lecture_Text)

debug("Parsing quizzes")
ParseOther(Quiz_CurrentText, Quiz_DateText, Quiz_DayText, Quiz_TimeText, Quiz_VenueText)

debug("Parsing Assignments")
ParseOther(Assignment_CurrentText, Assignment_DateText, Assignment_DayText, Assignment_TimeText, Assignment_VenueText)