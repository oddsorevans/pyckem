import os
import sys
import requests
from typing import Dict, List

# Try to load API keys from environment variables first, then from file
try:
    RAPID_API_KEY = os.environ.get('RAPID_API_KEY')
    RAPID_API_HOST = os.environ.get('RAPID_API_HOST')

    if not RAPID_API_KEY or not RAPID_API_HOST:
        from misc.rapid_api_key import x_rapid_key, x_rapid_host
        RAPID_API_KEY = x_rapid_key
        RAPID_API_HOST = x_rapid_host
except ImportError:
    if not os.environ.get('RAPID_API_KEY') or not os.environ.get('RAPID_API_HOST'):
        print("Error: API keys not found. Set RAPID_API_KEY and RAPID_API_HOST environment variables")
        sys.exit(1)

def getGamesData(dates: List[str]) -> Dict[str, Dict[str, str]]:
    """Fetch NFL game data from RapidAPI for the given dates.

    Args:
        dates: List of date strings in YYYY-MM-DD format

    Returns:
        Dictionary mapping game names to team information
        Format: {"Team1 vs. Team2": {"home": "Team1", "away": "Team2"}}

    Raises:
        requests.RequestException: If API request fails
    """
    url = "https://api-american-football.p.rapidapi.com/games"
    gameData = {}

    for date in dates:
        querystring = {"date": date, "league": "1"}
        headers = {
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": RAPID_API_HOST
        }

        try:
            response = requests.get(url, headers=headers, params=querystring, timeout=10)
            response.raise_for_status()
            json_response = response.json()

            if 'response' not in json_response:
                print(f"Warning: No 'response' field in API data for {date}")
                continue

            for game in json_response['response']:
                try:
                    home = game['teams']['home']['name']
                    away = game['teams']['away']['name']
                    versus = f"{home} vs. {away}"
                    gameData[versus] = {'home': home, 'away': away}
                except (KeyError, TypeError) as e:
                    print(f"Warning: Skipping malformed game data for {date}: {e}")
                    continue

        except requests.Timeout:
            print(f"Error: Request timeout for date {date}")
            continue
        except requests.HTTPError as e:
            print(f"Error: HTTP error for date {date}: {e}")
            continue
        except requests.RequestException as e:
            print(f"Error: Failed to fetch games for date {date}: {e}")
            continue
        except ValueError as e:
            print(f"Error: Invalid JSON response for date {date}: {e}")
            continue

    return gameData

