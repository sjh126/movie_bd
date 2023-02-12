package rule;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class FrequentPatternMapper extends Mapper<Object, Object, Text, Text>{

	@Override
	protected void map(Object key, Object value, Mapper<Object, Object, Text, Text>.Context context)
			throws IOException, InterruptedException {
			
		context.write(new Text(value.toString().split("\t")[0]), new Text(value.toString().split("\t")[1]));
		
	}
}
