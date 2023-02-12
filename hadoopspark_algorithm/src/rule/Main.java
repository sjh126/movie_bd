package rule;


import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.URI;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.util.ToolRunner;


public class Main {
	
	public final static Integer SUPPORT_DEGREE = 50;
	
	public static void main(String[] args) throws Exception {
			
			String HDFSAddr = "hdfs://192.168.204.128:9000/";
			String folderAddr = HDFSAddr + "FP/";
			
			String[] address = {HDFSAddr+"input.txt",folderAddr+"job1"};		
			int res = ToolRunner.run(new Configuration(), new CountDriver(), address);
			
			String[] address1 = {HDFSAddr+"input.txt",folderAddr+"job2"};		
			res = ToolRunner.run(new Configuration(), new TransactionsDriver(), address1);
			
			
			String[] address2 = {folderAddr+"job2/p*",folderAddr+"job3"};		
			res = ToolRunner.run(new Configuration(), new FrequentPatternDriver(), address2);
			  
	}
	
	
	
	
	
	
}
