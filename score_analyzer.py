import json
import numpy as np


class Analyzer(object):

    def __init__(self, path_to_scores):
        with open(path_to_scores, 'r') as file:
            self.scores = np.array(json.load(file))

        self.accuracies = []
        self.best_params = {}

    def process_scores(self):
        numbers = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6}
        for score in self.scores:
            for key in score['choice'].keys():
                score[key] = score['choice'][key]
            score['layers'] = numbers[score['layers']]
            score.pop('choice', None)
            score.pop('acuracy', None)  # due to bag

    def get_accuracies(self):
        for idx, score in enumerate(self.scores):
            self.accuracies.append((score['accuracy'], idx))
        self.accuracies.sort()

    def choose_best_params(self, count_voters=7):
        top_idx = self.accuracies[-count_voters:]  # sorted by accuracy list of tuples: (accuracy, idx)
        top_idx = list(list(zip(*top_idx))[1])  # list of indices

        for param in self.scores[0].keys():
            # TODO: Think over the default value in .get()
            cur_params_list = [score.get(param, None) for score in self.scores[top_idx]]
            cur_best_param = max(set(cur_params_list), key=cur_params_list.count)  # majority vote
            self.best_params[param] = cur_best_param

    def write_best_to_file(self, filename='./best_params.json'):
        with open(filename, 'w') as out:
            json.dump(self.best_params, out, indent=4)

    def run(self):
        self.process_scores()
        self.get_accuracies()
        self.choose_best_params()
        self.write_best_to_file()


def main():
    analyzer = Analyzer(path_to_scores='./scores.json')
    analyzer.run()


if __name__ == "__main__":
    main()
