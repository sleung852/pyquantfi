#include "kernel.h"
#include <stdexcept>
#include <algorithm>
#include <math.h>

// declare function to be ran in the GPU
__global__ void monte_carlo_sim(double* d_ST, const double* d_Zs,
	const double* d_S, const double* d_drift, const double* d_sigma,
	const double* d_deltaT, const int* d_n, const int* d_m);

// function to setup running Monte Carlo Simulation in the GPU
void run_mc(double* ST, double S, double sigma, double rate, double T, int n,
	int m, double* Zs) {

	// declare ptr values in the CPU
	double* h_S;
	double* h_sigma;
	double* h_deltaT;
	double* h_drift;
	int* h_n;
	int* h_m;

	// create ptr values in the hash
	h_S = new double;
	h_sigma = new double;
	h_deltaT = new double;
	h_drift = new double;
	h_n = new int;
	h_m = new int;

	// assign values in the CPU
	*h_S = S;
	*h_sigma = sigma;
	*h_deltaT = T/n;
	*h_drift = exp(rate - 0.5*(pow(sigma, 2.0))*T/n);
	*h_n = n;
	*h_m = m;

	// declarations for variables in the GPU
	//array
	double* d_ST = nullptr;
	double* d_Zs = nullptr;
	// double and int
	double* d_S;
	double* d_sigma;
	double* d_deltaT;
	double* d_drift;
	int* d_n;
	int* d_m;

	// memory allocations in GPU
	// array
	cudaMalloc((void**)&d_Zs, n*m*sizeof(double));
	cudaMalloc((void**)&d_ST, m * sizeof(double));
	// double & int
	cudaMalloc(&d_S, sizeof(double));
	cudaMalloc(&d_sigma, sizeof(double));
	cudaMalloc(&d_deltaT, sizeof(double));
	cudaMalloc(&d_drift, sizeof(double));
	cudaMalloc(&d_n, sizeof(int));
	cudaMalloc(&d_m, sizeof(int));

	// copy values from host (CPU) to device (GPU)
	// array
	cudaMemcpy(d_Zs, Zs, n*m*sizeof(double), cudaMemcpyHostToDevice);
	cudaMemcpy(d_ST, ST, m*sizeof(double), cudaMemcpyHostToDevice);
	// double & int
	cudaMemcpy(d_S, h_S, sizeof(double), cudaMemcpyHostToDevice);
	cudaMemcpy(d_sigma, h_sigma, sizeof(double), cudaMemcpyHostToDevice);
	cudaMemcpy(d_deltaT, h_deltaT, sizeof(double), cudaMemcpyHostToDevice);
	cudaMemcpy(d_drift, h_drift, sizeof(double), cudaMemcpyHostToDevice);
	cudaMemcpy(d_n, h_n, sizeof(int), cudaMemcpyHostToDevice);
	cudaMemcpy(d_m, h_m, sizeof(int), cudaMemcpyHostToDevice);

	// calculate the threads and blocks for the GPU
	int threadsPerBlock,blocksPerGrid;
	if (n*m<1024){
		threadsPerBlock = n*m;
		blocksPerGrid   = 1;
	} else {
		threadsPerBlock = 1024;
		blocksPerGrid   = ceil(double(n*m)/double(threadsPerBlock));
	}

	// invoke the Monte Carlo kernel
	monte_carlo_sim<<<blocksPerGrid,threadsPerBlock>>>(d_ST, d_Zs,
		d_S, d_drift, d_sigma, d_deltaT, d_n, d_m);

	// copy the results from the device (GPU) back to the host (CPU)
	cudaMemcpy(ST, d_ST, m*sizeof(double), cudaMemcpyDeviceToHost);

	// free device memory
	cudaFree(d_Zs);
	cudaFree(d_ST);
	cudaFree(d_S);
	cudaFree(d_sigma);
	cudaFree(d_deltaT);
	cudaFree(d_drift);
	cudaFree(d_n);
	cudaFree(d_m);

	// free host memory
	delete[] Zs;
	delete h_S;
	delete h_sigma;
	delete h_deltaT;
	delete h_drift;
	delete h_n;
	delete h_m;
}


__global__ void monte_carlo_sim(double* d_ST, const double* d_Zs,
	const double* d_S, const double* d_drift, const double* d_sigma,
	const double* d_deltaT, const int* d_n, const int* d_m) {

	// get thread, block ids and block dim
    const unsigned tid = threadIdx.x;
    const unsigned bid = blockIdx.x;
    const unsigned bsz = blockDim.x;

    // create stock_index and time_index
    int s_idx = tid + bid * bsz;
    int n_idx = tid + bid * bsz;

    double S = *d_S;

    // for each simluated stock
    if (s_idx < *d_m) {
    	int ni = 0;
    	do {
    		// compute stock price from previous stock price 
    		S = S * *d_drift * exp(*d_sigma * sqrt(*d_deltaT) * d_Zs[n_idx]);
    	}
    	// while time has not reached T
    	while (ni < *d_n);
    	d_ST[s_idx] = S;
    }
}