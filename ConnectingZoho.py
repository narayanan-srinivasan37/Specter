from os import error
import requests
import json
import pandas as pd
import time
from datetime import datetime
import csv
from pandas import ExcelWriter
from pandas import ExcelFile
from Call_Functions import get_function, refresh_token_function
with open("Secret_key.json",) as json_file:
    keys = json.load(json_file)
    json_file.close()
access_token = keys["access_token"]
refresh_token = keys["refresh_token"]
client_id = keys["client_id"]
client_secret = keys["client_secret"]
global data
print("Entering while loop")
while(1):
    my_headers = {
        "Authorization": 'Zoho-oauthtoken ' + access_token
    }
    response = get_function(my_headers)
    print(response.status_code)
    if(response.status_code == 401 or response.status_code == 404 or response.status_code == 429):
        status_code = refresh_token_function(
            refresh_token, client_id, client_secret, keys)
        print(status_code)
        if(status_code == 200):
            access_token = keys["access_token"]

    elif(response.status_code == 200):
        data = json.loads(response.text)
        data = data['data']
      
        datapushedtoexcel = []
        count = 0
        fields = []
        print(data)
        vchtype= "Sales Voucher"
        sales_ledger_name="Credit Sales"
        for record in data:
            datefield=record['Date_field']
            datetimeobject = datetime.strptime(datefield,'%d-%b-%Y')
            datefield = datetimeobject.strftime('%Y%m%d')
            products=record['Products'].split("\n")
            while("" in products) :
                products.remove("")
            address=record['Address'].split("\n")
            print(products,address)
            voucherdata="<ENVELOPE><HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER><BODY><IMPORTDATA><REQUESTDESC><REPORTNAME>Vouchers</REPORTNAME>"
            voucherdata+="<STATICVARIABLES><SVCURRENTCOMPANY>Apple Inc.</SVCURRENTCOMPANY></STATICVARIABLES></REQUESTDESC><REQUESTDATA>"
            voucherdata+="<TALLYMESSAGE xmlns:UDF=""\"TallyUDF\"""><VOUCHER VCHTYPE=""\"Sales\""" ACTION=""\"Create\""" OBJVIEW=""\"Invoice Voucher View\"""><ADDRESS.LIST TYPE=""\"String\""">"
            for i in address:
                voucherdata+="<ADDRESS>"+i+"</ADDRESS>"
            voucherdata+="</ADDRESS.LIST><BASICBUYERADDRESS.LIST TYPE=""\"String\""">"
            for i in address:
                voucherdata+="<BASICBUYERADDRESS>"+i+"</BASICBUYERADDRESS>"
            voucherdata+="</BASICBUYERADDRESS.LIST><OLDAUDITENTRYIDS.LIST><OLDAUDITENTRYIDS>-1</OLDAUDITENTRYIDS></OLDAUDITENTRYIDS.LIST>"
            voucherdata+="<DATE>"+datefield+"</DATE>"
            voucherdata+="<STATENAME>Tamil Nadu</STATENAME><NARRATION>Invoice voucher for"+record["Customer_Name"]+"</NARRATION>"
            voucherdata+="<COUNTRYOFRESIDENCE>India</COUNTRYOFRESIDENCE><PLACEOFSUPPLY>Tamil Nadu</PLACEOFSUPPLY>"
            if(record['GSTIN']!=None):
                voucherdata+="<PARTYGSTIN>"+record["GSTIN"]+"</PARTYGSTIN>"
            voucherdata+="<PARTYNAME>"+record['Customer_Name']+"</PARTYNAME><PARTYLEDGERNAME>"+record['Customer_Name']+"</PARTYLEDGERNAME>"
            voucherdata+="<VOUCHERTYPENAME>"+vchtype+"</VOUCHERTYPENAME><VOUCHERNUMBER>1</VOUCHERNUMBER>"
            voucherdata+="<BASICBASEPARTYNAME>"+record['Customer_Name']+"</BASICBASEPARTYNAME><CSTFORMISSUETYPE/><CSTFORMRECVTYPE/>"
            voucherdata+="<FBTPAYMENTTYPE>Default</FBTPAYMENTTYPE><PERSISTEDVIEW>Invoice Voucher View</PERSISTEDVIEW><DISPATCHFROMNAME>Appleinc.Com</DISPATCHFROMNAME>"
            voucherdata+="<DISPATCHFROMSTATENAME>Tamil Nadu</DISPATCHFROMSTATENAME><BASICBUYERNAME>"+record['Customer_Name']+"</BASICBUYERNAME>"
            if(record['Credit_Period']!=None):
                voucherdata+="<BASICDUEDATEOFPYMT>"+record['Credit_Period']+"</BASICDUEDATEOFPYMT>"
            else:
                voucherdata+="<BASICDUEDATEOFPYMT></BASICDUEDATEOFPYMT>"
            voucherdata+="<PARTYMAILINGNAME>"+record['Customer_Name']+"</PARTYMAILINGNAME><PARTYPINCODE>"+record['Pincode']+"</PARTYPINCODE>"
            voucherdata+="<CONSIGNEEMAILINGNAME>"+record['Customer_Name']+"</CONSIGNEEMAILINGNAME><CONSIGNEECOUNTRYNAME>India</CONSIGNEECOUNTRYNAME>"
            voucherdata+="<VCHGSTCLASS/><CONSIGNEESTATENAME>Tamil Nadu</CONSIGNEESTATENAME><CONSIGNEEPINCODE>"+record['Pincode']+"</CONSIGNEEPINCODE>"
            voucherdata+="<EFFECTIVEDATE>"+datefield+"</EFFECTIVEDATE><ISINVOICE>Yes</ISINVOICE><ISVATDUTYPAID>Yes</ISVATDUTYPAID><RESETIRNQRCODE>No</RESETIRNQRCODE>"
            item=[]
            for product in products:
                voucherdata+="<ALLINVENTORYENTRIES.LIST>"
                item =product.split(",")
                voucherdata+="<STOCKITEMNAME>"+item[0]+"</STOCKITEMNAME><ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE><ISLASTDEEMEDPOSITIVE>No</ISLASTDEEMEDPOSITIVE>"
                voucherdata+="<ISAUTONEGATE>No</ISAUTONEGATE><ISCUSTOMSCLEARANCE>No</ISCUSTOMSCLEARANCE><ISTRACKCOMPONENT>No</ISTRACKCOMPONENT><ISTRACKPRODUCTION>No</ISTRACKPRODUCTION>"
                voucherdata+="<ISPRIMARYITEM>No</ISPRIMARYITEM>ISSCRAP>No</ISSCRAP><RATE>"+item[3]+"</RATE><AMOUNT>"+item[2]+"</AMOUNT>"
                voucherdata+="<ACTUALQTY>"+item[1]+"</ACTUALQTY><BILLEDQTY>"+item[1]+"</BILLEDQTY><BATCHALLOCATIONS.LIST><GODOWNNAME>GODOWN</GODOWNNAME><BATCHNAME>Primary Batch</BATCHNAME>"
                voucherdata+="<INDENTNO/><ORDERNO>1</ORDERNO><TRACKINGNUMBER/><DYNAMICCSTISCLEARED>No</DYNAMICCSTISCLEARED><AMOUNT>"+item[2]+"</AMOUNT>"
                voucherdata+="<ACTUALQTY> "+item[1]+"</ACTUALQTY><BILLEDQTY>"+item[1]+"</BILLEDQTY>"
                if(record["Credit_Period"]!=None):
                    voucherdata+="<ORDERDUEDATE>"+record["Credit_Period"]+"</ORDERDUEDATE>"
                else:
                    voucherdata+="<ORDERDUEDATE></ORDERDUEDATE>"
                voucherdata+="</BATCHALLOCATIONS.LIST><ACCOUNTINGALLOCATIONS.LIST><OLDAUDITENTRYIDS.LIST TYPE=""\"Number\"""><OLDAUDITENTRYIDS>-1</OLDAUDITENTRYIDS>"
                voucherdata+="</OLDAUDITENTRYIDS.LIST><LEDGERNAME>"+sales_ledger_name+"</LEDGERNAME><GSTCLASS/><ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>"
                voucherdata+="<ISCAPVATTAXALTERED>No</ISCAPVATTAXALTERED><ISCAPVATNOTCLAIMED>No</ISCAPVATNOTCLAIMED><AMOUNT>"+item[2]+"</AMOUNT>"
                voucherdata+="<RATEDETAILS.LIST><GSTRATEDUTYHEAD>Integrated Tax</GSTRATEDUTYHEAD></RATEDETAILS.LIST><RATEDETAILS.LIST><GSTRATEDUTYHEAD>Central Tax</GSTRATEDUTYHEAD>"
                voucherdata+="</RATEDETAILS.LIST><RATEDETAILS.LIST><GSTRATEDUTYHEAD>State Tax</GSTRATEDUTYHEAD></RATEDETAILS.LIST><RATEDETAILS.LIST>"
                voucherdata+="<GSTRATEDUTYHEAD>Cess</GSTRATEDUTYHEAD></RATEDETAILS.LIST></ACCOUNTINGALLOCATIONS.LIST></ALLINVENTORYENTRIES.LIST>"
    

            if(count == 0):
                fields = list(record.keys())
                count = 1
                fieldslength=len(fields)
                

            datatemp = []
            for i in fields:
               datatemp.append(record[i])

            datapushedtoexcel.append(datatemp)
            #print(datapushedtoexcel)
        with open('DatafromZoho.csv', 'w') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(datapushedtoexcel)
        break
