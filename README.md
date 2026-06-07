# GapFinder: AI-Powered Research Gap IdentificatioArtificial Intelligence Semester Project (Assignment-2)

### University of Engineering and Technology, Taxila

### Software Engineering Department

---

### Submitted by

**(23-SE-57)**
**(23-SE-101)**

### Submitted to

**Dr. Kanwal Yousaf**
# GapFinder

**LLM-Based Agent for Automated Research Gap Identification** | Groq Llama 3 + Semantic Scholar

---

## What is GapFinder?

GapFinder automatically finds research gaps (unsolved problems) from academic papers. Enter a topic → get a ranked report of research gaps in 3-5 minutes.

---

## How It Works

```
User Input → Generate Queries → Fetch Papers → Analyze Each Paper → Find Patterns → Rank Gaps → Report
```

| Step | Module | What It Does |
|------|--------|---------------|
| 1 | query_formulator.py | Converts topic → search queries |
| 2 | paper_retriever.py | Fetches 20 papers from Semantic Scholar |
| 3 | per_paper_analyzer.py | Extracts methods, limitations, future work |
| 4 | synthesizer.py | Finds cross-paper patterns (Chain-of-Thought) |
| 5 | gps_scorer.py | Ranks gaps using GPS formula |
| 6 | report_generator.py | Creates GapFinder_Report.md |

---

## Setup (5 Minutes)

### 1. Prerequisites
- Python 3.10+
- Groq API Key (free from [console.groq.com](https://console.groq.com))

### 2. Install

```bash
git clone https://github.com/yourusername/GapFinder.git
cd GapFinder
pip install -r requirements.txt
```

### 3. Set API Key

Create `.env` file:
```
GROQ_API_KEY=your_key_here
```

### 4. Run

```bash
python main.py
```

---

## Usage Example

```bash
$ python main.py

Enter research topic: graph neural networks for drug discovery

[1/6] Generating queries... Done
[2/6] Fetching papers... 20 papers found
[3/6] Analyzing papers... Done
[4/6] Finding patterns... 14 gaps found
[5/6] Ranking gaps... Done
[6/6] Generating report... Done

✅ Report saved: GapFinder_Report.md
```

### Sample Output (Console)

```
TOP RESEARCH GAPS:
1. Changes in data sources pose risks to data quality (Score: 0.15)
2. Possible limitations of ML performance (Score: 0.15)
3. Dataset-bias of models used (Score: 0.075)
```

### Output File

`GapFinder_Report.md` contains: Executive Summary, Top Ranked Gaps with GPS Scores, Under-explored Methods, Dataset Limitations, Future Directions.

---

## GPS Formula

```
GPS = (Frequency / Total Papers) × Recency Weight × Specificity Score
```

| Factor | Range | Description |
|--------|-------|-------------|
| Frequency | 0-1 | Papers mentioning this gap |
| Recency | 1.0-1.5 | Higher for recent papers (last 2 years) |
| Specificity | 1-3 | Higher for technically specific gaps |

Higher GPS = Higher priority gap.

---

## Project Structure

```
GapFinder/
├── main.py                 # Run this
├── query_formulator.py     # Step 1
├── paper_retriever.py      # Step 2
├── per_paper_analyzer.py   # Step 3
├── synthesizer.py          # Step 4
├── gps_scorer.py           # Step 5
├── report_generator.py     # Step 6
├── requirements.txt        # Dependencies
├── .env                    # API key (create)
└── GapFinder_Report.md     # Output
```

---

## Requirements

```
groq>=0.9.0
requests>=2.31.0
python-dotenv>=1.0.0
```

---

## Limitations

- Analyzes **abstracts only** (not full text)
- Works best with **specific topics**
- Free-tier Llama 3 produces **broader gaps** than paid models



## `requirements.txt`

```txt
groq>=0.9.0
requests>=2.31.0
python-dotenv>=1.0.0
```

---

## `.env` (user creates)

```
GROQ_API_KEY=your_key_here
```

