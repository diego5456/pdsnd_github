import time
from calendar import MONDAY
from itertools import combinations

import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv',
              'miami': 'miami.csv'}
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
FILTER_TYPES = ['month', 'day', 'both', 'none']

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
    cities = [i.title() for i in CITY_DATA.keys()]
    city = ""
    month = ""
    day = -1
    filter_type = ""
    while city not in cities:
        city = input(f"Would you like to see data for {', '.join(cities)}: ").title().strip()

    while filter_type not in FILTER_TYPES:
        filter_type = input(
            "Would you like to filter data by month, day, both or none? Type \"none\" for no time filter. \n").lower().strip()
    if filter_type == 'month' or filter_type == "both":
        # get user input for month (all, january, february, ... , june)

        while month not in MONTHS:
            month = input(f"Which month? {', '.join(MONTHS)}?\n").strip()
        if month != 'all':
            # use the index of the months list to get the corresponding int
            month = MONTHS.index(month) + 1
    else:
        month = "all"

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_type == 'day' or filter_type == 'both':
        while day < 1 or day > 7:
            day = int(input("Which day? Please type your response as an integer (e.g., 1=Sunday).\n"))

    print('-'*40)
    return city.lower(), month, day


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
    try:
        df = pd.read_csv(CITY_DATA[city])
    except Exception as e:
        print(f"Error encounter reading the file: {e}")
        return None

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    if month != 'all':
        df = df[df['month'] == month]
    if day >= 0:
        df = df[df['day'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    print("What is the most popular month for traveling?")
    print(MONTHS[df['month'].mode()[0] - 1].title())

    # display the most common day of week
    print("What is the most popular day for traveling?")
    print(DAYS[df['day'].mode()[0] - 1])

    # display the most common start hour
    print("What is the most popular hour for traveling?")
    print(df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    series_dict = {
        "Start Station" : df['Start Station'],
        "End Station": df['End Station'],
        "Popular Trip": df.groupby(["Start Station"])["End Station"]
    }
    display_count_stats(series_dict)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print (f"Total travel time: {df['Trip Duration'].sum()}")


    # display mean travel time
    print(f"Mean travel time: {df['Trip Duration'].mean(): .2f}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()
    series_dict = {
        "User types": df['User Type']
        # "Gender": df['Gender']
    }
    if 'Gender' in df.columns:
        series_dict["Gender"] = df['Gender']
    display_count_stats(series_dict, display_all=True)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:

        print(f"\nEarliest birth year: {df['Birth Year'].min():.0f}")
        print(f"Most recent birth year: {df['Birth Year'].max():.0f}")
        print(f"Most common birth year: {df['Birth Year'].mode()[0]:.0f}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_count_stats(series_dict, display_all=False):
    """
    Displays counts of the provided series.

    Args:
        (dict) series_dict - dictionary of the type of stat and the series
        (bool) display_all - boolean to display all items in count
    """
    for name, series in series_dict.items():
        series_count = series.value_counts()
        if display_all:
            print(f"\n{name} count:")
            for index, value in series_count.items():
                print(f"{index} - {value}")
        else:
            print(f"{name}: {series_count.idxmax()}, Count: {series_count.max()}")
def restart_prompt():
    restart = input('\nWould you like to restart? Enter yes or no.\n')
    if restart.lower() != 'yes':
        return False
    return True

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df is None:
            if restart_prompt():
                continue
            else:
                break
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        if not restart_prompt():
            break


if __name__ == "__main__":
	main()
