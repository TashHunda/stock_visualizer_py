import datetime
import time
import pandas as pd
import pygal as pg
from webbrowser import get
from alpha_vantage.timeseries import TimeSeries

class DateError(Exception):
    pass


def fetchSymbol():
    userChoice = input("Enter the stock symbol you are looking for: ")
    return userChoice


def chartType():
    print("Chart Types:")
    print("------------")
    print("1. Bar")
    print("2. Line")
    chart_type = input("Choose what type of chart you want (1, 2): ")
    return chart_type


def dateFormatCheck(userDate):
    #check if given date is numerical
    ymd = userDate.split("-")
    if len(ymd) != 3:
        print("Please use the correct format(YYYY-MM-DD).")
        return startDate()

    for digit in ymd:
        if not digit.isdigit():
            print("Please enter numerical values only.")
            return startDate()

    #check if variables are valid in length and value
    year = ymd[0]
    month = ymd[1]
    day = ymd[2]
    if len(year) != 4 or len(month) != 2 or len(day) != 2:
        print("Please make sure date is in \"YYYY-MM-DD\" format.")
        return startDate()
    if int(month) > 12 or int(day) > 31:
        print("Please enter a valid Month/Day")
        return startDate()

    #check if user time is in the future
    userTime = time.strptime(userDate, "%Y-%m-%d")
    currentTime = time.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")
    if userTime > currentTime:
        print("Date cannot be after today.")
        return startDate()


def startDate():
    userDate = input("Enter the start date (YYYY-MM-DD): ")
    dateFormatCheck(userDate)
    return userDate


def getEndDate():
    begin_date = datetime.datetime.strptime('2022-07-11', '%Y-%m-%d')
    endingDate = input("Please enter the end date of the data in YYYY-MM-DD format: ")
    endDate = datetime.datetime.strptime(endingDate, "%Y-%m-%d")
    if endDate <= begin_date:
        raise DateError("The ending date must not be before the beginning date.")
    return endDate


def get_time_series():
    while True:
        try: 
            print("Select the Time Series of the chart you want to Generate")
            print("1. Intraday")
            print("2. Daily")
            print("3. Weekly")
            print("4. Monthly")
            userChoice = int(input("Enter the time series option(1,2,3,4): "))
        except ValueError:
            print("This is an unacceptable response, enter a valid value")
            continue
        else:
            return userChoice


def generateChart():
    data_frame = pd.read_csv("weekly_IBM.csv")
    data_frame.head
    #importing pandas library.
    data_frame = pd.read_csv("weekly_IBM.csv",
                    dtype={
                        "date" : str,
                        "open" : float, 
                        "high" : float,
                         "low" : float,
                        "close" : float
                    })

    #import pygal
    #append data
    a = []
    b = []
    c = []
    d = []

    line_chart = pg.Line()
    #titles 
    line_chart_title = 'Open, High, Low and Close'
    #range of months 1 to 12
    line_chart.x_labels = map(str, "date")
    for index, row in data_frame.iterrows():
        a.append(row["open"])
        b.append(row["high"])
        c.append(row["low"])
        d.append(row["close"])
    # adding appended list
    line_chart.add('open', a)
    line_chart.add('high', b)
    line_chart.add('low', c)
    line_chart.add('close', d)
    #file render
    line_chart.render_in_browser()


def main():
    key = 'SJ11I1BHEDRFJ1B6' # api key

    symbolChoice = fetchSymbol()
    chartChoice = chartType()
    startDateChoice = startDate()
    endDateChoice = getEndDate() # Random inputs cause a crash
    timeSeriesChoice = get_time_series()

    # Eventually this should take all the above stings as params
    generateChart() # Causes a crash on Brandon's system


main()
