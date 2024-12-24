import sys
import csv
import numpy as np

def read_games(filename):
    """
    Reads a CSV file with lines in the format:
    teamA,teamB,scoreA,scoreB
    """
    games = []
    teams_set = set()
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            teamA, teamB, scoreA, scoreB = row
            scoreA, scoreB = int(scoreA), int(scoreB)
            teams_set.update([teamA, teamB])
            games.append((teamA, teamB, scoreA, scoreB))
    return games, list(teams_set)

def build_colley_matrix(games, teams):
    n = len(teams)
    team_index = {team: i for i, team in enumerate(teams)}
    
    # Keep track of wins, losses, and number of matchups
    W = [0]*n
    L = [0]*n
    matchups = np.zeros((n,n), dtype=int)
    
    for teamA, teamB, scoreA, scoreB in games:
        i = team_index[teamA]
        j = team_index[teamB]
        matchups[i, j] += 1
        matchups[j, i] += 1
        
        if scoreA > scoreB:
            W[i] += 1
            L[j] += 1
        elif scoreB > scoreA:
            W[j] += 1
            L[i] += 1
    
    # Build Colley matrix C and vector b
    C = np.zeros((n, n), dtype=float)
    b = np.zeros(n, dtype=float)
    
    for i in range(n):
        # Diagonal entries: 2 + total games
        C[i, i] = 2 + sum(matchups[i, :])
        # Off-diagonal: -number of matchups
        for j in range(n):
            if i != j:
                C[i, j] = -matchups[i, j]
        # Right-hand side
        b[i] = 1 + (W[i] - L[i]) / 2.0
    
    return C, b, team_index

def main():
    if len(sys.argv) < 2:
        print("Usage: python colley.py input.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    games, teams = read_games(input_file)
    C, b, team_index = build_colley_matrix(games, teams)
    
    # Solve the linear system
    ratings = np.linalg.solve(C, b)
    
    # Pair each team with its rating
    team_ratings = [(team, ratings[idx]) for team, idx in team_index.items()]
    # Sort by rating descending
    team_ratings.sort(key=lambda x: x[1], reverse=True)
    
    print("Colley Rankings:")
    for rank, (team, rating) in enumerate(team_ratings, start=1):
        print(f"{rank}. {team}: {rating:.3f}")

if __name__ == "__main__":
    main()
