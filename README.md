# 💍 Feedback Hub – Customer Sentiment Analyzer (Assignment Solution)

This repository contains the solution for the **Customer Feedback Analyzer with Sentiment Dashboard** assignment.  
It is a full-stack application built for **Giva** to collect, analyze, and visualize customer reviews using a **rule-based logic engine (no external AI/ML models)**, strictly following the assignment guidelines.

---

## 📋 Logic Explanation (Mandatory for Submission)

As required in **Task A2** and **Task B3**, this system uses **deterministic, rule-based logic** instead of machine learning or external AI services.

---

### 1. Sentiment Engine (Task A2)

**Approach:**  
Bag-of-Words (Keyword Counting)

**Logic:**  
- Each review is converted to lowercase and tokenized into words.
- Words are compared against two predefined lists:
  - `POSITIVE_WORDS` → shiny, elegant, beautiful, perfect, amazing, good
  - `NEGATIVE_WORDS` → tarnish, broken, dull, bad, fragile, poor

**Decision Rule:**
- If **Positive Count > Negative Count** → **Positive**
- If **Negative Count > Positive Count** → **Negative**
- Else → **Neutral**

This logic is simple, explainable, and fully compliant with the “no external AI” constraint.

---

### 2. Theme Detection (Task A3)

**Approach:**  
Keyword Mapping (Multi-label Classification)

**Logic:**  
Each review is scanned for predefined keywords to classify it into one or more themes:

- **Comfort:** light, heavy, fit, wearable  
- **Durability:** broke, broken, strong, quality, fragile  
- **Appearance:** shiny, dull, design, polish, elegant  

A single review may belong to multiple themes if multiple keyword groups are matched.

---

### 3. Insight Generator (Task B3)

**Approach:**  
Threshold-Based Heuristics

**Logic:**  
Instead of showing raw statistics alone, the system generates **actionable insights** using fixed thresholds:

- **“Improve durability”**  
  Triggered if more than **30%** of reviews mention durability-related keywords.

- **“Consider lighter designs”**  
  Triggered if more than **30%** of reviews mention comfort-related keywords.

- **“Critical Sentiment Warning”**  
  Triggered if the number of **negative reviews exceeds positive reviews**.

These insights are dynamically generated on the dashboard.

---

## 🚀 Features Mapped to Assignment Tasks

### 🔹 Part A: Backend (FastAPI + SQLite)

- ✅ **Task A1 – Feedback APIs**  
  REST endpoints to submit feedback and fetch dashboard statistics.

- ✅ **Task A2 – Sentiment Engine**  
  Rule-based sentiment classification without external AI libraries.

- ✅ **Task A3 – Theme Detection**  
  Keyword-based categorization into Comfort, Durability, and Appearance.

---

### 🔹 Part B: Frontend (HTML, CSS, JavaScript)

- ✅ **Task B1 – Feedback Submission Form**  
  Inputs for Product ID, Rating (1–5), and Review Text.

- ✅ **Task B2 – Sentiment Dashboard**  
  Pie chart visualization for sentiment and theme counts using Chart.js.  
  Dashboard auto-refreshes after submission.

- ✅ **Task B3 – Insights Display**  
  Actionable insights dynamically shown based on backend analysis.

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy  
- **Database:** SQLite (File-based, no setup required)  
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API)  
- **Visualization:** Chart.js  

---

## 🔧 Setup & Execution

### 1. Prerequisites

Ensure **Python 3.8+** is installed.

---

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install fastapi uvicorn sqlalchemy
