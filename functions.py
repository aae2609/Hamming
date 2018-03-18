import pandas as pd


TRAIN_PATH = "/content/drive/Hamming/dataset_files/hamming.txt"

COLUMN_NAMES = ['id', 'plainword', 'codeword', 
                'id_error', 'bin_error', 'defective_codeword']

def hamming_distance(first: str, second: str) -> int:
	return len([1 for (x, y) in zip(first, second) if x != y])


def loss_hamming(y, y_pred):
	return sum(hamming_distance(f,s) for (f,s) in zip(y, y_pred)) / y.shape[0]


def load_data():
	data = pd.read_csv(TRAIN_PATH, sep=';', names=COLUMN_NAMES)

	# make features
	data['dec_defective_codeword'] = data['defective_codeword'][:].apply(lambda x: int(x, 2))
	for j in range(len(data['defective_codeword'][0])):
		data['bin_' + str(j)] = data['defective_codeword'][:].apply(lambda x: int(x[j]))
	data['dec_plainword'] = data['plainword'][:].apply(lambda x: int(x, 2))
	return data


def split_data(test_size):
	train_data, test_data, train_labels, test_labels = \
	model_selection.train_test_split(data.loc[:, 'dec_defective_codeword':'bin_30'], 
										data['id_error'], 
										test_size = test_size)	
	return train_data, test_data, train_labels, test_labels
