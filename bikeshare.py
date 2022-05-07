import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    city, filter_param, month, day = "", "", "all", "all"
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    filter_params = ['month', 'day', 'both', 'none']

    while True:
        try:
            if city == "":
                city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()
                if city not in ['chicago', 'new york city', 'washington']:
                    city = ""
                    raise Exception("error in city")
            # To determine what filter to use:
            if filter_param == "":
                filter_param = input(
                    "Would you like to filter the data by month, day, both, or not at all? Type \"none\" for no time filter.\n").lower()
                if filter_param not in filter_params:
                    filter_param = ""
                    raise Exception("error in filter param")
            # get user input for month (all, january, february, ... , june)
            if month == "all" and (filter_param == 'both' or filter_param == 'month'):
                month = input("Which month? January, February, March, April, May, or June?\n").lower()
                if month not in months:
                    month = "all"
                    raise Exception("error in month")
            # get user input for day of week (all, monday, tuesday, ... sunday)
            if day == "all" and (filter_param == 'both' or filter_param == 'day'):
                day = input("Which day? Please type your response in letters e.g. (sunday, monday, ..\n").lower()
                if day not in days:
                    day = "all"
                    raise Exception("error in day")

            break

        except Exception as ex:
            if ex.args[0] == "error in city":
                print("Please enter one city name only correctly.")
            elif ex.args[0] == "error in filter param":
                print("Please enter a correct filter.")
            elif ex.args[0] == "error in month":
                print("Please enter a valid month in letters.")
            elif ex.args[0] == "error in day":
                print("Please enter a valid integer value for the day(1 - 7).")

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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

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
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if df['month'].value_counts().iloc[0] != df['month'].size:
        most_comm_month = df['month'].mode()[0]
        count_month = df['month'].value_counts().loc[most_comm_month]
        print("The most common month is: {}, Count: {}.\n".format(most_comm_month,count_month))


    # display the most common day of week
    if df['day_of_week'].value_counts().iloc[0] != df['day_of_week'].size:
        most_comm_day = df['day_of_week'].mode()[0]
        count_day = df['day_of_week'].value_counts().loc[most_comm_day]
        print("The most common day is: {}, Count: {}.\n".format(most_comm_day,count_day))


    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    most_comm_hour = df['start_hour'].mode()[0]
    count_hour = df['start_hour'].value_counts().loc[most_comm_hour]
    print("The most common hour is: {}, Count: {}.\n".format(most_comm_hour,count_hour))





    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_star_st = df['Start Station'].mode()[0]
    count_star_st = df['Start Station'].value_counts().loc[most_common_star_st]
    print("Most common start station is: {}, Count: {}.\n".format(most_common_star_st,count_star_st))

    # display most commonly used end station
    most_common_end_st = df['End Station'].mode()[0]
    count_end_st = df['End Station'].value_counts().loc[most_common_end_st]
    print("Most common end station is: {}, Count: {}.\n".format(most_common_end_st, count_end_st))

    # display most frequent combination of start station and end station trip
    #first create a new column which is combination of start and end stations

    df['start_station_to_end'] = df['Start Station'] +' -- ' + df['End Station']
    most_frequent_trip = df['start_station_to_end'].mode()[0]
    count_trip = df['start_station_to_end'].value_counts().loc[most_frequent_trip]
    print("Most common trip is: {}, Count: {}.\n".format(most_frequent_trip, count_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_trav_time = df['Trip Duration'].sum()
    print("Total travel time is: {}.\n".format(tot_trav_time))

    # display mean travel time
    mean_trav_time = df['Trip Duration'].mean()
    print("Average travel time is: {}.\n".format(mean_trav_time))

    #number of trips
    count_trips = df['Trip Duration'].count()
    print("Number of trips is: {}.\n".format(count_trips))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_sub = df['User Type'].value_counts().loc['Subscriber']
    count_cust = df['User Type'].value_counts().loc['Customer']
    print("There are {} subscribers, and {} customer.\n".format(count_sub, count_cust))
    # Display counts of gender
    if 'Gender' in df.columns:
        count_male = df['Gender'].value_counts().loc['Male']
        count_female = df['Gender'].value_counts().loc['Female']
        print("There are {} male, and {} female.\n".format(count_male, count_female))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_comm_birth_year = df['Birth Year'].mode()[0]
        print("Earliest birth year: {},most recent birth year: {}, most common birth year: {}.\n".format(
            earliest_birth_year, most_recent_birth_year, most_comm_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    # Prompt user to print individual user data
    i = 0
    while True:
        show_ind_data = input("Would you like to view individual users data, answer by yes or no?\n").lower()
        if show_ind_data in ['yes', 'ok', 1]:
            finishing_index = i + 5
            for i in range(i,finishing_index,1):
                print(df.iloc[i].to_dict())
            i += 1
        else:
            break



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
