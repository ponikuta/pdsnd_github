import time
import pandas as pd

# Display all rows
pd.set_option('display.max_rows', None)

# Display all columns
pd.set_option('display.max_columns', None)

# Dictionary mapping city names to their respective CSV files
CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}


def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.

    Returns:
        tuple: Contains the city, month, and day chosen by the user.
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Define valid inputs
    valid_cities = CITY_DATA.keys()
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturdkirathimoay', 'sunday', 'all']

    # Get user input for city
    while True:
        city = input("Please enter the city you want to analyze (Chicago, New York City, Washington): ").strip().lower()
        if city in valid_cities:
            break
        else:
            print("Invalid input. Please enter a valid city name.")

    # Get user input for month
    while True:
        month = (
            input(
                "Please enter the month to filter by (January, February, March, April, May, June) or 'All' for no filter: "
            )
            .strip()
            .lower()
        )
        if month in valid_months:
            break
        else:
            print("Invalid input. Please enter a valid month name or 'all'.")

    # Get user input for day of week
    while True:
        day = (
            input("Please enter the day of week to filter by (Monday, Tuesday, ..., Sunday) or 'All' for no filter: ")
            .strip()
            .lower()
        )
        if day in valid_days:
            break
        else:
            print("Invalid input. Please enter a valid day of the week or 'all'.")

    print("=" * 100)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        city (str): Name of the city to analyze.
        month (str): Name of the month to filter by, or "all" to apply no month filter.
        day (str): Name of the day of week to filter by, or "all" to apply no day filter.

    Returns:
        pandas.DataFrame: Filtered data frame.
    """
    # Load data file into DataFrame
    try:
        df = pd.read_csv(CITY_DATA[city])
    except FileNotFoundError:
        print(f"Error: The data file for {city.title()} does not exist.")
        return pd.DataFrame()  # Return empty DataFrame

    # Convert Start Time and End Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
    df['End Time'] = pd.to_datetime(df['End Time'], errors='coerce')

    # Drop rows with invalid datetime entries
    df.dropna(subset=['Start Time', 'End Time'], inplace=True)

    # Extract month, day of week, and hour from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month) + 1
        df = df[df['month'] == month_index]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def display_data(df):
    """
    Displays raw data upon user request in increments of 5 rows.

    Args:
        df (pandas.DataFrame): The DataFrame containing bikeshare data.
    """
    show_data = input("\nWould you like to see 5 lines of raw data? Enter yes or no: ").strip().lower()
    start_loc = 0
    while show_data == 'yes':
        end_loc = start_loc + 5
        # Ensure we don't go out of bounds
        if start_loc >= len(df):
            print("No more data to display.")
            break
        print(df.iloc[start_loc:end_loc])
        start_loc += 5
        show_data = input("Would you like to see the next 5 lines of raw data? Enter yes or no: ").strip().lower()


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df (pandas.DataFrame): The DataFrame containing bikeshare data.
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Most common month
    common_month_num = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    common_month = months[common_month_num - 1]
    print(f"Most Common Month: {common_month}")

    # Most common day of week
    common_day = df['day_of_week'].mode()[0].title()
    print(f"Most Common Day of Week: {common_day}")

    # Most common start hour
    common_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {common_hour}:00 hrs")

    print(f"\nThis took {time.time() - start_time:.4f} seconds.")
    print("=" * 100)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        df (pandas.DataFrame): The DataFrame containing bikeshare data.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"Most Commonly Used Start Station: {common_start_station}")

    # Most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"Most Commonly Used End Station: {common_end_station}")

    # Most frequent combination of start and end station
    df['Start-End Combination'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['Start-End Combination'].mode()[0]
    print(f"Most Frequent Trip: {common_trip}")

    print(f"\nThis took {time.time() - start_time:.4f} seconds.")
    print("=" * 100)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        df (pandas.DataFrame): The DataFrame containing bikeshare data.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_readable = time.strftime("%H:%M:%S", time.gmtime(total_travel_time))
    print(f"Total Travel Time: {total_travel_time} seconds ({total_travel_time_readable})")

    # Mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time_readable = time.strftime("%M:%S", time.gmtime(mean_travel_time))
    print(f"Mean Travel Time: {mean_travel_time:.2f} seconds ({mean_travel_time_readable})")

    print(f"\nThis took {time.time() - start_time:.4f} seconds.")
    print("=" * 100)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        df (pandas.DataFrame): The DataFrame containing bikeshare data.
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Counts of user types
    user_types = df['User Type'].value_counts()
    print("User Types:")
    print(user_types.to_string())
    print()

    # Counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("Gender Counts:")
        print(gender_counts.to_string())
        print()
    else:
        print("Gender data not available for this city.\n")

    # Birth year statistics
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"Earliest Year of Birth: {earliest_year}")
        print(f"Most Recent Year of Birth: {recent_year}")
        print(f"Most Common Year of Birth: {common_year}")
    else:
        print("Birth Year data not available for this city.")

    print(f"\nThis took {time.time() - start_time:.4f} seconds.")
    print("=" * 100)


def main():
    """
    The main function that orchestrates the bikeshare data exploration.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print("No data available for the selected filters. Please try again with different inputs.")
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_data(df)

        # Ask user if they want to restart
        while True:
            restart = input('\nWould you like to restart? Enter yes or no: ').strip().lower()
            if restart in ['yes', 'no']:
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        if restart != 'yes':
            print("Thank you for using the Bikeshare Data Explorer. Goodbye!")
            break


if __name__ == "__main__":
    main()
