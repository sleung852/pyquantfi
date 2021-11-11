#include "kernel.h"
#include <stdexcept>
#include <algorithm>
#include <math.h>

// declare function to be ran in the GPU
__global__ void monte_carlo_sim(double* d_St, const double* d_Zs, const double* d_drift, const double* d_sigma,
	const double* d_deltaT, const int* d_n, const int* d_m) {

	// get thread, block ids and block dim
    const unsigned tid = threadIdx.x;
    const unsigned bid = blockIdx.x;
    const unsigned bsz = blockDim.x;

    // create stock_index
    int idx = tid + bid * bsz;

    // for each simluated stock
    if (idx < *d_m) {
		int t = 0;
		while (t < *d_n) {
    		// compute stock price from previous stock price 
    		d_St[idx] = d_St[idx] * (*d_drift) * exp((*d_sigma) * sqrt(*d_deltaT) * d_Zs[idx*(*d_n) + t]);
			t++;
    	}
    }
}

// function to setup running Monte Carlo Simulation in the GPU
void run_mc_cuda(double* ST, double S, double sigma, double rate, double T, int n,
	int m, double* Zs) {

	// assign values in the CPU
	double deltaT = T/n;
	double drift = exp((rate - 0.5*(pow(sigma, 2.0)))*T/n);
	for (size_t i=0; i<m; i++) ST[i] = S; 

	// declarations for variables in the GPU
	//array
	double* d_St = nullptr;
	double* d_Zs = nullptr;
	// double and int
	double* d_sigma = nullptr;
	double* d_deltaT = nullptr;
	double* d_drift = nullptr;
	int* d_n = nullptr;
	int* d_m = nullptr;

	// memory allocations in GPU
	// array
	cudaMalloc((void **) &d_Zs, n*m*sizeof(double));
	cudaMalloc((void **) &d_St, m*sizeof(double));
	// double & int
	cudaMalloc(&d_sigma, sizeof(double));
	cudaMalloc(&d_deltaT, sizeof(double));
	cudaMalloc(&d_drift, sizeof(double));
	cudaMalloc(&d_n, sizeof(int));
	cudaMalloc(&d_m, sizeof(int));

	// copy values from host (CPU) to device (GPU)
	// array
	cudaMemcpy(d_Zs, Zs, n*m*sizeof(double), cudaMemcpyHostToDevice);
	cudaMemcpy(d_St, ST, m*sizeof(double), cudaMemcpyHostToDevice);
	// double & int
	cudaMemcpy(d_sigma, &sigma, sizeof(double), cudaMemcpyHostToDevice);
	cudaMemcpy(d_deltaT, &deltaT, sizeof(double), cudaMemcpyHostToDevice);
	cudaMemcpy(d_drift, &drift, sizeof(double), cudaMemcpyHostToDevice);
	cudaMemcpy(d_n, &n, sizeof(int), cudaMemcpyHostToDevice);
	cudaMemcpy(d_m, &m, sizeof(int), cudaMemcpyHostToDevice);

	// Use either 128 or 256 for THREADS_PER_BLOCK
	int TPB = 1024;
	
	// invoke the Monte Carlo kernel
	monte_carlo_sim<<<(m+TPB-1)/TPB,TPB>>>(d_St, d_Zs, d_drift, d_sigma, d_deltaT, d_n, d_m);

	// copy the results from the device (GPU) back to the host (CPU)
	cudaMemcpy(ST, d_St, m*sizeof(double), cudaMemcpyDeviceToHost);

	// free device memory
	cudaFree(d_Zs);
	cudaFree(d_St);
	cudaFree(d_sigma);
	cudaFree(d_deltaT);
	cudaFree(d_drift);
	cudaFree(d_n);
	cudaFree(d_m);
}
