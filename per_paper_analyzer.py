"""
Per-Paper Analyzer - Step 3 of GapFinder pipeline
Extracts structured information from each paper
"""

import json
import time

class PerPaperAnalyzer:
    def __init__(self, model):
        self.model = model
    
    def analyze_batch(self, papers):
        """Analyze multiple papers"""
        results = []
        
        for i, paper in enumerate(papers):
            print(f"   Analyzing paper {i+1}/{len(papers)}...", end='\r')
            result = self.analyze_single(paper)
            if result:
                results.append(result)
            time.sleep(0.5)  # Wait between API calls
        
        print(f"\n   ✓ Analyzed {len(results)} papers")
        return results
    
    def analyze_single(self, paper):
        """Analyze a single paper using LLM"""
        title = paper.get('title', 'Unknown Title')
        abstract = paper.get('abstract', 'Abstract not available')
        
        # Handle missing abstract
        if not abstract or abstract == "":
            abstract = "Abstract not available in this paper"
        
        prompt = f"""
You are a scientific paper analyzer. Analyze this paper:

TITLE: {title}
ABSTRACT: {abstract}

Extract the following information. If information is missing, write "Not mentioned".

Return ONLY valid JSON, no other text:

{{
    "paper_id": "{paper.get('paperId', 'unknown')}",
    "title": "{title.replace('"', '\\"')}",
    "year": {paper.get('year', 0)},
    "citation_count": {paper.get('citationCount', 0)},
    "primary_method": "What main method/algorithm does this paper use?",
    "datasets_used": "What datasets or data sources are used?",
    "limitations_stated": "What limitations does the paper mention?",
    "future_work_mentioned": "What future work does the paper suggest?",
    "problems_not_addressed": "What problems remain unsolved?"
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text
            
            # Clean the response to get pure JSON
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0]
            elif '```' in text:
                text = text.split('```')[1].split('```')[0]
            
            # Clean any trailing commas or invalid JSON
            text = text.strip()
            
            result = json.loads(text)
            return result
            
        except Exception as e:
            print(f"\n   Warning: Could not analyze paper {title[:50]}...")
            # Return basic info if analysis fails
            return {
                "paper_id": paper.get('paperId', 'unknown'),
                "title": title,
                "year": paper.get('year', 0),
                "citation_count": paper.get('citationCount', 0),
                "primary_method": "Not mentioned",
                "datasets_used": "Not mentioned",
                "limitations_stated": "Not mentioned",
                "future_work_mentioned": "Not mentioned",
                "problems_not_addressed": "Not mentioned"
            }