from pathlib import *
from datetime import datetime
import os

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