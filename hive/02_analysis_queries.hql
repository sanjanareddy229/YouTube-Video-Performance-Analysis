-- ==============================================================
-- 02_analysis_queries.hql
-- Apache Hive Analytical Queries for Video Performance
-- ==============================================================

USE youtube_db;

-- --------------------------------------------------------------
-- Query 1: Top 10 Most Viewed Videos
-- --------------------------------------------------------------
INSERT OVERWRITE LOCAL DIRECTORY '/tmp/hive_top10_views'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 
    title,
    channel_title,
    category_name,
    views,
    likes,
    comment_count,
    engagement_rate_pct
FROM youtube_analytics
ORDER BY views DESC
LIMIT 10;

-- --------------------------------------------------------------
-- Query 2: Category Performance Breakdown
-- --------------------------------------------------------------
INSERT OVERWRITE LOCAL DIRECTORY '/tmp/hive_category_summary'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 
    category_name,
    COUNT(*) AS total_videos,
    SUM(views) AS total_views,
    SUM(likes) AS total_likes,
    SUM(comment_count) AS total_comments,
    ROUND(AVG(views), 0) AS avg_views,
    ROUND(AVG(likes), 0) AS avg_likes,
    ROUND(AVG(engagement_rate_pct), 2) AS avg_engagement_rate_pct
FROM youtube_analytics
GROUP BY category_name
ORDER BY total_views DESC;

-- --------------------------------------------------------------
-- Query 3: Top 10 Channels with Highest Aggregate Views
-- --------------------------------------------------------------
INSERT OVERWRITE LOCAL DIRECTORY '/tmp/hive_top_channels'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 
    channel_title,
    COUNT(*) AS video_count,
    SUM(views) AS total_views,
    SUM(likes) AS total_likes
FROM youtube_analytics
GROUP BY channel_title
ORDER BY total_views DESC
LIMIT 10;

-- --------------------------------------------------------------
-- Query 4: Highest Engagement Categories (Quality over Volume)
-- --------------------------------------------------------------
INSERT OVERWRITE LOCAL DIRECTORY '/tmp/hive_engagement_ranking'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 
    category_name,
    ROUND(AVG(engagement_rate_pct), 2) AS avg_engagement_pct,
    COUNT(*) AS video_count
FROM youtube_analytics
GROUP BY category_name
HAVING COUNT(*) > 50
ORDER BY avg_engagement_pct DESC;
