import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

day_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
months = ['january', 'february', 'march', 'april', 'may', 'june']
utypes = ['Subscriber', 'Customer']
genders = ['Male', 'Female']

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
    city = ''
    while CITY_DATA.get(city, 'no') == 'no':
        print('Would you like to see data for Chicago, New York City, or Washington?')
        response = input("Enter C for Chicago, N for New York City, or W for Washington\n")
        if response not in ('c', 'C', 'n', 'N', 'w', 'W'):
            print("Not a valid response.  Let's try again!\n")
        else:
            if response.lower() == 'c':
                city = 'chicago'
            elif response.lower() == 'n':
                city = 'new york city'
            else:
                city = 'washington'
    print("You've chosen {}.\n".format(city.title()))

    # get user input for month (all, january, february, ... , june)
    month = ''
    print('We have six months available for filtering: January through June.')
    print("If you wish to filter by a particular month, pick the month's corresponding number.")
    print("1 - January | 2 - February | 3 - March | 4 - April | 5 - May | 6 - June")
    response = input("Any other response will be interpreted as no month filtering.\n")

    if response not in [str(x + 1) for x in range(6)]:
        month = 'all'
        print('No month filter has been chosen.\n')
    else:
        month = months[int(response) - 1]
        print('Filter will be run on the month {}\n'.format(month))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    print("If you wish to filter by a particular day, pick the day's corresponding number.")
    print("1 - Monday | 2 - Tuesday | 3 - Wednesday | 4 - Thursday | 5 - Friday | 6 - Saturday | 7 - Sunday")
    response = input("Any other response will be interpreted as no day filtering.\n")

    if response not in [str(x + 1) for x in range(7)]:
        day = 'all'
        print('No day filter has been chosen\n')
    else:
        day = day_list[int(response) - 1]
        print('Filter will be run on the day {}\n'.format(day))

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
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA.get(city))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, hour and day of week from Start Time to create new columns
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['hour'] = pd.DatetimeIndex(df['Start Time']).hour
    df['day_of_week'] = (df['Start Time']).dt.weekday

    # combine start and end stations for use in mode call
    df['start and end'] = df['Start Station'].str.cat(df['End Station'], sep=" to ")

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day_list.index(day.title())]

    return df


def time_stats(df):
    # Displays statistics on the most frequent times of travel

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month & the count associated with it
    popular_month = df['month'].mode()[0]
    popular_month_count = np.count_nonzero(df['month'] == popular_month)
    print("The most popular month for your subset is {}; {} rentals were made"
          .format(months[popular_month - 1].title(), popular_month_count))

    # display the most common day of week & the count associated with it
    popular_day = df['day_of_week'].mode()[0]
    popular_day_count = np.count_nonzero(df['day_of_week'] == popular_day)
    print("The most popular weekday for your subset is {}; {} rentals were made"
          .format(day_list[popular_day].title(), popular_day_count))

    # display the most common start hour and convert to am/pm
    popular_hour = df['hour'].mode()[0]
    popular_hour_count = np.count_nonzero(df['hour'] == popular_hour)

    if popular_hour < 1:
        popular_hour_suffix = 'a.m.'
        popular_hour = 12
    elif popular_hour >= 12:
        popular_hour_suffix = 'p.m.'
        if popular_hour > 12:
            popular_hour -= 12
    else:
        popular_hour_suffix = 'a.m.'

    print("The most popular hour for your subset is {} {}; {} rentals were made"
          .format(popular_hour, popular_hour_suffix, popular_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city):
    # Displays statistics on the most popular stations and trip

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_count = np.count_nonzero(df['Start Station'] == popular_start_station)
    print("The most popular start station for your subset in {} is {}; {} trips began there"
          .format(city.title(), popular_start_station, popular_start_station_count))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_count = np.count_nonzero(df['End Station'] == popular_end_station)
    print("The most popular end station for your subset in {} is {}; {} trips finished there"
          .format(city.title(), popular_end_station, popular_end_station_count))

    # display most frequent combination of start station and end station trip
    popular_trip = df['start and end'].mode()[0]
    popular_trip_count = np.count_nonzero(df['start and end'] == popular_trip)
    print("The most popular trip for your subset in {} is {}; {} trips were taken"
          .format(city.title(), popular_trip, popular_trip_count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    # Displays statistics on the total and average trip duration.

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    td_by_hours = total_duration / 3600
    print('The total duration time for all trips is {} seconds, or {} hours'
          .format(total_duration, td_by_hours))

    # display mean travel time
    avg_duration = df['Trip Duration'].mean()
    ad_by_hours = avg_duration / 3600
    print('The average duration time for all trips is {} seconds, or {} hours'
          .format(avg_duration, ad_by_hours))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    # Displays statistics on bikeshare users

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = [np.count_nonzero(df['User Type'] == u_type) for u_type in utypes]
    print('{} trips were made by {}s, and the other {} trips were made by {}s'
          .format(user_counts[0], utypes[0], user_counts[1], utypes[1]))

    # Display counts of gender
    if city == 'washington':
        print('Gender counts not available for {}'.format(city.title()))
    else:
        gender_counts = [np.count_nonzero(df['Gender'] == gend) for gend in genders]
        print('Among subscribers, {} trips were made by {}s, and {} trips were made by {}s'
            .format(gender_counts[0], genders[0], gender_counts[1], genders[1]))

    # Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print('Birth year counts not available for {}'.format(city.title()))
    else:
        most_frequent_yob = df['Birth Year'].mode()
        earliest_yob = df['Birth Year'].min()
        latest_yob = df['Birth Year'].max()
        mfyob_count = np.count_nonzero(df['Birth Year'] == most_frequent_yob[0])
        print('Among subscribers, our oldest were born in {}, our youngest in {}'
            .format(int(earliest_yob), int(latest_yob)))
        print('The most frequent age is for those born in {}, with {} instances'
            .format(int(most_frequent_yob), mfyob_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw_data(df, pointer, city):
    # prints the raw data field by field

    print('\n Record {}\n'.format(pointer))
    print('Start Time : {}'.format(df['Start Time'][pointer]))
    print('End Time : {}'.format(df['End Time'][pointer]))
    print('Trip Duration : {}'.format(df['Trip Duration'][pointer]))
    print('Start Station : {}'.format(df['Start Station'][pointer]))
    print('End Station : {}'.format(df['End Station'][pointer]))
    print('User Type : {}'.format(df['User Type'][pointer]))
    if city != 'washington':
        print('Gender : {}'.format(df['Gender'][pointer]))
        print('Birth Year : {}'.format(df['Birth Year'][pointer]))

def get_five(df, point_start, city):
    # preps a group of five records for raw data printing
    for x in range(5):
        pointerval = x + point_start
        print_raw_data(df, pointerval, city)
    return pointerval + 1

def main():
    # central module hub
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df, city)
        trip_duration_stats(df)
        user_stats(df, city)

        # Raw data interactive section
        do_data = input('\nWant to see the raw data? Enter yes or no.\n')
        if do_data.lower() == 'yes':
            df.reset_index(drop=True, inplace=True)
            start_val = 0
            while do_data.lower() == 'yes':
                start_val = get_five(df, start_val, city)
                do_data = input('\nFive more rows?\n')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
