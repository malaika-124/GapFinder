"""
Query Formulator - Step 1 of GapFinder pipeline
Expands user topic into structured search queries
"""

class QueryFormulator:
    def __init__(self, model):
        self.model = model
    
    def formulate(self, topic):
        """
        Convert user topic into search queries
        """
        prompt = f"""
        You are a research query formulator. Given this research topic:
        "{topic}"
        
        Generate 3-5 specific search queries that would retrieve relevant academic papers.
        Return ONLY a Python list of strings, nothing else.
        
        Example format: ["query1", "query2", "query3"]
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Clean the response to extract the list
            text = response.text
            # Remove markdown code blocks if present
            if '```python' in text:
                text = text.split('```python')[1].split('```')[0]
            elif '```' in text:
                text = text.split('```')[1].split('```')[0]
            queries = eval(text)
            return queries
        except:
            # Fallback queries if something goes wrong
            return [topic, f"advances in {topic}", f"review of {topic}"]