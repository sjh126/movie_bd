package rule;
import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class CountMapper extends Mapper<Object, Object, Text, Text> {
	
	@Override
	protected void map(Object key, Object value, Mapper<Object, Object, Text, Text>.Context context)
			throws IOException, InterruptedException {
		String[] line = value.toString().split(" ");	
		for (String word : line) { 
			context.write(new Text(word), new Text("1")); 
		}
		
	}
}
