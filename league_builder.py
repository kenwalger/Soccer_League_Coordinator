import csv

from operator import itemgetter

"""
Build a Soccer League
"""

__author__ = "Ken W. Alger"
__email__ = "kenalger@comcast.net"
__copyright__ = "Copyright 2016"
__version__ = "1.0.0"

TEAMS = ['Raptors', 'Dragons', 'Sharks']
PRACTICE = ['Mar 18, 1:00PM', 'Mar 17, 1:00PM', 'Mar 17, 3:00PM']


def get_data(file):
    """
    Imports player data
    :param file:
    :return: list of players
    """
    try:
        with open(file, newline='') as file:
            players = csv.DictReader(file)
            # del list_of_players[0]
            players_list = list(players)
        return players_list
    except Exception as error:
        print("Sorry, there was an error trying to get the data. {}"
              .format(error))


def sort_players(list_of_players):
    """
    Sorts players by height into two lists, experienced and not experienced
    :param list_of_players:
    :return:
    """
    sorted_players = sorted(list_of_players,
                            key=itemgetter('Height (inches)'))

    experienced_players = []
    non_experienced_players = []
    for player in sorted_players:
        if player['Soccer Experience'] == 'YES':
            experienced_players.append(player)
        else:
            non_experienced_players.append(player)
    return experienced_players, non_experienced_players


def assign_team(exp, non_exp):
    """
    Assign players to three teams of 6
    :param exp:
    :param non_exp:
    :return:
    """
    teams = [[], [], []]

    for n in range(len(TEAMS)):
        while len(teams[n]) != 3:
            player = exp.pop()
            player.update({'Team': TEAMS[n]})
            player.update({'Practice': PRACTICE[n]})
            teams[n].append(player)
    for n in range(len(TEAMS)):
        while len(teams[n]) != 6:
            player = non_exp.pop()
            player.update({'Team': TEAMS[n]})
            player.update({'Practice': PRACTICE[n]})
            teams[n].append(player)
    return teams


def print_league(teams):
    """
    Print the entire league with player information
    :param teams:
    :return:
    """
    league_report = "Raptors: {} \n\nDragons: {}\n\nSharks: {}"

    try:
        with open('league.txt', 'w') as league_file:
            league_file.write(league_report.format(teams[0],
                                                   teams[1],
                                                   teams[2]))
    except Exception as error:
        print('There was an error writing the league report file: {}'
              .format(error))


def print_letters(teams):
    """
    Generates the player guardian letter files
    :param teams:
    :return:
    """
    letter = 'Hello {},\n\n' \
             'Congratulations! {} has been placed on the {} soccer team for ' \
             '\nthe upcoming season. The first team practice will be held {}.' \
             '\n\nWe are looking forward to the season.\n\n' \
             'See you at the first practice!\n' \
             'Coach Beckham'

    for team in teams:
        for player in team:
            filename = generate_filename(player['Name'])
            try:
                with open('{}.txt'.format(filename), 'w') as player_letter:
                    player_letter.write(letter.format(
                        player['Guardian Name(s)'],
                        player['Name'],
                        player['Team'],
                        player['Practice']
                    ))
            except Exception as error:
                print('There was an error writing the player letters to '
                      'file: {}'.format(error))


def generate_filename(player_name):
    """
    Helper method for file name generation
    :param player_name:
    :return:
    """
    name = player_name.split()
    filename = '_'.join(name).lower()
    return filename


if __name__ == '__main__':
    league = get_data("soccer_players.csv")
    experienced, non_experienced = sort_players(league)
    raptors, dragons, sharks = assign_team(experienced, non_experienced)
    teams_in_league = raptors, dragons, sharks
    print_league(teams_in_league)
    print_letters(teams_in_league)
