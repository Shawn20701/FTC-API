from imports import *
username = os.getenv('username')
authorization_key = os.getenv('authorization_key')
credentials = f'{username}:{authorization_key}'

encoded_credentials = base64.b64encode(credentials.encode()).decode()


headers = {
    'Authorization': f'Basic {encoded_credentials}'
}
cwd = os.getcwd()
class APIcalls:
    def retrieve_averages():
        main_team = input("Please enter the team number you wish to compare: ")
        season = input("which season do you want to pull data for: ")
        queries = misc.load_queries(f'{cwd}/queries.yaml')
        query = queries['teamData']['query'].replace('$teamNumber', main_team).replace('$season', season)
        url = 'https://api.ftcscout.org/graphql' 
        headers = {
            'Content-Type': 'application/json', 
        }
        response = requests.post(url, headers=headers, json={'query': query})
        if response.status_code == 200:
            data = response.json()
            name = data.get('data', {}).get('teamByNumber', {}).get('name', '')
            averages = data.get('data', {}).get('teamByNumber', {}).get('quickStats', {}).get('tot', {}).get('value', 0)
            threshold = averages
            time.sleep(3)
            misc.clear()
        else:
            print(colorama.Fore.RED + response.status_code + colorama.Style.RESET_ALL)
        file = input("Where is the file located: ")
        season = input(Fore.YELLOW + Style.BRIGHT + f"what season do you want to search for the file: " + Style.RESET_ALL)
        with open(file) as f:
            teams = [line.rstrip('\n') for line in f]
        team_names = []
        team_average = []
        for line in teams:
            team_num = line 
            queries = misc.load_queries(f'{cwd}/queries.yaml')
            query = queries['teamAverages']['query'].replace('$teamNumber', team_num).replace('$season', season)
            url = 'https://api.ftcscout.org/graphql' 
            headers = {
            'Content-Type': 'application/json', 
        }
            response = requests.post(url, headers=headers, json={'query': query})
            if response.status_code == 200:
                data = response.json()
                quick_stats = data.get('data', {}).get('teamByNumber', {}).get('quickStats', {})
                name = data.get('data', {}).get('teamByNumber', {}).get('name', '')
                if quick_stats is None:
                    print(f"No data for {name}-{team_num} in season {season}")
                    continue
                else:
                    team_names.append(name)
                    averages = data.get('data', {}).get('teamByNumber', {}).get('quickStats', {}).get('tot', {}).get('value', 0)
                    average_int = int(round(averages))
                    team_average.append(average_int)
        sorted_data = sorted(zip(team_names, team_average), key=lambda x: x[1], reverse=True)
        sorted_team_names, sorted_team_average = zip(*sorted_data)
        plt.figure(plt.figure(figsize=(10, 6)))
        colors = ['red' if avg < threshold else 'skyblue' for avg in sorted_team_average]
        plt.scatter(sorted_team_names, sorted_team_average, color=colors, edgecolor='black')
        plt.xlabel('Team Names')
        plt.ylabel('Average Score')
        plt.title('Team Averages')
        plt.xticks(rotation=75, ha='right')
        plt.tight_layout() 
        plt.show()
    def retrieve_scores(event_code, team_number):
        season = 2023
        tournamentLevel = 'qual'
        response = requests.get(f'http://ftc-api.firstinspires.org/v2.0/{season}/scores/{event_code}/{tournamentLevel}', headers=headers, params={
            "teamNumber":team_number
        })
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matchScores')
            for match in matches:
                alliances = match.get('alliances', {})
                print(alliances)
    def read_from_file():
        file = input("Where is the file located: ")
        with open(file) as f:
            teams = [line.rstrip('\n') for line in f]
        for line in teams:
            team_num = line 
            season = input(Fore.YELLOW + Style.BRIGHT + f"what season do you want to search for team {team_num}: " + Style.RESET_ALL)
            main.main_function(team_num, season)
    def input_data():
        try:
            team_num = input("Enter the team number: ")
            season = input("Enter the season year (e.g., 2023): ")
            option = input("would you like to recieve event data or match data (e/m): ").lower()
            if option == 'm':
                main.main_function(team_num, season)
            elif option == 'e':
                filename = input("where would you like to save the data: ")
                get_event_teams(team_num,season,filename)
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            exit()
def get_event_teams(team_num,season,filename):
    queries = misc.load_queries(f'{cwd}/queries.yaml')
    query = queries['Events']['query'].replace('$teamNumber', team_num).replace('$season', season)
    url = 'https://api.ftcscout.org/graphql' 
    headers = {
      'Content-Type': 'application/json', 
  }

    response = requests.post(url, headers=headers, json={'query': query})
    if response.status_code == 200:
        data = response.json()
        events = data.get('data', {}).get('teamByNumber', {}).get('events', [])
        seen_teams = set()
        for event in events:
            teams = event.get('event', {}).get('teams', [])
        for team in teams:
            team_number = team.get('teamNumber', 'N/A')
            if team_number not in seen_teams:
                        seen_teams.add(team_number)
                        print(team_number)
                        with open(filename, 'w') as file:
                            for team_number in seen_teams:
                                file.write(f"{team_number}\n")
    else: 
        print(response.status_code)

class misc:
    def clear():
        if os.name == 'nt':
            os.system('cls')
        else:  
            os.system('clear')
    def load_queries(filename):
        with open(filename, 'r') as file:
            return yaml.safe_load(file)
class main:
    def main_function(team_num, season):
        queries = misc.load_queries(f'{cwd}/queries.yaml')
        query = queries['Mainquery']['query'].replace('$teamNumber', team_num).replace('$season', season)
        url = 'https://api.ftcscout.org/graphql' 
        headers = {
            'Content-Type': 'application/json', 
        }

        response = requests.post(url, headers=headers, json={'query': query})
        total_score = 0
        misc.clear()
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
        elif response.status_code == 429:  
                wait_time = 2 ** attempt
                print(f"Rate limited. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                fetch_data(team_num, season, attempt + 1)
        else:
            print(f"Request failed with status code {response.status_code}")
            print(response.text)