import requests
import json
import colorama
from colorama import Back, Fore, Style
import time
import os
colorama.init()
def clear():
    if os.name == 'nt':
        os.system('cls')
    else:  
        os.system('clear')
clear()
def read_from_file():
  file = input("Where is the file located: ")
  with open(file) as f:
    teams = [line.rstrip('\n') for line in f]
  for line in teams:
    team_num = line 
    season = input(Fore.YELLOW + Style.BRIGHT + f"what season do you want to search for team {team_num}: " + Style.RESET_ALL)
    main_function(team_num, season)
def input_data():
    try:
        team_num = int(input("Enter the team number: "))
        season = int(input("Enter the season year (e.g., 2023): "))
        main_function(team_num, season)
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        exit()
def main_function(team_num, season):
  query = f"""
  query {{
    teamByNumber(number: {team_num}) {{
      name
      quickStats(season: {season}) {{
        auto {{
          value
        }}
        dc {{
          value
        }}
        eg {{
          value
        }}
        tot {{
          value
        }}
        count
      }}
      matches(season: {season}) {{
        teamNumber
        eventCode
        matchId
        alliance
        allianceRole
        onField
        match {{
          id
          matchNum
          season
          eventCode
          scores {{
            __typename
            ... on MatchScores2023 {{
              red {{
                totalPoints
              }}
              blue {{
                totalPoints
              }}
            }}
          }}
          teams {{
            teamNumber
            alliance
          team{{
              name
            }}
          }}
          event {{
            name
          }}
        }}
      }}
    }}
  }}
  """
  url = 'https://api.ftcscout.org/graphql' 
  headers = {
      'Content-Type': 'application/json', 
  }

  response = requests.post(url, headers=headers, json={'query': query})
  total_score = 0
  clear()
  if response.status_code == 200:
      data = response.json()
      matches = data.get('data', {}).get('teamByNumber', {}).get('matches', [])
      if matches:
          for match in matches:
              match_data = match['match']
              match_num = match_data.get('matchNum', 0)
              event_code = match_data.get('eventCode', 0)
              event_name = match_data.get('event', {}).get('name', 0)

              print("-" * 50)
              print("Basic info: ")
              print(Fore.GREEN + f"Match Num: {match_num}" + Style.RESET_ALL)
              print(Fore.MAGENTA + f"Event Code: {event_code}" + Style.RESET_ALL)
              print(Fore.CYAN + f"Event Name: {event_name}" + Style.RESET_ALL)
              print("-" * 50)
              scores = match_data.get('scores', {})
              print("-" * 50)
              print(Fore.YELLOW + "Alliance scores:" + Style.RESET_ALL)
              red_score = scores.get('red', {}).get('totalPoints', 'N/A')
              blue_score = scores.get('blue', {}).get('totalPoints', 'N/A')
              total_score = red_score + blue_score
              print(Fore.RED + f"Red alliance score: {red_score}" + Style.RESET_ALL)
              print(Fore.BLUE + f"Blue alliance score: {blue_score}" + Style.RESET_ALL)
              blue_win = Back.BLUE
              red_win = Back.RED
              print(Fore.MAGENTA + f"total_score: {total_score}" + Style.RESET_ALL)
              if blue_score > red_score:
                  print(blue_win + "!Winner Blue alliance!"+ Style.RESET_ALL)
              elif red_score > blue_score:
                  print(red_win + "!Winner Red alliance!" + Style.RESET_ALL)
              elif red_score == blue_score:
                  print(Back.YELLOW + "!Tie!" + Style.RESET_ALL)
              print("-" * 50)
              print(Fore.YELLOW + "Teams in match: " + Style.RESET_ALL)
              for team in match_data['teams']:
                  alliance = team['alliance']
                  team_number = team['teamNumber']
                  team_name = team['team']['name']
                  if alliance == 'Red':
                      color_team_number = Fore.RED
                      color_alliance = Back.RED + Fore.WHITE
                  elif alliance == 'Blue':
                      color_team_number = Fore.BLUE
                      color_alliance = Back.BLUE + Fore.WHITE
                  else:
                      color_team_number = Fore.RESET
                      color_alliance = Back.RESET + Fore.RESET
                  
                  print(f"{color_team_number}Team: {team_name} - {team_number}, {Style.RESET_ALL} {color_alliance}Alliance: {alliance}{Style.RESET_ALL}")

              print("-" * 50)
              time.sleep(2)
      average = data.get('data', {}).get('teamByNumber', {}).get('quickStats', [])
      name = data.get('data', {}).get('teamByNumber', {}).get('name', 'N/A')
      if average:
        print("*" * 50)
        print(Fore.MAGENTA + f"Averages for {name}-{team_num}" + Style.RESET_ALL)
        drivecont = average.get('dc', {}).get('value', 0)
        auto = average.get('auto', {}).get('value', 0)
        endgame = average.get('eg', {}).get('value', 0)
        total = average.get('tot', {}).get('value', 0)
        drivecont = round(drivecont, 2)
        auto = round(auto, 2)
        endgame = round(endgame, 2)
        total = round(total, 2)
        print(Fore.GREEN + f"Autonomous average: {auto},"+ Style.RESET_ALL, Fore.LIGHTMAGENTA_EX + f"Driver control average: {drivecont}," + Style.RESET_ALL, Fore.CYAN + f"Endgame average: {endgame}" + Style.RESET_ALL, Fore.YELLOW + f"Total average: {total}" + Style.RESET_ALL)
        print("*" * 50)
  else:
      print(f"Request failed with status code {response.status_code}")
      print(response.text)

if __name__ == "__main__":
  option = input("1. Read team numbers from file" "\n" "2. Input team number manually" "\n" "3. Exit" "\n" "Enter an option: ")
  if option == "1":
    read_from_file()
  elif option == "2":
    input_data()
  elif option == "3":
    exit()
  else:
    exit()