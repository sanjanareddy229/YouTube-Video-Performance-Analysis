package com.youtube.analysis;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;
import java.util.regex.Pattern;

/**
 * Executes the full Category Performance MapReduce job
 * generating the standard part-r-00000 output.
 */
public class LocalMapReduceRunner {

    private static final Pattern CSV_PATTERN = Pattern.compile(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)");

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

    public static void main(String[] args) throws Exception {
        String inputPath = (args.length > 0) ? args[0] : "data/youtube_trending_data.csv";
        String outputDir = (args.length > 1) ? args[1] : "outputs/mapreduce_output";

        File outFolder = new File(outputDir);
        if (!outFolder.exists()) {
            outFolder.mkdirs();
        }

        File outFile = new File(outFolder, "part-r-00000");
        File successFile = new File(outFolder, "_SUCCESS");

        Map<String, long[]> categoryAggregates = new TreeMap<>();

        int totalRecords = 0;
        try (BufferedReader br = new BufferedReader(new FileReader(inputPath))) {
            String line = br.readLine(); // Header
            while ((line = br.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty()) continue;

                String[] tokens = CSV_PATTERN.split(line, -1);
                if (tokens.length >= 11) {
                    try {
                        String rawCatId = tokens[4].trim().replace("\"", "");
                        long views = Long.parseLong(tokens[7].trim().replace("\"", ""));
                        long likes = Long.parseLong(tokens[8].trim().replace("\"", ""));
                        long comments = Long.parseLong(tokens[10].trim().replace("\"", ""));

                        String categoryName = CATEGORY_MAP.getOrDefault(rawCatId, "Other (" + rawCatId + ")");

                        categoryAggregates.putIfAbsent(categoryName, new long[4]);
                        long[] arr = categoryAggregates.get(categoryName);
                        arr[0] += 1;          // Total videos
                        arr[1] += views;      // Total views
                        arr[2] += likes;      // Total likes
                        arr[3] += comments;   // Total comments
                        totalRecords++;
                    } catch (Exception ignored) {}
                }
            }
        }

        // Write Hadoop part-r-00000
        try (PrintWriter pw = new PrintWriter(new FileWriter(outFile))) {
            pw.println("Category\tTotalVideos\tTotalViews\tTotalLikes\tTotalComments\tAvgViews\tAvgLikes\tEngagementRate");
            for (Map.Entry<String, long[]> entry : categoryAggregates.entrySet()) {
                String cat = entry.getKey();
                long[] v = entry.getValue();
                long avgViews = v[1] / v[0];
                long avgLikes = v[2] / v[0];
                double engagement = (v[1] > 0) ? ((double)(v[2] + v[3]) / v[1]) * 100.0 : 0.0;

                pw.printf("%s\t%d\t%d\t%d\t%d\t%d\t%d\t%.2f%%\n",
                        cat, v[0], v[1], v[2], v[3], avgViews, avgLikes, engagement);
            }
        }

        // Write _SUCCESS file
        successFile.createNewFile();

        System.out.println("==================================================");
        System.out.println("MapReduce Job Output Generated Successfully!");
        System.out.println("Total Records Processed: " + totalRecords);
        System.out.println("Output File: " + outFile.getAbsolutePath());
        System.out.println("HDFS Success Marker: " + successFile.getAbsolutePath());
        System.out.println("==================================================");
    }
}
