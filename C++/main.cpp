#include <iostream>
#include <fstream>
#include <unordered_map> 
#include <string>
#include <sstream>
#include <vector>
#include "method.hpp"


using namespace std;

#ifndef TEST
#define TEST 0


#if TEST!=1
int main () {
  unordered_map<string, int> term_ID;	// <term, termID>
  vector<string> ID_term;  				// <termID, term>
  vector<int> lexicon;					// <termID, file_offset>
  int ID=0, pos_offset=0, last_pos=0, docID=0, last_docID=0;
  string line, word="";
  ifstream readfile ("G:\\A2\\posting_b");
//  ofstream writefile ("inverted-index.bin", ios::binary);
  ofstream writefile ("test.bin", ios::binary);
  if (readfile.is_open())
  {	
  	cout<<"opened"<<endl;
	int i=0;
    while ( getline (readfile,line) )
    {	
    	if(i++>5000000)
    		break;
  		vector<string> temp;	// WORD, DOCID, DOCID, DOCID...
      	stringstream ss(line);
      	string item;
     	while (getline(ss, item, '\ ')) 
		{
//			cout<<item<<endl;
			temp.push_back(item);
    	}			
		docID = stoi(temp[1]);
    	if(temp[0]==word && docID==last_docID)
    		;
    	else
    	{
			if(temp[0]!=word)		// encounter a new word
	    	{	
				word=temp[0];
				// add into lexicon
				term_ID[word]=ID++;
				ID_term.push_back(word);
				lexicon.push_back(pos_offset);  
				last_pos=writefile.tellp(); 
			} 	
//			cout<<docID<<" docID "<<last_docID<<endl;
			last_docID=docID;
			// write into file
			writefile.seekp(0, ios::end);
			writefile.write((char*)(&docID), sizeof(docID));
			// accumulate pos
			pos_offset=writefile.tellp() - last_pos; // store difference to compress. In binary mode each int occupies 4 bytes	   	
		}
		if(i>=100000 && i==(i/100000)*100000)
			cout<<i<<" lines finishes "<<endl;		
	}
	writefile.close();
    readfile.close();
  }
  else 
  		cout << "Unable to open file"; 
 
 	
//  read_b_file("");
  setup_lexicon(lexicon, ID_term);
  return 0;
}

#else
int main()
{
	cout<<"this is test mode!"<<endl;
	ifstream readfile ("G:\\A2\\posting_b",ios::binary);
	ifstream file ("test", ios::in|ios::binary|ios::ate);
	string line="";
	streampos size;
  	int * memblock;	
	if (readfile.is_open())
  		cout<<"opened"<<endl;
  	else
  		cout<<"not"<<endl;
  	while(getline(readfile,line))
	{
		cout<<line<<endl;
	}

//  if (file.is_open())
//  {
//    size = file.tellg();
//    memblock = new int [size];
//    file.seekg (0, ios::beg);
//    file.read ((char*)memblock, size);
//    file.close();
//
//    cout << "the entire file content is in memory\n";
//	for(int i=0;i*4<size;i++)
//		cout << memblock[i] << " "<<i<<endl;
//    delete[] memblock;
//    return 1;	// succeed return 1
//  }
//  else 
//  {
//	cout << "Unable to open file";
//	return -1;	// fail return -1
//  }
////	-------------------------------------------test------------------------------------------	
//    	int a[10] = { 0 };
//		for (int i = 0; i<9; i++)
//			a[i + 1] = a[i] * 10 + i + 1;
//		for (int i = 0; i<9; i++)
//			writefile.write((char*)(&a[i]), sizeof(a[i]));
////	------------------------------------------------------------------------------------------
	return 0;
}

#endif
#endif


