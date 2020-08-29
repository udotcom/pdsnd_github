import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']
days_of_wk = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']  # datetime function has 0=Monday ...


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        try:
            city_entry = input("Enter city name from the following list of choices:\n\t * Chicago \n\t * New York City \n\t * Washington DC \n")
        
            if city_entry.lower() in CITY_DATA:
                break
            else:
                print("Sorry, {} is not a valid entry in the menu.".format(city_entry))   
        except:
            continue
                
    city = city_entry                        # accept input and copy to variable city
    print("\n ---- City ", city)

    while True:
        try:
            mo_entry = input("Enter the month for which you want to see the data or enter 'all' for full time period. Data is available from January to June:\n >> ")
            if ((mo_entry.lower() in months) or (mo_entry.lower() == 'all')):
                break
            else:
                print("Sorry, {} is not a valid entry in the list of available months.".format(mo_entry)) 
        except: 
            continue
    month = mo_entry                        # accept input and copy to variable month
    print("\n--- Month  ", month)


    while True:
         try:
             day_entry = input("Enter the day of week for which you want to see the data e.g. 'Tuesday'' or enter 'all' for the entire week\n")
             if ((day_entry.lower() in days_of_wk) or (day_entry.lower() == 'all')):
                 break
             else:
                 print("Sorry, {} is not a valid entry in the list of available monhts.".format(day_entry))   
         except:
             continue
    day = day_entry                        # accept input and copy to variable day
    print("\n---Day ", day)
               

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
    df = pd.read_csv('C://Users//mur//Documents//TUTORIALS//UDACITY//NanoDegree_Prog_for_DataSci//Project_Python_2//'+CITY_DATA[city])
    print("\n--- DEBUG CSV loaded in fram ---",df.head(3))           # for DEBUG
    
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    print("\n --- DEBUG --- month and dow column added --", df[['month', 'day_of_week']].head(50))
    
    # filter by month if applicable
    if month != 'all':                  # dont filter if month is all
        # use the index of the months list to get the corresponding int
        #months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = [ months.index(mo) for mo in months if month==mo]   # matches alpa month name to list and looks up its index, returns list with single element
        month=month[0]+1   # updated variable to make it consitent and simple
        # filter by month to create the new dataframe
        df = (df[df['month']==month])

    # filter by day of week if applicable
    if day != 'all':                # dont filter if day of week is all
        # filter by day of week to create the new dataframe
        #days_of_wk = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = [ days_of_wk.index(dy) for dy in days_of_wk if day==dy] # list comprehension with condition
        day = day[0]                        # to avoid length mismatch since evaulation statement above returned a list with single element rather than a single element
        df=(df[df['day_of_week']==day])
    
       

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    frequent_month=df['month'].mode()[0]
    print("\n\t  Most Popular Month of Travel:", frequent_month)


    # TO DO: display the most common day of week
    frequent_dow=df['day_of_week'].mode()[0]
    print("\n\t Most popular Day of Travel:", days_of_wk[frequent_dow].title())

    # TO DO: display the most common start hour
    #df['Hour']=['Start Time'].dt.hour
    frequent_hr=(df['Start Time'].dt.hour).mode()[0]
    print("\n\t Most popular Hour of Travel:", frequent_hr)   # will return day name instead of number. -1 to adjust for list lookup that is zero indexed

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_pick=df['Start Station'].mode()[0]
    print("Most common pickup point is: {}".format(popular_pick) )
    
    # TO DO: display most commonly used end station
    popular_drop=df['End Station'].mode()[0]
    print("Most common drop-off point is: {}".format(popular_drop) )

    # TO DO: display most frequent combination of start station and end station trip
    df['Start_End'] = df['Start Station'] + " --> "+ df['End Station']
    popular_trip = df['Start_End'].mode()[0]
    print("\nMost common trip: {}".format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    totsec=df['Trip Duration'].sum()
    min, sec = divmod(totsec, 60) 
    hour, min = divmod(min, 60) 
    print("Total Trip Duration time is %d hours %02d minutes and %02d seconds \n" % (hour, min, sec))
    

    # TO DO: display mean travel time
    meansec=df['Trip Duration'].mean()
    print("Average trip duration is %02d seconds \n" % meansec)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types=df.groupby('User Type')['User Type'].count()
    print('\n\t Count of user types \n',user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_count=df.groupby('Gender')['Gender'].count()
        print('\n\t Count of customer gender types \n',gender_count)
    else:
        print("\n No gender information available for {} dataset".format(city))

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        oldest_customer=df['Birth Year'].min()
        youngest_customer=df['Birth Year'].max()
        common_yob=df['Birth Year'].mode()[0]
        print("\nOldest user's year of birth:", int(oldest_customer))
        print("\nYoungest user's year of birth:", int(youngest_customer))
        print("\nMost common year of birth:", int(common_yob))
    else:
        print("\n No age information available for {} dataset".format(city))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw_frame(df):
    start_index = 0

    raw_data = input("\n View 'raw' unfiltered data from dataset? Press Y or y to display data or any other key to continue ").lower()
    while True:
    	if raw_data =='y':
    		print(df.iloc[start_index:start_index + 5])
    		start_index +=5
    		raw_data = input("\nContinue with more records, Press Y or y to continue or any other key to continue ").lower()
    	else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        print_raw_frame(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
