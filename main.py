import argparse
import sys
from datetime import datetime, timedelta
import nfl_request
import write_form

def generate_dates(start_date, end_date):
    """Generate a list of dates between start_date and end_date (inclusive).

    Note: Saturday and Monday night football may need date +1 due to an API quirk.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format

    Returns:
        List of date strings in YYYY-MM-DD format
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError as e:
        print(f"Error: Invalid date format. Use YYYY-MM-DD. {e}")
        sys.exit(1)

    if start > end:
        print("Error: Start date must be before or equal to end date")
        sys.exit(1)

    delta = timedelta(days=1)
    dates = []

    while start <= end:
        dates.append(start.strftime('%Y-%m-%d'))
        start += delta

    return dates

def main():
    parser = argparse.ArgumentParser(
        description='Generate NFL Pick-em Google Form for a given week'
    )
    parser.add_argument(
        '--start-date',
        required=True,
        help='Start date for games (YYYY-MM-DD format)'
    )
    parser.add_argument(
        '--end-date',
        required=True,
        help='End date for games (YYYY-MM-DD format)'
    )
    parser.add_argument(
        '--week',
        type=int,
        required=True,
        help='NFL week number'
    )
    parser.add_argument(
        '--final-game',
        required=True,
        help='Final game for tiebreaker (e.g., "Texans vs. Seahawks")'
    )

    args = parser.parse_args()

    print(f"Generating form for Week {args.week}")
    print(f"Date range: {args.start_date} to {args.end_date}")

    # Generate dates and fetch game data
    dates = generate_dates(args.start_date, args.end_date)
    print(f"Fetching games for {len(dates)} date(s)...")

    gameData = nfl_request.getGamesData(dates)

    if not gameData:
        print("Warning: No games found for the specified date range")
        sys.exit(1)

    print(f"Found {len(gameData)} game(s)")

    # Create the Google Form
    print("Creating Google Form...")
    write_form.create_write_form(gameData, week=args.week, final=args.final_game)
    print("Form created successfully!")

if __name__ == '__main__':
    main()