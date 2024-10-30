import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt


def get_valid_symbol(prompt):
    while True:
        symbol = input(prompt)
        if symbol.isalpha():
            return symbol.upper()
        else:
            print("Please enter a valid symbol using only alphabetic characters.")


def get_valid_input(prompt):
    while True:
        user_input = input(prompt)
        try:
            value = int(user_input)
            if 0 < value < 255:
                return value
            else:
                print("Please enter a integer value between 0 and 255.")
        except ValueError:
            print("Please enter an integer value.")


def read_Data(symbol):

    # The os.getlogin() method returns the name of the user logged in to the terminal.
    # with this way, file path changes dynamically from user to user.
    user_name = os.getlogin()

    # read the downloaded csv file and assign the datas into df variable.
    df = pd.read_csv(f"C:\\Users\\{user_name}\\Downloads\\{symbol}.csv")

    return df


def delete_csv_file(symbol):
    
    user_name = os.getlogin()

    # Define the file path which you want to delete
    file_path = f"C:\\Users\\{user_name}\\Downloads\\{symbol}.csv"

    # Check the existing of the file, if it exits then delete.
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} is deleted succesfully.")
    else:
        print(f"{file_path} couldn't find or already deleted.")


def calculate_ema(df, short_ema, long_ema):

    df['ema_short'] = df['Close'].ewm(span = short_ema, adjust=False).mean()
    df['ema_long'] = df['Close'].ewm(span = long_ema, adjust=False).mean()

    df['bullish'] = 0.0
    df['bullish'] = np.where(df['ema_short'] > df['ema_long'], 1.0, 0.0)
    df['crossover'] = df['bullish'].diff()  
    # Gets the difference between two consecutive rows in the 'bullish' column.
    

def show_graph(df, symbol):

    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(1, 1, 1, ylabel='Price in $')

    df['Close'].plot(ax=ax1, color='blue', lw=2.)
    df['ema_short'].plot(ax=ax1, color='yellow', lw=2.)
    df['ema_long'].plot(ax=ax1, color='purple', lw=2.)

    print(df)

    ax1.plot(df.loc[df.crossover == 1.0].index, 
                    df.ema_short[df.crossover == 1.0],
                    '^', markersize=10, color='g', lw=0, label='Buy Signal')

    ax1.plot(df.loc[df.crossover == -1.0].index, 
             df.ema_short[df.crossover == -1.0],
             'v', markersize=10, color='r', lw=0, label='Sell Signal')

    # Set the properties of the graph
    ax1.legend(["Close", f"short_ema ({short_ema})", f"short_ema ({long_ema})", "Buy", "Sell"])
    ax1.grid(True)
    ax1.set_title(f'Graph of "{symbol.upper()}" and BUY/SELL Signals with Moving Averages')
    ax1.set_xlabel('Range')
    ax1.set_ylabel('Price')

    # Show the graph
    plt.show()



symbol = get_valid_symbol("Enter the symbol: ")
short_ema = get_valid_input("Enter the short term value: ")
long_ema = get_valid_input("Enter the long term value: ")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")  # set to full-size screen

# selenium library starts the google chrome
driver = webdriver.Chrome(options=chrome_options)

url = f"https://finance.yahoo.com/quote/{symbol}/history"

# make a request to visit the given website link
driver.get(url)

# Set a timeout to allow the cookie window to open and find the appropriate button to reject the cookies :)
driver.implicitly_wait(20)

# find the button which scrolls down to make the reject cookie button appear and then clik
go_to_end_button = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/button').click()
time.sleep(5)

# reject the cookies by clicking appropriate place by finding its XPATH 
reject_cookie = driver.find_element(By.XPATH, '/html/body/div/div/div/div/form/div[2]/div[2]/button[2]').click()

# Set a timeout to be able to allow the relavent window to open and download the historical datas
driver.implicitly_wait(5)

# find the download button by using its XPATH then download it
element = driver.find_element(By.XPATH ,'//*[@id="nimbus-app"]/section/section/section/article/div[1]/div[2]/div/a').click()

# set a timeout
time.sleep(2)

# close the browser
driver.quit()


# read the datas from inside of the csv file and assign them into the variable.
default_df = read_Data(symbol)

# remove unnecessary coloumns from within the csv file
modified_df = default_df.drop(columns=['Open','High','Low','Adj Close','Volume'])

# calculates the Exponantial Moving Averages according to the given datas
calculate_ema(modified_df, short_ema, long_ema)

# Show the graph to show the buy & sell points and the other lines.
show_graph(modified_df, symbol)

# delete the file which was downloaded at the beginning.
delete_csv_file(symbol)