import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_month_filter():
    '''Ask user to specify month filter'''

    while True:
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = input('Which month? January, February, March, April, May, June?\n')
        if month.title() in months:
            return month.lower()
        else:
            print('Invalid Month...Please Enter again')


def get_weekday_filter():
    '''Ask user to specify weekday filter'''

    while True:
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day = input('Which day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday?\n')
        if day.title() in days:
            return day.title()
        else:
            print('Invalid Week Day...Please Enter again')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    month = 'all'
    day = 'all'
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        cities = {'Chicago': 'chicago', 'New York': 'new york city', 'Washington': 'washington'}
        city_name = input('Would you like to see data for Chicago, New York, or Washington\n')
        if city_name.title() in cities:
            city = cities[city_name.title().strip()]
            break
        else:
            print('Invalid Input...Please Enter again\n')

    # condition
    filter = 'all'
    while True:
        filters = ['none', 'month', 'day', 'both']
        filter = input(
            'Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.\n')
        if filter.lower() in filters:
            break
        else:
            print('Invalid Input...Please Enter again\n')

    # TO DO: get user input for month (all, january, february, ... , june)
    if filter.lower() == 'both':
        month = get_month_filter()
        day = get_weekday_filter()
    elif filter.lower() == 'month':
        month = get_month_filter()
    elif filter.lower() == 'day':
        day = get_weekday_filter()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    print('-' * 40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def calculate_mode(df, column_name):
    """
    Calculate MODE for the given column_name

    Args:
        (DataFrame) df - dataframe object to calculate mode
        (str) column_name - name of the column to calculate mode

    Returns:
        MODE value for given column name
    """
    return df[column_name].mode()[0]


def calculate_max_count(df, column_name):
    """
    Calculate max value count for the given column_name

    Args:
        (DataFrame) df - dataframe object to calculate Max Value
        (str) column_name - name of the column to calculate MODE

    Returns:
        max value count value for given column name
    """
    return df[column_name].value_counts().max()


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = calculate_mode(df, 'month')
    max_month_value = calculate_max_count(df, 'month')
    print('Most common Month : {}, having Count : {}'.format(months[month - 1].title(), max_month_value))

    # TO DO: display the most common day of week
    weekday = calculate_mode(df, 'day_of_week')
    max_weekday_value = calculate_max_count(df, 'day_of_week')
    print('Most common Weekday : {}, having Count : {}'.format(weekday, max_weekday_value))

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # TO DO: display the most common start hour

    hour = calculate_mode(df, 'hour')
    max_hour_value = calculate_max_count(df, 'hour')
    print('Most common Start Hour : {}, having Count : {}'.format(hour, max_hour_value))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = calculate_mode(df, 'Start Station')
    max_start_station_value = calculate_max_count(df, 'Start Station')
    print('Most common start station : {}, having Count : {}'.format(start_station, max_start_station_value))

    # TO DO: display most commonly used end station
    end_station = calculate_mode(df, 'End Station')
    max_end_station_value = calculate_max_count(df, 'End Station')
    print('Most common End station : {}, having Count : {}'.format(end_station, max_end_station_value))

    # TO DO: display most frequent combination of start station and end station trip
    station_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    trip_count = df.groupby(['Start Station', 'End Station']).size().max()
    print('Most popular Trip is {}, having Count : {}'.format(station_combination, trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display Total Travel Time
    print('Total Travel Time : {}'.format(df['Trip Duration'].sum()))
    print('Count : {}'.format(df['Trip Duration'].value_counts().sum()))
    # TO DO: display mean travel time
    print('Average Travel Time : {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('User Statistic...')
    user_types = zip(df['User Type'].value_counts().index, df['User Type'].value_counts().values)

    for user_type, count in user_types:
        print(user_type, ':', count, end='    ')

    if city == 'washington':
        print('\nGender Data and Birth Data is not available for Statistic Calculation')
    else:
        # TO DO: Display counts of gender
        print('\n\nGender Statistic...')
        gender_types = zip(df['Gender'].value_counts().index, df['Gender'].value_counts().values)

        for gender_type, count in gender_types:
            print(gender_type, ':', count, end='    ')

        # TO DO: Display earliest, most recent, and most common year of birth
        print('\n\nDate of Birth Statistic...')
        print('\nEarliest Date of Birth: {}'.format(int(df['Birth Year'].min())))
        print('Most Recent Date of Birth: {}'.format(int(df['Birth Year'].max())))

        dob = calculate_mode(df, 'Birth Year')
        max_dob_value = calculate_max_count(df, 'Birth Year')
        print('Most Common Date of Birth: {}, having count {}'.format(int(dob), max_dob_value))

        print("\nThis took %s seconds." % (time.time() - start_time))

    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        print('Calculating Statistics for city {}'.format(city))
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        print('\n----------------Raw Data----------------\n')
        i, j = 0, 5
        choice = 'yes'
        while True:
            print(df.iloc[i:j])
            while True:
                choice = input('Do you want to see more 5 lines of raw data? Enter yes or no.\n')
                if choice.lower() == 'yes' or choice.lower() == 'no':
                    break
                else:
                    print('Invalid Input... Please Enter again')
            if choice == 'no':
                break
            else:
                i += 5
                j = i + 5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
