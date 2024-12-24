import sys
import csv
import math

K = 100  # Adjust to your preference

def expected_score(ratingA, ratingB):
    return 1.0 / (1.0 + 10 ** ((ratingB - ratingA) / 400.0))

def main():
    if len(sys.argv) < 2:
        print("Usage: python elo.py input.csv")
        sys.exit(1)

    input_file = sys.argv[1]

    # Dictionary to hold team -> rating
    ratings = {}

    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        # If there's a header, uncomment the next line:
        # next(reader, None)  # skip header row if present

        for row in reader:
            if len(row) < 4:
                continue

            teamA, teamB, scoreA, scoreB = row
            scoreA, scoreB = int(scoreA), int(scoreB)

            if teamA not in ratings:
                ratings[teamA] = 1500.0
            if teamB not in ratings:
                ratings[teamB] = 1500.0

            eloA = ratings[teamA]
            eloB = ratings[teamB]

            # Determine winner/loser or tie
            if scoreA > scoreB:
                actualA, actualB = 1.0, 0.0
            elif scoreB > scoreA:
                actualA, actualB = 0.0, 1.0
            else:
                # Tie scenario (unlikely in basketball, but just in case)
                actualA, actualB = 0.5, 0.5

            expectedA = expected_score(eloA, eloB)
            expectedB = 1.0 - expectedA

            # Update ratings
            ratings[teamA] = eloA + K * (actualA - expectedA)
            ratings[teamB] = eloB + K * (actualB - expectedB)

    # Sort final ratings descending
    sorted_ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)

    print("Final Elo Ratings:")
    for rank, (team, rating) in enumerate(sorted_ratings, start=1):
        print(f"{rank}. {team}: {rating:.1f}")

if __name__ == "__main__":
    main()
