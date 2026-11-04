import csv
import urllib.request
import json

URL = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/rankings"

def update_cfp_rankings():
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            cfp_poll = None
            for ranking in data.get('rankings', []):
                # Search for the official CFP poll name/type
                if ranking.get('type') == 'cfp' or 'Playoff' in ranking.get('name', ''):
                    cfp_poll = ranking
                    break
            
            # Fall back to AP poll if CFP rankings have not been released yet this season
            if not cfp_poll and data.get('rankings'):
                cfp_poll = data['rankings'][0]

            if not cfp_poll or 'ranks' not in cfp_poll:
                print("No ranking data found.")
                return

            rows = [["Rank", "Team", "Record", "Previous Rank", "Points"]]
            for item in cfp_poll['ranks']:
                rank = item.get('current', '')
                team_info = item.get('team', {})
                team_name = team_info.get('nickname') or team_info.get('location', 'N/A')
                record = item.get('recordSummary', 'N/A')
                prev_rank = item.get('previous', 'N/A')
                points = item.get('points', 0)
                
                rows.append([rank, team_name, record, prev_rank, points])

            with open('rankings.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
                
            print("Successfully updated rankings.csv")

    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    update_cfp_rankings()
