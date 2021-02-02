#ifndef ARRAY_OPERATIONS_H
#define ARRAY_OPERATIONS_H

#include "array_types.hpp"


template <class T>
Matrix<T> matmul(Matrix<T> mat1, Matrix<T> mat2) {
    Matrix<T> product(mat1.nrows(), mat2.ncols());

#pragma omp parallel for
    for (ptrdiff_t i = 0; i < mat1.nrows(); i++) {
        for (ptrdiff_t j = 0; j < mat2.ncols(); j++) {
            product(i, j) = 0;
        }

        for (ptrdiff_t k = 0; k < mat1.ncols(); k++) {
            for (ptrdiff_t j = 0; j < mat2.ncols(); j++) {
                product(i, j) += mat1(i, k) * mat2(k, j);
            }
        }
    }

    return product;
}

template <class T>
Matrix<T> matsum(Matrix<T> mat1, Matrix<T> mat2) {
    Matrix<T> sum(mat1.nrows(), mat2.ncols());

    for (ptrdiff_t i = 0; i < mat1.nrows(); i++) {
        for (ptrdiff_t j = 0; j < mat2.ncols(); j++) {
            sum(i, j) = mat1(i, j) + mat2(i, j);
        }
    }

    return sum;
}

template <class T>
Matrix<T> matsubtract(Matrix<T> mat1, Matrix<T> mat2) {
    Matrix<T> difference(mat1.nrows(), mat2.ncols());

    for (ptrdiff_t i = 0; i < mat1.nrows(); i++) {
        for (ptrdiff_t j = 0; j < mat2.ncols(); j++) {
            difference(i, j) = mat1(i, j) - mat2(i, j);
        }
    }

    return difference;
}

template <class T>
Matrix<T> transpose(Matrix<T> mat) {
    Matrix<T> transposed(mat.ncols(), mat.nrows());

    for (ptrdiff_t i = 0; i < transposed.nrows(); i++) {
        for (ptrdiff_t j = 0; j < transposed.ncols(); j++) {
            transposed(i, j) = mat(j, i);
        }
    }

    return transposed;
}

template <class T>
bool check_decomposition(Matrix<T> mat1, Matrix<T> mat2, double eps = 1e-5) {
    for (ptrdiff_t i = 0; i < mat1.nrows(); i++) {
        for (ptrdiff_t j = 0; j < mat1.ncols(); j++) {
            if (abs(mat1(i, j) - mat2(i, j)) > eps) {
                return false;
            }
        }
    }
    return true;
}

#endif
