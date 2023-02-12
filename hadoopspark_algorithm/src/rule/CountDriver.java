package rule;


import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;

public class CountDriver extends Configured implements Tool{

	@Override
	public int run(String[] args) throws Exception {
		
		Configuration configuration = new Configuration();
		
		
		Job job = Job.getInstance(configuration);
		
		job.setMapperClass(CountMapper.class);
		job.setReducerClass(CountReducer.class);
		job.setJar("bigdata.jar");
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		
		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		
		
		return job.waitForCompletion(true) ? 0 : 1 ;
	}


	
	
}
