# include <string>
# include <fstream>
using namespace std;

void writer(string filename, string lines) {
	ifstream file;
	file.open(filename.c_str());
	if (file.is_open()) {
		file << string << endl;
	}
}