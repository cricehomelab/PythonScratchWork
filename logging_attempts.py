import os
import logging
from datetime import date, datetime



def today_is():
    current_day = date.today()
    current_day = current_day.strftime("%Y%m%d")
    return current_day


def log_time():
    next_time = datetime.now()
    next_time = next_time.strftime("%Y%m%d %H:%M:%S.%f")
    return next_time

def add_log(message, type):
    if type == "info":
        logging.info(f'{log_time()} : {message}')
    elif type == "debug":
        logging.debug(f'{log_time()} : {message}')
    elif type == "warning":
        logging.warning(f'{log_time()} : {message}')

day = today_is()

logging.basicConfig(filename=f'{day}-logtest.log', encoding='utf-8', filemode='w', level=logging.DEBUG)

logging.debug(f'This message should go to the log file {day}')
# get a time baseline
logging.info(f'{log_time()} So should this')

# doing something to take a fraction of a second
i = 0
for i in range(1000):
    i += 1
    print(i)

# milliseconds should be different
logging.warning(f'{log_time()} And this, too')