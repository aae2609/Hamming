#!/usr/bin/env python


"""
(31, 26) Hamming code

data   G    codeword
1x26 26x31 = 1x31
1*k  k*n     1*n

H = (I, P)
G = (P.t, I)
"""

import scipy.stats as st
import pandas as pd
import csv
import os

from random import sample


class Hamming(object):

    def __init__(self, n, k, file_name='hamming.txt', size_of_sample=100):
        self.G = []  # Generative matrix of code
        # self.H = []  # Parity check matrix
        self.n = n  # codeword length
        self.k = k  # data length
        self.file_name = file_name  # where data will been written
        self.size_of_sample = size_of_sample  # quantity words in sample

    @staticmethod
    def show_matrix(M):
        for s in M:
            print(s)

    def int_to_bin_str(self, num):
        return bin(num)[2:].zfill(self.k)

    def err_to_bin_str(self, id_err):
        return bin(2 ** id_err)[2:].zfill(self.n)[::-1]

    def create_error_iter(self):
        uniform = st.uniform(loc=0, scale=self.n-1)
        return uniform.rvs(size=self.size_of_sample)

    def create_data_iter(self):
        return sample(range(2**self.k), self.size_of_sample)
#         uniform = st.uniform(loc=0, scale=2**self.k)
#         return uniform.rvs(size=self.size_of_sample)

    def encode_hamming(self, num):
        str_data = self.int_to_bin_str(num)
        codeword = ''.join([str(bin(int(i, 2) & int(str_data, 2)).count('1') % 2) for i in self.G])
        return codeword

    def choose_bits_to_spoil(self, count):
        return sample(range(self.n + 1), count)
    
    @staticmethod
    def add_error(codeword, num_err):
        return codeword[:num_err] + str(1 - int(codeword[num_err])) + codeword[num_err + 1:]

    def make_data_and_write(self, clean_words, count_errors, filename):
        with open(filename, 'w', newline='\n') as file:
            out = csv.writer(file, delimiter=';')
            # fieldnames = ('id', 'plainword', 'codeword', 'id_error', 'bin_error', 'defective_codeword')
            for word in clean_words:
                str_word = self.int_to_bin_str(int(word))
                codeword = self.encode_hamming(int(word))
                err_list = self.choose_bits_to_spoil(count_errors)
                for j in err_list:
                    if j == self.n:
                        out.writerow((str(str_word), codeword, -1, '0' * self.n, codeword))
                        continue
                    ind_error = j
                    bin_error = self.err_to_bin_str(j)
                    codeword_err = self.add_error(codeword, ind_error)
                    out.writerow((str(str_word), codeword, ind_error, bin_error, codeword_err))

    @staticmethod
    def get_matrix_from_txt(filename):
        file = open(filename, 'r', newline='\n')
        M = []
        for line in file:
            M.append(line[:-1])
        return M

    @staticmethod
    def get_matrix_from_csv(filename):
        M = pd.read_csv(filename, header=None)
        M = [''.join(line) for line in M.values.T.astype(str)]
        return M

    def get_matrix(self, filename):
        extension = os.path.splitext(filename)[1]
        if extension == '.txt':
            M = self.get_matrix_from_txt(filename)
        elif extension == '.csv':
            M = self.get_matrix_from_csv(filename)
        return M

    def run(self, filename, generative_matrix, count_errors):
        self.G = self.get_matrix(generative_matrix)
        # self.H = self.get_matrix('h.txt')

        clean_words = self.create_data_iter()
        # errors = self.create_error_iter()
        self.make_data_and_write(clean_words, count_errors, filename)


def write_for_maple(string):
    print('[', ', '.join(string), ']')


def main():
    # encoder = Hamming(n=31, k=26, size_of_sample=2 ** 16)
    # encoder.run(filename='hamming.txt', generative_matrix='g.txt', count_errors=32)

    encoder = Hamming(n=16, k=11, size_of_sample=2 ** 11)
    encoder.run(filename='hamming_15_11_all_sys.txt', generative_matrix='g_16_11_systematic.csv', count_errors=17)

    # encoder = Hamming(n=16, k=11, size_of_sample=2 ** 9)
    # encoder.run(filename='hamming_15_11.txt', generative_matrix='g_16_11_nonsystematic.csv', count_errors=10)

    print('Done.')


if __name__ == '__main__':
    main()
    # write_for_maple('10011101111')
    # write_for_maple('1011100111101111')


