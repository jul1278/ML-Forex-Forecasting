// ProcessPairs.cpp

#include <iterator>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cstring>
#include <vector>
#include <chrono>
#include <ctime>
#include <stdint.h>
#include <stdlib.h>
#include <algorithm>

unsigned int numHeaders = 6;
const unsigned int bufferSize = 2 * 2048;

//----------------------------------------------------------------------------------------------------------------
// Name: DateTimePrice
//----------------------------------------------------------------------------------------------------------------
struct DateTimePrice {
	uint16_t year;
	
	uint8_t month;
	uint8_t day;
	uint8_t hour;
	uint8_t minute;
	uint8_t second;

	uint32_t millisec;

	uint32_t quote; 

	//----------------------------------------------------------------------------------------------------------------
	// Name: operator>
	// Desc:
	//----------------------------------------------------------------------------------------------------------------
	bool operator>(const DateTimePrice& other) {
		uint64_t a = MsProduct(*this);
		uint64_t b = MsProduct(other); 

		return (a > b); 
	}

	//----------------------------------------------------------------------------------------------------------------
	// Name: operator<
	// Desc:
	//----------------------------------------------------------------------------------------------------------------
	bool operator<(const DateTimePrice& other) {
		uint64_t a = MsProduct(*this);
		uint64_t b = MsProduct(other); 

		return (a < b); 
	}

	//----------------------------------------------------------------------------------------------------------------
	// Name: operator==
	// Desc:
	//----------------------------------------------------------------------------------------------------------------
	bool operator==(const DateTimePrice& other) {
		return memcmp(this, &other, sizeof(DateTimePrice)) == 0; 
	}

private:

	//----------------------------------------------------------------------------------------------------------------
	// Name: operator>
	// Desc:
	//----------------------------------------------------------------------------------------------------------------
	inline static uint64_t MsProduct(const DateTimePrice& dateTimePrice)
	{
		uint64_t a = dateTimePrice.millisec;
		if (dateTimePrice.second > 0) a *= dateTimePrice.second; 
		if (dateTimePrice.minute > 0) a *= dateTimePrice.minute; 
		if (dateTimePrice.hour > 0) a *= dateTimePrice.hour;
		if (dateTimePrice.day > 0) a *= dateTimePrice.day;
		if (dateTimePrice.month > 0) a *= dateTimePrice.month; 
		if (dateTimePrice.year > 0) a *= dateTimePrice.year; 

		return a; 
	}

};

//-------------------------------------------------------------------------------------------------------------------
// Name: DateTimePricePair
// Desc:
//-------------------------------------------------------------------------------------------------------------------
struct DateTimePricePair {	
	DateTimePrice dateTimePrice;
	uint32_t pairQuote;

	//----------------------------------------------------------------
	// DateTimePricePair
	//----------------------------------------------------------------
	DateTimePricePair() {}

	//----------------------------------------------------------------
	// DateTimePricePair
	//----------------------------------------------------------------
	DateTimePricePair(DateTimePrice& dateTimePrice) {
		memcpy(&this->dateTimePrice, &dateTimePrice, sizeof(DateTimePrice)); 
	}
};

