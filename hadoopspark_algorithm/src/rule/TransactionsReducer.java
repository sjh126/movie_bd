package rule;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Map;
import java.util.TreeMap;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;


public class TransactionsReducer extends Reducer<Text, Text, Text, Text> {
	
	@Override
	protected void reduce(Text key, Iterable<Text> values, Reducer<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
			
		TreeMap<Integer, String> map = new TreeMap<Integer,String>();
		
		for(Text value : values){
			String movie = value.toString().split(",")[0];
			Integer rank = Integer.valueOf(value.toString().split(",")[1]);
			
			map.put(rank, movie);
		}
		
		
		ArrayList<String> arrayList = new ArrayList<>();
		for(Map.Entry<Integer, String> entry : map.entrySet()){
			
			arrayList.add(entry.getValue()); // movie 
			
		}
		
	  
			
			for(int i = arrayList.size()-1 ; i > 0; i--){

				String valueStr = null;
				for (int j = i - 1 ; j >= 0; j--){
					
					if(valueStr == null) {
						valueStr = arrayList.get(j);
					}else{
						valueStr += "," + arrayList.get(j);
					}
					
				}
				
				System.out.println(arrayList.get(i) + ":" + valueStr);
				context.write(new Text(arrayList.get(i)), new Text(valueStr));
				
			}
		
		
		
		
	}
	
	
	
}
