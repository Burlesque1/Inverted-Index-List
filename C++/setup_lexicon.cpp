#include <iostream>
#include <fstream>
#include <vector> 
#include <string>
#include "method.hpp"


#ifndef BINARYMODE
#define BINARYMODE 1


int setup_lexicon(vector<int> &lexicon, vector<string> &termID){

#if BINARYMODE
	cout<<"now binary mode"<<endl;
	
	ofstream lf ("lexicon_b", ios::binary);
	lf.seekp (0, ios::end);
	for(auto l:lexicon)
	{
		int tmp = l;
		lf.write ((char*)(&tmp), sizeof(tmp));		
	}
	lf.close();
	
	  
#else // ASCii mode
	cout<<"now ASCii mode"<<endl;
	ofstream lf ("lexicon_a");
	char *buffer=new char[33];
	for(int i=0;i<lexicon.size();i++)
	{
//		itoa(l.second, buffer, 10);string s(buffer);
	    lf << termID[i] +' '+ to_string(lexicon[i]) +'\n';	
	}
	lf.close();
	return 1;
#endif
}
#endif
