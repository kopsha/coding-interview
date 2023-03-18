#include <iostream>
#include <iomanip>
#include <cmath>
#include <vector>

using namespace std;

/*
32
000073af 00000000
*/

void computeSmallPrimeList()
{
	// generate all prime numbers that fit into 16 bits
	unsigned long q;
	unsigned long r;
	vector<bool> isPrime( 0xFFFF, true );
	vector<unsigned int> primeList;

	isPrime[0] = false;

	for (q = 2; q <= 0xFFFF-1; q++)
	{
		if (isPrime[q])
		{
			// remove all multiples of q
			r = q;
			do {
				r += q;
				isPrime[r] = false;
			} while (r < 0xFFFF);
		}
	}

	primeList.reserve( 6543 );
	for (q = 2; q < 0xFFFF-1; q++)
		if (isPrime[q])
			primeList.push_back( q );

	cout << endl << "primeList = {" << hex;
	for (q = 0; q < primeList.size(); q++)
	{
		if ((q % 16)==0)
			cout << endl << "\t";
		cout << "0x" << setw(4) << setfill('0') << primeList[q] << ", ";
	}

	cout << endl << "};" << endl;
}

int main()
{
	unsigned long n = 29615;
	n = 0xFFFFFFFF;
	cout << "size of big int: " << sizeof(n)*8 << endl;
	cout << "attempting to decompose: " << n << endl;
	unsigned long top = lround(sqrt(n));
	cout << "sqrt: " << top << endl;

	cout << "n is 0x" << setw(8) << setfill('0') << hex << n << endl;
	computeSmallPrimeList();

	return 0;
}