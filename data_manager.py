import requests
import json

class GridDataManager:
    def __init__(self, api_key):
        self.url = "https://api-op.grid.gg/central-data/graphql"
        self.headers = {"Content-Type": "application/json", "x-api-key": api_key}

    def _execute_query(self, query, variables=None):
        payload = {"query": query}
        if variables: payload["variables"] = variables
        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"GRID API Error: {e}")
            return None

    def get_tournaments(self, title_id="3"):
        query = """query Tournaments($titleId: [ID!]) {
            tournaments(filter: { title: { id: { in: $titleId } } }) {
                edges { node { id name } }
            }
        }"""
        result = self._execute_query(query, {"titleId": [title_id]})
        return [edge['node'] for edge in result['data']['tournaments']['edges']] if result else []
    
    def get_teams(self, title_id="3"):
        """
        Fetches teams for the selection dropdown. 
        Title ID '3' is League of Legends.
        """
        query = """
            query Teams($titleId: [ID!]) {
                teams(filter: { titleId: { in: $titleId }, externalIds: { source: "POWER_STATS" } }, first: 50) {
                    edges { node { id name } }
                }
            }
            """
        result = self._execute_query(query, {"titleId": [title_id]})
        if result and 'data' in result and 'teams' in result['data']:
            return [edge['node'] for edge in result['data']['teams']['edges']]
        return []

    def get_recent_series_by_team(self, team_id):
        """
        Scours GRID data for the last 10 series played by a specific team.
        """
        query = """
        query TeamSeries($teamId: [ID!]) {
            allSeries(filter: { teams: { id: { in: $teamId } } }, first: 10, orderBy: StartTimeScheduled) {
                edges { 
                    node { 
                        id 
                    } 
                }
            }
        }
        """
        result = self._execute_query(query, {"teamId": [team_id]})
        if result and 'data' in result and 'allSeries' in result['data']:
            return [edge['node'] for edge in result['data']['allSeries']['edges']]
        return []

    def get_series_stats(self, series_id):
        """
        Retrieves granular match and participant data for the analytics engine.
        Uses aliases to match the engine's expected field names.
        """
        query = """
        query Series($id: ID!) {
            series(id: $id) {
                matches {
                    side win patch
                    first_blood: firstBlood
                    first_tower: firstTower
                    first_dragon: firstDragon
                    first_herald: firstHerald
                    gold_diff_15: goldDiff15
                    participants {
                        player { name }
                        hero { name }
                        role
                        kills deaths assists
                    }
                }
            }
        }
        """
        result = self._execute_query(query, {"id": series_id})
        if result and result.get('data') and result['data'].get('series'):
            matches = result['data']['series'].get('matches', [])
            return matches if matches else None
        return None


