import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

MONTHS = ( 'January', 'February', 'March', 'April', 'May', 'June' )

DAYS = ( 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' )

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_input = input('\nCity? (New York, Chicago, Washington)\n')
    while city_input.title() not in list(CITY_DATA):
        print('\n' + str(city_input) + ' is no valid input for city.')
        city_input = input('\nCity? (New York City, Chicago, Washington)\n')

    # get user input for month (all, january, february, ... , june)
    month_input = input('Month? (January, February, .. December - or all)\n')
    while (month_input.title() not in MONTHS) and (month_input.title() != 'All'):
        print('\n' + str(month_input) + ' is no valid input for month.')
        month_input = input('\Month? (January, February, .. December - or all)\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_input = input('Day? (Monday, Tuesday, ... Sunday - or all)\n')
    while (day_input.title() not in DAYS) and (day_input.title() != 'All'):
        print('\n' + str(day_input) + ' is no valid input for day.')
        day_input = input('\Day? (Monday, Tuesday, ... Sunday - or all)\n')

    city = city_input.title()
    month = month_input.title()
    day = day_input.title()

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
    df = pd.read_csv(CITY_DATA[city])
    start_and_endstations = []
    # add start/end station column
    for i in df.index:
        start_and_endstations.append(df['Start Station'][i] + ' and ' + df['End Station'][i])
        #df.insert(i, 'Start And Endstation', df['Start Station'][i] + ' and  ' + df['End Station'][i])
        #print(df)
    df['Start And Endstation'] = start_and_endstations
        
    
    # extract month (str) and day of week (str) from start time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.day_name()

    #print(month)
    # filter for month
    if(month != 'All'):
        df = df[df['month'] == month]

    # filter for day
    if(day != 'All'):
        df = df[df['day'] == day]

    #print(df)
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # check: values_month = df['month'].value_counts()
    # check: print(values_month)
    most_com_month = df['month'].mode()
    print('The most common month is ' + most_com_month.to_string(index=False) + '.')

    # display the most common day of week
    # check: values_day = df['day'].value_counts()
    # check: print(values_day)
    most_com_day = df['day'].mode()
    print('The most common weekday is ' + most_com_day.to_string(index=False) + '.')
    # display the most common start hour
    # check: values_hour = df['Start Time'].dt.hour.value_counts()
    # check: print(values_hour)
    most_com_start_hour = df['Start Time'].dt.hour.mode()
    print('The most common hour is ' + most_com_start_hour.to_string(index=False) + '.')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # check: most_com_sstation_val = df['Start Station'].value_counts()
    # check: print(most_com_sstation_val)
    most_com_sstation = df['Start Station'].mode()
    print('The most common start station is ' + most_com_sstation.to_string(index=False) + '.')

    # display most commonly used end station
    # check: most_com_estation_val = df['End Station'].value_counts()
    # check: print(most_com_estation_val)
    most_com_estation = df['End Station'].mode()
    print('The most common end station is ' + most_com_estation.to_string(index=False) + '.')

    # display most frequent combination of start station and end station trip
    most_com_start_end_station = df['Start And Endstation'].mode()
    print('The most frequent start and end station combination is ' + most_com_start_end_station.to_string(index=False))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time_total = df['Trip Duration'].sum()
    print('The total travel time is {}'.format(convert_sec(int(travel_time_total))))

    # display mean travel time
    travel_time_mean = df['Trip Duration'].mean()
    print('The mean travel time is {}'.format(convert_sec(int(travel_time_mean)))) 

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def convert_sec(time):
    """Convert seconds into days, hours, minutes, seconds"""
    days = hours = minutes = seconds = 0

    days = int(time / 86400) # seconds into days
    temp_hour_in_seconds = time % 86400 # rest reconds
    hours = int(temp_hour_in_seconds / 3600) # how many hours are the rest reconds
    temp_minutes_in_seconds = temp_hour_in_seconds % 3600
    minutes = int(temp_minutes_in_seconds / 60) # remaining minutes
    seconds = int(temp_minutes_in_seconds % 60) # remaining seconds
    return '{} days, {} hours, {} minutes and {} seconds'.format(days, hours, minutes, seconds)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print(user_type_count.to_string(index=True))
    
    # Display counts of gender
    try:
        user_type_count = df['Gender'].value_counts()
        print('\n' + user_type_count.to_string(index=True))
    except:
        print('\nNo gender data available.')


    # Display earliest, most recent, and most common year of birth
    try:
        birth_years = df['Birth Year']
        print('\nEarliest year of birth: ' + str(birth_years.min()))
        print('Most recent year of birth: ' + str(birth_years.max()))
        print('Most common year of birth: ' + str(birth_years.mode()))
    except:
        print('\nNo birth year data available.')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def show_raw_data():
    print()

def main():
    pd.set_option('display.max_colwidth', None)
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # ask if user wants to see 5 lines of raw data
        i_first = 0
        i_last = 5
        while (i_first < df.shape[0]):
            if(i_first > 0):
                show_raw_data = input('Do you want to see the next 5 lines of raw data? Type yes or no.\n')
            else:
                show_raw_data = input('Do you want to see the first 5 lines of raw data? Type yes or no.\n')
            if(show_raw_data == 'yes'):
                print(df[i_first:i_last])
                i_first+=5
                i_last+=5
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == '__main__':
	main()
