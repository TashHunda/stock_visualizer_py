from ast import Lambda
from cgitb import lookup
from os import times
import time
from tkinter import NS
import pandas as pd
import pygal as pg


def fetchSymbol():
    userChoice = input("Enter the stock symbol you are looking for: ")
    return userChoice.upper()


def chartType():
    while True:
        try:
            print("Chart Types:")
            print("------------")
            print("1. Bar")
            print("2. Line")
            chart_type = int(input("Choose what type of chart you want (1, 2): "))
            if chart_type != 1 and chart_type != 2:
                print("\nError: Please only enter 1 or 2\n")
                continue
        except ValueError:
                print("\nError: Please only enter 1 or 2\n")
                continue
        else:
            return chart_type

        
def get_time_series():
    again = True
    while again:
        try: 
            interval = Lambda
            print("Select the Time Series of the chart you want to Generate")
            print("1. Intraday")
            print("2. Daily")
            print("3. Weekly")
            print("4. Monthly")
            series = input("Enter the time series option(1,2,3,4): ")
            if series is not "1" or series is not "2" or series is not "3" or series is not "4":
                again = True
                return again

            if series == "1":
                print("\n\n1. 1min")
                print("2. 5min")
                print("3. 15min")
                print("4. 30min")
                print("5. 60min")
                interval = input("Please choose time interval: ")
            timeSeriesObject = {"series": series,
                                "interval": interval}
            again = False
        except ValueError:
            print("This is an unacceptable response, enter a valid value")
        
    return timeSeriesObject

        
def dateFormatCheck(date):
    
    #check if given date is numerical
    ymd = date.split("-")
    if len(ymd) != 3:
        print("Please use the correct format(YYYY-MM-DD).")
        return getDates()

    for digit in ymd:
        if not digit.isdigit():
            print("Please enter numerical values only.")
            return getDates()

    #check if variables are valid in length and value
    year = ymd[0]
    month = ymd[1]
    day = ymd[2]
    if len(year) != 4 or len(month) != 2 or len(day) != 2:
        print("Please make sure date is in \"YYYY-MM-DD\" format.")
        return getDates()
    if int(month) > 12 or int(day) > 31:
        print("Please enter a valid Month/Day")
        return getDates()

    #check if user time is in the future
    userTime = time.strptime(date, "%Y-%m-%d")
    currentTime = time.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")
    if userTime > currentTime:
        print("Date cannot be after today.")
        return getDates()

    
def getDates():
    #begin date
    beginDate = input("Please enter the start date (YYYY-MM-DD) format: ")

    #end date
    endDate = input("Please enter the end date (YYYY-MM-DD) format: ")
    if endDate <= beginDate:
        print("The ending date must not be before the beginning date. \nPlease try again.")
        getDates()

    #date format check
    datesArray = [beginDate, endDate]
    for date in datesArray:
        dateFormatCheck(date)

    return datesArray


def api(userObject):

    key = 'SJ11I1BHEDRFJ1B6' # api key
    symbol = userObject["symbol"]
    try:
        match userObject["timeSeriesObject"]["series"]:
            case "1":
                intraInterval = userObject["timeSeriesObject"]["interval"]
                intraday = "TIME_SERIES_INTRADAY"
                url = f"https://www.alphavantage.co/query?function={intraday}&symbol={symbol}&interval={intraInterval}min&apikey={key}&datatype=csv"
            case "2":
                daily = "TIME_SERIES_DAILY"
                url = f"https://www.alphavantage.co/query?function={daily}&symbol={symbol}&apikey={key}&datatype=csv"
            case "3":
                weekly = "TIME_SERIES_WEEKLY"
                url = f"https://www.alphavantage.co/query?function={weekly}&symbol={symbol}&apikey={key}&datatype=csv"
            case "4":
                monthly = "TIME_SERIES_MONTHLY"
                url = f"https://www.alphavantage.co/query?function={monthly}&symbol={symbol}&apikey={key}&datatype=csv"
            case _:
                print("Error occured. Please try again.")
                main()
        generateChart(url,userObject)
    except Exception as e:
        print(f"Error occurred: {e}. Please check if symbol is correct.")

            
def generateChart(url,userObject):

    symbol = userObject["symbol"]
    beginDate = userObject["datesObject"][0]
    endDate = userObject["datesObject"][1]
    chartChoice = str(userObject["chart"])

    if chartChoice == "1":
        chart = pg.Bar()
    if chartChoice == "2":
        chart = pg.Line(x_label_rotation=20)
    
    csvRow = pd.read_csv(url,
                    dtype={
                        "timestamp" : str,
                        "open" : float, 
                        "high" : float,
                        "low" : float,
                        "close" : float
                    })
    csvRow["timestamp"] = pd.to_datetime(csvRow["timestamp"])
    mask = (csvRow["timestamp"] > beginDate) & (csvRow["timestamp"] <= endDate)

    data_Frame = csvRow.loc[mask]

    chart.title = f"Stock Data for {symbol}: {beginDate} to {endDate}"

    timestamp = []
    open = []
    high = []
    low = []
    close = []

    print(data_Frame)

    for i, r in data_Frame.iterrows():
        timestamp.append(r["timestamp"])
        open.append(r["open"])
        high.append(r["high"])
        low.append(r["low"])
        close.append(r["close"])

    chart.x_labels = timestamp

    chart.add('open', open)
    chart.add('high', high)
    chart.add('low', low)
    chart.add('close', close)

    chart.render_in_browser()


def createUserObject():
    symbol = fetchSymbol()
    chart = chartType()
    timeSeriesObject = get_time_series()
    datesArray = getDates()

    userObject = {"symbol": symbol,
                "chart": chart,
                "timeSeriesObject": timeSeriesObject,
                "datesObject": datesArray}

    return userObject

def main():
    while True:
        userObject = createUserObject()
        api(userObject)

        runAgain = input("Would you like to view more stock data? (y/n): ")
        if runAgain.lower() != 'y':
            print("Goodbye!")
            break


main()
