import requests
import csv
import xml.etree.ElementTree as Et
url = 'http://localhost:9000'
xml = "<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST>"
xml += "<TYPE>DATA</TYPE><ID>Bills Receivable</ID></HEADER><BODY>"
xml += "<DESC><STATICVARIABLES><SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>"
xml += "</STATICVARIABLES></DESC></BODY></ENVELOPE>"
req = requests.post(url=url, data=xml)

res = req.text.strip()
responseXML = Et.fromstring(res)
bill_fixed = []
bill_cl=[]
bill_due=[]
bill_ovdue=[]
outstanding_report=[]
for item in responseXML.findall('./BILLFIXED'):
    stock_item = []
    stock_item.append(item.find('./BILLREF').text)
    stock_item.append(item.find('./BILLPARTY').text)
    bill_fixed.append(stock_item)
print(bill_fixed)
for item in responseXML.findall('./BILLCL'):
    bill_cl.append(item.text)
print(bill_cl)
for item in responseXML.findall('./BILLDUE'):
    bill_due.append(item.text)
print(bill_due)
for item in responseXML.findall('./BILLOVERDUE'):
    bill_ovdue.append(item.text)
print(bill_ovdue)
count=0
for i,j,k,l in zip(bill_fixed,bill_cl,bill_due,bill_ovdue):
    one_rp = []
    one_rp.append(i[count])
    one_rp.append(i[count+1])
    one_rp.append(j)
    one_rp.append(k)
    one_rp.append(l)
    outstanding_report.append(one_rp)
print(outstanding_report)
fields=["REFERENCE","COMPANY NAME", "DUE AMOUNT","DUE DATE", "OVER DUE DAYS"]
with open('somefiles.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(outstanding_report)