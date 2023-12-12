# Importing necessary libraries
import re
import pandas as pd
import os


# Function to parse match information from HTML files
def parse_matches(html_file_path):
    print(html_file_path)

    # Read the HTML content from the local file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html = file.read()

    # Extract information using regular expressions
    match_info = {}

    # Match information
    match_match = re.search(
        r'<div class="container-flow box-header box-header--no-margin box-header--bigger">([\d.]+) (.*?)</div>', html)

    # Teams' names
    team_names = re.findall(r'class="hidden-xs">([^<]+)<', html)
    match_info['Home Team'] = team_names[0]
    match_info['Away Team'] = team_names[1]

    # Date and Stadium
    date_stadium_match = re.search(r'([\d.]+), (\d{2}:\d{2}) \| ([^<]+)</div>', html)
    if date_stadium_match:
        match_info['Date'] = date_stadium_match.group(1)
        match_info['Time'] = date_stadium_match.group(2)
        match_info['Stadium'] = date_stadium_match.group(3)

    # Goals and Cards information
    goals_match = re.findall(
        r'<div class="game__goals__item"><a href="[^"]+" title=""><i class="ico ico-ball"></i><span class="hidden-xs">(.*?)</span> (.*?)</a> \((\d+)“\)</div>',
        html)
    cards_match = re.findall(
        r'<div class="game__cards__item"><a href="[^"]+" title=""> <i class="ico ico-card yellow"></i><span class="hidden-xs">(.*?)</span>(.*?)</a> \((\d+)“\)</div>',
        html)
    r_cards_match = re.findall(
        r'<div class="game__cards__item"><a href="[^"]+" title=""> <i class="ico ico-card red"></i><span class="hidden-xs">(.*?)</span>(.*?)</a> \((\d+)“\)</div>',
        html)

    # Extracted Goals and Cards data
    goals = [f'{player} {surname} ({minute})' for player, surname, minute in goals_match]
    cards = [f'{player} {_} ({minute})' for player, _, minute in cards_match]
    r_cards = [f'{player} {_} ({minute})' for player, _, minute in r_cards_match]

    scoreline = re.findall(r'<div class="game__scoreboard__fulltime ">(\d+):(\d+)</div>', html)
    if len(scoreline) == 0:
        return
    match_info['Goals Home'] = scoreline[0][0]
    match_info['Goals Away'] = scoreline[0][1]

    # Additional Info
    additional_info_match = re.findall(r'<div class="game__additional">(.*?)</div>', html)
    if additional_info_match:
        spectators_match = re.search(r'(\d+) divákov', additional_info_match[0])
        if spectators_match:
            match_info['Additional Info'] = [f'Zápas navštívilo {spectators_match.group(1)} divákov']
        else:
            match_info['Additional Info'] = [additional_info_match[0]]

    # Add the extracted Goals and Cards data to the match_info dictionary
    match_info['Goals'] = ', '.join(goals)  # Convert the goals list to a comma-separated string
    match_info['Cards'] = ', '.join(cards)  # Convert the cards list to a comma-separated string
    match_info['Red Cards'] = ', '.join(r_cards)  # Convert the cards list to a comma-separated string

    # Create a DataFrame from the extracted information
    df = pd.DataFrame(match_info, index=['1'])

    # Save the DataFrame to a CSV file in append mode
    df.to_csv('matches.csv', mode='a', index=False, header=False)


# Function to parse player information from HTML files
def parse_players(html_file_path):
    # Read the HTML content from the local file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_code = file.read()
    print(html_file_path)

    # Define regular expressions
    name_pattern = re.compile(r'<h1.*?><span>(\d+)</span>(.*?)</h1>')
    team_pattern = re.compile(
        r'class="player__header__item__value[^"]*"><img src="[^"]*" alt=""><span>(.*?)</span><\/div>', re.DOTALL)
    position_pattern = re.compile(
        r'<div class="player__header__item__value player__header__item__value--position">(.*?)</div>')
    birth_date_pattern = re.compile(r'class="player__header__item__value">(.*?)</div>')
    age_pattern = re.compile(
        r'<div class="player__header__item__header">Vek<span>&nbsp;</span></div><div class="player__header__item__value">(.*?)</div>')
    seasons_pattern = re.compile(r'class="player__career__item__value">(.*?)</div>')

    # Extract player details using regular expressions
    name_match = name_pattern.search(html_code)
    team_match = team_pattern.search(html_code)
    position_match = position_pattern.search(html_code)
    birth_date_match = birth_date_pattern.search(html_code)
    age_match = age_pattern.search(html_code)
    seasons_match = seasons_pattern.findall(html_code)

    # Create a dictionary to store player details
    player_details = {
        'name': name_match.group(2).strip() if name_match else None,
        'team': team_match.group(1).strip() if team_match else None,
        'position': position_match.group(1).strip() if position_match else None,
        'birth_date': birth_date_match.group(1).strip() if birth_date_match else None,
        'age': age_match.group(1).strip() if age_match else None,
        'seasons': seasons_match[0].strip() if seasons_match else None,
        'matches': seasons_match[1].strip() if seasons_match else None,
        'goals': seasons_match[2].strip() if seasons_match else None,
        'yellow_cards': seasons_match[3].strip() if seasons_match else None,
        'red_cards': seasons_match[4].strip() if seasons_match else None,
    }

    # Check if player details contain a valid name
    if player_details['name'] != None:
        # Create a DataFrame from the extracted information
        df = pd.DataFrame(player_details, index=['1'])

        # Save the DataFrame to a CSV file in append mode
        df.to_csv('players.csv', mode='a', index=False, header=False)
        # print("Data for player saved.")


# Directory path and file pattern for HTML files
directory_path = './nikeliga_data/'
file_pattern = r'^\d+-[a-zA-Z]{3}-[a-zA-Z]{3}\.html$'
i = 1
j = 1

# Loop through files in the directory
for filename in os.listdir(directory_path):
    if re.match(file_pattern, filename):
        file_path = os.path.join(directory_path, filename)
        parse_matches(file_path)
        # print("Number of match files processed: ", i)
        i = i + 1
    else:
        file_path = os.path.join(directory_path, filename)
        # print(filename)
        parse_players(file_path)
        # print("Number of player files processed: ", j)
        j = j + 1

# Print a message indicating the completion of processing
print("Done! Number of match files processed: ", i, ". Number of player files processed: ", j)

# Read the CSV files into DataFrames
read_file = pd.read_csv('players.csv')
read_file.to_excel('players.xlsx', index=False,
                   header=["name", "team", "position", "birth_date", "age", "seasons", "matches", "goals",
                           "yellow_cards", "red_cards"], sheet_name='players', )
read_file = pd.read_csv('matches.csv')
read_file.to_excel('matches.xlsx', index=False,
                   header=["Home Team", "Away Team", "Date", "Time", "Stadium", "Goals Home", "Goals Away", "Goals",
                           "Cards", "Red Cards"], sheet_name='matches')

# Print a message indicating the completion of file conversion
print("All files converted to CSV and XLSX files.")

