import java.io.*;
import java.util.*;
import java.util.regex.*;

public class testVoc{
	public static void main(String[] args){
		String infile = "attributelist.txt";
		String outfile = "out.txt";
		System.out.println("Start serching vocabulary");
		
		String line = null;
		LinkedList<String> vocabulary = new LinkedList<String>();
		
		int wordNum = 0;
		String voc[] = null;
		
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
			
			for(int i = 0;i < wordNum;i++){
				String att = vocabulary.getFirst();
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
								String t = tmp[j-1];
								tmp[j-1] = tmp[j+1];
								tmp[j+1] = t;
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
}
