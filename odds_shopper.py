### returns the lines for games for the sport of the user choice
import requests
import pandas as pd
import os

# Access the secret
api_key = os.getenv('ODDS_API')

def get_odds(sport="americanfootball_nfl",region="us", markets = "totals"):

    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"

    params = {
        "apiKey": api_key,
        "regions": region,
        "markets": {markets},
        "oddsFormat": "american",
        "dateFormat": "iso"
    }

    response = requests.get(url, params=params)

    json_data = response.json()
    lines = pd.DataFrame(data=json_data)
    lines = lines.sort_values(by=["commence_time"])

def process_odds(lines, type="totals"):
    for index, row in lines.iterrows():
        counter = 0
        bet_one_key  = None
        bet_one_line = None
        bet_one_odds = None
        bet_two_key = None
        bet_two_line = None
        bet_two_odds = None
        for book in row['bookmakers']:
            book_name = book['title']
            book_lines = book['markets'][0]['outcomes']
            if counter == 0:
                bet_one_key = book_name
                bet_one_odds = book_lines[0]['price']
                bet_two_key = book_name
                bet_two_odds = book_lines[1]['price']

                if type != "ml":
                    bet_one_line = book_lines[0]['point']
                    bet_two_line = book_lines[1]['point']

                counter +=1
            else:
                
                one_price = book_lines[0]['price']
                two_price = book_lines[1]['price']

                if type != "ml":
                    one_line = book_lines[0]['point']
                    two_line = book_lines[1]['point']
                

                if type == "ml":
                    if one_price > bet_one_odds:
                        bet_one_key = book_name
                        bet_one_odds = one_price

                    if two_price > bet_two_odds:
                        bet_two_key = book_name
                        bet_two_odds = two_price

                elif type == "totals":
                    if one_line < bet_one_line:
                        bet_one_key = book_name
                        bet_one_odds = one_price
                        bet_one_line = one_line
                    elif (one_price > bet_one_odds) & (one_line == bet_one_line):
                        bet_one_key = book_name
                        bet_one_line = one_line
                        bet_one_odds = one_price
                

                    if two_line > bet_two_line:
                        bet_two_key = book_name
                        bet_two_odds = two_price
                        bet_two_line = two_line
                    elif (two_price > bet_two_odds) & (two_line == bet_two_line):
                        bet_two_key = book_name
                        bet_two_line = two_line
                        bet_two_odds = two_price

                #Spreads
                else:
                    if one_line > bet_one_line:
                        bet_one_key = book_name
                        bet_one_odds = one_price
                        bet_one_line = one_line
                    elif (one_price > bet_one_odds) & (one_line == bet_one_line):
                        bet_one_key = book_name
                        bet_one_line = one_line
                        bet_one_odds = one_price

                counter += 1
            

        lines.at[index, 'one_sportsbook'] = bet_one_key
        lines.at[index, 'one_line'] = bet_one_line
        lines.at[index, 'one_odds'] = bet_one_odds
        lines.at[index, 'two_sportsbook'] = bet_two_key
        lines.at[index, 'two_line'] = bet_two_line
        lines.at[index, 'two_odds'] = bet_two_odds

    lines.drop(columns=['bookmakers'], inplace=True)
    return lines



def get_in_season_sports():

    url = f"https://api.the-odds-api.com/v4/sports/?apiKey={api_key}"
    response = requests.get(url)

    data = response.json()

    sports = [x['key'] for x in data]

    return sports


def user_selection_odds():

    selection = input("Please input user sport:")
    in_season_sports = get_in_season_sports()
    if selection not in in_season_sports:
        print("Error: Sport is not in season")
    #sportsbook_selection = input("sportsbook_selection")

    totals_odds = get_odds(sport = selection, markets = "totals")
    spreads_odds = get_odds(sport = selection, markets = "spreads")
    ml_odds = get_odds(sport = selection, markets = "h2h")

    totals = process_odds(totals_odds, "totals")
    spreads = process_odds(spreads_odds, "totals")
    ml = process_odds(ml_odds, "totals")

    #rename columns to match subject
    spreads[["one_sportsbook", "one_line", "one_odds", "two_sportsbook", "two_line", "two_odds"]].rename([
        'away_spread_book',
        'away_spread'
        'away_odds',
        'home_spread_book',
        'home_spread',
        'home_odds'
    ],inplace=True)

    totals[["one_sportsbook", "one_line", "one_odds", "two_sportsbook", "two_line", "two_odds"]].rename([
        'over_book',
        'over_total'
        'over_odds',
        'under_book',
        'under_total',
        'under_odds'
    ],inplace=True)

    ml[["one_sportsbook", "one_line", "one_odds", "two_sportsbook", "two_line", "two_odds"]].rename([
        'away_ml_book',
        'away_ml_odds',
        'home_ml_book',
        'home_ml_odds'
    ],inplace=True)

    
    totals_to_add = totals[['id', 'over_book', 'over_total','over_odds', 'under_book', 'under_total', 'under_odds']]
    ml_to_add = ml[['id', 'away_ml_book', 'away_ml_odds', 'home_ml_book', 'home_ml_odds']]
    game_lines = spreads.merge(
        totals_to_add,
        on="id",
        how="left",
    )
    game_lines = game_lines.merge(
        ml_to_add,
        on="id",
        how="left",
    )
    return game_lines

