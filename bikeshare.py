# Python 3.8.8
# Pandas 1.2.4
# Numpy  1.20.1

import time
import pandas as pd
import numpy as np
from datetime import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = { 'January': 1,
               'February': 2,
               'March': 3,
               'April': 4,
               'May': 5,
               'June': 6,
               'July': 7,
               'August': 8,
               'September': 9,
               'October': 10,
               'November': 11,
               'December': 12 }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        log_enable = input('Would you like to enable runtime logs? (Y/N): ')
        global LOGGING
        if log_enable.lower() == 'y':
            LOGGING = True
            print('Runtime logs enabled.\n')
            break
        elif log_enable.lower() == 'n':
            LOGGING = False
            print('Runtime logs disabled.\n')
            break
        print('Invalid input. Please enter Y or N.')
    
    # get user input for city (chicago, new york city, washington).
    while True:
        city = input(('Where would you like to see data from?\n'
                     'Choose from Chicago, New York, or Washington: '))
        if city.lower() in ['chicago', 'new york city', 'washington']:
            city = city.lower()
            break
        elif city.lower() in ['nyc', 'ny', 'new york']:
            city = 'new york city'
            break
        elif city.lower() == 'or washington':
            print("Don't get smart with me. You know what an Oxford Comma is.")
        print('Invalid Input. Please choose from: Chicago, New York, or Washington.')
    
    # ask user if they would like to filter by month, day, or both
    data_filter = False
    while True:
        data_filter = input(('How would you like to filter the data?\n'
                            'Choose from Month, Day, Both, or leave blank for no filter: '))
        if data_filter.lower() in ['month', 'day', 'both'] or not data_filter:
            data_filter = data_filter.lower()
            break
        print('Invalid Input. Choose from Month, Day, Both, or leave blank for no filter.')
    
    # get user input for month (all, january, february, ... , june)
    month = 'all'
    if data_filter in ['month', 'both']:
        while True:
            month = input(('Would you like to filter data\n'
                          'Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec,'
                          ' or leave blank for no filter: '))
            try:
                month = [x for x in MONTH_DATA.keys() if x.lower().startswith(month)][0]
            except IndexError:
                month = 'err'
            
            if not month:
                month = 'all'
                break
            elif month != 'err':
                break
            print(('Invalid Input. Please select from the following: Jan, Feb, Mar, Apr, May, Jun,'
                  ' Jul, Aug, Sep, Oct, Nov, Dec, or leave blank for no filter.'))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = 'all'
    if data_filter in ['day', 'both']:
        while True:
            day = input(('Please select a day to filter by from the following:\n'
                         'Mon, Tue, Wed, Thu, Fri, Sat, Sun, or leave blank for no filter: '))
            if day.title() in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
                day = day.title()
                break
            elif not day:
                day = 'all'
                break;
            print(('Invalid Input. Please select from the following: '
                   'Mon, Tue, Wed, Thu, Fri, Sat, Sun, or leave blank for no filter.'))

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    df = pd.read_csv(CITY_DATA[city.lower()])
    
    # Convert Start Time to DateTime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract Start Time month and day
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # Filter by month
    if month != 'all':
        month = MONTH_DATA[month.title()]
        df = df[df['month'] == month]
    
    # Filter by day
    if day != 'all':
        df = df[df['day_of_week'].str.startswith(day.title())]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    Args:
        (Pandas DataFrame) df - DataFrame containing the filtered city data
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # convert start time to DateTime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].value_counts().head(1)
    month_name = list(MONTH_DATA.keys())[list(MONTH_DATA.values()).index(popular_month.index[0])]
    month_count = popular_month[popular_month.index[0]]

    # display the most common day of week
    df['weekday'] = df['Start Time'].dt.day_name()
    common_day = df['weekday'].value_counts().head(1)
    day_name = common_day.index[0]
    day_count = common_day[0]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].value_counts().head(1)
    hour = dt.strptime(str(popular_hour.index[0]), '%H').strftime("%I %p").lstrip('0')
    hour_count = popular_hour.iloc[0]
    
    print('Most Frequent Month:'.ljust(30), month_name.ljust(20), 'Count: ', month_count)
    print('Most Frequent Day:'.ljust(30), day_name.ljust(20), 'Count: ', day_count)
    print('Most Frequent Hour:'.ljust(30), hour.ljust(20), 'Count: ', hour_count)

    log_print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    Args:
        (Pandas DataFrame) df - DataFrame containing the filtered city data
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    
    common_start = df['Start Station'].value_counts().head(1)
    start_station = common_start.index[0]
    start_count = common_start[0]

    # display most commonly used end station
    common_end = df['End Station'].value_counts().head(1)
    end_station = common_end.index[0]
    end_count = common_end[0]

    # display most frequent combination of start station and end station trip
    common_trip = (df['Start Station'] + ',' + df['End Station']).value_counts().head(1)
    trip_start, trip_end = common_trip.index[0].split(',')
    trip_count = common_trip[0]
    
    print('Most Popular Start Station:'.ljust(30), start_station.ljust(35), 'Count: ', start_count)
    print('Most Popular End Station:'.ljust(30), end_station.ljust(35), 'Count: ', end_count)
    print('Most Popular Trip:'.ljust(30), '|', trip_start.center(31), '|', 'Count: ', trip_count)
    print(''.rjust(30), '|', trip_end.center(31), '|')

    log_print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    Args:
        (Pandas DataFrame) df - DataFrame containing the filtered city data
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    
    print('Total Travel Time:'.ljust(30), total_travel)
    print('Average Travel Time:'.ljust(30), mean_travel)

    log_print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    Args:
        (Pandas DataFrame) df - DataFrame containing the filtered city data
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    try:
        # Display counts of user types
        print('User distribution:')
        user_types = df['User Type'].value_counts(dropna=False)
        for i, name in enumerate(user_types.index.tolist()):
            if pd.isnull(name):
                name = 'Unknown'
            print((name+':').ljust(30), user_types[i])
    except KeyError:
        print('No user type data is available for this city.')
        
    try:
        # Display counts of gender
        print('\nGender distribution:')
        genders = df['Gender'].value_counts(dropna=False)
        for i, name in enumerate(genders.index.tolist()):
            if pd.isnull(name):
                name = 'Unknown'
            print((name+':').ljust(30), genders[i])
    except KeyError:
        print('No gender data is available for this city.')
        
    try:
        # Display earliest, most recent, and most common year of birth
        print('\nBirth year statistics:')
        common_year = df['Birth Year'].value_counts().head(1)
        print('Earliest Birth Year:'.ljust(30), int(df['Birth Year'].min()))
        print('Most Recent Birth Year:'.ljust(30), int(df['Birth Year'].max()))
        print('Most Common Birth Year:'.ljust(30), str(int(common_year.index[0])).ljust(15), \
            'Count: ', common_year.iloc[0])
    except KeyError as e:
        print('No birth year data is available for this city.')
        
    log_print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """
    Incrementally prints the next 5 lines of the given DataFrame until the end is reached,
    or the user cancels at the prompt.
    Args:
        (Pandas DataFrame) df - DataFrame containing the filtered city data
    """
    user_input = input('Would you like to display the raw data for this filter? (Y/N): ')
    
    if user_input.lower() == 'y':
        #display next five lines of data
        for lines, start, end in chunker(df):
            print('Lines {} to {} of {}:'.format(start, end, df.shape[0]))
            for line in lines:
                print(line, '\n')
            #ask if user wants to continue
            while True:
                user_input = input('Would you like to display the next five trips? (Y/N): ')
                if user_input.lower() == 'n':
                    print('Cancelling print.\n')
                    return
                elif user_input.lower() == 'y':
                    break
                print('Invalid input. Please enter Y or N.')
    else:
        print('Not showing raw data.\n')

