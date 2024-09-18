from imports import *
class APIcalls:
    def retrieve_averages():
        main_team = input("Please enter the team number you wish to compare: ")
        season = input("which season do you want to pull data for: ")
        cwd = os.getcwd()
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
                    name = data.get('data', {}).get('teamByNumber', {}).get('name', '')
                    team_names.append(name)
                    averages = data.get('data', {}).get('teamByNumber', {}).get('quickStats', {}).get('tot', {}).get('value', 0)
                    average_int = int(round(averages))
                    team_average.append(average_int)
        sorted_data = sorted(zip(team_names, team_average), key=lambda x: x[1], reverse=True)
        sorted_team_names, sorted_team_average = zip(*sorted_data)
        plt.figure(plt.figure(figsize=(10, 6)))
        colors = ['red' if avg < threshold else 'skyblue' for avg in sorted_team_average]
        plt.scatter(sorted_team_names, sorted_team_average, edgecolor='black')
        plt.xlabel('Team Names')
        plt.ylabel('Average Score')
        plt.title('Team Averages')
        plt.xticks(rotation=75, ha='right')
        plt.tight_layout() 
        plt.show()
class misc:
    def clear():
        if os.name == 'nt':
            os.system('cls')
        else:  
            os.system('clear')
    def load_queries(filename):
        with open(filename, 'r') as file:
            return yaml.safe_load(file)