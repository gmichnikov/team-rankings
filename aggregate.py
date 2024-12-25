import re


def parse_ranking(file_path):
    rankings = {}
    pattern = re.compile(r"^(\d+)\.\s+([^:]+):?\s*[\d\.]*$")
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = pattern.match(line)
            if match:
                rank = int(match.group(1))
                team_name = match.group(2).strip()
                rankings[team_name] = rank
    return rankings


def main():
    colley_file = "colley.txt"
    elo_file = "elo.txt"
    massey_file = "massey.txt"

    colley_rankings = parse_ranking(colley_file)
    elo_rankings = parse_ranking(elo_file)
    massey_rankings = parse_ranking(massey_file)

    all_teams = (
        set(colley_rankings.keys())
        | set(elo_rankings.keys())
        | set(massey_rankings.keys())
    )

    final_table = []

    for team in all_teams:
        colley_rank = colley_rankings.get(team)
        elo_rank = elo_rankings.get(team)
        massey_rank = massey_rankings.get(team)

        # Assign a default rank if missing
        max_rank = len(all_teams) + 1
        colley_rank = colley_rank if colley_rank is not None else max_rank
        elo_rank = elo_rank if elo_rank is not None else max_rank
        massey_rank = massey_rank if massey_rank is not None else max_rank

        avg_rank = (colley_rank + elo_rank + massey_rank) / 3.0
        final_table.append((team, colley_rank, elo_rank, massey_rank, avg_rank))

    # Sort by average rank ascending
    final_table.sort(key=lambda x: x[4])

    # Print the table
    print(f"{'Team':<30} {'Colley':<7} {'Elo':<5} {'Massey':<7} {'Avg Rank':<10}")
    print("-" * 60)
    for row in final_table:
        team, colley, elo, massey, avg = row
        print(f"{team:<30} {colley:<7} {elo:<5} {massey:<7} {avg:<10.2f}")


if __name__ == "__main__":
    main()
