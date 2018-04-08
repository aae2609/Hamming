"""
(31, 26) Hamming code

data   G    codeword
1x26 26x31 = 1x31
1*k  k*n     1*n

H = (I, P)
G = (P.t, I)

"""
import scipy.stats as st
import csv


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
        uniform = st.uniform(loc=0, scale=2**self.k)
        return uniform.rvs(size=self.size_of_sample)

    def encode_hamming(self, num):
        str_data = self.int_to_bin_str(num)
        codeword = ''.join([str(bin(int(i, 2) & int(str_data, 2)).count('1') % 2) for i in self.G])
        return codeword

    @staticmethod
    def add_error(codeword, num_err):
        return codeword[:num_err] + str(1 - int(codeword[num_err])) + codeword[num_err + 1:]

    def make_data_and_write(self, clean_words, errors):
        with open('hamming.txt', 'w', newline='\n') as file:
            out = csv.writer(file, delimiter=';')
            # fieldnames = ('id', 'plainword', 'codeword', 'id_error', 'bin_error', 'defective_codeword')
            for word in clean_words:
                str_word = self.int_to_bin_str(int(word))
                codeword = self.encode_hamming(int(word))
                out.writerow((str(str_word), codeword, -1, '0' * 31, codeword))
                for j in range(0, 31):
                    ind_error = j
                    bin_error = self.err_to_bin_str(j)
                    codeword_err = self.add_error(codeword, ind_error)
                    out.writerow((str(str_word), codeword, ind_error, bin_error, codeword_err))
    @staticmethod
    def get_matrix(filename):
        file = open(filename, 'r', newline='\n')
        M = []
        for line in file:
            M.append(line[:-2])

        return M

    def run(self):
        self.G = self.get_matrix('g.txt')
        # self.H = self.get_matrix('h.txt')
        clean_words = self.create_data_iter()
        errors = self.create_error_iter()
        self.make_data_and_write(clean_words, errors)


def main():
    encoder = Hamming(n=31, k=26, size_of_sample=2 ** 16)
    encoder.run()


if __name__ == '__main__':
    main()