def chunker(df, size=5):
    """
    Returns the next size rows of the given DataFrame
    Args:
        (Pandas DataFrame) df - DataFrame containing the filtered city data
        (int) size - the number of lines to split the DataFrame into. Default: 5
    """
    for start in range(0, df.shape[0], size):
        #get end point
        end = min(start + size, df.shape[0])
        #append next five lines to return list
        next_chunk = []
        for i in range(start, end):
            next_chunk.append(df.iloc[i])
        yield next_chunk, start, end-1

def log_print(text):
    """
    Prints the input to console only if the LOGGING global variable is enabled
    Args:
        (str) text - The text to print
    """
    if LOGGING:
        print(text)

def main():
    """ The main body of the program."""
    while True:
        try:
            #ask user for data filters
            city, month, day = get_filters()
            #load data into DataFrame
            df = load_data(city, month, day)
            #run statistics if df has data
            if not df.empty:
                time_stats(df)
                station_stats(df)
                trip_duration_stats(df)
                user_stats(df)
                show_raw_data(df)
            else:
                print('There is no data to display for this filter.')
            #prompt user for restart
            restart = input('\nWould you like to restart? (Y/N).\n')
            if restart.lower() != 'y':
                break
        except KeyboardInterrupt:
            #gracefully exit the program on ctrl+c intercept
            print('\n\nKeyboard Interrupt detected. Exiting program.')
            break

#run main if this file is not an import
if __name__ == "__main__":
	main()
