import pandas as pd
import requests as req

# Function to fetch data from the API
def fetch_data(url):
    try:
        response = req.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        return response.json()  # Parse JSON data
    except req.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

# Function to split and save CSV files based on column groups
def split_and_save_csv(df, file_name_part1, file_name_part2):
    # Define the columns for each CSV part based on your vehicle model
    columns_part1 = ['vin', 'manufacturer', 'year']  # Update with actual columns
    columns_part2 = ['transmission','price','status']

    # Ensure the columns exist in the DataFrame
    missing_columns = set(columns_part1 + columns_part2) - set(df.columns)
    if missing_columns:
        print(f"Missing columns in DataFrame: {missing_columns}")
        return

    # Split the DataFrame into two parts
    df_part1 = df[columns_part1]
    df_part2 = df[columns_part2]

    # Save each part to a CSV file
    df_part1.to_csv(file_name_part1, index=False)
    df_part2.to_csv(file_name_part2, index=False)
    print(f"Data saved as {file_name_part1} and {file_name_part2}.")

# Function to concatenate two CSVs and print each part
def concatenate_and_print_csv(file_name_part1, file_name_part2):
    # Load both CSV files into DataFrames
    df_part1 = pd.read_csv(file_name_part1)
    df_part2 = pd.read_csv(file_name_part2)

    # Print each part
    print(f"Part 1 (Columns: {df_part1.columns}):")
    print(df_part1.head(), "\n")
    print(f"Part 2 (Columns: {df_part2.columns}):")
    print(df_part2.head(), "\n")

    # Concatenate the two DataFrames along the columns
    concatenated_df = pd.concat([df_part1, df_part2], axis=1)

    # Print the concatenated DataFrame
    print("Concatenated DataFrame (Full Data):")
    print(f"All parts combined (Columns: {concatenated_df.columns}):")
    return concatenated_df

# Main code for fetching and processing vehicle data from API
vehicles_api_url = 'http://127.0.0.1:8000/vehicles/'  # Update with your actual vehicles API endpoint

# Fetch vehicle data from API
vehicles_data = fetch_data(vehicles_api_url)

# If the data was successfully fetched, process it
if vehicles_data:
    # Check if 'vehicles' key exists in the response
    if 'vehicles' in vehicles_data:
        vehicles_list = vehicles_data['vehicles']  # Extract list of vehicles

        # Convert the data to a DataFrame
        vehicles_df = pd.DataFrame(vehicles_list)

        # Preview the DataFrame
        print(f"DataFrame shape (rows, columns): {vehicles_df.shape}")
        print("\nData preview (first 5 rows):")
        print(vehicles_df.head())

        # Split the data and save it to CSV files
        split_and_save_csv(vehicles_df, 'vehicles_part1.csv', 'vehicles_part2.csv')

        # Concatenate the split CSV files and print
        concatenated_df = concatenate_and_print_csv('vehicles_part1.csv', 'vehicles_part2.csv')
        concatenated_df.to_csv("combined.csv", index=False)
        print("Combined CSV saved as 'combined.csv'.")
    else:
        print("No 'vehicles' key found in the API response.")
else:
    print("Failed to load vehicle data.")
