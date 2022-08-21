import time
import pandas as pd
import numpy as np
import calendar as cl

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
    def input_city() :
        city = input('please specify the city: (chicago, new york city or washington) ').lower().strip()
        while city not in CITY_DATA :
            city = input_city()
        return city
    city = input_city()
    # TO DO: get user input for month (all, january, february, ... , june)
    def input_month() :
        month = input('please specify the name of month (January to June, or type "all" for no filter) : ').lower().strip()
        months = '|'.join(cl.month_name[1: 7])
        while month.title() not in months :
            if month == 'all':
                break
            month = input_month()
        return month.title()
    month = input_month()
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    def input_day() :
        day = input('please specify the weekday(or type "all" for no filter) : ').lower().strip()
        days = '|'.join(cl.day_name)
        while day.title() not in days :
            if day == 'all':
                break
            day = input_day()
        return day.title()
    day = input_day()
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

    df = pd.read_csv(CITY_DATA[city], parse_dates=True)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['start hour'] = df['Start Time'].dt.hour
    if month != 'All':
        df = df[df['month']==month]
    if day != 'All' :
        df = df[df['day_of_week']==day]

    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month == 'All' :
        common_month = df['month'].mode()[0]
        print("{}'s most common month of the year filtered by (day = {}) :\n".format(city, day), common_month)
    # TO DO: display the most common day of week
    if day == 'All' :
        common_day = df['day_of_week'].mode()[0]
        print("{}'s the most common day of the week filtered by (month = {}) :\n".format(city, month), common_day)
    # TO DO: display the most common start hour
    common_hour = df['start hour'].mode()[0]
    print("{}'s most common hour of the day filtered by (day = {}, month = {}) :\n".format(city, day, month), common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city, month, day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("{}'s most commonly used start station filtered by (day = {}, month = {}) :\n".format(city, day, month), common_start_station)
    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("{}'s most commonly used end station filtered by (day = {}, month = {}) :\n".format(city, day, month), common_end_station)
    # TO DO: display most frequent combination of start station and end station trip
    common_station_combination = df.groupby(['Start Station','End Station']).size().idxmax()
    print("{}'s most commonly used station combination filtered by (day = {}, month = {}) :\n".format(city, day, month), common_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    minutes, seconds = divmod(total_travel_time, 60)
    hours, minutes = divmod(minutes, 60)
    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print("{}'s time statistics filtered by (day = {}, month = {}) :\n".format(city, day, month))
    print('Total travel time = {} seconds \nequals {} hours, {} minutes & {} seconds '.format(total_travel_time, int(hours), int(minutes), int(seconds)))
    print('average travel time is : {} seconds \n'.format(int(mean_travel_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city, month, day):
    """Displays statistics on bikeshare users. User Types , Age & gender statistics"""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if 'Birth Year' and 'Gender' in df :
        user_types = df['User Type'].unique()
        count_of_types = df['User Type'].dropna().value_counts()
        # TO DO: Display counts of gender
        count_of_gender = df['Gender'].dropna().value_counts()
        percentage_of_gender = df['Gender'].dropna().value_counts(normalize=True).mul(100).round(2).astype(str).add(' %')
        # TO DO: Display earliest, most recent, and most common year of birth
        oldest_user = int(df['Birth Year'].min())
        youngest_user = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode())

        print("{}'s user statistics filtered by (day = {}, month = {}) :\n".format(city, day, month))
        print("The different user types are: {}\nthe count of each type is:\n{}\n".format(user_types, count_of_types))
        print("The count of each gender is :\n{}\nthe percentage of each gender is:\n{}\n ".format(count_of_gender, percentage_of_gender))
        print("User age statistics :\nOldest User is {} years old born in {}\nYoungest User is {} years old born in {}\n".format(2017 - oldest_user, oldest_user, 2017 - youngest_user, youngest_user))
        print("The most common birth year is : {}\nThe most common age is : {}\n".format(common_birth_year, 2017 - common_birth_year))
    elif 'birth Year' or 'Gender' not in df :
        print('User data for chosen city is not available , please choose a different city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_data(df, city, month, day):
    """asks the user if he wants to view raw data and displays it 5 rows at a time , prompting the user after every time"""

    def raw_data(df):
        runs = 0
        while True:
            ask_user = input('Would you like to view more raw data for the current filters? \nPrint yes or no: ')
            if ask_user == 'yes':
                runs += 1 #Adds 1 to current value, same as runs = runs + 1
                print(df.iloc[(runs-1)*5:runs*5])
            elif ask_user == 'no':
                return
    raw_data(df)


def main():
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)


        time_stats(df, city, month, day)
        station_stats(df, city, month, day)
        trip_duration_stats(df, city, month, day)
        user_stats(df, city, month, day)
        view_data(df, city, month, day)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
