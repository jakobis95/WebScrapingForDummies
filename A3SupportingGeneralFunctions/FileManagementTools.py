from pathlib import *
from datetime import datetime
import os

def check_files_timeliness(files):
    uptodate = True
    for file in files:
        if is_uptodate(file):
            print("uptodate\n ->>", file)
        else:
            print("NOT UPTODATE\n ->>", file)
            uptodate = False

    if uptodate == False:
        print("Outdated File detected!!!, you want to continue anyway?")
        decision = False
        while decision != True:
            response = input("Press y to continue or n to terminate programm")
            if response == "y":
                decision = True
                return True
            if response == "n":
                decision = True
                return False
    else:
        return True

def askForToken(tokenPath):
    tokentxt = input("Bitte geben Sie einen aktuellen Authentifizierungstoken ein und bestätigen Sie mit Enter")
    with open(tokenPath, 'w') as f:
        f.write(tokentxt)
    f.close()

def was_created(file):
    p = Path(file)
    pct = p.stat().st_ctime #creation Time
    return datetime.fromtimestamp(p.stat().st_ctime)
    #return print("ctime", datetime.fromtimestamp(p.stat().st_ctime).strftime('%Y-%m-%d %H:%M:%S'))

def is_not_older_then(ctime, ageInDays):
    curDateTime = datetime.today()
    dif = curDateTime - ctime
    if dif.days <= ageInDays:
        return True
    else:
        return False
def is_uptodate(file):
    if is_not_older_then(was_created(file), 1):
        return True
    else:
        return False


if __name__ == "__main__":
    UserName = os.getlogin()
    file = "C:\\Users\\" + str(UserName) + "\\Downloads\\HVACOverview.xlsx"
    print(was_created(file))