import sys
import csv
from bs4 import BeautifulSoup


def main():
    if len(sys.argv) < 3:
        print("Usage: python parse_html.py input.html output.csv")
        sys.exit(1)

    input_html = sys.argv[1]
    output_csv = sys.argv[2]

    with open(input_html, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml")

    rows_out = []
    # Each game table has border="1" and includes exactly 3 rows:
    # 1) header (FINAL - date/time), 2) team A/score, 3) team B/score
    for table in soup.find_all("table", border="1"):
        # Confirm the header row has "FINAL"
        header = table.find("tr", height="23")
        if not header or "FINAL" not in header.get_text():
            continue

        # The next two rows are the teams and scores
        data_rows = table.find_all("tr", height="25")
        if len(data_rows) != 2:
            continue

        # First team
        tds_a = data_rows[0].find_all("td")
        teamA = tds_a[0].get_text(strip=True)
        scoreA = tds_a[1].get_text(strip=True)

        # Second team
        tds_b = data_rows[1].find_all("td")
        teamB = tds_b[0].get_text(strip=True)
        scoreB = tds_b[1].get_text(strip=True)

        rows_out.append([teamA, teamB, scoreA, scoreB])

    # Write to CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out)
        # Optional header row
        writer.writerow(["teamA", "teamB", "scoreA", "scoreB"])
        for row in rows_out:
            writer.writerow(row)


if __name__ == "__main__":
    main()
