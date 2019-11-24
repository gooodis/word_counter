import re
from heapq import heappush, heappop

import datefinder


def parse_date(line):
    """
    Parsed date if it exist in the line
    :param line:
    :return: datetime object if date parsed succefully else None
    """
    parsed_dates = list(datefinder.find_dates(line))
    if parsed_dates:
        return parsed_dates[0]


def get_top_n_frequent(words, n):
    """
    Get the 'n' most frequent words in the Trie
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


def get_chunks(l, n):
    """Yield successive n-sized chunks from l."""
    return [l[i:i + n] for i in range(0, len(l), n)]


def merge_intervals(intervals):
    """
    This function receive list of intervals and return overlapping time ranges
    :param intervals:
    :return: List[overlapping intervals]
    """
    intervals.sort(key=lambda interval: interval[0])
    merged = [intervals[0]]
    for current in intervals:
        previous = merged[-1]
        if current[0] <= previous[1]:
            previous[1] = max(previous[1], current[1])
        else:
            merged.append(current)
    print(f'Merged intervals: {merged}')
    return merged


def find_legal_date(line):
    retval = []
    pattern = '([0-2][0-9]:[0-5][0-9]:[0-5][0-9])'
    if re.search(pattern, line):
        splitted_line = re.split(pattern, line)
        for sub_line in splitted_line:
            retval.append(sub_line)
            if re.search(pattern, sub_line):
                break
    return ''.join(retval)
