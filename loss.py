
def hamming_distance(first: str, second: str) -> int:
    return len([1 for (x, y) in zip(first, second) if x != y])


if __name__ == '__main__':
    pass
