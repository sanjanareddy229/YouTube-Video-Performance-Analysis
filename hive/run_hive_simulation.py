import os
import pandas as pd

def run_hive_queries():
    data_path = "data/youtube_trending_data.csv"
    output_dir = "outputs/hive_results"
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    # Load dataset
    df = pd.read_csv(data_path, low_memory=False)

    # Clean numeric fields
    for col in ['views', 'likes', 'comment_count']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype('int64')

    # Category map matching Hive schema
    category_map = {
        1: "Film & Animation",
        2: "Autos & Vehicles",
        10: "Music",
        15: "Pets & Animals",
        17: "Sports",
        18: "Short Movies",
        19: "Travel & Events",
        20: "Gaming",
        21: "Videoblogging",
        22: "People & Blogs",
        23: "Comedy",
        24: "Entertainment",
        25: "News & Politics",
        26: "Howto & Style",
        27: "Education",
        28: "Science & Technology",
        29: "Nonprofits & Activism",
        30: "Movies",
        43: "Shows"
    }

    df['category_id'] = pd.to_numeric(df['category_id'], errors='coerce').fillna(0).astype(int)
    df['category_name'] = df['category_id'].map(category_map).fillna("Other")

    # Safe engagement rate calculation
    safe_views = df['views'].apply(lambda v: v if v > 0 else 1)
    df['engagement_rate_pct'] = ((df['likes'] + df['comment_count']) / safe_views) * 100
    df['engagement_rate_pct'] = df['engagement_rate_pct'].round(2)

    # -------------------------------------------------------------
    # Query 1: Top 10 Most Viewed Videos
    # -------------------------------------------------------------
    q1 = df[['title', 'channel_title', 'category_name', 'views', 'likes', 'comment_count', 'engagement_rate_pct']] \
        .sort_values(by='views', ascending=False).head(10)
    q1.to_csv(os.path.join(output_dir, "hive_top10_views.tsv"), sep="\t", index=False)
    print("Saved: hive_top10_views.tsv")

    # -------------------------------------------------------------
    # Query 2: Category Performance Breakdown
    # -------------------------------------------------------------
    q2 = df.groupby('category_name').agg(
        total_videos=('title', 'count'),
        total_views=('views', 'sum'),
        total_likes=('likes', 'sum'),
        total_comments=('comment_count', 'sum'),
        avg_views=('views', 'mean'),
        avg_likes=('likes', 'mean'),
        avg_engagement_pct=('engagement_rate_pct', 'mean')
    ).reset_index().sort_values(by='total_views', ascending=False)
    q2['avg_views'] = q2['avg_views'].round(0).astype('int64')
    q2['avg_likes'] = q2['avg_likes'].round(0).astype('int64')
    q2['avg_engagement_pct'] = q2['avg_engagement_pct'].round(2)
    q2.to_csv(os.path.join(output_dir, "hive_category_summary.tsv"), sep="\t", index=False)
    print("Saved: hive_category_summary.tsv")

    # -------------------------------------------------------------
    # Query 3: Top 10 Channels by Aggregate Views
    # -------------------------------------------------------------
    q3 = df.groupby('channel_title').agg(
        video_count=('title', 'count'),
        total_views=('views', 'sum'),
        total_likes=('likes', 'sum')
    ).reset_index().sort_values(by='total_views', ascending=False).head(10)
    q3.to_csv(os.path.join(output_dir, "hive_top_channels.tsv"), sep="\t", index=False)
    print("Saved: hive_top_channels.tsv")

    # -------------------------------------------------------------
    # Query 4: Highest Engagement Categories (Quality Ranking)
    # -------------------------------------------------------------
    q4 = q2[q2['total_videos'] > 50][['category_name', 'avg_engagement_pct', 'total_videos']] \
        .sort_values(by='avg_engagement_pct', ascending=False)
    q4.to_csv(os.path.join(output_dir, "hive_engagement_ranking.tsv"), sep="\t", index=False)
    print("Saved: hive_engagement_ranking.tsv")

    print("\nALL HIVE ANALYTICAL QUERY RESULTS GENERATED SUCCESSFULLY!")

if __name__ == "__main__":
    run_hive_queries()
