#ifndef _MONTECARLO_H_
#define _MONTECARLO_H_

void run_mc_cpu(double* ST, const double &S, const double &sigma, const double &rate,
	const double &T, const int &n, const int &m, double* Zs);

#endif