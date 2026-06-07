class GPSScorer:
    def __init__(self):
        pass
    
    def score_and_rank(self, gaps, papers_data):
        if not gaps:
            return []
        
        paper_info = {}
        for p in papers_data:
            title = p.get("title", "")
            year = p.get("year", 0)
            try:
                paper_info[title] = int(year)
            except:
                paper_info[title] = 2024
        
        current_year = 2024
        
        for gap in gaps:
            supporting_titles = gap.get("supporting_papers", [])
            frequency = len(supporting_titles)
            N = len(papers_data)
            freq_score = frequency / N if N > 0 else 0
            
            recent_count = 0
            for title in supporting_titles:
                year = paper_info.get(title, 2024)
                if year >= current_year - 2:
                    recent_count += 1
            
            recency_weight = 1.0 + (0.5 * (recent_count / len(supporting_titles))) if supporting_titles else 1.0
            specificity_score = self._calculate_specificity(gap.get("description", ""))
            gap["gps_score"] = round(freq_score * recency_weight * specificity_score, 3)
            gap["frequency"] = frequency
        
        return sorted(gaps, key=lambda x: x.get("gps_score", 0), reverse=True)
    
    def _calculate_specificity(self, description):
        desc = description.lower()
        technical = ["gnn", "transformer", "cnn", "rnn", "lstm", "bert", "attention", "graph", "neural"]
        dataset = ["dataset", "benchmark", "corpus"]
        action = ["combine", "apply", "evaluate", "compare", "integrate", "develop"]
        
        has_technical = any(t in desc for t in technical)
        has_dataset = any(d in desc for d in dataset)
        has_action = any(a in desc for a in action)
        
        if has_technical and has_dataset and has_action:
            return 3
        elif (has_technical and has_dataset) or (has_technical and has_action):
            return 2
        else:
            return 1
