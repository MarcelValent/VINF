import re
import pandas as pd
import os
# Loop through HTML files in the directory and parse each one


def parse_matches(html_file_path):
    print(html_file_path)
    # Read the HTML content from the local file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html = file.read()
    # Extract information using regular expressions
    match_info = {}

    # Match information
    match_match = re.search(r'<div class="container-flow box-header box-header--no-margin box-header--bigger">([\d.]+) (.*?)</div>', html)



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
    goals_match = re.findall(r'<div class="game__goals__item"><a href="[^"]+" title=""><i class="ico ico-ball"></i><span class="hidden-xs">(.*?)</span> (.*?)</a> \((\d+)“\)</div>', html)
    cards_match = re.findall(r'<div class="game__cards__item"><a href="[^"]+" title=""> <i class="ico ico-card yellow"></i><span class="hidden-xs">(.*?)</span>(.*?)</a> \((\d+)“\)</div>', html)
    r_cards_match = re.findall(r'<div class="game__cards__item"><a href="[^"]+" title=""> <i class="ico ico-card red"></i><span class="hidden-xs">(.*?)</span>(.*?)</a> \((\d+)“\)</div>', html)
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
    # Save the DataFrame to an Excel file
    df.to_csv('data.csv', mode='a', index=False)

    print("Data for match saved.")
# Specify the directory path containing the HTML files
directory_path = './nikeliga_data/'

# Define a regular expression pattern for matching filenames
file_pattern = r'^\d+-[a-zA-Z]{3}-[a-zA-Z]{3}\.html$'

# Loop through HTML files in the directory and parse each one
i = 1
for filename in os.listdir(directory_path):
    if re.match(file_pattern, filename):
        file_path = os.path.join(directory_path, filename)
        parse_matches(file_path)
        print("Number of files processed: ", i)
        i = i + 1
read_file = pd.read_csv('data.csv')
read_file.to_excel('data.xlsx', index=None, header=False)




