#include <iostream>
#include <vector>
#include <string>
#include <windows.h>
#include <libxl.h>
#include <algorithm>
#include <numeric>
using namespace std;
using namespace libxl;
void processExcel(const wchar_t* filename, vector<vector<wstring>>& dataMatrix, vector<wstring>& samplcity) {
	Book* book = xlCreateBook();
	// Configure your own LibXL license locally; embedded license removed.
	if (book) {
		if (book->load(filename)) { // 加载xlsx文件
			Sheet* sheet = book->getSheet(0); // 获取第一个工作表
			if (sheet) {
				// 存储首行数据（城市名称）
				for (int col = 1; col <= sheet->lastCol(); col++) {
					CellType cellType = sheet->cellType(0, col);
					if (cellType == CELLTYPE_STRING) {
						const wchar_t* value = sheet->readStr(0, col);
						samplcity.push_back(value);

					}
					/*else {
						samplcity.push_back(L"");
					}*/
				}

				// 导出表格数据
				for (int row = 1; row < sheet->lastRow(); row++) { // 从第二行开始
					vector<wstring> rowData;
					for (int col = 1; col <= sheet->lastCol(); col++) { // 从第二列开始
						CellType cellType = sheet->cellType(row, col);
						if (cellType == CELLTYPE_STRING) {
							const wchar_t* value = sheet->readStr(row, col);
							rowData.push_back(value);

						}
						/*else {
							rowData.push_back(L"");
						}*/
					}
					dataMatrix.push_back(rowData); // 存储一行数据到矩阵中
				}
			}
			else {
				cerr << "Unable to get sheet" << endl;
			}
		}
		else {
			cerr << "Unable to load workbook" << endl;
		}
		book->release(); // 释放工作簿对象
	}
	else {
		cerr << "Unable to create workbook" << endl;
	}
}
void exportM(const wchar_t* filename, const vector<vector<wstring>>& dataMatrix, int startRow, int startCol) {
	// 创建新的 Excel 工作簿
	Book* book = xlCreateBook();
	// Configure your own LibXL license locally; embedded license removed.
	if (book) {
		// 添加新的工作表
		Sheet* sheet = book->addSheet(L"Sheet1");
		if (sheet) {
			// 将 dataMatrix 数据写入工作表
			for (size_t row = 0; row < dataMatrix.size(); ++row) {
				for (size_t col = 0; col < dataMatrix[row].size(); ++col) {
					sheet->writeStr(startRow + row, startCol + col, dataMatrix[row][col].c_str());
				}
			}
			// 保存工作簿到文件
			if (book->save(filename)) {
				wcout << L"File " << filename << L" has been created successfully." << endl;
			}
			else {
				cerr << "Failed to save the workbook." << endl;
			}
		}
		else {
			cerr << "Unable to create sheet." << endl;
		}
		book->release(); // 释放工作簿对象
	}
	else {
		cerr << "Unable to create workbook." << endl;
	}
}
void exportM(const wchar_t* filename, const vector<wstring>& datacol, int startRow, int startCol) {
	// 创建新的 Excel 工作簿
	Book* book = xlCreateBook();
	if (!book) {
		cerr << "Unable to create workbook." << endl;
		return;
	}

	// Configure your own LibXL license locally; embedded license removed.

	// 添加新的工作表
	Sheet* sheet = book->addSheet(L"Sheet1");
	if (!sheet) {
		cerr << "Unable to create sheet." << endl;
		book->release();
		return;
	}

	// 将 datacol 数据写入工作表
	for (size_t row = 0; row < datacol.size(); ++row) {
		if (!sheet->writeStr(startRow + row, startCol, datacol[row].c_str())) {
			cerr << "Failed to write to cell (" << startRow + row << ", " << startCol << ")." << endl;
		}
	}

	// 保存工作簿到文件
	if (book->save(filename)) {
		wcout << L" successfully." << endl;
	}
	else {
		cerr << "Failed to save the workbook." << endl;
	}

	book->release(); // 释放工作簿对象
}
void exportM(const wchar_t* filename, const vector<vector<double>>& dataMatrix, int startRow, int startCol) {
	// 创建新的 Excel 工作簿
	Book* book = xlCreateBook();
	// Configure your own LibXL license locally; embedded license removed.
	if (book) {
		// 添加新的工作表
		Sheet* sheet = book->addSheet(L"Sheet1");
		if (sheet) {
			// 将 dataMatrix 数据写入工作表
			for (size_t row = 0; row < dataMatrix.size(); ++row) {
				for (size_t col = 0; col < dataMatrix[row].size(); ++col) {
					wstring cellValue = std::to_wstring(dataMatrix[row][col]);
					sheet->writeStr(startRow + row, startCol + col, cellValue.c_str());
				}
			}
			// 保存工作簿到文件
			if (book->save(filename)) {
				wcout << L"File " << filename << L" has been created successfully." << endl;
			}
			else {
				cerr << "Failed to save the workbook." << endl;
			}
		}
		else {
			cerr << "Unable to create sheet." << endl;
		}
		book->release(); // 释放工作簿对象
	}
	else {
		cerr << "Unable to create workbook." << endl;
	}
}
void exportM(const wchar_t* filename, const vector<vector<int>>& dataMatrix, int startRow, int startCol) {
	// 创建新的 Excel 工作簿
	Book* book = xlCreateBook();
	// Configure your own LibXL license locally; embedded license removed.
	if (book) {
		// 添加新的工作表
		Sheet* sheet = book->addSheet(L"Sheet1");
		if (sheet) {
			// 将 dataMatrix 数据写入工作表
			for (size_t row = 0; row < dataMatrix.size(); ++row) {
				for (size_t col = 0; col < dataMatrix[row].size(); ++col) {
					wstring cellValue = std::to_wstring(dataMatrix[row][col]);
					sheet->writeStr(startRow + row, startCol + col, cellValue.c_str());
				}
			}
			// 保存工作簿到文件
			if (book->save(filename)) {
				wcout << L" has been created successfully." << endl;
			}
			else {
				cerr << "Failed to save the workbook." << endl;
			}
		}
		else {
			cerr << "Unable to create sheet." << endl;
		}
		book->release(); // 释放工作簿对象
	}
	else {
		cerr << "Unable to create workbook." << endl;
	}
}
bool anyvoice(wchar_t element_str, const vector<wstring> Voice) {
	bool found = false;
	for (const auto& voice : Voice) {
		if (voice.find(element_str) != wstring::npos) {
			found = true;
			break;
		}
	}
	return found;
}
bool ifinitial(wchar_t element) {
	vector<wstring> consonants = {
		L"ʰ", L"ŋ", L"ȵ", L"n", L"l", L"s", L"t", L"ʂ", L"Ø", L"ɕ", L"ŋ", L"ɣ", L"k",
		L"ʃ", L"ʒ", L"m", L"ɳ", L"x", L"c", L"ʔ", L"p", L"ʐ", L"z", L"ʷ", L"v", L"f",
		L"h", L"ɬ", L"ɸ", L"ɓ", L"b", L"d", L"ʈ", L"ʑ", L"ɖ", L"β", L"ɮ", L"θ", L"ð",
		L"ɻ", L"χ", L"ʁ", L"ɣ", L"ɦ", L"ɹ", L"ɗ"
	};
	if (anyvoice(element, consonants)) return TRUE;
	else return FALSE;
}
bool iftone(wchar_t element) {
	vector<wstring> consonants = { L"0" ,L"1" ,L"2" ,L"3" ,L"4" ,L"5" ,L"6" };
	if (anyvoice(element, consonants)) return TRUE;

	else return FALSE;
}
bool ifvowel(wchar_t element) {
	vector<wstring> voice_1 = { L"e",L"ʅ",L"ɿ",L"ɛ",L"œ",L"æ",L"a",L"ɑ",L"ᴀ",L"ø",L"ɘ",L"ə",L"ɵ",L"ɐ",L"ɞ",L"ɨ",L"ʉ",L"ɤ",L"o",L"ʌ",L"ɔ",L"ɒ",L"ɶ",L"ɚ",L"ɐ˞",L"a˞" };
	vector<wstring> voice_2 = { L"i",L"u",L"ʯ",L"ʮ",L"y",L"ɯ",L"ʊ",L"ʋ" };
	bool dv = anyvoice(element, voice_1);
	if (dv) dv = anyvoice(element, voice_1);
	return dv;
}
void cut(vector<vector<wstring>> Voicedata, vector<vector<wstring>>& initialdata, vector<vector<wstring>>& voweldata, vector<vector<wstring>>& tonedata) {
	for (size_t row = 0; row < Voicedata.size(); row++) {
		for (size_t col = 0; col < Voicedata[row].size(); col++) {
			const wstring& element = Voicedata[row][col];
			size_t element_str = element.size();
			bool if0 = true;
			bool if1 = true;

			for (size_t i = 0; i < element_str; i++) {
				wchar_t ch = element[i];

				if (i == 0 && ch == L'#') {

					initialdata[row][col] = L"Ø";
					if (element_str > 1) {

						voweldata[row][col] = element[1];
						if (element_str > 2) {

							tonedata[row][col] = element.substr(2);

						}
					}
					if0 = false;
					if1 = false;
					break;
				}

				if (ifinitial(ch) && if0) {
					initialdata[row][col] += ch;
				}
				else {
					if0 = false;
					if (iftone(ch)) {
						tonedata[row][col] += ch;
					}
					else {
						if (if1) {
							voweldata[row][col] += ch;
						}
					}
				}
			}
		}
	}
}
void cut2(vector<vector<wstring>> compoundata, vector<vector<wstring>>& preposdata, vector<vector<wstring>>& voweldata, vector<vector<wstring>>& taildata) {
	for (size_t row = 0; row < compoundata.size(); row++) {
		for (size_t col = 0; col < compoundata[row].size(); col++) {
			const wstring& element = compoundata[row][col];
			size_t element_str = element.size();

			for (size_t i = 0; i < element_str; i++) {
				wchar_t ch = element[i];
				if (element_str == 1) {
					preposdata[row][col] = L"0";
					voweldata[row][col] = ch;
					taildata[row][col] = L"0";
				}
				else if (element_str == 2 && ifvowel(ch)) {
					voweldata[row][col] = ch;
					if (element[0] != ch) {
						preposdata[row][col] = element[0];
						taildata[row][col] = L"0";
					}
					else {
						taildata[row][col] = element[1];
						preposdata[row][col] = L"0";
					}
				}

				else if (element_str == 3) {
					if (ifvowel(ch)) {
						voweldata[row][col] = ch;
						preposdata[row][col] = element[0];


						if (element[2] != L'˞' && element[2] != L'r')  taildata[row][col] = element[2];
						else voweldata[row][col] += element[2];
					}
				}
			}
		}
	}
}
void dataplus(vector<vector<wstring>>& data, vector<vector<wstring>>& data1, vector<vector<wstring>>& data2) {
	for (size_t row = 0; row < data1.size(); row++) {
		for (size_t col = 0; col < data1[0].size(); col++) {
			data[row][col] = data1[row][col] + data2[row][col];
		}
	}
}
void transformdata(
	vector<vector<vector<int>>>& changedata, vector<vector<wstring>>initialdata, vector<vector<wstring>>compoundata,
	vector<vector<wstring>>tonedata, vector<vector<wstring>>preposdata, vector<vector<wstring>>voweldata,
	vector<vector<wstring>>taildata, vector<vector<wstring>>iniposdata, vector<vector<wstring>>vowaildata
) {
	for (int k = 0; k < initialdata[0].size(); k++) {
		for (int i = 0; i < initialdata.size(); i++) {
			for (int j = i + 1; j < initialdata.size(); j++) {

				int sum = i * (2 * initialdata.size() - i - 1) * 0.5 + j - i - 1;

				changedata[0][k][sum] = (initialdata[i][k] == initialdata[j][k]) ? 1 : 0;
				changedata[1][k][sum] = (compoundata[i][k] == compoundata[j][k]) ? 1 : 0;
				changedata[2][k][sum] = (tonedata[i][k] == tonedata[j][k]) ? 1 : 0;
				changedata[3][k][sum] = (preposdata[i][k] == preposdata[j][k]) ? 1 : 0;
				changedata[4][k][sum] = (voweldata[i][k] == voweldata[j][k]) ? 1 : 0;
				changedata[5][k][sum] = (taildata[i][k] == taildata[j][k]) ? 1 : 0;
				changedata[6][k][sum] = (iniposdata[i][k] == iniposdata[j][k]) ? 1 : 0;
				changedata[7][k][sum] = (vowaildata[i][k] == vowaildata[j][k]) ? 1 : 0;

			}
		}
	}

	int dataSize = initialdata.size();
	int featureSize = initialdata[0].size();

	size_t totalSize = static_cast<size_t>(dataSize * (dataSize - 1) * 0.5);
	for (size_t s = 0; s < totalSize; ++s) {
		for (int feature = 0; feature < 8; ++feature) {
			vector<int> featureVector;
			for (int k = 0; k < featureSize; ++k) {
				featureVector.push_back(changedata[feature][k][s]);
			}
			int accsum = accumulate(featureVector.begin(), featureVector.end(), 0);
			if (accsum <= 3 || accsum >= changedata[0].size() - 3) {
				for (int k = 0; k < featureSize; ++k) {
					changedata[feature][k][s] = -1;
				}
			}
		}
	}

}
void calculate(vector<vector<vector<int>>> changedata, vector<vector<vector<double>>>& rate) {
	for (size_t k = 0; k < changedata.size(); k++) {
		for (size_t i = 0; i < changedata[0].size(); i++) {
			for (size_t j = 0; j < changedata[0].size(); j++) {
				double num_1 = 0.0; double num_2 = 0.0;
				for (size_t m = 0; m < changedata[0][0].size(); m++) {
					if (changedata[k][i][m] != -1) {
						if (changedata[k][i][m] == changedata[k][j][m] && changedata[k][i][m] != -1) num_1++;
						else num_2++;
					}
				}
				rate[k][i][j] = num_1 / (num_1 + num_2);
			}
		}
	}
}
void average(vector<vector<vector<double>>> rate_3d, vector<vector<double>>& rate, vector<double> weight) {
	for (size_t i = 0; i < rate_3d.size(); i++) {
		for (size_t j = 0; j < rate.size(); j++) {
			for (size_t k = 0; k < rate[j].size(); k++) {
				rate[j][k] += weight[i] * rate_3d[i][j][k];
			}
		}
	}
	double accsum = accumulate(weight.begin(), weight.end(), 0.0);
	for (size_t j = 0; j < rate.size(); j++) {
		for (size_t k = 0; k < rate[j].size(); k++) {
			rate[j][k] /= accsum;
		}
	}

}

