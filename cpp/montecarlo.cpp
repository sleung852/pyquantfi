#include <math.h>

void run_mc_cpu(double* ST, const double &S, const double &sigma, const double &rate,
	const double &T, const int &n, const int &m, double* Zs) {
	double deltaT = T/n;
	double drift = exp((rate - 0.5*(pow(sigma, 2.0)))*deltaT);
	// for each stock path...
	for (int s_ind=0; s_ind<m; s_ind++) {
		// set initial stock price
		ST[s_ind] = S;
		// for each time period...
		for (int t=0; t<n; t++) {
			ST[s_ind] = ST[s_ind]* drift * exp(sigma * sqrt(deltaT) * Zs[s_ind*n + t]);
		}
	}
}
