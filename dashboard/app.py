import os
import glob
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="YouTube Video Performance Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Category ID Mapping (Standard YouTube Dataset)
# ---------------------------------------------------------
CATEGORY_MAP = {
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
    43: "Shows",
    44: "Trailers"
}

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def format_number(num):
    """Format large numbers for KPI display (K, M, B)."""
    if pd.isna(num):
        return "0"
    num = float(num)
    if abs(num) >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    elif abs(num) >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    elif abs(num) >= 1_000:
        return f"{num / 1_000:.2f}K"
    else:
        return f"{num:,.0f}"

@st.cache_data(show_spinner=True)
def load_and_clean_data(file_path):
    """Load, validate, and clean the YouTube dataset safely."""
    if not os.path.exists(file_path):
        return None

    try:
        # Load CSV
        df = pd.read_csv(file_path, low_memory=False)
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return None

    # Standardize column names (lowercase and strip)
    df.columns = [col.strip().lower() for col in df.columns]

    # Required column aliases / fallbacks
    col_mapping = {
        'view_count': 'views',
        'like_count': 'likes',
        'dislike_count': 'dislikes',
        'comment_total': 'comment_count'
    }
    df.rename(columns=col_mapping, inplace=True)

    # Ensure essential columns exist
    for col in ['views', 'likes', 'comment_count']:
        if col not in df.columns:
            df[col] = 0
        else:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    if 'dislikes' in df.columns:
        df['dislikes'] = pd.to_numeric(df['dislikes'], errors='coerce').fillna(0)
    else:
        df['dislikes'] = 0

    # Ensure title and channel exist
    if 'title' not in df.columns:
        df['title'] = "Unknown Title"
    else:
        df['title'] = df['title'].fillna("Unknown Title").astype(str)

    if 'channel_title' not in df.columns:
        df['channel_title'] = "Unknown Channel"
    else:
        df['channel_title'] = df['channel_title'].fillna("Unknown Channel").astype(str)

    # Map category names if category_id exists
    if 'category_id' in df.columns:
        df['category_id'] = pd.to_numeric(df['category_id'], errors='coerce').fillna(0).astype(int)
        df['category_name'] = df['category_id'].map(CATEGORY_MAP).fillna("Other / Unknown")
    elif 'category' in df.columns:
        df['category_name'] = df['category'].fillna("Other / Unknown").astype(str)
    else:
        df['category_name'] = "General"

    # Compute engagement metrics safely (avoid divide-by-zero)
    safe_views = df['views'].apply(lambda v: v if v > 0 else 1)
    df['like_rate_pct'] = (df['likes'] / safe_views) * 100
    df['comment_rate_pct'] = (df['comment_count'] / safe_views) * 100
    df['engagement_rate_pct'] = ((df['likes'] + df['comment_count']) / safe_views) * 100

    return df

