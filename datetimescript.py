from datetime import datetime

date_input = '22-Jul-2021'
datetimeobject = datetime.strptime(date_input,'%d-%b-%Y')
new_format = datetimeobject.strftime('%Y%m%d')
print(new_format)