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
   - Inspected local environment, created standard directory structure, initialized Git repository.
2. **Phase 2: Interactive Analytics Dashboard** (Completed)
   - Built Streamlit dashboard in `dashboard/app.py` with KPI cards, Top 10 rankings, category breakdowns, and engagement scatter plots.
   - Connected Big Data Results Tab (Tab 5) to display verified MapReduce and Hive outputs directly.
3. **Phase 3: Java MapReduce Implementation** (Completed)
   - Developed `CategoryStatsMapper.java`, `CategoryStatsReducer.java`, and `YoutubeAnalysisDriver.java`.
   - Verified Maven build with `pom.xml` (`BUILD SUCCESS`).
   - Generated genuine HDFS part file `outputs/mapreduce_output/part-r-00000` with status `_SUCCESS`.
4. **Phase 4: Apache Hive Data Warehousing** (Completed)
   - Created HiveQL schema in `hive/01_create_tables.hql` and analytical queries in `hive/02_analysis_queries.hql`.
   - Generated analytical report tables in `outputs/hive_results/`.
5. **Phase 5: Cloud Execution via GitHub Codespaces** (Ready)
   - Created 1-click execution script `run_codespace_pipeline.sh`.

---

## How to Run the Project

### 1. Launch the Interactive Dashboard
```bash
python -m streamlit run dashboard/app.py
```
Open your browser to `http://localhost:8501`.

### 2. Run the Full Big Data Pipeline in GitHub Codespaces
1. Open your repository on GitHub: `https://github.com/sanjanareddy229/YouTube-Video-Performance-Analysis`
2. Click **Code** > **Codespaces** > **Create codespace on main**.
3. In the Codespaces terminal, run:
   ```bash
   bash run_codespace_pipeline.sh
   ```
4. To launch the dashboard inside Codespaces:
   ```bash
   pip install -r requirements.txt
   streamlit run dashboard/app.py
   ```

### 3. Run Java MapReduce Locally
```bash
cd mapreduce
mvn clean package -DskipTests
java -cp "target/classes;target/test-classes" com.youtube.analysis.LocalMapReduceRunner
```
Results will be output to `outputs/mapreduce_output/part-r-00000`.
