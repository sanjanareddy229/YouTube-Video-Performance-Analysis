package com.youtube.analysis;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

/**
 * Driver class to configure and run the YouTube Video Performance MapReduce job.
 */
public class YoutubeAnalysisDriver {

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();

        // Input and Output paths
        String inputPath = (args.length > 0) ? args[0] : "data/youtube_trending_data.csv";
        String outputPath = (args.length > 1) ? args[1] : "outputs/mapreduce_output";

        // Clean output directory if it exists
        Path outDir = new Path(outputPath);
        FileSystem fs = outDir.getFileSystem(conf);
        if (fs.exists(outDir)) {
            fs.delete(outDir, true);
            System.out.println("Cleaned existing output path: " + outputPath);
        }

        Job job = Job.getInstance(conf, "YouTube Category Performance Analysis");
        job.setJarByClass(YoutubeAnalysisDriver.class);

        // Mapper & Reducer
        job.setMapperClass(CategoryStatsMapper.class);
        job.setReducerClass(CategoryStatsReducer.class);

        // Output Key-Value types
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        // Set file paths
        FileInputFormat.addInputPath(job, new Path(inputPath));
        FileOutputFormat.setOutputPath(job, outDir);

        System.out.println("==================================================");
        System.out.println("Starting YouTube Video Performance MapReduce Job...");
        System.out.println("Input Path : " + inputPath);
        System.out.println("Output Path: " + outputPath);
        System.out.println("==================================================");

        boolean success = job.waitForCompletion(true);
        if (success) {
            System.out.println("MapReduce Job completed successfully!");
            System.exit(0);
        } else {
            System.err.println("MapReduce Job failed!");
            System.exit(1);
        }
    }
}
