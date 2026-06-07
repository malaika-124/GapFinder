"""
Synthesizer - Step 4 of GapFinder pipeline
Identifies research gaps by analyzing patterns across papers
"""

import json

class Synthesizer:
    def __init__(self, model):
        self.model = model
    
    def synthesize(self, papers_data):
        """
        Identify research gaps from analyzed papers
        """
        # If no papers, return empty list
        if not papers_data:
            return []
        
        # Prepare a summary for the LLM (limit to avoid token limits)
        summary = []
        for p in papers_data[:30]:  # Limit to 30 papers
            summary.append({
                "title": p.get('title', ''),
                "limitations": p.get('limitations_stated', ''),
                "future_work": p.get('future_work_mentioned', ''),
                "problems": p.get('problems_not_addressed', '')
            })
        
        prompt = f"""
You are a research synthesizer. Analyze these {len(papers_data)} papers:

PAPER SUMMARIES:
{json.dumps(summary, indent=2)[:6000]}

Follow this Chain-of-Thought process:

STEP 1: List all limitations mentioned across papers
STEP 2: Identify methods that are never combined together
STEP 3: Note underrepresented datasets or populations
STEP 4: List explicit future work suggestions

Now, identify research gaps. Return ONLY a JSON list. Each gap should have:
- description: Clear description of the gap
- supporting_papers: List of paper titles that mention this
- gap_type: One of ["limitation", "method_combination", "dataset", "future_work"]

Example: [{{"description": "No deep learning method has been applied to this specific problem", "supporting_papers": ["Paper1 Title"], "gap_type": "method_combination"}}]

Return ONLY the JSON list, no other text.
"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text
            
            # Extract JSON
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0]
            elif '```' in text:
                text = text.split('```')[1].split('```')[0]
            
            gaps = json.loads(text)
            return gaps if gaps else self._get_default_gaps()
            
        except Exception as e:
            print(f"   Synthesis warning: {e}")
            return self._get_default_gaps()
    
    def _get_default_gaps(self):
        """Return default gaps if synthesis fails"""
        return [
            {
                "description": "Limited research applying modern AI methods to this domain",
                "supporting_papers": [],
                "gap_type": "method_combination"
            },
            {
                "description": "Need for larger, more diverse datasets in this area",
                "supporting_papers": [],
                "gap_type": "dataset"
            }
        ]