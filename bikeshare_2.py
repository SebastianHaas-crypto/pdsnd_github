import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# general text modules
cancel_text = 'Do you want to continue? Enter "n" to end program or any button to continue. '
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

# retrieve user input for data to be explored
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (int) month - number 1...6 as placeholder for name of the month to filter by, or 7 to apply no month filter
        (str) week_day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    text_OK = False
    city_conf_text = 'Chosen city is {}? Enter "y" to confirm. '
    while True:
        city = input('\nFor which city would you like to run an evaluation? Chicago (CH), New York City (NY) or Washington (WA)? \n\
Please Enter abbreviation. ')
        if city[0:2].lower() == 'ch':
            city = 'chicago'
            text_OK = True
        elif city[0:2].lower() == 'ny':
            city = 'new york city'
            text_OK = True
        elif city[0:2].lower() == 'wa':
            city = 'washington'
            text_OK = True
        else:
            print('\nInput for city selection could not be evaluated. Please enter valid abbreviation and check for typing errors. ')
            conf_request = input(cancel_text)
            if conf_request.lower() == 'n':
                return
        if text_OK == True:
            conf_input = input(city_conf_text.format(city.title()))
            if conf_input.lower() == 'y':
                break
            else:
                text_OK = False
                conf_request = input(cancel_text)
                if conf_request.lower() == 'n':
                    return

    # get user input for month (all, january, february, ... , june)
    text_OK = False
    month_conf_text = 'Chosen month(s) is {}? Enter "y" to confirm. '
    while True:
        month = input('\nFor which month(s) would you like to run an evaluation?\n\
The following months are available: January (Jan), February (Feb), March (Mar), April (Apr), May (May), June (Jun) or all (all). \n\
Please enter abbreviation. ')
        # months list transferred to main program head in order to make it available for call of other functions
        for i in range(len(months)):
             if month[0:3].lower() == months[i][0:3]:
                 month_name = months[i].title()
                 month = i+1
                 text_OK = True
                 break
        if text_OK == True:
            conf_input = input(month_conf_text.format(month_name.title()))
            if conf_input.lower() == 'y':
                break
            else:
                text_OK = False
                conf_request = input(cancel_text)
                if conf_request.lower() == 'n':
                    return
        else:
            print('\nInput for month selection could not be evaluated. Please check for typing errors. ')
            conf_request = input(cancel_text)
            if conf_request.lower() == 'n':
                return

    # get user input for day of week (all, monday, tuesday, ... sunday)
    text_OK = False
    day_conf_text = 'Chosen day(s) of week is {}? Enter "y" to confirm. '
    day_except_text = 'Please enter an integer number. '
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input('\nFor which day(s) would you like to run an evaluation?\n\
Please enter specific day as number (Monday = 1 ... Sunday = 7) or enter "8" to select all. ')
        try:
            for i in range(len(days)):
                if (int(day)-1) == i:
                    week_day = days[int(day)-1].title()
                    text_OK = True
                    break
            if text_OK == True:
                conf_input = input(day_conf_text.format(week_day.title()))
                if conf_input.lower() == 'y':
                    if day == '5':
                        print("Thank god it's friday !")
                        time.sleep(2)
                    break
                else:
                    text_OK = False
                    conf_request = input(cancel_text)
                    if conf_request.lower() == 'n':
                        return
            else:
                print('\nInput for day selection could not be evaluated. Please check for typing errors.')
                conf_request = input(cancel_text)
                if conf_request.lower() == 'n':
                    return
        except Exception as e:
            print('Exception occurred: {}'.format(e))
            print(day_except_text)
            conf_request = input(cancel_text)
            if conf_request.lower() == 'n':
                return
    print('-'*40)
    return city, month, week_day


