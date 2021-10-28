#include <iostream>
#include <string>
#include <random>
#include <vector>
#include <math.h>

#include <boost/math/distributions/normal.hpp>

#include "halton.hpp"

using namespace std;

/*
Utilities Function
*/

double arith_mean(vector<double> values_vec) {
	double mean = 0;
	for (double v: values_vec) {
		mean += v/values_vec.size();
	}
	return mean;
}

double geo_mean(vector<double> values_vec) {
	double log_mean = 0;
	for (double v: values_vec) {
		log_mean += log(v)/values_vec.size();
	}
	return exp(log_mean);
}

/*
Random Number Generator
*/

vector<vector<double>> quasi_random_number(int n, int m, int seed) {

	boost::math::normal norm;

	double* quasi_seq = halton(seed, n*m);
	vector<vector<double>> rand_nums(m, vector<double> (n, 0));

	for (int mi=0; mi<m; mi++){
		for (int ni=0; ni<n; ni++){
			double halton_num = *(quasi_seq+mi+ni);
			rand_nums[mi][ni] = quantile(complement(norm, halton_num));
		}
	}

	return rand_nums;
}

vector<double> quasi_random_number_1d(int size, int skip) {
    boost::math::normal norm;
    const int LIMIT = 1600;
    int dim = 1;
    double* quasi_seq = halton(dim, LIMIT);
    int count = 0;

    vector<double> rand_nums;

    while (true) {
        quasi_seq = halton(dim, LIMIT);
        for (int i=0; i<LIMIT; i=i+skip){
            halton_num = *(quasi_seq+i);
            quasi_num = quantile(complement(norm, halton_num));
            count++;
            if (count >= size) break;
        }
        dim += 1;
    }
    cout << endl;
    return rand_nums;
}

vector<vector<double>> pseudo_random_number_2d(int n, int m, int seed) {
	std::default_random_engine generator(seed);
	std::normal_distribution<double> distribution (0.0,1.0);

	vector<vector<double>> rand_nums(m, vector<double> (n, 0));

	for (int mi=0; mi<m; mi++){
		for (int ni=0; ni<n; ni++){
			rand_nums[mi][ni] = distribution(generator);
		}
	}

	return rand_nums;
}



/*
Monte Carlo Simulation
*/

double compute_growth_factor(const double &drift, const double &sigma, const double &deltaT, const double &Z) {
	return drift * exp(sigma * sqrt(deltaT) * Z);
}

vector<vector<double>> monte_carlo_simulate(double S, double sigma, double rate, double T, double K, int n, int m, int seed=1126) {
	/*
	S - stock price
	sigma - stock variance
	rate - discount rate
	T - time periods
	K - strike price
	n - number of simulation period
	m - number of simulations
	*/

	double deltaT = T/n;
	double drift = exp(rate - 0.5*(pow(sigma, 2.0))*deltaT);

	// vector<vector<double>>  Zs = pseudo_random_number(n, m, seed);
	vector<vector<double>>  Zs = quasi_random_number(n, m, seed);

	double growth_factor;
	vector<vector<double>> S_path(m, vector<double> (n, 0));

	for (int mi=0; mi<m; mi++) {
		vector<double> Z = Zs.at(mi);
		double growth_factor = compute_growth_factor(drift, sigma, deltaT, Z.at(0));
		S_path[mi][0] = S * growth_factor;
		for (int ni=1; ni<n; ni++) {
			growth_factor = compute_growth_factor(drift, sigma, deltaT, Z.at(ni));
			S_path[mi][ni] = growth_factor * S_path[mi][ni-1];
		}
	}
	return S_path;
}

int main() {

 	vector<vector<double>> stock_paths = monte_carlo_simulate(100, 0.2, 0.02, 3, 95, 10, 10);

  	for (int x=0; x<stock_paths.size(); x++) {
  		for (int y=0; y<stock_paths[0].size(); y++) {
  			std::cout << stock_paths[x][y] << " ";
  		}
  		std::cout << std::endl;
  	}

  	// vector<vector<double>>  Zs = quasi_random_number(100, 10, 10);

  	// for (int x=0; x<Zs.size(); x++) {
  	// 	for (int y=0; y<Zs[0].size(); y++) {
  	// 		std::cout << Zs[x][y] << " ";
  	// 	}
  	// 	std::cout << std::endl;
  	// } 	

	return 0;
}