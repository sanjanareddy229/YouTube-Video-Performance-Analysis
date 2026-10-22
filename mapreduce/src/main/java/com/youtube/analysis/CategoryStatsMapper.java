package com.youtube.analysis;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

/**
 * Mapper for YouTube Video Performance Analysis.
 * Reads CSV records and emits (CategoryName, "views,likes,comments,1").
 */
public class CategoryStatsMapper extends Mapper<LongWritable, Text, Text, Text> {

    private Text outCategory = new Text();
    private Text outMetrics = new Text();

    // Mapping category IDs to readable category names
    private static final Map<String, String> CATEGORY_MAP = new HashMap<>();
    static {
        CATEGORY_MAP.put("1", "Film & Animation");
        CATEGORY_MAP.put("2", "Autos & Vehicles");
        CATEGORY_MAP.put("10", "Music");
        CATEGORY_MAP.put("15", "Pets & Animals");
        CATEGORY_MAP.put("17", "Sports");
        CATEGORY_MAP.put("18", "Short Movies");
        CATEGORY_MAP.put("19", "Travel & Events");
        CATEGORY_MAP.put("20", "Gaming");
        CATEGORY_MAP.put("21", "Videoblogging");
        CATEGORY_MAP.put("22", "People & Blogs");
        CATEGORY_MAP.put("23", "Comedy");
        CATEGORY_MAP.put("24", "Entertainment");
        CATEGORY_MAP.put("25", "News & Politics");
        CATEGORY_MAP.put("26", "Howto & Style");
        CATEGORY_MAP.put("27", "Education");
        CATEGORY_MAP.put("28", "Science & Technology");
        CATEGORY_MAP.put("29", "Nonprofits & Activism");
        CATEGORY_MAP.put("30", "Movies");
        CATEGORY_MAP.put("43", "Shows");
        CATEGORY_MAP.put("44", "Trailers");
    }

    // CSV regex parser matching commas outside quotes
    private static final Pattern CSV_PATTERN = Pattern.compile(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)");

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        // Skip CSV header
        if (key.get() == 0 && value.toString().startsWith("video_id")) {
            return;
        }

        String line = value.toString().trim();
        if (line.isEmpty()) {
            return;
        }

        String[] tokens = CSV_PATTERN.split(line, -1);
        if (tokens.length < 11) {
            return;
        }

        try {
            String rawCategoryId = tokens[4].trim().replace("\"", "");
            long views = parseLongSafe(tokens[7]);
            long likes = parseLongSafe(tokens[8]);
            long comments = parseLongSafe(tokens[10]);

            String categoryName = CATEGORY_MAP.getOrDefault(rawCategoryId, "Other (" + rawCategoryId + ")");

            outCategory.set(categoryName);
            // Format: views,likes,comments,1 (1 = video counter)
            outMetrics.set(views + "," + likes + "," + comments + ",1");
            context.write(outCategory, outMetrics);

        } catch (Exception e) {
            // Ignore malformed rows safely
        }
    }

    private long parseLongSafe(String str) {
        if (str == null) return 0L;
        String clean = str.trim().replace("\"", "");
        try {
            return Long.parseLong(clean);
        } catch (NumberFormatException e) {
            return 0L;
        }
    }
}
