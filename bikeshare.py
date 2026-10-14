import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['all','january', 'february', 'march', 'april', 'may', 'june']
days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']


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
    city = None
    cities = list(CITY_DATA.keys())
    while city not in cities:
        city = input("Enter a city name {}: ".format(cities).title())
        city = city.lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = None
    while month not in months:
        month = input("Enter a month {}: ".format(months).title())
        month = month.lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = None
    while day not in days:
        day = input("Enter a weekday {}: ".format(days).title())
        day = day.lower()

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
    ## load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")

    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    if day != 'all':
        # filter by day to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    print('-'*40)

    # TO DO: display the most common month
    if month == 'all':
        ## extract month from the Start Time column to create an hour column
        df['month'] = df['Start Time'].dt.month
        ## find the most popular hour
        popular_month = df['month'].mode()[0]
        
        print('Most Popular Month:', months[popular_month].title())
    else:
        print('You already filtered Month:', month.title())


    # TO DO: display the most common day of week
    if day == 'all':
        df['day_of_week'] = df['Start Time'].dt.weekday_name
        ## find the most popular weekday
        popular_wd = df['day_of_week'].mode()[0]
    
        print('Most Popular Weekday:', popular_wd)
    else:
        print('You already filtered Weekday:', day.title())

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour + 1

    ## find the most popular hour
    popular_hour = df['hour'].mode()[0]
    
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    print('-'*40)

    # TO DO: display most commonly used start station
    popular_ss = df['Start Station'].mode()[0]
    popular_sscount = pd.DataFrame.sum(df['Start Station'] == popular_ss)
    print('Most Popular Start Station:', popular_ss, ', Count: ', popular_sscount)

    # TO DO: display most commonly used end station
    popular_es = df['End Station'].mode()[0]
    popular_escount = pd.DataFrame.sum(df['End Station'] == popular_es)
    print('Most Popular End Station:', popular_es, ', Count: ', popular_escount)

    # TO DO: display most frequent combination of start station and end station trip
    df['combined'] = df['Start Station'] + ' to ' + df['End Station']
    popular_comb = df['combined'].mode()[0]
    popular_comb_count = pd.DataFrame.sum(df['combined'] == popular_comb)
    
    print('Most Popular Start-End trip:', popular_comb, ', Count: ',popular_comb_count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = pd.DataFrame.sum(df['Trip Duration'])
    print('Total travel time: ', total_time)

    # TO DO: display mean travel time
    mean_time = pd.DataFrame.mean(df['Trip Duration'])
    print('Mean travel time: ', mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts().to_dict()
    print('\nUser type counts:')
    for user in user_types.keys():
        print('- {}: {}'.format(user, user_types[user]))

    if city != 'washington':
        # TO DO: Display counts of gender
        genders = df['Gender'].value_counts().to_dict()
        print('\nGender counts:')
        for gender in genders.keys():
            print('- {}: {}'.format(gender, genders[gender]))

        # TO DO: Display earliest, most recent, and most common year of birth
        min_year = pd.DataFrame.min(df['Birth Year'])
        max_year = pd.DataFrame.max(df['Birth Year'])
        popular_year = df['Birth Year'].mode()[0]
        print('\nBirth Year: ')
        print('- earliest: ', int(min_year))
        print('- most recent: ', int(max_year))
        print('- most common: ', int(popular_year))
    else:
        print('\nGender and Birth Year data not available for', city)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_output(df):

    #df = df.sort_index(axis = 0)

    # Display 5 lines raw data
    def chunker():
        for i in range(0, len(df), 5):
            yield(df[i:i + 5])

    for chunk in chunker():
        for index, row in chunk.iterrows():
            print('\nRow {}'.format(index))
            for col in chunk.columns:
                print('  {}: {}'.format(col,row[col]))

        more = input('\nNext 5 rows ?, Enter yes.\n')
        if more != 'yes':
            break
        #print('df data: {}'.format(df[:2].to_string()))

            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        output = input('\nLike to see some raw data(total {} rows) ? Enter yes.\n'.format(len(df)))
        if output.lower() == 'yes':
            raw_output(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
