package rule;

import java.util.Random;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;


public class TransactionsMapper extends Mapper<Object, Object, Text, Text>{
	
	private static HashMap<String, String> movRankMap = new HashMap<String,String>();
	
	
	static{
		Configuration configuration = new Configuration();
		configuration.setBoolean("dfs.support.append", true);
		configuration.set("fs.defalutFS","hdfs://192.168.204.128:9000");
		
		FileSystem fileSystem = null;
		FileStatus[] status = null; 
		
		String addr = "hdfs://192.168.204.128:9000/FP/job1/part-r-*";
		
		try {
			fileSystem = FileSystem.get(configuration);
			status = fileSystem.globStatus(new Path(addr));
		} catch (IOException e1) {
			e1.printStackTrace();
		}
		
		
		BufferedReader reader = null;
		for(FileStatus fileStatus : status){
		
			try {
						
				FSDataInputStream inputStream = fileSystem.open(fileStatus.getPath());
				reader = new BufferedReader(new InputStreamReader(inputStream));	
				 			 
				HashMap< String, Integer > map = new HashMap<>();
				String aLine;
				while(( aLine = reader.readLine()) != null){
					
					String[] split = aLine.split("\t");
					map.put(split[0], Integer.valueOf(split[1]));
	
				}
	
				ArrayList< Map.Entry<String, Integer> > list = new ArrayList< Map.Entry<String, Integer>>(map.entrySet());
				
				Collections.sort( list,new Comparator<Map.Entry<String, Integer>>() {
	
					@Override
					public int compare(Entry<String, Integer> o1, Entry<String, Integer> o2) {
						return o1.getValue().equals(o2.getValue()) ? 0 : ( o1.getValue() < o2.getValue() ? 1 : -1 );
					}
				} );
				
				
				for(Integer i = 0 ; i < list.size(); i++){
					movRankMap.put(list.get(i).getKey(), i.toString()); 
				}
				
						
				
			} catch (Exception e) {
				e.printStackTrace();
			}finally {
				try {
					reader.close();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				
			}
		}
	}
	
	
	
	static int cnt=0;
	
	@Override
	protected void map(Object key, Object value, Mapper<Object, Object, Text, Text>.Context context)
			throws IOException, InterruptedException {
		Random r = new Random();
		int prefix=r.nextInt(11451);
		cnt++;
		String[] split = value.toString().split(" ");
		String user = String.valueOf(prefix).concat(String.valueOf(cnt));
		for (String movie : split) {
			if(movRankMap.containsKey(movie)){ // infrequent items eliminated
			
				String rank = movRankMap.get(movie);
				context.write(new Text(value.toString()), new Text(movie+","+rank));
			
		}
		
		
		}
		
		
	}
}
