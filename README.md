# YouTube Video Performance Analysis using Big Data Technologies

## Project Overview
This project performs an end-to-end performance analysis of YouTube trending video metrics using modern Big Data analytics tools and interactive visualization frameworks. The system processes video interaction metrics (views, likes, comments, engagement rates, category popularity) to discover key viewer engagement trends.

---

## Objectives
1. **Data Ingestion & Storage:** Store raw, semi-structured YouTube metadata in Hadoop Distributed File System (HDFS).
2. **Batch Processing:** Implement Java MapReduce algorithms to calculate category aggregate statistics (total views, average likes, top performers).
3. **Structured Querying:** Utilize Apache Hive to create schemas, partition data, and execute analytical SQL (HQL) queries.
4. **Data Transformation & ETL:** Utilize Apache Pig Latin scripts to clean, filter, and extract high-engagement video records.
5. **Interactive Dashboard:** Build an interactive visual analytics dashboard using Python, Streamlit, Pandas, and Plotly for real-time exploratory analysis.

---

## Technology Stack
- **Operating System:** Windows 11 (64-bit)
- **Programming & Scripting:** Python 3.13, Java 17, Pig Latin, HiveQL
- **Big Data Ecosystem:**
  - Apache Hadoop (HDFS & MapReduce)
  - Apache Hive (Data Warehousing & SQL Analytics)
  - Apache Pig (Dataflow scripting)
- **Analytics & Dashboard:**
  - Streamlit (Web UI)
  - Pandas (Data manipulation & cleaning)
  - Plotly Express / Graph Objects (Interactive visualizations)

---

## Project Structure
```text
YouTube-Video-Performance-Analysis/
├── data/                 # Raw and cleaned CSV datasets
├── dashboard/            # Streamlit dashboard application (app.py)
├── mapreduce/            # Java MapReduce driver, mapper, and reducer code
├── hive/                 # Hive HQL queries and table definitions
├── pig/                  # Pig Latin scripts (.pig)
├── outputs/              # Output reports, query results, and MR outputs
├── docs/                 # Documentation and project reports
├── screenshots/          # Proof-of-work screenshots for CBP review
├── requirements.txt      # Python dependencies for the dashboard
└── README.md             # Project documentation
```

---

## Planned Execution Steps
1. **Phase 1: Environment Inspection & Project Setup** (Completed)
   - Inspect local environment, directory creation, baseline documentation.
2. **Phase 2: Interactive Analytics Dashboard**
   - Acquire/prepare the YouTube dataset in `data/`.
   - Build Streamlit dashboard with summary KPIs, Top 10 rankings, category breakdowns, and engagement metrics.
3. **Phase 3: Java MapReduce Implementation**
   - Build Mapper, Reducer, and Driver classes to aggregate views and engagement by category.
4. **Phase 4: Apache Hive Data Warehousing**
   - Define Hive external tables, load data, run analytical HQL queries, and export results to `outputs/`.
5. **Phase 5: Apache Pig Transformation**
   - Execute Pig Latin scripts to filter top viral videos and compute engagement ratios.
