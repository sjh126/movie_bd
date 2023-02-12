package rule;
import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;


public class CountReducer extends Reducer<Text, Text, Text, Text> {
	
	@Override
	protected void reduce(Text key, Iterable<Text> values, Reducer<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		
		Integer count = 0;
		for(Text value : values){
			count++;
		}
		
		if(count >= Main.SUPPORT_DEGREE ){
			context.write(key, new Text(count.toString()));
		}
		
	}
	
}
