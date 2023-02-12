package cluster;
 
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
 
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
 
public class KMeansMapper extends Mapper<Object, Text, IntWritable, Text> {
    public void map(Object key, Text value, Context context)
    throws IOException, InterruptedException{
        String[] str = value.toString().split(" ");
        List<ArrayList<Float>> centers = Assistance.getCenters(context.getConfiguration().get("centerpath"));
        int k = Integer.parseInt(context.getConfiguration().get("kpath"));
        float minn = 114514;
        int belongto = -1;
        
        for (int i = 0; i < k; i++){
            float dis = 0;
            for (int j = 0; j < str.length; j++){
                float onedis = Math.abs(centers.get(i).get(j) - Float.parseFloat(str[j]));
                dis += onedis*onedis;
            }
            if (minn > dis){
            	minn = dis;
                belongto = i;
            }
            
        }
        context.write(new IntWritable(belongto), new Text(value));  
    }
}