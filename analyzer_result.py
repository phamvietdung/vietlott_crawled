import csv
import argparse
from collections import Counter
from itertools import combinations

def read_results(file_path):
    results = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            results.append([int(num) for num in row[1:]])
    return results

def analyze_frequency_results(results):
    all_numbers = [num for sublist in results for num in sublist]
    number_counts = Counter(all_numbers)
    most_common = number_counts.most_common()
    return most_common

def analyze_pair_frequency_results(results):
    pair_counts = Counter()
    for result in results:
        pairs = combinations(result, 2)
        pair_counts.update(pairs)
    most_common_pairs = pair_counts.most_common()
    return most_common_pairs

def analyze_triplet_frequency_results(results):
    triplet_counts = Counter()
    for result in results:
        triplets = combinations(result, 3)
        triplet_counts.update(triplets)
    most_common_triplets = triplet_counts.most_common()
    return most_common_triplets

def analyze_never_appearing_pairs(results):
    all_numbers = set(num for sublist in results for num in sublist)
    all_pairs = set(combinations(all_numbers, 2))
    appearing_pairs = set()

    for result in results:
        pairs = combinations(result, 2)
        appearing_pairs.update(pairs)

    never_appearing_pairs = all_pairs - appearing_pairs
    return never_appearing_pairs

def analyze_sum_of_numbers(results):
    sums = [sum(result) for result in results]
    sum_counts = Counter(sums)
    most_common_sums = sum_counts.most_common()
    return most_common_sums

def main():
    parser = argparse.ArgumentParser(description="Analyze Vietlott results")
    subparsers = parser.add_subparsers(dest="command")

    freq_parser = subparsers.add_parser("frequency", help="Analyze single number frequencies")
    pair_freq_parser = subparsers.add_parser("pair_frequency", help="Analyze pair frequencies")
    never_pair_parser = subparsers.add_parser("never_pairs", help="Analyze pairs that never appear together")
    triplet_freq_parser = subparsers.add_parser("triplet_frequency", help="Analyze triplet frequencies")
    sum_parser = subparsers.add_parser("sum", help="Analyze sum of numbers")

    args = parser.parse_args()

    file_path = 'result.csv'
    results = read_results(file_path)

    if args.command == "frequency":
        frequencies = analyze_frequency_results(results)
        print("Number Frequency Analysis:")
        for number, count in frequencies:
            print(f"Number {number}: {count} times")
    elif args.command == "pair_frequency":
        pair_frequencies = analyze_pair_frequency_results(results)
        print("\nPair Frequency Analysis:")
        for pair, count in pair_frequencies:
            print(f"Pair {pair}: {count} times")
    elif args.command == "never_pairs":
        never_appearing_pairs = analyze_never_appearing_pairs(results)
        print("\nPairs that never appear together:")
        for pair in never_appearing_pairs:
            print(f"Pair {pair}")
    elif args.command == "triplet_frequency":
        triplet_frequencies = analyze_triplet_frequency_results(results)
        print("\nTriplet Frequency Analysis:")
        for triplet, count in triplet_frequencies:
            print(f"Triplet {triplet}: {count} times")
    elif args.command == "sum":
        sum_frequencies = analyze_sum_of_numbers(results)
        print("\nSum of Numbers Analysis:")
        for sum_value, count in sum_frequencies:
            print(f"Sum {sum_value}: {count} times")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
