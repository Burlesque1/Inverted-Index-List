#include <iostream>
#include <fstream>
#include <map> 
#include <string>
#include <sstream>
#include <vector>
#include "method.hpp"


using namespace std;

#ifndef TEST
#define TEST 1


#if TEST!=0
int main () {
  map<string, int> lexicon_m;
  vector<string> termID(500, "2");  
  vector<int> lexicon(termID.size(), 1);
  int i=0;
  string line, word="";
  int pos=0;
  ifstream readfile ("merged-file");
  ofstream writefile ("inverted-index.bin", ios::binary);
  if (readfile.is_open())
  {
    while ( getline (readfile,line) )
    {
  		vector<string> temp;
      	stringstream ss(line);
      	string item;
     	while (getline(ss, item, '\ ')) 
		{
			temp.push_back(item);
    	}
    	if(temp[0]!=word)
    	{	
			word=temp[0];
			// add into lexicon
			lexicon_m[word]=pos;
			lexicon[termID[word]]=pos;    	
		}
	
		for(int i=1;i<temp.size();i++)
		{
			int tmp = stoi(temp[i]);
			// write into file
			writefile.seekp(0, ios::end);
			writefile.write((char*)(&tmp), sizeof(tmp));
			// accumulate pos
			pos=writefile.tellp(); // how many bytes each? each int 4 bytes	
		}		
		i++;
    }
////	-------------------------------------------test------------------------------------------	
//    	int a[10] = { 0 };
//		for (int i = 0; i<9; i++)
//			a[i + 1] = a[i] * 10 + i + 1;
//		for (int i = 0; i<9; i++)
//			writefile.write((char*)(&a[i]), sizeof(a[i]));
////	------------------------------------------------------------------------------------------
    writefile.close();
    readfile.close();
  }
  else 
  		cout << "Unable to open file"; 
  	
  for(auto l:lexicon_m)
  	cout<<l.first<<" "<<l.second<<endl;
 
 	cout<<i<<endl;
//  read_b_file("");
  	setup_lexicon(lexicon, termID);
  return 0;
}

#else
int main()
{
	cout<<"this is test mode!"<<endl;
	int a=0;
	cout<<to_string(a);
	return 0;
}

#endif
#endif


