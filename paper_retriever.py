"""
Paper Retriever - Step 2 of GapFinder pipeline
Fetches papers from Semantic Scholar API
"""

import requests
import time

class PaperRetriever:
    def __init__(self):
        self.base_url = "https://api.semanticscholar.org/graph/v1"
    
    def retrieve(self, queries, num_papers=30, guided_papers=None):
        """
        Retrieve papers from Semantic Scholar
        """
        all_papers = {}
        
        # Add guided papers if provided (user's own papers)
        if guided_papers:
            for paper_id in guided_papers:
                paper = self._get_paper_by_id(paper_id)
                if paper and paper.get('paperId'):
                    all_papers[paper_id] = paper
        
        # Search using each query
        for query in queries:
            print(f"   Searching: '{query}'")
            papers = self._search_papers(query, num_papers)
            for paper in papers:
                if paper.get('paperId') and paper['paperId'] not in all_papers:
                    all_papers[paper['paperId']] = paper
            
            # Wait to avoid hitting API rate limits
            time.sleep(1)
        
        # Return list, limited to num_papers
        return list(all_papers.values())[:num_papers]
    
    def _search_papers(self, query, limit=30):
        """Search papers using Semantic Scholar API"""
        url = f"{self.base_url}/paper/search"
        params = {
            'query': query,
            'limit': limit,
            'fields': 'title,abstract,year,venue,citationCount,authors,paperId'
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return data.get('data', [])
            else:
                print(f"   API error: {response.status_code}")
                return []
        except Exception as e:
            print(f"   Search error: {e}")
            return []
    
    def _get_paper_by_id(self, paper_id):
        """Get single paper by ID"""
        url = f"{self.base_url}/paper/{paper_id}"
        params = {'fields': 'title,abstract,year,venue,citationCount,paperId'}
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None