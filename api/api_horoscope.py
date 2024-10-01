import requests


def get_daily_horoscope(sign: str, day: str) -> dict:
    """Get daily horoscope for a zodiac sign.

    Keyword arguments:
    sign:str - Zodiac sign
    day:str - TODAY OR TOMORROW OR YESTERDAY
    Return:dict - JSON data
    """
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)

    return response.json()

def get_monthly_horoscope(sign: str) -> dict:
    """Get monthly horoscope for a zodiac sign.

    Keyword arguments:
    sign:str - Zodiac sign
    Return:dict - JSON data
    """
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/monthly"
    params = {"sign": sign}
    response = requests.get(url, params)

    return response.json()


def get_weekly_horoscope(sign: str) -> dict:
    """Get weekly horoscope for a zodiac sign.

    Keyword arguments:
    sign:str - Zodiac sign
    Return:dict - JSON data
    """
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/weekly"
    params = {"sign": sign}
    response = requests.get(url, params)

    return response.json()

