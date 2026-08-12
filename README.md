# 🏛️ Municipal Complaint Intelligence

An end-to-end data engineering and analytics system built to analyze municipal 311 service requests, evaluate SLA compliance, identify operational bottlenecks, and map geographic complaint clusters across New York City.

---

## 🛠️ Tech Stack & Tools Used
* **Language:** Python 3.12+
* **Data Processing:** Pandas, NumPy
* **Database & SQL:** SQLite, Window Functions (`RANK`), Aggregations (`CASE`, `HAVING`)
* **Data Visualization:** Matplotlib, Seaborn, Folium (Leaflet Interactive Maps)
* **Text Mining / NLP:** Scikit-Learn (`TfidfVectorizer`), N-Grams

---

## 📁 Project Architecture

```text
municipal-complaint-intelligence/
├── data/
│   ├── raw/                   # Original sample 311 CSV dataset
│   ├── processed/             # Cleaned dataset & exported summary tables
│   └── municipal_complaints.db# SQLite Database File
├── src/
│   ├── data_loader.py         # Pipeline for raw data loading & audit
│   ├── data_cleaner.py        # Data cleaning, null handling, datetime parsing
│   ├── eda.py                 # EDA chart generation script
│   ├── nlp_analysis.py        # TF-IDF keyword extraction
│   ├── analysis.py           # SLA breach & operational breakdown
│   ├── geo_analysis.py       # Folium map generation
│   └── db_analysis.py        # SQLite loader & SQL query engine
├── reports/
│   ├── figures/               # Saved charts (PNG format)
│   ├── nyc_complaint_heatmap.html # Interactive Folium heatmap
│   ├── sla_breach_hotspots.html  # Interactive Folium breach clusters
│   └── EXECUTIVE_SUMMARY.md   # Final business insights report
├── sql/
│   └── analysis_queries.sql   # Documented analytical SQL queries
├── requirements.txt           # Python dependencies
└── README.md                  # Portfolio documentation