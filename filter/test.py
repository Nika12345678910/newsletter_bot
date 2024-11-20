from datetime import datetime

s = "2007-12-12"
print(datetime.now().year, datetime.now().month)
print(datetime.now().year >= int(s[:4]))
print(datetime.now().month >= int(s[4:6]))
print(datetime.today(), str(datetime.today())[8:10])