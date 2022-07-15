from ast import Lambda
import time
import pandas as pd
import pygal as pg

def fetchSymbol():
    print('')
    userChoice = input("Enter the stock symbol you are looking for: ")
    return userChoice


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

        
def get_time_series(symbol):
    while True:
        try: 
            intervalOption = Lambda
            print("Select the Time Series of the chart you want to Generate")
            print("1. Intraday")
            print("2. Daily")
            print("3. Weekly")
            print("4. Monthly")
            timeSeries = input("Enter the time series option(1,2,3,4): ")
            if timeSeries == "1":
                print("\n\n1. 1min")
                print("2. 5min")
                print("3. 15min")
                print("4. 30min")
                print("5. 60min")
                intervalOption = input("Please choose time interval: ")
            userChoiceArray = [timeSeries, intervalOption, symbol]
        except ValueError:
            print("This is an unacceptable response, enter a valid value")
            continue
        else:
            return userChoiceArray

        
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


def api(condition, datesArray, chartChoice):

    key = 'SJ11I1BHEDRFJ1B6' # api key

    match condition[0]:
        case "1":
            intraInterval = condition[1]
            intraday = "TIME_SERIES_INTRADAY"
            url = f"https://www.alphavantage.co/query?function={intraday}&symbol={condition[2]}&interval={intraInterval}min&apikey={key}&datatype=csv"
            generateChart(url, chartChoice)
        case "2":
            daily = "TIME_SERIES_DAILY"
            url = f"https://www.alphavantage.co/query?function={daily}&symbol={condition[2]}&apikey={key}&datatype=csv"
            generateChart(url, chartChoice)
        case "3":
            weekly = "TIME_SERIES_WEEKLY"
            url = f"https://www.alphavantage.co/query?function={weekly}&symbol={condition[2]}&apikey={key}&datatype=csv"
            generateChart(url, chartChoice)
        case "4":
            monthly = "TIME_SERIES_MONTHLY"
            url = f"https://www.alphavantage.co/query?function={monthly}&symbol={condition[2]}&apikey={key}&datatype=csv"
            generateChart(url, chartChoice)
            # url2 = f"https://www.alphavantage.co/query?function={monthly}&symbol={condition[2]}&start.date=%7BstartDate%7D&end.date=%7BgetEndDate%7D&inte&apikey=%7BBSJ11I1BHEDRFJ1B6%7D"
        case _:
            print("Error occured. Please try again.")
            main()

            
def generateChart(url, chartChoice):
    data_frame = pd.read_csv(url)
    data_frame.head
    data_frame = pd.read_csv(url,
                    dtype={
                        "date" : str,
                        "open" : float, 
                        "high" : float,
                         "low" : float,
                        "close" : float
                    })

    a = []
    b = []
    c = []
    d = []

    chart = pg.Bar() if chartChoice == 1 else pg.Line()
    #titles 
    line_chart_title = 'Open, High, Low and Close'
    #range of months 1 to 12
    chart.x_labels = map(str, range(2002, 208))
    for index, row in data_frame.iterrows():
        a.append(row["open"])
        b.append(row["high"])
        c.append(row["low"])
        d.append(row["close"])
    # adding appended list
    chart.add('open', a)
    chart.add('high', b)
    chart.add('low', c)
    chart.add('close', d)
    #file render
    chart.render_in_browser()


def main():
    while True:
        symbol = fetchSymbol()
        chartChoice = chartType()
        userChoiceArray = get_time_series(symbol)
        datesArray = getDates()
        api(userChoiceArray, datesArray, chartChoice)

        print('')
        runAgain = input("Would you like to view more stock data? (y/n): ")
        if runAgain.lower() != 'y':
            print("Goodbye!")
            break


main()
