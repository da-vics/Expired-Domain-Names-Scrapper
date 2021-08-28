from DbContext import DataBaseManager, ExpOptions
from webScrapper import Scrapper
import webbrowser


def main():

    print("Press 1. to get Domain List")
    print("Press 2. to Export Domains expiring today")
    print("Press 3. to Export domains expiring this week")
    print("Press 4. to Purge Old Domains")
    print("Press 5. to Exit")

    IsActive = True

    while IsActive:

        str = input("Input Option: ")

        if str == '1':
            scrap = Scrapper()
            scrap.Login()
            if scrap.isLoggIn:
                scrap.GetDomainList()

        elif str == '2':
            DBManger = DataBaseManager()
            DBManger.Export_Csv(ExpOptions.Today)

        elif str == '3':
            DBManger = DataBaseManager()
            DBManger.Export_Csv(ExpOptions.Week)

        elif str == '4':
            DBManger = DataBaseManager()
            DBManger.PurgeTable()

        elif str == '5':
            IsActive = False
            print("Program Stopped..")
            break

        else:
            print("Invalid Option!")

if __name__ == "__main__":
    main()

