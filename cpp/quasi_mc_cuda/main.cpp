#include <chrono>
#include <iostream>
#include <string>
#include <random>
#include <vector>
#include <math.h>
#include <cuda_runtime.h>
#include <curand.h>
#include <boost/math/distributions/normal.hpp>

#include "kernel.h"
#include "halton.hpp"

using namespace std;

/*
Utilities Function
*/
// function that returns a arithimatic mean
double arith_mean(vector<double> values_vec) {
    double mean = 0;
    for (double v: values_vec) {
        mean += v/values_vec.size();
    }
    return mean;
}
// function that returns a geometric mean
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
void quasi_random_number_1d(double* rand_nums, int size, int skip) {
    /*
    rand_nums: output array for holding the quasi numbers
    size: the size of the output array
    skip: no of values to skip
    */

    boost::math::normal norm; 
    int count = 0; // nth value
    int dim = 1; // initial dimension
    const int LIMIT = 1600; // dimension limit

    // declare placeholders
    double halton_num;
    float quasi_num;
    double* quasi_seq;

    while (true) {
        quasi_seq = halton(dim, LIMIT);
        for (int i=0; i<LIMIT; i=i+skip){
            halton_num = *(quasi_seq+i);
            rand_nums[count] = (quantile(complement(norm, halton_num))); // compute the ppf
            count++;
            if (count >= size) break;
        }
        dim += 1;
    }
}

/*
Monte Carlo Simulation
*/
int main() {

    double S = 100; // initial stock price
    double sigma = 0.2; // variance
    double rate = 0.02; // interest rate
    double T = 3; // no of years
    double K = 95; // strike price
    int n = 10; // no of step (num of time)
    int m = 10; // no of path (num of simulations)

    try {
        double Zs [n*m]; // declare a quasi random variables array
        quasi_random_number_1d(Zs, n*m, 2); // generate quasi random varibles
        double ST [m]; // declare an array for simluated stock price at time T

        run_mc(ST, S, sigma, rate, T, n, m, Zs); // run simulations in GPU

        // print values
        for (int i=0; i<m; i++) {
            cout << ST[i] << " ";
        }
        cout << endl;
    }
    catch(exception& e) {
        cout << "exception: " << e.what() << endl;
    }



    return 0;
}