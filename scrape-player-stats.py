from nba_api.stats.endpoints import playergamelogs
from datetime import date
import pandas as pd
import csv

# Variables
currentSeason = '2023-24'                                       # current season year
num_last_games = 1                                              # number of last games to go back
today = date.today()                                            # get todays date
last_n_games_date = today - pd.DateOffset(days=num_last_games)  # subtract today from number of last games to go back

print("Starting Data Pull Process...")test

# Create Data Object
playergamelogs_data  = playergamelogs.PlayerGameLogs(
    date_from_nullable=last_n_games_date.strftime('%m/%d/%Y'),
    date_to_nullable=today.strftime('%m/%d/%Y'),
    season_nullable=currentSeason
)

# Retrieve Data Set
data_sets = playergamelogs_data.get_data_frames()

# Filter Specific Data Set and Only Display Specific Fields
specific_data_set = data_sets[0]
filtered_data_set = specific_data_set[['SEASON_YEAR', 'GAME_DATE', 'MATCHUP', 'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'TEAM_NAME',  'MIN', 'FGM', 'FG3M', 'FTM', 'REB', 'AST', 'TOV', 'STL', 'BLK']]
filtered_data_set.to_csv('output.csv', index=False)

print("Games Pulled from " + last_n_games_date.strftime('%Y-%m-%d') + " to " + today.strftime('%Y-%m-%d'))
print("Data Pull Complete!")
print("---------------------")
print("Starting Data Conversion...")

# Read the CSV file into a list of lists
with open('output.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    data = list(reader)

# Apply math per column per row
for row_index, row in enumerate(data):
    if row_index == 0:              # IF row 1, skip
        continue
    row[8] = int(row[8]) * 2        # FGM value x 2
    row[11] = int(row[11]) * 1.2    # REB value x 1.2
    row[12] = int(row[12]) * 1.5    # AST value x 1.5
    row[13] = -abs(int(row[13]))    # TOV value make negative
    row[14] = int(row[14]) * 3      # STL value x 3
    row[15] = int(row[15]) * 3      # BLK value x 3

# Write the modified data to a new CSV file
with open('updated-output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in data:
        writer.writerow(row)

print("Data Conversion Complete!")
print("-------------------------")