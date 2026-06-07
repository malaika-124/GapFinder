
# GapFinder: AI-Powered Research Gap Identification Tool

**Artificial Intelligence Semester Project (Assignment-2)**  
**University of Engineering and Technology, Taxila**  
**Software Engineering Department**

---

### **Submitted by:**
(23-SE-57)  
(23-SE-101)

### **Submitted to:**  
Dr. Kanwal Yousaf

---

## 📋 Project Overview

**GapFinder** is a smart **task-oriented AI agent** that automatically identifies research gaps from scientific literature.  

You simply enter a research topic in natural language, and the system:
- Retrieves relevant academic papers using real APIs
- Analyzes each paper using Large Language Models (Gemini)
- Performs cross-paper synthesis using Chain-of-Thought
- Ranks the gaps using **Gap Priority Score (GPS)**
- Generates a professional, well-formatted research report

This is the **complete working implementation** of the Research Gap Identification Assistant proposed in **Assignment-1**.

---

## ✨ Key Features

- Real-time paper retrieval from Semantic Scholar and arXiv
- Multi-agent architecture with 6 specialized agents
- Structured JSON analysis of paper abstracts
- Cross-document gap synthesis
- Intelligent Gap Priority Score (GPS) ranking
- Professional Markdown and HTML report generation
- Robust fallback mechanisms when APIs are slow or unavailable

---

## 🛠 Technology Stack

- **Programming Language:** Python 3
- **Primary LLM:** Google Gemini 1.5 Flash
- **Fallback LLM:** Groq Llama-3.3
- **APIs:** Semantic Scholar API, arXiv API
- **Libraries:** requests, google-generativeai, python-dotenv, etc.

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/GapFinder.git
cd GapFinder
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add Gemini API Key
Create a new file named `.env` in the main folder and paste:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
Get free key from: https://aistudio.google.com/app/apikey

### 4. Run the Tool
```bash
python main.py
```

---

## 📁 Project Structure

```
GapFinder/
├── main.py                    # Main program
├── query_formulator.py
├── paper_retriever.py
├── per_paper_analyzer.py
├── synthesizer.py
├── gps_scorer.py
├── report_generator.py
├── arxiv_gapfinder.py
├── final.py
├── requirements.txt
├── FINAL_REPORT.md
├── GapFinder_arXiv_Report.md
├── GapFinder_Dynamic_Report.html
└── README.md
```

---

## 📊 Sample Reports

- `FINAL_REPORT.md` → Generated using Groq LLM
- `GapFinder_arXiv_Report.md` → Generated using arXiv API
- `GapFinder_Dynamic_Report.html` → Beautiful HTML version

---

## 📄 Assignment Documents

- Full **Assignment-2 Research Paper** (PDF) is included
- All source code files and generated reports are provided
- This project fully implements the proposal from Assignment-1

---



## 🛠 Future Work

- Support for full-text PDF analysis
- Web-based user interface
- Integration with more academic databases
- Citation network analysis for better gap validation

---

**Thank You!**  


**Now paste the above text into your `README.md` file on GitHub.**

After pasting, reply with **"Done"** and I will give you the full detailed research paper.
