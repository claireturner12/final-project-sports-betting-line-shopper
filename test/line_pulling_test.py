from app.odds_shopper import get_in_season_sports

def test_api_working():
    assert isinstance(get_in_season_sports(), list)