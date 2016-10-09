#include <iostream>
#include <fstream>
#include <map> 
#include <string>
#include <sstream>
#include <vector>
using namespace std;

int main () {
  
  map<string, int> lexicon;  
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
//			cout<<" > "<<item<<" ";
			temp.push_back(item);
    	}
    	if(temp[0]!=word)
    	{	
			word=temp[0];
			// add into lexicon
			lexicon[word]=pos;    	
		}
	
		for(int i=1;i<temp.size();i++)
		{
			int tmp = stoi(temp[i]);
//			 write into file
			writefile.seekp(0, ios::end);
			writefile.write((char*)(&tmp), sizeof(tmp));
//			 accumulate pos
			pos=writefile.tellp(); // how many bytes each? each int 4 bytes			
//			cout<<writefile.tellp()<<" "<<pos<<endl;
		}		
      	if(i++>2)
      		break;
    }
////	-------------------------------------------test------------------------------------------	
//    	int a[10] = { 0 };
//		for (int i = 0; i<9; i++)
//			a[i + 1] = a[i] * 10 + i + 1;
//		for (int i = 0; i<9; i++)
//			writefile.write((char*)(&a[i]), sizeof(a[i]));
////	------------------------------------------------------------------------------------------
    readfile.close();
    writefile.close();
  }
  else 
  		cout << "Unable to open file"; 
  	
	
  streampos size;
  int * memblock;

  ifstream file ("inverted-index.bin", ios::in|ios::binary|ios::ate);
//  ifstream file ("ok2002com.bin", ios::in|ios::binary|ios::ate);
  if (file.is_open())
  {
    size = file.tellg();
    memblock = new int [size];
    file.seekg (0, ios::beg);
    file.read ((char*)memblock, size);
    file.close();

    cout << "the entire file content is in memory\n";
	for(int i=0;i*4<size;i++)
		cout << memblock[i] << " "<<i<<endl;
    delete[] memblock;
  }
  else 
  	cout << "Unable to open file";
  return 0;
}
