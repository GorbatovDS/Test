#ifndef ARRAY_TYPES_H

#define ARRAY_TYPES_H
#include <memory>
#include <utility>
#include <cstring>

using ptrdiff_t = std::ptrdiff_t;

template <class T>
class Vec final
{
    private:
    ptrdiff_t len;
    std::shared_ptr<T[]> data;

    public:
    Vec(ptrdiff_t n) : len(n), data(new T[n]) {};
    ~Vec() = default;
    ptrdiff_t length() {return len;}
    T* raw_ptr() {return data.get();}
    T& operator()(ptrdiff_t idx) {return data[idx];}
};

template <class T>
class Matrix final
{
    private:
    ptrdiff_t nr_, nc_;
    std::shared_ptr<T[]> data;

    public:
    Matrix(ptrdiff_t nr, ptrdiff_t nc) : nr_(nr), nc_(nc), data(new T[nr*nc]) {};
    ~Matrix() = default;
    ptrdiff_t length() {return nr_ * nc_;}
    ptrdiff_t nrows() {return nr_;}
    ptrdiff_t ncols() {return nc_;}
    T* raw_ptr() {return data.get();}
    T& operator()(ptrdiff_t row, ptrdiff_t col) {return data[row * nc_ + col];}
    T& operator()(ptrdiff_t idx) {return data[idx];}
    Vec<T> row(ptrdiff_t);
    Vec<T> col(ptrdiff_t);
};

template <class T>
Vec<T> Matrix<T>::row(ptrdiff_t r)
{
    Vec<T> v(nc_);
    std::memcpy(v.raw_ptr(), raw_ptr() + r * nc_, nc_ * sizeof(T));
    return v;
}

template <class T>
Vec<T> Matrix<T>::col(ptrdiff_t c)
{
    Vec<T> v(nr_);
    for(ptrdiff_t i=0; i < nr_; i++)
    {
        v(i) = data[i * nc_ + c];
    }
    return v;
}

#endif
