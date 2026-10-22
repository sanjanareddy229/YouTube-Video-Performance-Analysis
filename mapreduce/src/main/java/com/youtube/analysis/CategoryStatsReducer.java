package com.youtube.analysis;

import java.io.IOException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

/**
 * Reducer for YouTube Video Performance Analysis.
 * Aggregates views, likes, comments, and computes category-level statistics.
 */
public class CategoryStatsReducer extends Reducer<Text, Text, Text, Text> {

    private Text result = new Text();

    @Override
    protected void reduce(Text key, Iterable<Text> values, Context context)
            throws IOException, InterruptedException {

        long totalVideos = 0;
        long totalViews = 0;
        long totalLikes = 0;
        long totalComments = 0;

        for (Text val : values) {
            String[] parts = val.toString().split(",");
            if (parts.length >= 4) {
                try {
                    long views = Long.parseLong(parts[0]);
                    long likes = Long.parseLong(parts[1]);
                    long comments = Long.parseLong(parts[2]);
                    long count = Long.parseLong(parts[3]);

                    totalViews += views;
                    totalLikes += likes;
                    totalComments += comments;
                    totalVideos += count;
                } catch (NumberFormatException ignored) {
                }
            }
        }

        if (totalVideos > 0) {
            long avgViews = totalViews / totalVideos;
            long avgLikes = totalLikes / totalVideos;
            double engagementRate = (totalViews > 0) ? ((double)(totalLikes + totalComments) / totalViews) * 100.0 : 0.0;

            // Tab-separated summary: TotalVideos \t TotalViews \t TotalLikes \t TotalComments \t AvgViews \t AvgLikes \t EngagementRate%
            String outputStr = String.format("%d\t%d\t%d\t%d\t%d\t%d\t%.2f%%",
                    totalVideos, totalViews, totalLikes, totalComments, avgViews, avgLikes, engagementRate);

            result.set(outputStr);
            context.write(key, result);
        }
    }
}
