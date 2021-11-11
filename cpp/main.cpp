#include <chrono>
#include <iostream>
#include <math.h>
#include <cuda_runtime.h>
#include <curand.h>
#include <boost/math/distributions/normal.hpp>

#include "kernel.h"
#include "montecarlo.h"
#include "sobol.hpp"

using namespace std;

/*
Utilities Function
*/
// function that returns a arithimatic mean
double arith_mean(double* arr, int size) {
    double mean = 0;
    for (size_t i=0; i<size; i++) {
        mean += arr[i];
    }
    return mean/size;
}
// function that returns a geometric mean
double geo_mean(double* arr, int size) {
    double log_mean = 0;
    for (size_t i=0; i<size; i++) {
        log_mean += log(arr[i])/size;
    }
    return exp(log_mean);
}

/*
Random Number Generator
*/
void quasi_random_number_1d(double* rand_nums, const int &size, const int &skip) {
    /*
    rand_nums: output array for holding the quasi numbers
    size: the size of the output array
    skip: no of values to skip
    */
    boost::math::normal norm; 
    double* quasi_seq = i8_sobol_generate(1, size, skip);

    for (int i=0; i<size; i++)
        rand_nums[i] = (quantile(complement(norm, quasi_seq[i]))); // compute the ppf
}

/*
Monte Carlo Simulation
*/
int main() {

    double S = 100; // initial stock price
    double sigma = 0.3; // variance
    double rate = 0.05; // interest rate
    double T = 3; // no of years
    double K = 100; // strike price
    int n = 50; // no of step (num of time)
    int m = 1000000; // no of path (num of simulations)

    try {
        double* Zs = new double[n*m]; // declare a quasi random variables array
        quasi_random_number_1d(Zs, n*m, 1); // generate quasi random varibles
        double* ST_gpu = new double[m]; // declare an array for simluated stock price at time T
        double* ST_cpu = new double[m]; // declare an array for simluated stock price at t ime T

        double gpu_start=double(clock())/CLOCKS_PER_SEC;
        run_mc_cuda(ST_gpu, S, sigma, rate, T, n, m, Zs); // run simulations in GPU
        double gpu_end=double(clock())/CLOCKS_PER_SEC;

        double cpu_start=double(clock())/CLOCKS_PER_SEC;
        run_mc_cpu(ST_cpu, S, sigma, rate, T, n, m, Zs);
        double cpu_end=double(clock())/CLOCKS_PER_SEC;

        cout<<"****************** INPUTS ****************\n";
        cout<<"Initial Stock Price: " << S << "\n";
        cout<<"              Sigma: " << sigma << "\n";
        cout<<"      Interest Rate: " << rate << "\n";
        cout<<"                  T: " << T << "\n";
        cout<<"        No of steps: " << n << "\n";
        cout<<"  No of simulations: " << m << "\n";
        cout<<"****************** OUTPUTS ***************\n";
        cout<<"GPU Stock Price: " << arith_mean(ST_gpu, m) << "\n";
        cout<<"CPU Stock Price: " << arith_mean(ST_cpu, m) << "\n";        
        cout<<"******************* TIME *****************\n";
        cout<<"GPU Monte Carlo Computation: " << (gpu_end-gpu_start)*1e3 << " ms\n";
        cout<<"CPU Monte Carlo Computation: " << (cpu_end-cpu_start)*1e3 << " ms\n";
        cout<<"******************* END *****************\n";

        // delete[] Zs;
        delete[] ST_gpu;
        delete[] ST_cpu;
    }

    catch(exception& e) {
        cout << "exception: " << e.what() << endl;
    }
    
    return 0;
}
