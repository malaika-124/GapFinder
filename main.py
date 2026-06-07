"""
GapFinder - Main File
Uses Groq (FREE) + Semantic Scholar (FREE)
Just run:  python main.py
"""

import os, sys, time
from groq import Groq
from dotenv import load_dotenv

# Load key from .env file
load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_KEY:
    print("="*50)
    print("ERROR: No Groq API key found!")
    print("="*50)
    print("\nSteps to fix:")
    print("1. Go to:  https://console.groq.com/keys")
    print("2. Sign up FREE and create an API key")
    print("3. Create a file named  .env  in this folder")
    print("4. Paste this inside it:")
    print("   GROQ_API_KEY=your_key_here")
    print("5. Run again: python main.py")
    sys.exit()

# ── Wrapper so all your modules work without any changes ─────────────────────
# Your modules call:  model.generate_content(prompt)
# This wrapper makes Groq look exactly the same

client = Groq(api_key=GROQ_KEY)

class GroqWrapper:
    def generate_content(self, prompt):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",   # free Groq model
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.3,
            )
            text = response.choices[0].message.content
            # Return object with .text attribute — same as Gemini
            return type("R", (), {"text": text})()
        except Exception as e:
            print(f"   Groq error: {e}")
            return type("R", (), {"text": ""})()

model = GroqWrapper()

# ── Import your 6 pipeline modules ───────────────────────────────────────────
from query_formulator   import QueryFormulator
from paper_retriever    import PaperRetriever
from per_paper_analyzer import PerPaperAnalyzer
from synthesizer        import Synthesizer
from gps_scorer         import GPSScorer
from report_generator   import ReportGenerator

# ── Start ─────────────────────────────────────────────────────────────────────
print("\n" + "="*55)
print("  GAPFINDER - Research Gap Identification")
print("  FREE  |  Groq (Llama 3) + Semantic Scholar")
print("="*55)

topic = input("\nEnter your research topic: ").strip()
if not topic:
    print("No topic entered.")
    sys.exit()

# STEP 1 ── Query Formulation
print("\n[1/6] Generating search queries...")
queries = QueryFormulator(model).formulate(topic)
print(f"      Done — {len(queries)} queries")

# STEP 2 ── Paper Retrieval
print("\n[2/6] Fetching papers from Semantic Scholar...")
papers = PaperRetriever().retrieve(queries, num_papers=20)
print(f"      Done — {len(papers)} papers found")

if not papers:
    print("\nNo papers found. Try a broader topic.")
    sys.exit()

# STEP 3 ── Per-Paper Analysis
print("\n[3/6] Analyzing each paper...")
analyzed = PerPaperAnalyzer(model).analyze_batch(papers)
print(f"\n      Done — {len(analyzed)} papers analyzed")

# STEP 4 ── Synthesis
print("\n[4/6] Finding patterns across all papers...")
gaps = Synthesizer(model).synthesize(analyzed)
print(f"      Done — {len(gaps)} gap candidates found")

# STEP 5 ── GPS Scoring
print("\n[5/6] Ranking gaps by priority score...")
ranked = GPSScorer().score_and_rank(gaps, analyzed)
print(f"      Done — gaps ranked")

# STEP 6 ── Report
print("\n[6/6] Writing final report...")
report = ReportGenerator(model).generate(topic, ranked, analyzed)

filename = "GapFinder_Report.md"
with open(filename, "w", encoding="utf-8") as f:
    f.write(report)
print(f"      Done — saved as  {filename}")

# ── Show results ──────────────────────────────────────────────────────────────
print("\n" + "="*55)
print("  TOP RESEARCH GAPS")
print("="*55)
for i, g in enumerate(ranked[:5], 1):
    print(f"\n{i}. {g.get('description','')[:80]}")
    print(f"   Score: {g.get('gps_score', 0)}")

print("\n" + "="*55)
print(f"  Report saved:  {filename}")
print("="*55)
