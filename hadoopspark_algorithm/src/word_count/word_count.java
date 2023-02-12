package word_count;
import java.io.IOException;
 
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
 
public class word_count {

	public static class WordCount_Mapper extends Mapper<LongWritable, Text, Text, IntWritable>{
		@Override	
		protected void map(LongWritable key, Text value, Mapper<LongWritable, Text,
				Text, IntWritable>.Context context)
				throws IOException, InterruptedException {
			String[] line = value.toString().split(" ");	
			for (String word : line) { 
				context.write(new Text(word), new IntWritable(1)); 
			}
		}												
	}
	
	public static class WordCount_Reducer extends Reducer<Text, IntWritable, Text, IntWritable>{
		@Override
		protected void reduce(Text key, Iterable<IntWritable> values,
				Reducer<Text, IntWritable, Text, IntWritable>.Context context)
						throws IOException, InterruptedException {
			int sum = 0;	
			for (IntWritable intWritable : values) {
				sum += intWritable.get();
			}
			context.write(key, new IntWritable(sum));	
		}
	}
 
	//提交工作
	public static void main(String[] args) throws Exception {
		
		String inPath= "hdfs://192.168.204.128:9000/input.txt";
		String outPath = "hdfs://192.168.204.128:9000/output/";
		Configuration conf = new Configuration();
		Job job = Job.getInstance();	//创建Job对象job
		FileSystem fs = FileSystem.get(conf);
		if (fs.exists(new Path(outPath))) {
			fs.delete(new Path(outPath), true);
		}
		job.setJarByClass(word_count.class); 	//设置运行的主类MyWordCount
		job.setMapperClass(WordCount_Mapper.class); 	//设置Mapper的主类
		job.setReducerClass(WordCount_Reducer.class); 	//设置Reduce的主类
		job.setOutputKeyClass(Text.class); 	//设置输出key的类型
		job.setOutputValueClass(IntWritable.class); 	//设置输出value的类型
		
		FileInputFormat.addInputPath(job, new Path(inPath));	
		FileOutputFormat.setOutputPath(job, new Path(outPath));
		System.exit((job.waitForCompletion(true)?0:1)); 	//提交任务并等待任务完成
	}
}