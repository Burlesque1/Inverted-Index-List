#include <iostream>
#include <fstream>
#include <map> 
#include <string>
#include <sstream>
#include <vector>
using namespace std;

int read_b_file(string file_name)
{
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
    return 1;	// succeed return 1
  }
  else 
  {
	cout << "Unable to open file";
	return -1;	// fail return -1
  }
}
