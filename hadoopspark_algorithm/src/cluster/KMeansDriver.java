package cluster;
 
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;
 
import java.io.IOException;
 
public class KMeansDriver{
	static int k=5;//聚类k值
    public static void main(String[] args) throws Exception{
        int round = 0;
        
        do {
            Configuration conf = new Configuration();

            conf.set("centerpath", "hdfs://192.168.204.128:9000/oldcenter/part-r-00000");
            conf.set("kpath", String.valueOf(k));
            Job job = new Job(conf, "KMeansCluster");//新建MapReduce作业
            job.setJarByClass(KMeansDriver.class);//设置作业启动类
            
            Path in = new Path("hdfs://192.168.204.128:9000/cluster_input.txt");
            Path out = new Path("hdfs://192.168.204.128:9000/newcenter/");
            
            FileSystem fs = FileSystem.get(conf);
            if (fs.exists(out)){
                fs.delete(out, true);
            }
            
            FileInputFormat.addInputPath(job, in);
            FileOutputFormat.setOutputPath(job, out);
    		
            job.setMapperClass(KMeansMapper.class);//设置Map类
            job.setReducerClass(KMeansReducer.class);//设置Reduce类
 
            job.setOutputKeyClass(IntWritable.class);//设置输出键的类
            job.setOutputValueClass(Text.class);//设置输出值的类
 
            job.waitForCompletion(true);//启动作业
 
            round++;
            System.out.printf("round: %d\n",round);
         } while ((round < 10 && (Assistance.isFinished("hdfs://192.168.204.128:9000/oldcenter/part-r-00000", "hdfs://192.168.204.128:9000/newcenter/part-r-00000", k, Float.valueOf("0.001")) == false)));
        //根据最终得到的聚类中心对数据集进行聚类
        Cluster(args);
    }
    public static void Cluster(String[] args)
            throws IOException, InterruptedException, ClassNotFoundException{
        Configuration conf = new Configuration();
   
        conf.set("centerpath", "hdfs://192.168.204.128:9000/oldcenter/part-r-00000");
        conf.set("kpath", String.valueOf(k));
        Job job = new Job(conf, "KMeansCluster");
        job.setJarByClass(KMeansDriver.class);
 
        Path in = new Path("hdfs://192.168.204.128:9000/cluster_input.txt");
        Path out = new Path("hdfs://192.168.204.128:9000/output");
        
        FileSystem fs = FileSystem.get(conf);
        if (fs.exists(out)){
            fs.delete(out, true);
        }
        
        FileInputFormat.addInputPath(job, in);
        FileOutputFormat.setOutputPath(job, out);
 
        //因为只是将样本点聚类，不需要reduce操作，故不设置Reduce类
        job.setMapperClass(KMeansMapper.class);
 
        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(Text.class);
 
        job.waitForCompletion(true);
    }
}