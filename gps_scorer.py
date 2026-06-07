"""
GPS Scorer - Step 5 of GapFinder pipeline
Calculates Gap Priority Scores for ranking
"""

class GPSScorer:
    def __init__(self):
        pass
    
    def score_and_rank(self, gaps, papers_data):
        """
        Calculate GPS for each gap and rank them
        
        GPS = (Frequency/N) × Recency Weight × Specificity Score
        """
        if not gaps:
            return []
        
        # Create mapping from title to year
        paper_info = {}
        for p in papers_data:
            title = p.get('title', '')
            year = p.get('year', 0)
            paper_info[title] = year
        
        current_year = 2024
        
        for gap in gaps:
            # Calculate frequency (how many papers mention this gap)
            supporting_titles = gap.get('supporting_papers', [])
            frequency = len(supporting_titles)
            N = len(papers_data)
            
            if N == 0:
                freq_score = 0
            else:
                freq_score = frequency / N
            
            # Calculate recency weight (newer papers get higher weight)
            recent_count = 0
            for title in supporting_titles:
                year = paper_info.get(title, 0)
                if year >= current_year - 2:
                    recent_count += 1
            
            if len(supporting_titles) > 0:
                recency_weight = 1.0 + (0.5 * (recent_count / len(supporting_titles)))
            else:
                recency_weight = 1.0
            
            # Calculate specificity score (1-3)
            specificity_score = self._calculate_specificity(gap.get('description', ''))
            
            # Calculate final GPS
            gap['gps_score'] = round(freq_score * recency_weight * specificity_score, 3)
            gap['frequency'] = frequency
            gap['recency_weight'] = round(recency_weight, 2)
            gap['specificity_score'] = specificity_score
        
        # Sort by GPS score (highest first)
        ranked_gaps = sorted(gaps, key=lambda x: x.get('gps_score', 0), reverse=True)
        
        return ranked_gaps
    
    def _calculate_specificity(self, description):
        """Calculate how specific the gap description is (1-3)"""
        description_lower = description.lower()
        
        # Check for specific technical terms
        technical_terms = ['gnn', 'transformer', 'cnn', 'rnn', 'lstm', 'bert', 
                          'gpt', 'attention', 'graph', 'neural', 'deep learning']
        
        # Check for dataset terms
        dataset_terms = ['dataset', 'bindingdb', 'chembl', 'pubmed', 'imagenet',
                        'benchmark', 'corpus', 'knowledge graph']
        
        # Check for action terms
        action_terms = ['combine', 'apply', 'evaluate', 'compare', 'integrate',
                       'develop', 'create', 'design', 'propose']
        
        has_technical = any(term in description_lower for term in technical_terms)
        has_dataset = any(term in description_lower for term in dataset_terms)
        has_action = any(term in description_lower for term in action_terms)
        
        if has_technical and has_dataset and has_action:
            return 3  # Very specific - method + dataset + action
        elif (has_technical and has_dataset) or (has_technical and has_action):
            return 2  # Moderately specific
        else:
            return 1  # Vague/general