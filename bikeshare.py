import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = {'january':1, 'february':2, 'march':3,
              'april':4, 'may':5, 'june':6}

WEEK_DATA = {'monday':0, 'tuesday':1, 'wednesday':2,
             'thursday':3, 'friday':4, 'saturday':5, 'sunday':6}
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
    while True:
        city = input('Pick a city available (chicago, new york city, washington):')
        if city in list(CITY_DATA.keys()):
            break
        print('That\'s not a valid input, please try again')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Check all 6 months (all); Pick a month available (january, february, ... , june):')
        if month in list(MONTH_DATA.keys()) or month == 'all':
            break
        print('That\'s not a valid input, please try again')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Check all 7 days (all); Pick a day of week (monday, tuesday, ... sunday):')
        if day in list(WEEK_DATA.keys()) or day == 'all':
            break
        print('That\'s not a valid input, please try again')

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
    #filter city
    df = pd.read_csv(CITY_DATA[city])

    #filter month
    df['month'] = pd.to_datetime(df['Start Time']).dt.month

    if month != 'all':
        month = MONTH_DATA[month]
        df = df[df['month'] == month]

    #filter dayofweek
    df['dayofweek'] = pd.to_datetime(df['Start Time']).dt.weekday

    if day != 'all':
        day = WEEK_DATA[day]
        df = df[df['dayofweek']==day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if df['month'].nunique() != 1:
        popular_month_num = df['month'].value_counts().index[0]
        popular_month = list(MONTH_DATA.keys())[popular_month_num-1]
        print('the most common month:  ', popular_month)

    # display the most common day of week
    if df['dayofweek'].nunique() != 1:
        popular_day_num = df['dayofweek'].value_counts().index[0]
        popular_day = list(WEEK_DATA.keys())[popular_day_num]
        print('the most common day of week:  ', popular_day)

    # display the most common start hour
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    popular_starthour = df['hour'].value_counts().index[0]
    print('the most common start hour:  ', popular_starthour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_stations = df['Start Station'].value_counts()
    popular_start = start_stations.index[0]
    print('the most popular start station:  ', popular_start)

    # display most commonly used end station
    end_stations = df['End Station'].value_counts()
    popular_end = end_stations.index[0]
    print('the most popular end station:  ', popular_end)
    print('\n')

    # display most frequent combination of start station and end station trip
    grdf2 = df.groupby(by = ['Start Station', 'End Station'] ).size().reset_index(name='num').nlargest(1, 'num', keep='first')
    print('most popular combination of start station and end station trip:')
    print(grdf2)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = np.sum(df['Trip Duration'])
    r_total_time = round(total_time)
    print('total travel time:  ', r_total_time)

    # display mean travel time
    meantime = np.mean(df['Trip Duration'])
    r_mean_time = round(meantime)
    print('mean travel time:  ', r_mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    count_usertype = df['User Type'].value_counts()
    print('counts of user types:')
    print(count_usertype)
    print('\n')
    # display counts of gender
    if 'Gender' not in df.columns:
        print('No data available on users\' gender information')
    else:
        count_gender = df['Gender'].value_counts()
        print('counts of gender:')
        print(count_gender)
        print('\n')
    # display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
        print('No data available on users\' birth year information')
    else:
        df1 = df.dropna()
        sort_by = list(df1['Birth Year'].sort_values(ascending = False))
        count_by = df1['Birth Year'].value_counts()

        earliest = int(sort_by[-1])
        most_recent = int(sort_by[0])
        most_common = int(count_by.index[0])

        print('earliest year of birth:  ', earliest)
        print('most recent year of birth:  ', most_recent)
        print('most common year of birth:  ', most_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