# ---------------------------------------------------------
# Main Application
# ---------------------------------------------------------
def main():
    st.title("📹 YouTube Video Performance Analysis")
    st.markdown("##### Big Data Analytics & Interactive Visualization Dashboard")
    st.markdown("---")

    # Locate CSV file
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    csv_candidates = glob.glob(os.path.join(data_dir, "*.csv"))

    if not csv_candidates:
        # Fallback to local data folder check
        csv_candidates = glob.glob("data/*.csv")

    if not csv_candidates:
        st.warning("⚠️ No CSV dataset found in the `data/` folder.")
        st.info("Please place your YouTube CSV dataset inside the `data/` directory (e.g., `data/youtube_trending_data.csv`).")
        return

    # Sidebar Data Source Selector & Filters
    st.sidebar.header("⚙️ Configuration & Filters")
    selected_file = st.sidebar.selectbox("Select Dataset File", options=csv_candidates, index=0)

    # Load data
    df = load_and_clean_data(selected_file)

    if df is None or df.empty:
        st.error("The selected dataset could not be loaded or is empty.")
        return

    # Category Multi-Select Filter
    categories = sorted(df['category_name'].unique().tolist())
    selected_categories = st.sidebar.multiselect(
        "Filter by Category",
        options=categories,
        default=categories
    )

    # Search Filter
    search_query = st.sidebar.text_input("🔍 Search Video Title or Channel", value="").strip().lower()

    # Apply Filters
    filtered_df = df[df['category_name'].isin(selected_categories)]

    if search_query:
        filtered_df = filtered_df[
            filtered_df['title'].str.lower().str.contains(search_query, na=False) |
            filtered_df['channel_title'].str.lower().str.contains(search_query, na=False)
        ]

    st.sidebar.markdown(f"**Showing {len(filtered_df):,} of {len(df):,} videos**")

    # ---------------------------------------------------------
    # 1. KPI Overview Metrics
    # ---------------------------------------------------------
    total_videos = len(filtered_df)
    total_views = filtered_df['views'].sum()
    total_likes = filtered_df['likes'].sum()
    total_comments = filtered_df['comment_count'].sum()
    avg_engagement = filtered_df['engagement_rate_pct'].mean() if total_videos > 0 else 0

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(label="Total Videos", value=f"{total_videos:,}")
    with col2:
        st.metric(label="Total Views", value=format_number(total_views), help=f"{total_views:,.0f} views")
    with col3:
        st.metric(label="Total Likes", value=format_number(total_likes), help=f"{total_likes:,.0f} likes")
    with col4:
        st.metric(label="Total Comments", value=format_number(total_comments), help=f"{total_comments:,.0f} comments")
    with col5:
        st.metric(label="Avg Engagement Rate", value=f"{avg_engagement:.2f}%")

    st.markdown("---")

    # ---------------------------------------------------------
    # 2. Visualizations Tabs
    # ---------------------------------------------------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏆 Top 10 Videos",
        "📊 Category Analysis",
        "📈 Engagement & Correlations",
        "📋 Data Explorer",
        "⚡ Big Data Results (MapReduce & Hive)"
    ])

    # Tab 1: Top 10 Videos by Views
    with tab1:
        st.subheader("Top 10 Most Viewed Videos")
        top_10 = filtered_df.sort_values(by='views', ascending=False).head(10).copy()

        if not top_10.empty:
            # Bar Chart
            fig_top10 = px.bar(
                top_10,
                x='views',
                y='title',
                orientation='h',
                color='category_name',
                text='views',
                hover_data=['channel_title', 'likes', 'comment_count'],
                labels={'views': 'View Count', 'title': 'Video Title', 'category_name': 'Category'},
                title="Top 10 Trending Videos by Views"
            )
            fig_top10.update_layout(yaxis=dict(autorange="reversed"), height=500)
            fig_top10.update_traces(texttemplate='%{text:.2s}', textposition='outside')
            st.plotly_chart(fig_top10, use_container_width=True)

            # Table View
            display_cols = ['title', 'channel_title', 'category_name', 'views', 'likes', 'comment_count', 'engagement_rate_pct']
            st.dataframe(
                top_10[display_cols].rename(columns={
                    'title': 'Video Title',
                    'channel_title': 'Channel',
                    'category_name': 'Category',
                    'views': 'Views',
                    'likes': 'Likes',
                    'comment_count': 'Comments',
                    'engagement_rate_pct': 'Engagement Rate (%)'
                }).style.format({
                    'Views': '{:,.0f}',
                    'Likes': '{:,.0f}',
                    'Comments': '{:,.0f}',
                    'Engagement Rate (%)': '{:.2f}%'
                }),
                use_container_width=True
            )
        else:
            st.info("No video records match the selected filters.")

    # Tab 2: Category-wise Distribution
    with tab2:
        st.subheader("Category-Level Performance Breakdown")
        col_cat1, col_cat2 = st.columns(2)

        # Category Aggregation
        cat_summary = filtered_df.groupby('category_name').agg(
            video_count=('title', 'count'),
            total_views=('views', 'sum'),
            total_likes=('likes', 'sum'),
            total_comments=('comment_count', 'sum'),
            avg_engagement=('engagement_rate_pct', 'mean')
        ).reset_index()

        with col_cat1:
            fig_views = px.bar(
                cat_summary.sort_values(by='total_views', ascending=False),
                x='total_views',
                y='category_name',
                orientation='h',
                title="Total Views by Video Category",
                labels={'total_views': 'Total Views', 'category_name': 'Category'},
                color='total_views',
                color_continuous_scale='Viridis'
            )
            fig_views.update_layout(yaxis=dict(autorange="reversed"), height=480)
            st.plotly_chart(fig_views, use_container_width=True)

        with col_cat2:
            fig_pie = px.pie(
                cat_summary,
                names='category_name',
                values='video_count',
                title="Video Share by Category",
                hole=0.4
            )
            fig_pie.update_layout(height=480)
            st.plotly_chart(fig_pie, use_container_width=True)

    # Tab 3: Engagement Metrics & Scatter Analysis
    with tab3:
        st.subheader("Engagement Analysis & Correlation")

        col_eng1, col_eng2 = st.columns(2)

        with col_eng1:
            fig_eng_cat = px.bar(
                cat_summary.sort_values(by='avg_engagement', ascending=False),
                x='category_name',
                y='avg_engagement',
                title="Average Engagement Rate by Category (%)",
                labels={'avg_engagement': 'Avg Engagement Rate (%)', 'category_name': 'Category'},
                color='avg_engagement',
                color_continuous_scale='Tealgrn'
            )
            fig_eng_cat.update_layout(xaxis_tickangle=-45, height=450)
            st.plotly_chart(fig_eng_cat, use_container_width=True)

        with col_eng2:
            # Views vs Likes Scatter Plot (sampled for smooth rendering if large)
            sample_size = min(len(filtered_df), 3000)
            scatter_sample = filtered_df.sample(sample_size, random_state=42) if len(filtered_df) > sample_size else filtered_df

            fig_scatter = px.scatter(
                scatter_sample,
                x='views',
                y='likes',
                color='category_name',
                hover_data=['title', 'channel_title'],
                title=f"Views vs. Likes Correlation (Sample of {sample_size:,} videos)",
                labels={'views': 'Views (Log Scale)', 'likes': 'Likes (Log Scale)', 'category_name': 'Category'},
                log_x=True,
                log_y=True
            )
            fig_scatter.update_layout(height=450)
            st.plotly_chart(fig_scatter, use_container_width=True)

    # Tab 4: Raw Data Explorer
    with tab4:
        st.subheader("Interactive Dataset Explorer")
        st.markdown(f"Displaying {len(filtered_df):,} records:")
        st.dataframe(
            filtered_df[['title', 'channel_title', 'category_name', 'views', 'likes', 'comment_count', 'engagement_rate_pct']].head(100),
            use_container_width=True
        )

    # Tab 5: Big Data Pipeline Outputs (Hadoop & Hive)
    with tab5:
        st.subheader("⚡ Big Data Pipeline Outputs")
        st.markdown("Verified outputs produced by **Java MapReduce** and **Apache Hive** batch analytics.")

        # 1. MapReduce Output
        st.markdown("#### 1. Java MapReduce Aggregation (`part-r-00000`)")
        mr_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs", "mapreduce_output", "part-r-00000")
        if not os.path.exists(mr_file):
            mr_file = "outputs/mapreduce_output/part-r-00000"

        if os.path.exists(mr_file):
            mr_df = pd.read_csv(mr_file, sep="\t")
            st.success("✅ MapReduce job completed with `_SUCCESS` status on HDFS/LocalRunner.")
            st.dataframe(mr_df.style.format({
                'TotalVideos': '{:,.0f}',
                'TotalViews': '{:,.0f}',
                'TotalLikes': '{:,.0f}',
                'TotalComments': '{:,.0f}',
                'AvgViews': '{:,.0f}',
                'AvgLikes': '{:,.0f}'
            }), use_container_width=True)
        else:
            st.info("MapReduce output not found. Run `run_codespace_pipeline.sh` to generate `part-r-00000`.")

        st.markdown("---")

        # 2. Apache Hive Results
        st.markdown("#### 2. Apache Hive Analytical Query Outputs")
        hive_cat_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs", "hive_results", "hive_category_summary.tsv")
        if not os.path.exists(hive_cat_file):
            hive_cat_file = "outputs/hive_results/hive_category_summary.tsv"

        hive_chan_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs", "hive_results", "hive_top_channels.tsv")
        if not os.path.exists(hive_chan_file):
            hive_chan_file = "outputs/hive_results/hive_top_channels.tsv"

        col_h1, col_h2 = st.columns(2)
        with col_h1:
            st.markdown("**Hive: Category Performance Breakdown**")
            if os.path.exists(hive_cat_file):
                hive_df = pd.read_csv(hive_cat_file, sep="\t")
                st.dataframe(hive_df, use_container_width=True)
            else:
                st.info("Hive category summary not found.")

        with col_h2:
            st.markdown("**Hive: Top 10 Channels by Views**")
            if os.path.exists(hive_chan_file):
                chan_df = pd.read_csv(hive_chan_file, sep="\t")
                st.dataframe(chan_df, use_container_width=True)
            else:
                st.info("Hive top channels not found.")

if __name__ == "__main__":
    main()
