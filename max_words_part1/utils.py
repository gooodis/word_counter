import os
from heapq import heappush, heappop


def get_top_n_frequent(words, n):
    """
    :type words: Trie[str]
    :type n: int
    :rtype: List[tupe]
    """
    if words is None or len(words) == 0:
        return []
    PQ = []
    for key in words:
        heappush(PQ, (-words[key], key))
    return [heappop(PQ) for _ in range(n)]


def get_text_files_from_paths(paths):
    text_files_path = []
    for path in paths:
        if os.path.isdir(path):
            for dirpath, unused_dirnames, filenames in os.walk(path):
                for filename in filenames:
                    if filename.split('.')[-1] == 'txt':
                        text_files_path.append(os.path.join(dirpath, filename))
        elif path.split('.')[-1] == 'txt':
            text_files_path.append(os.path.join(dirpath, filename))
        else:
            print('Error: could not find folder/text file.')
    return text_files_path
