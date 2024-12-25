import sys
import csv
import numpy as np


def read_games(filename):
    """
    Reads a CSV file with lines:
    teamA,teamB,scoreA,scoreB
    """
    games = []
    teams_set = set()
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        # If there's a header, uncomment next line:
        # next(reader, None)
        for row in reader:
            if len(row) < 4:
                continue
            teamA, teamB, scoreA, scoreB = row
            scoreA, scoreB = int(scoreA), int(scoreB)
            teams_set.update([teamA, teamB])
            games.append((teamA, teamB, scoreA, scoreB))
    return games, list(teams_set)


def build_massey_matrix(games, teams):
    """
    Massey system: for each game (A vs B), rating[A] - rating[B] = (scoreA - scoreB).
    We accumulate these into a matrix M and vector p, then fix the last row so sum(ratings)=0.
    """
    n = len(teams)
    team_index = {team: i for i, team in enumerate(teams)}

    M = np.zeros((n, n), dtype=float)
    p = np.zeros(n, dtype=float)

    # For each game, update M and p
    for teamA, teamB, scoreA, scoreB in games:
        i = team_index[teamA]
        j = team_index[teamB]
        diff = scoreA - scoreB

        # rating[i] - rating[j] = diff
        M[i, i] += 1
        M[i, j] -= 1
        M[j, j] += 1
        M[j, i] -= 1

        p[i] += diff
        p[j] -= diff

    # Fix the system (make sum of all ratings = 0)
    # Replace the last row with [1,1,1,...,1] and p[last] = 0
    # so the solution is unique.
    for col in range(n):
        M[n - 1, col] = 1
    p[n - 1] = 0

    return M, p, team_index


def main():
    if len(sys.argv) < 2:
        print("Usage: python massey.py input.csv")
        sys.exit(1)

    input_file = sys.argv[1]

    games, teams = read_games(input_file)
    M, p, team_index = build_massey_matrix(games, teams)

    # Solve M * r = p
    # Use lstsq in case the matrix isn't perfectly square after fixing the row
    ratings, _, _, _ = np.linalg.lstsq(M, p, rcond=None)

    # Pair team name with rating
    team_ratings = [(team, ratings[idx]) for team, idx in team_index.items()]
    # Sort descending
    team_ratings.sort(key=lambda x: x[1], reverse=True)

    print("Massey Ratings:")
    for rank, (team, rating) in enumerate(team_ratings, start=1):
        print(f"{rank}. {team}: {rating:.3f}")


if __name__ == "__main__":
    main()
