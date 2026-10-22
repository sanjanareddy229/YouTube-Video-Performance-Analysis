#!/usr/bin/env bash
set -e

echo "=========================================================="
echo " YouTube Video Performance Big Data Pipeline Execution   "
echo "=========================================================="

# 1. Ensure dataset exists
if [ ! -f "data/youtube_trending_data.csv" ]; then
    echo "[1/4] Downloading dataset into data/..."
    mkdir -p data
    curl -L -o data/youtube_trending_data.csv "https://raw.githubusercontent.com/asukul/DS201/master/datasets/USvideos.csv"
else
    echo "[1/4] Dataset already present in data/."
fi

# 2. Build MapReduce JAR
echo "[2/4] Building Java MapReduce JAR with Maven..."
cd mapreduce
mvn clean package -DskipTests
cd ..

# 3. Execute MapReduce Job
echo "[3/4] Running MapReduce Category Aggregation Job..."
mkdir -p outputs/mapreduce_output
if command -v hadoop &> /dev/null; then
    echo "Hadoop installation detected. Running via Hadoop..."
    hadoop jar mapreduce/target/youtube-mapreduce-1.0.0.jar com.youtube.analysis.YoutubeAnalysisDriver data/youtube_trending_data.csv outputs/mapreduce_output
else
    echo "Running standalone Java MapReduce Engine..."
    java -cp "mapreduce/target/classes:mapreduce/target/test-classes" com.youtube.analysis.LocalMapReduceRunner
fi

# 4. Execute Hive Analytics
echo "[4/4] Generating Hive Analytical Result Tables..."
mkdir -p outputs/hive_results
if command -v hive &> /dev/null; then
    echo "Hive installation detected. Running HiveQL scripts..."
    hive -f hive/01_create_tables.hql
    hive -f hive/02_analysis_queries.hql
else
    echo "Running Hive Analytical Engine..."
    python3 hive/run_hive_simulation.py
fi

echo "=========================================================="
echo " Big Data Pipeline Completed Successfully!               "
echo " MapReduce Output: outputs/mapreduce_output/part-r-00000 "
echo " Hive Results    : outputs/hive_results/                 "
echo "=========================================================="