int main()
{
	for (int km = 1; km <= 1; km++) {

		vector<vector<wstring>> Voicedata;
		vector<wstring> samplcity;
		wstring filePath = L"PATH";
		//filePath += to_wstring(km); 
		//filePath += L".xlsx";

		processExcel(filePath.c_str(), Voicedata, samplcity);
		vector<vector<wstring>> initialdata(Voicedata.size(), vector<wstring>(Voicedata[0].size()));
		vector<vector<wstring>> compoundata(Voicedata.size(), vector<wstring>(Voicedata[0].size()));
		vector<vector<wstring>> tonedata(Voicedata.size(), vector<wstring>(Voicedata[0].size()));

		vector<vector<wstring>> preposdata(Voicedata.size(), vector<wstring>(Voicedata[0].size()));
		vector<vector<wstring>> voweldata(Voicedata.size(), vector<wstring>(Voicedata[0].size()));
		vector<vector<wstring>> taildata(Voicedata.size(), vector<wstring>(Voicedata[0].size()));
		vector<vector<wstring>> iniposdata(Voicedata.size(), vector<wstring>(Voicedata[0].size()));
		vector<vector<wstring>> vowaildata(Voicedata.size(), vector<wstring>(Voicedata[0].size()));

		vector<vector<vector<int>>> changedata(8, vector<vector<int>>(Voicedata[0].size(), vector<int>(Voicedata.size() * (Voicedata.size() - 1) * 0.5)));
		vector<vector<vector<double>>> rate_3d(changedata.size(), vector<vector<double>>(Voicedata[0].size(), vector<double>(Voicedata[0].size())));
		vector<vector<double>> rate(Voicedata[0].size(), vector<double>(Voicedata[0].size()));


		cut(Voicedata, initialdata, compoundata, tonedata);

		cut2(compoundata, preposdata, voweldata, taildata);

		dataplus(iniposdata, initialdata, preposdata);
		dataplus(vowaildata, voweldata, taildata);
		vector<double> weight(8);
		weight[0] = 4.0; weight[1] = 4.0; weight[2] = 1.0; weight[3] = 1.0; weight[4] = 1.0; weight[5] = 1.0; weight[6] = 2.0; weight[7] = 2.0;
		transformdata(changedata, initialdata, compoundata, tonedata, preposdata, voweldata, taildata, iniposdata, vowaildata);
		calculate(changedata, rate_3d);

		average(rate_3d, rate, weight);
		wstring outPath = L"PATH2";
		//outPath += to_wstring(km); 
		//outPath += L".xlsx";
		exportM(outPath.c_str(), rate, 0, 0);
	}
	return 0;
}