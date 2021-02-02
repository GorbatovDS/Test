#include <iostream>
#include <fstream>
#include <omp.h>
#include <cmath>
#include "array_types.hpp"
#include "array_operations.hpp"
#include "cholesky_decomposition.hpp"

using namespace std;

int main(int argc, const char * argv[]) {
    char fname[256]{"matrix_100x100.txt"};

    if (argc > 1) strcpy(fname, argv[1]);
    ifstream stream(fname);

    ptrdiff_t n = 0;
    stream >> n;

    Matrix<double> mat(n, n);

    for (ptrdiff_t i = 0; i < n; i++) {
        for (ptrdiff_t j = 0; j < n; j++) {
            stream >> mat(i, j);
        }
    }

    int r = n / 10;
    if (argc > 2) r = stoi(argv[2]);

    cout << "Executing Cholesky block decomposition..." << endl;
    double start = omp_get_wtime();
    Matrix<double> factor = decompose_cholesky_block(mat, r);
    double finish = omp_get_wtime();
    cout << "Time spent: " << finish - start << '\n' << endl;

    cout << "Validating decomposition..." << endl;
    Matrix<double> result = matmul(factor, transpose(factor));

    cout << "Decomposed succesfully: " << boolalpha << check_decomposition(mat, result) << endl;

    return 0;
}
