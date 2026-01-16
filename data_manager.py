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

    def get_recent_series(self, tournament_id):
        query = """query AllSeries($tournamentId: [ID!]) {
            allSeries(filter: { tournament: { id: { in: $tournamentId } } }, orderBy: StartTimeScheduled) {
                edges { node { id } }
            }
        }"""
        result = self._execute_query(query, {"tournamentId": [tournament_id]})
        return [edge['node'] for edge in result['data']['allSeries']['edges']] if result else []

    def get_series_stats(self, series_id):
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
