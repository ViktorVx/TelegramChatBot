
import datetime
dt = datetime.date(2018, 12, 31)
#print(dt.replace(dt.year+1))
#print(dt.replace(dt.year, dt.month))
#print(dt.replace(dt.year, dt.month, dt.day+1))
print(dt + datetime.timedelta(7))