def load_data(city, month, week_day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (int) month - number 1...6 as place holder for the name of the month to filter by, or 7 to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
#   name for day variable changed from "day_name" into week_day to take into account new pandas method ".day_name()"
#   read in file form selected city
    df = pd.read_csv(CITY_DATA[city])
#   create additional columns for months, days, start/ end times, hours and station combinations
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month_start'] = df['Start Time'].dt.month
    df['month_end'] = df['End Time'].dt.month
    df['day_start'] = df['Start Time'].dt.day_name()
    df['day_end'] = df['End Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    df['station_comb'] = df['Start Station'] + ' &AND& ' + df['End Station']
#   filter data file by month: capture start and end months
    if month != 7:
        df1 = df[df['month_start'] == month]
        df2 = df1.append(df[df['month_end'] == month])
        df = df2.drop_duplicates()
#   filter data file by day: capture start and end days
    if week_day != 'All':
        df3 = df[df['day_start'] == week_day]
        df4 = df3.append(df[df['day_end'] == week_day])
        df = df4.drop_duplicates()
#   reset index to facilitate looping in station_stats function
    df = df.reset_index()
#   check if user wants to check first data lines
    req_check_df = input('\nIf you want to check the selected data please enter y.')
    if req_check_df[0:1].lower() == 'y':
        print('check df = \n', df.head())
        wait = input('Press Enter to continue. ')

    return df


def time_stats(df, month, week_day):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    if month == 7:
        pop_month_start_num = df['month_start'].mode()[0]
        pop_month_start = months[pop_month_start_num - 1].title()
        pop_month_end_num = df['month_end'].mode()[0]
        pop_month_end = months[pop_month_end_num - 1].title()
#       Theoretically  most popular start month could differ from end month.
        if pop_month_start != pop_month_end:
            print('The most popular MONTH for renting a bike is {} but for returning it is {}. '.format(pop_month_start, pop_month_end))
            print('This indicates that renting frequently occured at the end of {}. '.format(pop_month_start))
        else:
            print('The most popular MONTH for renting a bike is {}. '.format(pop_month_start))
#   evaluation of most popular month does not make sense for selected month
    else:
        print('As a specific MONTH has been selected, NO statistic evaluation for most common MONTH is performed.')
    # display the most common day of week
    if week_day == 'All':
        pop_day_start = df['day_start'].mode()[0]
        pop_day_end = df['day_end'].mode()[0]
#       Theoretically  most popular start day could differ from end day.
        if pop_day_start != pop_day_end:
            print('The most popular WEEKDAY for renting a bike is {} but for returning it is {}. '.format(pop_day_start, pop_day_end))
            print('This indicates that renting frequently occured at the evening of {}. '.format(pop_day_start))
        else:
            print('The most popular WEEKDAY for renting a bike is {}. '.format(pop_day_start))
#   evaluation of most popular day does not make sense for selected day
    else:
        print('As a specific DAY has been selected, NO statistic evaluation for most common DAY is performed.')

    # display the most common start hour
    pop_hour = df['hour'].mode()[0]
    print('The most popular START HOUR for renting a bike is {}h. '.format(pop_hour))
    # terminal part of function
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    wait = input('Press Enter to continue. ')


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start_station = df['Start Station'].mode()[0]
    print('The most popular START STATION for renting a bike is {}. '.format(pop_start_station))

    # display most commonly used end station
    pop_end_station = df['End Station'].mode()[0]
    print('The most popular END STATION for renting a bike is {}. '.format(pop_end_station))

    # display most frequent combination of start station and end station trip
    pop_station_comb = df['station_comb'].mode()[0]
    print('The most popular combination of START STATION AND END STATION for renting a bike is: {} with {} uses. '.format(pop_station_comb, df.loc[df['station_comb'] == pop_station_comb]['station_comb'].count()))

    print("\nThis took %s seconds." % (time.time() - start_time))

    # calculate the combinations by mathematical definition
    req_det_calc = input('\nIf you want to have the most popular combination of START STATION AND END STATION calculated according to mathematical definition \n\
(START STATION AND END STATION = END STATION AND START STATION), please enter y. Please be aware that this can take several minutes.')
    if req_det_calc[0:1].lower() == 'y':
        start_time = time.time()
        print('calculating...')
        dict_station_combs = {}
        i = 0
        for i in range(df.shape[0]):
            if ( df.loc[i]['Start Station'] +  ' AND&AND ' + df.loc[i]['End Station'] in dict_station_combs ) or ( df.loc[i]['End Station'] +  ' AND&AND ' + df.loc[i]['Start Station'] in dict_station_combs ):
                if ( df.loc[i]['Start Station'] +  ' AND&AND ' + df.loc[i]['End Station'] ) in dict_station_combs:
                    dict_station_combs[df.loc[i]['Start Station'] +  ' AND&AND ' + df.loc[i]['End Station']] += 1
                else:
                    dict_station_combs[df.loc[i]['End Station'] +  ' AND&AND ' + df.loc[i]['Start Station']] += 1
            else:
                dict_station_combs[df.loc[i]['Start Station'] +  ' AND&AND ' + df.loc[i]['End Station']] = 1

        pop_station_comb2 = max(dict_station_combs, key=dict_station_combs.get)
        print('The most popular combination of START AND END STATIONS for renting a bike according to mathematical definition is: {} with {} uses. '.format(pop_station_comb2, dict_station_combs[pop_station_comb2]))
        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    wait = input('Press Enter to continue. ')


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    tot_sum = (df['End Time'] - df['Start Time']).sum()
    print('The total travel time for all trips within the selected data set is {} (hh:mm:ss).'.format(tot_sum))
    # display mean travel time
    mean_trav_time = (df['End Time'] - df['Start Time']).mean()
    print('The mean travel time for all trips within the selected data set is {} (hh:mm:ss).'.format(mean_trav_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    wait = input('Press Enter to continue. ')


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
#   maximal possible age assumed for user
    max_age = 105
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Different user types and counts of user types:\n', user_types)
    print('Most common user types is {}.'.format(df['User Type'].mode()[0]))
    # Display counts of gender if data available
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('Counts of gender:\n', gender_counts)
        print('Most common sex is {}.'.format(df['Gender'].mode()[0]))
    else:
        print('Counts of gender cannot be printed because no data is available.')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        early_birth = int(df['Birth Year'].min())
        recent_birth = int(df['Birth Year'].max())
        common_birth = int(df['Birth Year'].mode()[0])
        print('Earliest birth year of users: ', early_birth)
#       check if earliest birt year makes sense
        if early_birth < datetime.datetime.now().year - max_age:
            print('Earliest birth year according to data seems to be out of range, potentially caused by typing error. ')
            early_birth2 = int(min([value for value in df['Birth Year'] if value >= datetime.datetime.now().year - max_age]))
            number_early_birth2 = (df['Birth Year'].value_counts())
            print('Most probable earliest birth year of users: ', early_birth2)
            print('Counts of 20 earliest birth years of users:\n', number_early_birth2.sort_index().head(20))
        print('Most recent birth year of users: ', recent_birth)
        print('Most common birth year of users: ', common_birth)
    else:
        print('Evaluation of birth years cannot be printed because no data is available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    wait = input('Press Enter to continue. ')

def main():

    while True:
        city, month, week_day = get_filters()
        df = load_data(city, month, week_day)

        time_stats(df, month, week_day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter y to restart or any other key to end program.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
