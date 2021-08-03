import requests
import xml.etree.ElementTree as Et
import csv
url = 'http://localhost:9000'
url = 'http://localhost:9000'
data = "<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST><TYPE>COLLECTION</TYPE><ID>Godown</ID></HEADER>"
data += "<BODY><DESC><STATICVARIABLES><EXPLODEALLLEVELS>Yes</EXPLODEALLLEVELS><SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT></STATICVARIABLES><TDL><TDLMESSAGE><COLLECTION Name='StockItems'>"
data += "<TYPE>Godown</TYPE><FETCH>STOCKITEM, </FETCH></COLLECTION></TDLMESSAGE></TDL></DESC></BODY></ENVELOPE>"
req = requests.post(url=url, data=data)
res = req.text.strip()
print(res)