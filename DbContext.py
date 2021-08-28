import sqlite3
from enum import Enum
import csv
import datetime
import os

class ExpOptions(Enum):
    Today = 0
    Week = 1

class DataBaseManager:

    def __init__(self):
        if not os.path.exists('CsvData'):
            os.makedirs('CsvData')

    def ConnectDB(self):
        
        DB_Connection = sqlite3.connect("DomainData.db")
        DB_Cursour = DB_Connection.cursor()
    
        DB_Cursour.execute("""CREATE TABLE IF NOT EXISTS DomainInfo (
                        DomainName TEXT,
                        Expiring_Time TEXT,
                        PageRank TEXT,
                        AlexaRank TEXT,
                        Backlink_Info TEXT
        )""")

        DB_Connection.commit()
        DB_Connection.close()

    def InsertData(self,domName,ExpTime,PgRank,ARank,BlInfo):
        DB_Connection = sqlite3.connect("DomainData.db")
        DB_Cur = DB_Connection.cursor()
        DB_Cur.execute("INSERT INTO DomainInfo Values(?,?,?,?,?)",(domName,ExpTime,PgRank,ARank,BlInfo))
        DB_Connection.commit();
        DB_Connection.close();
    
    def Export_Csv(self,EnumType):
        
        if EnumType == ExpOptions.Today:

            print("Performing Task...")

            try:
                DB_Connection = sqlite3.connect("DomainData.db")
                DB_Cur = DB_Connection.cursor()
                dt = datetime.datetime.now()
                date_time = dt.strftime("%Y-%m-%d")
                DB_Cur.execute("""SELECT * FROM DomainInfo WHERE Expiring_Time = ?""",(date_time,))
                DataList = DB_Cur.fetchall()
                DB_Connection.close();

                with open('CsvData/domainsToday.csv','w+') as file:
                    datafile = csv.writer(file)
                    datafile.writerow(['DomainName','Expiring_Date','PageRank','AlexaRank','Backlink_Info'])
                    datafile.writerows(DataList)

                print("Operation Completed!")

            except Exception as err:
                exception_type = type(err).__name__
                print("Error Occured! " + exception_type)

        elif EnumType == ExpOptions.Week:

            print("Performing Task...")

            try:
                DB_Connection = sqlite3.connect("DomainData.db")
                DB_Cur = DB_Connection.cursor()
                dt = datetime.datetime.now()
                date_time = dt.strftime("%Y-%m-%d")
                DB_Cur.execute("""SELECT * FROM DomainInfo WHERE Expiring_Time >= ?""",(date_time,))
                DataList = DB_Cur.fetchall()
                DB_Connection.close();

                with open('CsvData/domainsThis_Week.csv','w+') as file:
                    datafile = csv.writer(file)
                    datafile.writerow(['DomainName','Expiring_Date','PageRank','AlexaRank','Backlink_Info'])
                    datafile.writerows(DataList)

                print("Operation Completed!")

            except Exception as err:
                exception_type = type(err).__name__
                print("Error Occured!" + exception_type)


    def PurgeTable(self):
        print("Performing Task...")
        try:
            DB_Connection = sqlite3.connect("CsvData/DomainData.db")
            DB_Cur = DB_Connection.cursor()
            dt = datetime.datetime.now()
            date_time = dt.strftime("%Y-%m-%d")
            DB_Cur.execute("""DELETE FROM DomainInfo WHERE Expiring_Time < ?""",(date_time,))
            DB_Connection.commit();
            DB_Connection.close();
            print("Purge Complete")

        except Exception as err:
            exception_type = type(err).__name__
            print("Error Occured! " + exception_type)
