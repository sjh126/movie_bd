package cluster;
 
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
 
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
 
public class KMeansReducer extends Reducer<IntWritable, Text, IntWritable, Text> {
    public void reduce(IntWritable key, Iterable<Text> value, Context context)
    throws IOException, InterruptedException{
        List<ArrayList<Float>> all_list = new ArrayList<ArrayList<Float>>();
        String ans = "";
        for (Text val : value){//集合当前质心下的数据
            String[] str = val.toString().split(" ");
            List<Float> onelist = new ArrayList<Float>();
            for (int i = 0; i < str.length; i++){
            	onelist.add(Float.valueOf(str[i]));
            }
            all_list.add((ArrayList<Float>) onelist);
        }
        
        for (int i = 0; i < all_list.get(0).size(); i++){
            float sum = 0;
            for (int j = 0; j < all_list.size(); j++){
                sum += all_list.get(j).get(i);
            }
            float oneans = sum / all_list.size();
            if (i == 0){
                ans += oneans;
            }
            else{
                ans += " " + oneans;
            }
        }
        Text result = new Text(ans);
        context.write(key, result);

    }
}