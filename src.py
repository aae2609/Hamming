"""
1x20 20x25 = 1x25
1*k  k*n     1*n

G = (I, P)
H = (P.t, I)

H = (A, I_)
G = (I, A.t)

"""

import scipy.stats as st
import csv


class Hamming():

    def __init__(self, n, k, file_name='hamming.txt', h=0, q=0, generate_h_q=True, size_of_sample=100):
        self.G = []  # generative matrix of code
        self.n = n  # codeword length
        self.k = k  # data length
        self.file_name = file_name  # where data will been written
        self.size_of_sample = size_of_sample  # quantity words in sample

        if (generate_h_q):
            self.choose_h_q()
        else:
            self.h = h  # step of diviation in kernel in G
            self.q = q  # quantity of using bits

    def choose_h_q(self):
        for h in range(self.k):
            for q in range(self.k):
                if ((self.n - self.k - 1) * h + q) == self.k \
                        and q * (self.n - self.k) > self.k:
                    self.h = h
                    self.q = q
                    break

    def create_str_H(self):
        self.H = [bin(i)[2:].zfill(self.n-self.k) for i in range(self.n)]
        self.show_matr(self.H)


    def create_str_G_with_H(self):
        A = [s for s in self.H]



    def create_str_G(self):
        I = [bin(2 ** (i))[2:].zfill(self.k) for i in range(self.k)][::-1]
        P = []
        for i in range(self.n - self.k):
            a = sum([2 ** (self.h * i + j) for j in range(self.q)])
            P.append(bin(a)[2:].zfill(self.k))
        P.reverse()
        I.extend(P)
        self.G = I
        self.show_matr(I)

    def show_matr(self, M):
        for s in M:
            print(s)

    def int_to_bin_str(self, num):
        return bin(num)[2:].zfill(self.k)

    def err_to_bin_str(self, id_err):
        return bin(2 ** id_err)[2:].zfill(self.n)[::-1]

    def create_error_iter(self):
        uniform = st.uniform(loc=0, scale=self.n)
        return uniform.rvs(size=self.size_of_sample)

    def create_data_iter(self):
        uniform = st.uniform(loc=0, scale=2 ** (self.k))
        return uniform.rvs(size=self.size_of_sample)

    def encode_hamming(self, num):
        str_data = self.int_to_bin_str(num)
        codeword = ''.join([str(bin(int(i, 2) & int(str_data, 2)).count('1') % 2) for i in self.G])
        return codeword

    def add_error(self, codeword, num_err):
        return codeword[:num_err] + str(1 - int(codeword[num_err])) + codeword[num_err+1:]

    def make_data_and_write(self, clean_words, errors):
        with open('hamming.txt', 'w', newline='\n') as file:
            out = csv.writer(file, delimiter=';')
            # fieldnames = ('id', 'plainword', 'codeword', 'id_error', 'bin_error', 'defective_codeword')
            for i, word in enumerate(clean_words):
                str_word = self.int_to_bin_str(int(word))
                codeword = self.encode_hamming(int(word))
                ind_error = int(errors[i])
                bin_error = self.err_to_bin_str(int(errors[i]))
                codeword_err = self.add_error(codeword, ind_error)

                out.writerow((i, str(str_word), codeword, ind_error, bin_error, codeword_err))

    def run(self):
        self.create_str_H()
        # self.create_str_G()
        # clean_words = self.create_data_iter()
        # errors = self.create_error_iter()
        # self.make_data_and_write(clean_words, errors)



def main():
    encoder = Hamming(n=36, k=30, generate_h_q=True, size_of_sample=2**16)
    encoder.run()


if __name__ == '__main__':
    main()
