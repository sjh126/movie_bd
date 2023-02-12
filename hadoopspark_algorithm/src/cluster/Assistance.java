package cluster;
 
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.util.LineReader;
 
import java.io.IOException;
import java.util.*;
 
public class Assistance {
	
    public static List<ArrayList<Float>> getCenters(String inputpath){
        List<ArrayList<Float>> result = new ArrayList<ArrayList<Float>>();
        Configuration conf = new Configuration();
        try {
            FileSystem hdfs = FileSystem.get(conf);
            Path in = new Path(inputpath);
            FSDataInputStream fsIn = hdfs.open(in);
            LineReader lineIn = new LineReader(fsIn, conf);
            Text line = new Text();
            while (lineIn.readLine(line) > 0){
                String record = line.toString();
            
                String[] str = record.replace("\t", " ").split(" ");
                List<Float> onelist = new ArrayList<Float>();
                for (int i = 1; i < str.length; i++){//不读入最前面的序号
                	onelist.add(Float.parseFloat(str[i]));
                }
                result.add((ArrayList<Float>) onelist);
            }
            fsIn.close();
        } catch (IOException e){
            e.printStackTrace();
        }
        return result;
    }
 
    public static void deleteLastResult(String path){
        Configuration conf = new Configuration();
        try {
            FileSystem hdfs = FileSystem.get(conf);
            Path delete_path = new Path(path);
            hdfs.delete(delete_path, true);
        } catch (IOException e){
            e.printStackTrace();
        }
    }
  
    public static boolean isFinished(String oldpath, String newpath, int k, float threshold)
    throws IOException{
        List<ArrayList<Float>> oldcenters = Assistance.getCenters(oldpath);
        List<ArrayList<Float>> newcenters = Assistance.getCenters(newpath);
        float distance = 0;
        for (int i = 0; i < k; ++i){
            for (int j = 1; j < oldcenters.get(i).size(); ++j){
                float tmp = Math.abs(oldcenters.get(i).get(j) - newcenters.get(i).get(j));
                distance += Math.pow(tmp, 2);
            }
        }
        System.out.println("Distance = " + distance + " Threshold = " + threshold);
        if (distance < threshold)
            return true;
       
        Assistance.deleteLastResult(oldpath);
        Configuration conf = new Configuration();
        FileSystem hdfs = FileSystem.get(conf);
        hdfs.copyToLocalFile(new Path(newpath), new Path("part-r-00000"));
        hdfs.delete(new Path(oldpath), true);
        hdfs.moveFromLocalFile(new Path("part-r-00000"), new Path(oldpath));//覆盖旧的中心文件
        return false;
    }
}