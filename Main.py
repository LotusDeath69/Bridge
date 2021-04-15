import requests
"""
Bridge_Duel =  solo mode (1v1)
Bridge_doubles = double mode (2v2)
Bridge_four = 4s mode (4v4)
There are also modes for 3v3v3v3 and 2v2v2v2
Final stats are calculated by adding all of these modes up
Total_games_played = wins + losses + ties
"""
api = 'INSERT_KEY_HERE'


def uuid(ign):
    data = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}').json()
    return data['id']


def formatPercentage(x):
    return "{:.0%}".format(x)


def stats(ign, key):
    data = requests.get(f'https://api.hypixel.net/player?key={key}&uuid={uuid(ign)}').json()
    try:
        deaths = data['player']['stats']['Duels']['bridge_deaths']
        kills = data['player']['stats']['Duels']['bridge_kills']
    except KeyError:
        return f'{ign} has no bridge stats'
    
    total_wins = 0
    total_losses = 0
    total_games_played = 0
    total_goals = 0
    modes = ['duel', 'doubles', 'four']
    for i in modes:
        try:
            total_wins += data['player']['stats']['Duels'][f'bridge_{i}_wins']
        except KeyError:
            continue
    for i in modes:
        try:
            total_losses += data['player']['stats']['Duels'][f'bridge_{i}_losses']
        except KeyError:
            continue

    for i in modes:
        try:
            total_games_played += data['player']['stats']['Duels'][f'bridge_{i}_rounds_played']
        except KeyError:
            continue

    for i in modes:
        try:
            total_goals += data['player']['stats']['Duels'][f'bridge_{i}_goals']
        except KeyError:
            continue
    
    KD_ratio = round(kills/deaths, 2)
    winrate = formatPercentage(round(total_wins / (total_losses + total_wins), 2))
    ties = total_games_played - (total_wins + total_losses)

    return f'Wins: {total_wins} Losses: {total_losses} Ties: {ties} Kills: {kills} Deaths: {deaths} KD Ratio: {KD_ratio} Win rate:'\
    f' {winrate} Games Played: {total_games_played} goals: {total_goals}'


print(stats('thatbananaking', api))
