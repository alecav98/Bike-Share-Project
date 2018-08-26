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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input("What city do you want to look at? Options include: chicago, new york city, and washington.\n"))
            city = city.lower()
            if city in ('chicago', 'new york city', 'washington'):
                print('The city you chose to analyze is: ', city)
                break
            else:
                print("I didn't understand you. Please type either: 'chicago', 'new york city', or 'washington'.")
                continue
        except:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("\nDo you want to filter by month? If not type 'all', if yes type: 'january', 'february', ..., 'june'.\n")
            month = month.lower()
            if month in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
                print('The month you chose to filter by is: ', month)
                break
            else:
                print("I didn't understand you. Please type a month from january to june, in all lowercase.")
                continue
        except:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("\nDo you want to filter by day? If not, type 'all', if yes, type: 'monday', 'tuesday', etc.\n")
            day = day.lower()
            if day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
                print('The day you chose to filter by is: ', day)
                break
            else:
                print("I didn't understand you. Please type a day from monday to sunday, in all lowercase.")
                continue
        except:
            break

    print('-'*40)
    return city, month, day
#--------------------------------------------------------------------------------------------------------------------------------------

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
        df = df[df['day_of_week'] == day.title()]

    return df
#--------------------------------------------------------------------------------------------------------------------------------------

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # First thing to do is convert Start Time column to date time before doing any calculations.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # TO DO: display the most common month
    # 1) extract month from Start Time to create new column
    df['month'] = df['Start Time'].dt.month

    # 2) find the most common month from january to june
    popular_month = df['month'].mode()[0]
    print('The most common month, as January = 1 and December = 12, was: {}.\n'.format(popular_month))

    # TO DO: display the most common day of week
    # 1) extract day of week from Start Time to create new column
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # 2) find the most common day of the week from monday to sunday.
    popular_day = df['day_of_week'].mode()[0]
    print('The most common day of the week was: {}.\n'.format(popular_day))

    # TO DO: display the most common start hour
    # 1) extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # 2) find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0] #need the [0] to tell it its the mode for each column
    print('The most common Start Hour was: {}.\n'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#--------------------------------------------------------------------------------------------------------------------------------------
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('The most common start station was: {}.\n'.format(start_station))

    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('The most common end station was: {}.\n'.format(end_station))

    # TO DO: display most frequent combination of start station and end station trip
    comm_trip = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
    print('The most common round trip was:\n{}.'.format(comm_trip.head(1)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#--------------------------------------------------------------------------------------------------------------------------------------
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    tot_time = df['Trip Duration'].sum()
    num_hrs = tot_time // 3600
    num_min = (tot_time - (num_hrs * 3600)) // 60
    num_sec = (tot_time - (num_hrs * 3600)) - (num_min * 60)
    print('The total travel time was: {} hours, {} minutes, and {} seconds.'.format(num_hrs, num_min, num_sec))

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    hrs = mean_time // 3600
    minutes = (mean_time - (hrs * 3600)) // 60
    seconds = (mean_time - (hrs * 3600)) - (minutes * 60)
    print('The average travel time was: {} hours, {} minutes, and {} seconds.'.format(hrs, minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#--------------------------------------------------------------------------------------------------------------------------------------
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # 1) print value counts for each user type
    user_types = df['User Type'].value_counts()
    print('The most common user types are:\n', user_types)

    # TO DO: Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print('\nThe gender counts are:\n', gender_types)
    except:
        print('\nSorry, no gender data is available.')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_yob = df['Birth Year'].min()
        print('\nThe earliest year of birth was: {}.'.format(earliest_yob))

        mrecent_yob = df['Birth Year'].max()
        print('The most recent year of birth was: {}.'.format(mrecent_yob))

        comm_yob = df['Birth Year'].mode()[0]
        print('The most common year of birth was: {}.'.format(comm_yob))
    except:
        print('\nSorry, no birth year data is available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#--------------------------------------------------------------------------------------------------------------------------------------
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        n = 5
        answer = input("Would you like to see individual data? Please type 'yes' or 'no'.\n")
        while answer == 'yes':
            print(df.sort_index().head(n))
            n = n + 5 #i = i + 1 reassigns i, i += 1 increments i by 1
            answer = input("Would you like to see the next five lines of raw data?\n")
        else:
            print('Okay, you chose not to look at individual data.')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