//----------------------------------------------------------------------------------------------------------
// Name: StreamReadBlock
// Desc:
//----------------------------------------------------------------------------------------------------------
std::vector<DateTimePrice> StreamReadBlock(std::string& filename) {

	std::ifstream filestream(filename);

	if (!filestream.is_open()) {
		
		std::cout << "Error opening file."; 
		return std::vector<DateTimePrice>();
	}

	std::vector<DateTimePrice> dateTimePrices;
	dateTimePrices.clear(); 

	char buffer[bufferSize];
	memset(buffer, 0, sizeof(buffer));

	// We want to ignore the headers so discard characters until the first newline
	unsigned int offset = 0;
	while (filestream.get() != '\n') {
		offset++;
	}

	unsigned int bufferOffset = 0; 
	unsigned int headerCounter = 0; 

	DateTimePrice dateTimePrice;
	
	while (filestream) {

		filestream.read(&buffer[bufferOffset], sizeof(buffer) - bufferOffset);
		unsigned int lastCommaIndex = 0; 

		for (auto i = 0; i < sizeof(buffer); i++) {

			// read until we find a ',' then insert a null terminator
			if (buffer[i] == ',' || buffer[i] == '\n') {
				
				char lastChar = buffer[i];
				buffer[i] = 0; 

				if (headerCounter == 3) {

					unsigned int year;
					unsigned int month;
					unsigned int day;
					unsigned int hour;
					unsigned int minute;
					unsigned int second;
					unsigned int millisec;

					// datetime
#ifdef _MSC_VER
					sscanf_s(&buffer[lastCommaIndex], "%d-%d-%d %d:%d:%d.%d", &year, &month, &day, &hour, &minute, &second, &millisec); 
#else
					sscanf(&buffer[lastCommaIndex], "%d-%d-%d %d:%d:%d.%d", &year, &month, &day, &hour, &minute, &second, &millisec); 
#endif
					dateTimePrice.year = year;
					dateTimePrice.month = month;
					dateTimePrice.day = day;
					dateTimePrice.hour = hour;
					dateTimePrice.minute = minute;
					dateTimePrice.second = second;
					dateTimePrice.millisec = millisec / 1000000UL;

				} else if (headerCounter == 4) {

					// do this to avoid constructing an std::string
					char bidStrBuffer[32];
					unsigned int counter = lastCommaIndex; 
					unsigned int copyCounter = 0; 

					while (buffer[counter]) {
						if (buffer[counter] != '.') {
							bidStrBuffer[copyCounter] = buffer[counter]; 
							copyCounter++; 
						}

						counter++; 
					}

					bidStrBuffer[copyCounter] = 0; 

					dateTimePrice.quote = std::atoi(bidStrBuffer);
					dateTimePrices.push_back(dateTimePrice);
				}

				if (headerCounter >= (numHeaders - 1) || lastChar == '\n') {
					headerCounter = 0;

				} else {

					headerCounter++;
				}

				lastCommaIndex = i + 1; // plus one because we want the element after
			}
			// we're at the last element
			else {
				
				if (i == sizeof(buffer) - 1) {

					// copy the remaining characters back to the beginning of the buffer
					memcpy(buffer, &buffer[lastCommaIndex], i - lastCommaIndex + 1);
					bufferOffset = i - lastCommaIndex + 1; 

					lastCommaIndex = 0; 
				}
			}

		}
	}

	filestream.close();
	return dateTimePrices;
}

//---------------------------------------------------------------------------------------------------------------------
// Name: PricePairs
// Desc:
//---------------------------------------------------------------------------------------------------------------------
void SavePricePairs(std::string& file1, std::string file2) {
    
	auto file1Prices = StreamReadBlock(file1); 
    auto file2Prices = StreamReadBlock(file2); 

	auto f1Index = 0;
	auto f2Index = 0; 

	std::vector<DateTimePricePair> pairs; 

	if (file1Prices[f1Index] > file2Prices[f2Index]) {
		
		// file 1 first datetime occurs after the first datetime of file 2
		while (file2Prices[f2Index] < file1Prices[f1Index]) {
			f2Index++; 
		}

	} else {

		// file 2 first datetime occurs after the first datetime of file 1
		while (file1Prices[f1Index] < file2Prices[f2Index]) {
			f1Index++; 
		}
	}

	uint32_t quote1Last = 0;
	uint32_t quote2Last = 0; 

	while(f1Index < file1Prices.size() && f2Index < file2Prices.size()) {

		DateTimePricePair pair; 

		// put file1Price[] and file2Price[] into output array
		if (file1Prices[f1Index] > file2Prices[f2Index]) {

			// update f2 price
			f2Index++;
		} else {

			// update f1 price
			f1Index++; 
		}
		
		pairs.push_back(pair);
	}

	// write to file
	std::ofstream outStream("pairs.csv");
	outStream << "date_time, quote_1, quote_2\n"; 

	if (outStream.is_open()) {

		for (auto pair : pairs) {

			outStream << std::setfill('0') << std::setw(4) << std::to_string(pair.dateTimePrice.year) << "-";
			outStream << std::setw(2) << std::to_string(pair.dateTimePrice.month) << "-";
			outStream << std::setw(2) << std::to_string(pair.dateTimePrice.day) << " ";
			outStream << std::setw(2) << std::to_string(pair.dateTimePrice.hour) << ":";
			outStream << std::setw(2) << std::to_string(pair.dateTimePrice.minute) << ":";
			outStream << std::setw(2) << std::to_string(pair.dateTimePrice.second) << ".";
			outStream << std::to_string(pair.dateTimePrice.millisec) << ", ";
			outStream << std::to_string(pair.dateTimePrice.quote) << ", ";
			outStream << std::to_string(pair.pairQuote) << "\n"; 
		}
	}

	outStream.close(); 
}

//----------------------------------------------------------------------------------------------------------------
// Name:
// Desc: 
//----------------------------------------------------------------------------------------------------------------
int main(int argc, char** argv) {
	if (argc < 3) {
		std::cout << "need two file paths as arguments"; 
		return 0;
	}

	std::string file1 = argv[1]; 
	std::string file2 = argv[2]; 

	SavePricePairs(file1, file2); 

	return 0; 
}


