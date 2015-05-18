import java.io.*;
import java.util.*;
import java.util.regex.*;


//run format: java java_key_cleaner "inputFile" "outputFile"
//
public class java_key_cleaner{
	
	public static int number_of_char = 10; //number of chars in string to check for similartys
	public static int ignore_occurance = 100; //number of attributes with less than this occurances will be ignored
	public boolean outputStats = true; //output statistics
	
	String infile = "../debug/attribute_keys_cleaned.txt";
	String outfile = "../debug/correct_attributes.txt";
	
	/*
	Input: String a, Length of a, String b, Length of b
	returns the distance between 2 strings*/
	public int distance(String a,int al,String b,int bl){
		
		if(al == 0){
			return bl;
		}
		if(bl == 0){
			return al;
		}
		
		int cost;
		
		if(a.charAt(al-1)==b.charAt(bl-1)){
			cost = 0;
		}
		else{
			cost = 1;
		}
		
		return min(distance(a,al-1,b,bl)+1,distance(a,al,b,bl-1)+1,distance(a,al-1,b,bl-1)+cost);
	}
	
	public int min(int a,int b,int c){
		int min = a;
		if(b < min){
			min = b;
		}
		if(c < min){
			min = c;
		}
		return min;
	}
	
	public void run(){
		//String infile = "attribute_keys_cleaned.txt";
		//infile = "fil2.txt";
		//String outfile = "correct_attributes.txt";
		//System.out.println("Start serching vocabulary");
		
		LinkedList<String> vocabulary = new LinkedList<String>();
		LinkedList<Integer> num_of_occurences = new LinkedList<Integer>();
		
		int wordNum = 0;
		int ignore = 0;
		String voc[] = null;
		String orgVoc[] = null;
		int numOcc[] = null;
		
		try{
			FileReader fr = new FileReader(infile);
			
			BufferedReader in = new BufferedReader(fr);
			
			String line = null;
			while((line = in.readLine()) != null) {
				if(line.indexOf('\t')!=-1){
					System.out.println("Warning \""+line+"\" contains a tab");
				}
				String mult[] = line.split("\\s+");
				line = "";
				for(int i=1;i<mult.length-1;i++){
					line+=mult[i]+" ";
				}
                line+=mult[mult.length-1];
				if(Integer.parseInt(mult[0])<ignore_occurance){
					ignore++;
				}
				vocabulary.add(line);
				num_of_occurences.add(Integer.parseInt(mult[0]));
				//System.out.println(line);
			}
			//System.out.println("ignore terms: "+ignore);
			
			//System.out.println("number of attributes: "+vocabulary.size());
			wordNum = vocabulary.size();
			
			voc = new String[wordNum];
			orgVoc = new String[wordNum];
			numOcc = new int[wordNum];
			
			in.close();
		}
		catch(Exception e){
			System.err.println(e);
			System.exit(1);
		}
		
		for(int i = 0;i < wordNum;i++){
			numOcc[i] = num_of_occurences.getFirst();
			num_of_occurences.removeFirst();
		
			String att = vocabulary.getFirst();
			orgVoc[i] = att;
			// to lower case
			att = att.toLowerCase();
			//remove special char
			att = att.replace("&lt;ref&gt;{{"," ");
			att = att.replace("-"," ");
			att = att.replace("_"," ");
			att = att.replace(":"," ");
			att = att.replace("+"," ");
			att = att.replace("'"," ");
			att = att.replace("|"," ");
			
			//remove "of"
			Pattern p = Pattern.compile("(.+) of (.+)");
			
			Matcher m = p.matcher(att);
			if(m.find()){
				//System.out.println(att);
				String tmp[] = att.split("\\s+");
				for(int j = 0;j < tmp.length;j++){
					if(j>0 && tmp[j].equals("of") && (j+1) < tmp.length){
						String tmpo = tmp[j-1];
						tmp[j-1] = tmp[j+1];
						tmp[j+1] = tmpo;
						tmp[j] = "";
					}
				}
				att="";
				for(int j=0;j<tmp.length;j++){
					att+=tmp[j];
				}
				//System.out.println(voc[i]);
			}
			//add result
			voc[i] = att;
			//System.out.println(att);
			//vocabulary.add(att);
			vocabulary.removeFirst();
		}
		
		//removee any whitespaces remaining
		for(int i = 0;i < wordNum;i++){
			String att = voc[i];
			String mult[] = att.split("\\s+");
			if(mult.length>1){
				voc[i] = "";
				for(int j=0;j<mult.length;j++){
					voc[i]+=mult[j];
					
				}
			}
		}
		
		//used for debug
		LinkedList<String> changelist = new LinkedList<String>();
		
		//now we need to fix the text mispellings
		HashMap<String, String> translate = new HashMap<String, String>();
		
		int attributes_to_compare = wordNum - ignore;
		//attributes_to_compare = 3;
		int c=0;
		
		int changes = 0;
		//check for similar terms
		for(int i=0;i<attributes_to_compare;i++){
			String att = voc[i];
			
			Pattern p3 = Pattern.compile(".+[0-9]");
			Matcher m3 = p3.matcher(att/*att.substring(att.length() - 1)*/);
			
			//System.out.println(att);
			if(!translate.containsKey(att)){
				translate.put(att,att);
			}
			
			if(att.length()<number_of_char && att.length()>4 && !m3.find()){
			
			for(int j=0;j<wordNum;j++){
				String check = voc[j];
				
				String first4 = "";
				if(att.length()>3){
					first4 = att.substring(0,4);
				}
				Pattern p = Pattern.compile(first4);
			
				Matcher m = p.matcher(check);
				/*if(m.find()){
					System.out.println(att+" "+check);
				}*/
				
				
				
				if(m.find() && check.length()-2 < att.length() && att.length() < check.length()+2){
				//System.out.println(att+" "+check);
				String last = check.substring(check.length() - 1);
				Pattern p2 = Pattern.compile(".+[0-9]");
				Matcher m2 = p2.matcher(check/*last*/);
				//System.out.println("check "+att+" "+check);
				if(!translate.containsKey(check) && !m2.find()){
					int diff = distance(att,att.length(),check,check.length());
					/*if(m.find()){
						System.out.println("diff: "+diff);
					}*/
					if(diff < 2){
						translate.put(check,att);
						changelist.add(check+"\t"+att);
						//System.out.println("correcting "+check+" to "+att);
						changes++;
					}
					//System.out.println("check done "+att+" "+check+" diff "+diff);
				}
				}
			}
			}
			c++; //:P
			//System.out.println(c+"/"+wordNum+" translate: "+translate.size()+" # to test: "+attributes_to_compare);
			//System.out.println(att);
			//System.out.println(sortedCommon);
		}/**/
		
		//System.out.println(translate.size()+" "+changes);
		
		//correct spelling in voc
		for(int i=0;i<wordNum;i++){
			String att = voc[i];
			if(translate.containsKey(voc[i])){
				voc[i]=translate.get(voc[i]);
			}
		}/**/
		
		HashMap<String,String> translationToken = new HashMap<String,String>();
		for(int i=0;i<wordNum;i++){
			String att = voc[i];
			if(!translationToken.containsKey(voc[i])){
				translationToken.put(voc[i],orgVoc[i]);
			}
		}
		
		for(int i=0;i<wordNum;i++){
			String att = voc[i];
			voc[i] = translationToken.get(att);
		}
		
		/*System.out.println(translationToken);*/
		
		if(outputStats){
			try{
				FileWriter fw = new FileWriter("../debug/attribute_changes.txt");
				BufferedWriter out = new BufferedWriter(fw);
				out.write("#A total of "+translate.size()+" keys where changed due to misspellings or formatting errors");
				out.newLine();
				int numOfChangesInJSON = 0;
				for(int i=0;i<wordNum;i++){
					if(!orgVoc[i].equals(voc[i])){
						numOfChangesInJSON+=numOcc[i];
					}
				}
				out.write("#A total of "+numOfChangesInJSON+" keys in the JSON file was corrected.\n#These words changed where the following:");
				out.newLine();
				out.write("#NUM_WORDS_CHANGED="+translate.size());
				out.newLine();
				out.write("#NUM_KEYS_CHANGED="+numOfChangesInJSON);
				out.newLine();
				for(int i=0;i<wordNum;i++){
					if(!orgVoc[i].equals(voc[i])){
						out.write(numOcc[i]+" "+orgVoc[i]+"\t"+voc[i]);
						out.newLine();
					}
				}
				out.close();
			}
			catch(Exception e){
				System.err.println(e);
			}
		}
		
		try{
			FileWriter fw = new FileWriter(outfile);
			BufferedWriter out = new BufferedWriter(fw);
			for(int i=0;i<wordNum;i++){
				voc[i] = voc[i].replace("-","_");
				out.write(orgVoc[i]+"\t"+voc[i]);
				out.newLine();
			}
			out.close();
		}
		catch(Exception e){
			System.err.println(e);
			System.exit(1);
		}
		
	}
	
	public java_key_cleaner(){

	}
	
	public java_key_cleaner(String in,String out){
		infile = in;
		outfile = out;
	}
	
	public static void main(String[] args){
		java_key_cleaner a;
		if(args.length == 2){
			//System.out.println("got arguments");
			a = new java_key_cleaner(args[0],args[1]);
			//infile = args[0];
			//outfile = args[1];
		}
		else if(args.length == 3){
			a = new java_key_cleaner(args[0],args[1]);
			number_of_char = Integer.parseInt(args[2]);
		}
		else{
			a = new java_key_cleaner();
		}
		a.run();
	}
}
