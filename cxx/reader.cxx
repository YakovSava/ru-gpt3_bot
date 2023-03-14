# include <string>
# include <fstream>
using namespace std;

string read(string filename) {
	string line, lines = "", endline = "\n";
	ofstream file;
	file.open(filename.c_str());
	if (file.is_open()) {
		while (getline(file, line)) {
			lines = lines + endline + line;
		}
	}

	return lines;
}