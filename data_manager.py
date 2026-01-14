import requests
import json

class GridDataManager:
    def __init__(self, api_key):
        self.url = "https://api-op.grid.gg/central-data/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key
        }

    def _execute_query(self, query, variables=None):
        """Internal helper to execute GraphQL queries."""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
            
        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"GRID API Error: {e}")
            return None

    def get_titles(self):
        """Fetches available game titles (LoL, VAL, etc.)."""
        query = """
        query Titles {
            titles {
                id
                name
            }
        }
        """
        result = self._execute_query(query)
        return result['data']['titles'] if result else []

    def get_tournaments(self, title_id="3"):
        """Fetches tournaments for a specific title (Default 3 = LoL)."""
        query = """
        query Tournaments($titleId: [ID!]) {
            tournaments(filter: { title: { id: { in: $titleId } } }) {
                edges {
                    node {
                        id
                        name
                    }
                }
            }
        }
        """
        variables = {"titleId": [title_id]}
        result = self._execute_query(query, variables)
        return [edge['node'] for edge in result['data']['tournaments']['edges']] if result else []

    def get_recent_series(self, tournament_id):
        """Fetches series history for Recon and Drafting analysis."""
        query = """
        query AllSeries($tournamentId: [ID!]) {
            allSeries(
                filter: { tournament: { id: { in: $tournamentId }, includeChildren: { equals: true } } }
                orderBy: StartTimeScheduled
            ) {
                edges {
                    node {
                        id
                        startTimeScheduled
                        teams {
                            baseInfo {
                                id
                                name
                            }
                        }
                    }
                }
            }
        }
        """
        variables = {"tournamentId": [tournament_id]}
        result = self._execute_query(query, variables)
        return [edge['node'] for edge in result['data']['allSeries']['edges']] if result else []
