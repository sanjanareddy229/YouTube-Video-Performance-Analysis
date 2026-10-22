-- ==============================================================
-- 01_create_tables.hql
-- Apache Hive Schema Definitions for YouTube Video Performance Analysis
-- ==============================================================

CREATE DATABASE IF NOT EXISTS youtube_db;
USE youtube_db;

-- 1. Raw External Table mapped directly to HDFS CSV data
DROP TABLE IF EXISTS youtube_raw;

CREATE EXTERNAL TABLE IF NOT EXISTS youtube_raw (
    video_id STRING,
    trending_date STRING,
    title STRING,
    channel_title STRING,
    category_id INT,
    publish_time STRING,
    tags STRING,
    views BIGINT,
    likes BIGINT,
    dislikes BIGINT,
    comment_count BIGINT,
    thumbnail_link STRING,
    comments_disabled BOOLEAN,
    ratings_disabled BOOLEAN,
    video_error_or_removed BOOLEAN,
    description STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ",",
    "quoteChar"     = "\"",
    "escapeChar"    = "\\"
)
STORED AS TEXTFILE
LOCATION '/youtube/data'
TBLPROPERTIES ("skip.header.line.count"="1");

-- 2. Cleaned Analytical ORC Table with Category Name Mapping
DROP TABLE IF EXISTS youtube_analytics;

CREATE TABLE youtube_analytics STORED AS ORC AS
SELECT 
    video_id,
    title,
    channel_title,
    category_id,
    CASE category_id
        WHEN 1 THEN 'Film & Animation'
        WHEN 2 THEN 'Autos & Vehicles'
        WHEN 10 THEN 'Music'
        WHEN 15 THEN 'Pets & Animals'
        WHEN 17 THEN 'Sports'
        WHEN 18 THEN 'Short Movies'
        WHEN 19 THEN 'Travel & Events'
        WHEN 20 THEN 'Gaming'
        WHEN 21 THEN 'Videoblogging'
        WHEN 22 THEN 'People & Blogs'
        WHEN 23 THEN 'Comedy'
        WHEN 24 THEN 'Entertainment'
        WHEN 25 THEN 'News & Politics'
        WHEN 26 THEN 'Howto & Style'
        WHEN 27 THEN 'Education'
        WHEN 28 THEN 'Science & Technology'
        WHEN 29 THEN 'Nonprofits & Activism'
        WHEN 30 THEN 'Movies'
        WHEN 43 THEN 'Shows'
        ELSE 'Other'
    END AS category_name,
    CAST(views AS BIGINT) AS views,
    CAST(likes AS BIGINT) AS likes,
    CAST(comment_count AS BIGINT) AS comment_count,
    ROUND(((CAST(likes AS BIGINT) + CAST(comment_count AS BIGINT)) / IF(CAST(views AS BIGINT) > 0, CAST(views AS BIGINT), 1)) * 100, 2) AS engagement_rate_pct
FROM youtube_raw
WHERE views IS NOT NULL AND CAST(views AS BIGINT) > 0;
