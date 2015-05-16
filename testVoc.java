import java.io.*;
import java.util.*;
import java.util.regex.*;

public class testVoc{
	
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
		//String infile = "fil.txt";//"attributelist.txt";
		String infile = "attributelist.txt";
		String outfile = "out2.txt";
		System.out.println("Start serching vocabulary");
		
		String line = null;
		LinkedList<String> vocabulary = new LinkedList<String>();
		
		int wordNum = 0;
		String voc[] = null;
		String orgVoc[] = null;
		
		try{
			FileReader fr = new FileReader(infile);
			
			BufferedReader in = new BufferedReader(fr);
			
			while((line = in.readLine()) != null) {
				vocabulary.add(line);
				System.out.println(line);
			}
			
			System.out.println(vocabulary.size());
			wordNum = vocabulary.size();
			
			voc = new String[wordNum];
			orgVoc = new String[wordNum];
			
			for(int i = 0;i < wordNum;i++){
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
					System.out.println(att);
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
					System.out.println(voc[i]);
				}
				
				/*String mult[] = att.split("\\s+");
				if(mult.length > 1){
					att = "";
					for(int j=0;j<mult.length;j++){
						if(mult[j].equals("of")){
							//ignore "of"
						}
						else{
							att = att + mult[j]+" ";
						}
					}
				}/**/
				//print result
				/*System.out.println(att+" "+mult.length);
				System.out.println();
				/**/
				//add result
				voc[i] = att;
				//vocabulary.add(att);
				vocabulary.removeFirst();
			}
			
			
			
			//System.out.println(words.get(2).get(0));
			
			in.close();
		}
		catch(Exception e){
			System.err.println(e);
		}
		
		//conatins word
		/*LinkedList<LinkedList> words = new LinkedList<LinkedList>();
		HashMap<String,Integer> map = new HashMap<String,Integer>();
		int wordCounter = 0;
		//LinkedList<Integer> cont = new LinkedList<Integer>();
		
		for(int i = 0;i < wordNum;i++){
			String att = voc[i];
			String mult[] = att.split("\\s+");
			for(int j=0;j<mult.length;j++){
				if(!map.containsKey(mult[j])){
					System.out.println("new key found: "+mult[j]);
					map.put(mult[j],wordCounter);
					
					Pattern p = Pattern.compile(mult[j]);
					Matcher m;
					LinkedList<Integer> list = new LinkedList<Integer>();
					for(int k = 0;k < wordNum;k++){
						m = p.matcher(voc[k]);
						if(m.find()){
							list.add(k);
							System.out.println(k);
						}
					}
					words.add(list);
					wordCounter++;
				}
			}
		}*/
		
		/*LinkedList<LinkedList> vocComp = new LinkedList<LinkedList>();
		
		for(int i=0;i<wordNum;i++){
			vocComp.add(new LinkedList<Integer>);
		}*/
		
		/*String ans[] = new String[wordNum];
		int counter=1;
		
		ListIterator<LinkedList> linkedIter = words.listIterator();
		while(linkedIter.hasNext()){
			LinkedList<Integer> list = linkedIter.next();
			ListIterator<Integer> iter = list.listIterator();
			while(iter.hasNext()){
				int num = iter.next();
				if(ans[num]==null){
					ans[num] = ""+counter;
				}
				else{
					ans[num]=ans[num]+" "+counter;
				}
				//System.out.println(num);
			}
			counter++;
		}*/
		/*for(int i=0;i<words.size();i++){
			//LinkedList<Integer> list = words.get(i);
			//ListIterator<Integer> iter = list.listIterator();
		}*/
		
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
		
		HashMap<String, Integer> common = new HashMap<String, Integer>();
		ValueMap vm = new ValueMap(common);
		TreeMap<String, Integer> sortedCommon = new TreeMap<String, Integer>(vm);
		
		//count the variables
		for(int i=0;i<wordNum;i++){
			String att = voc[i];
			if(common.containsKey(att)){
				int value = common.get(att);
				value++;
				common.put(att,value);
			}
			else{
				common.put(att,1);
			}
		}
		
		//System.out.println("map:"+common);
		
		sortedCommon.putAll(common);
		
		System.out.println(sortedCommon);
		
		common.clear();
		common.putAll(sortedCommon);
		
		int cn=0;
		//remove singles
		for(int i=0;i<wordNum;i++){
			String att = voc[i];
			if(common.containsKey(att)){
				//System.out.println(att);
				int value = common.get(att);
				if(value==1){
					System.out.println(att);
					cn++;
				}
			}
		}
		System.out.println(cn);
		//System.out.println(sortedCommon.firstKey());
		
		HashMap<String, String> translate = new HashMap<String, String>();
		
		int uniqWords = sortedCommon.size();
		
		LinkedList<String> sortedWords = new LinkedList<String>(sortedCommon.keySet());
		//System.out.println(sortedWords);
		int c=0;
		//check for similar terms
		/*for(int i=0;i<uniqWords;i++){
			String att = sortedWords.getFirst();
			sortedWords.removeFirst();
			//System.out.println(rem);
			if(!translate.containsKey(att)){
				translate.put(att,att);
			}
			if(att.length()<10){
			for(int j=0;j<wordNum;j++){
				String check = voc[j];
				if(check.length()-2 < att.length() && att.length() < check.length()+2){
				if(!att.equals(check) && !translate.containsKey(check)){
					int diff = distance(att,att.length(),check,check.length());
					if(diff < 2){
						translate.put(check,att);
						//System.out.println("shit");
					}
				}
				}
			}
			}
			c++;
			System.out.println(c+"/"+wordNum+" translate: "+translate.size()+" #uniq "+sortedCommon.size());
			//System.out.println(att);
			//System.out.println(sortedCommon);
		}/**/
		
		//System.out.println(translate);
		
		// correct spelling
		for(int i=0;i<wordNum;i++){
			String att = voc[i];
			if(translate.containsKey(voc[i])){
				voc[i]=translate.get(voc[i]);
			}
		}
		
		try{
			FileWriter fw = new FileWriter(outfile);
			BufferedWriter out = new BufferedWriter(fw);
			for(int i=0;i<wordNum;i++){
				out.write(voc[i]);
				out.newLine();
			}
			out.close();
		}
		catch(Exception e){
			System.err.println(e);
		}
	}
	
	public static void main(String[] args){
		testVoc t = new testVoc();
		t.run();
	}
}

/* Used to sort a map on the for <String, Integer> since this is quite bad praxis*/
class ValueMap implements Comparator<String>{
	
	Map<String,Integer> map;
	
	public ValueMap(Map<String,Integer> m){
		this.map = m;
	}
	
	public int compare(String a,String b){
		if(map.get(a)<=map.get(b)){
			return 1;
		}
		else{
			return -1;
		}
	}
}
