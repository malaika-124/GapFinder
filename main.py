"""
GapFinder - Working Version
"""

import os
import time
import requests
import json
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: No API key found in .env file")
    exit()

# Setup Gemini (using the old package - still works)
import google.generativeai as genai
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

print("\n" + "="*50)
print("GAPFINDER - Research Gap Identification")
print("="*50)

# Get topic
topic = input("\n📌 Enter research topic: ")

if not topic:
    print("No topic entered")
    exit()

print(f"\n🔍 Searching for papers on: {topic}")

# Search for papers with retry logic
max_retries = 3
papers = []

for attempt in range(max_retries):
    try:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": topic,
            "limit": 10,
            "fields": "title,abstract,year,citationCount"
        }
        
        print(f"   Attempt {attempt + 1}/{max_retries}...")
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            papers = data.get("data", [])
            print(f"   ✓ Found {len(papers)} papers")
            break
        elif response.status_code == 429:
            print(f"   ⚠️ Rate limited (429). Waiting 10 seconds...")
            time.sleep(10)
        else:
            print(f"   ⚠️ Error {response.status_code}")
            time.sleep(5)
            
    except Exception as e:
        print(f"   ⚠️ Error: {e}")
        time.sleep(5)

if not papers:
    print("\n❌ No papers found. Please try:")
    print("   1. Wait 1 minute and try again")
    print("   2. Use a different topic")
    print("   3. Check your internet connection")
    exit()

print(f"\n📚 Analyzing {len(papers)} papers...")
print("-" * 50)

# Analyze each paper
gaps = []

for i, paper in enumerate(papers, 1):
    title = paper.get("title", "Unknown Title")
    abstract = paper.get("abstract", "Abstract not available")
    year = paper.get("year", "Unknown year")
    
    print(f"\n[{i}/{len(papers)}] {title[:60]}... ({year})")
    
    # Skip if abstract is missing
    if not abstract or abstract == "":
        gaps.append({
            "title": title,
            "year": year,
            "gap": "Abstract not available to analyze"
        })
        continue
    
    # Create prompt for Gemini
    prompt = f"""
You are analyzing a research paper. Find ONE research gap or limitation.

PAPER TITLE: {title}
YEAR: {year}
ABSTRACT: {abstract}

Answer with EXACTLY ONE SENTENCE describing a gap, limitation, or future work needed.

Example answers:
- "The model was only tested on small datasets, leaving scalability unproven."
- "No comparison with state-of-the-art methods was performed."
- "The approach cannot handle real-world noisy data."

YOUR ANSWER (one sentence only):
"""
    
    try:
        response = model.generate_content(prompt)
        gap_text = response.text.strip()
        
        # Clean up the response
        gap_text = gap_text.replace('\n', ' ').strip()
        
        gaps.append({
            "title": title,
            "year": year,
            "gap": gap_text
        })
        print(f"   ✓ Gap identified")
        
    except Exception as e:
        print(f"   ⚠️ Analysis failed: {e}")
        gaps.append({
            "title": title,
            "year": year,
            "gap": f"Could not analyze (error: {str(e)[:50]})"
        })
    
    # Wait to avoid rate limits
    time.sleep(2)

# Generate report
print("\n" + "="*50)
print("📝 Generating Report...")
print("="*50)

report = f"""# Research Gap Report

## Topic
**{topic}**

## Date
{time.strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- **Papers Analyzed:** {len(papers)} papers
- **Total Gaps Identified:** {len([g for g in gaps if g['gap'] and 'Could not analyze' not in g['gap']])}

---

## Research Gaps Identified

"""

for i, gap in enumerate(gaps, 1):
    if 'Could not analyze' in gap['gap']:
        continue
    report += f"""
### Gap {i}: {gap['title']} ({gap['year']})

**Identified Gap:**
> {gap['gap']}

---"""

report += f"""

## Complete Paper List

| # | Paper Title | Year | Gap Identified |
|---|-------------|------|----------------|
"""
for i, gap in enumerate(gaps, 1):
    gap_preview = gap['gap'][:80] + "..." if len(gap['gap']) > 80 else gap['gap']
    report += f"| {i} | {gap['title'][:60]} | {gap['year']} | {gap_preview} |\n"

report += f"""

## Methodology

GapFinder identified research gaps by:
1. Retrieving relevant papers from Semantic Scholar API
2. Analyzing each paper's abstract using Gemini LLM
3. Extracting stated limitations, missing components, and future work suggestions
4. Consolidating findings into this report

## How to Use These Gaps

Each identified gap represents a potential research direction. Choose gaps that:
- Align with your expertise
- Have high practical impact
- Are feasible within your timeframe

---

*Report generated by GapFinder - AI-powered Research Gap Identification Tool*
"""

# Save report
report_file = "GapFinder_Final_Report.md"
with open(report_file, "w", encoding="utf-8") as f:
    f.write(report)

print(f"\n✅ REPORT SAVED: {report_file}")
print("\n" + "="*50)
print("TOP RESEARCH GAPS FOUND:")
print("="*50)

# Show top gaps
gap_count = 0
for gap in gaps:
    if 'Could not analyze' not in gap['gap'] and gap_count < 5:
        gap_count += 1
        print(f"\n{gap_count}. {gap['title'][:70]}")
        print(f"   → {gap['gap'][:150]}...")

if gap_count == 0:
    print("\n   No gaps were successfully identified.")
    print("   Try running again with a different topic.")

print("\n" + "="*50)
print("✅ DONE! Open the .md file to see full report.")
print("="*50)