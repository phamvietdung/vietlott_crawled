import csv
import argparse
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import random

def read_results(file_path):
    results = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            results.append([int(num) for num in row[1:]])
    return results

def analyze_number_distribution_over_time(results):
    number_distribution = defaultdict(list)
    for draw_index, result in enumerate(results):
        for number in result:
            number_distribution[number].append(draw_index + 1)
    return number_distribution

def analyze_most_common_winning_numbers(results):
    all_numbers = [num for sublist in results for num in sublist]
    number_counts = Counter(all_numbers)
    most_common = number_counts.most_common()
    return most_common

def analyze_consecutive_numbers(results):
    consecutive_counts = Counter()
    for result in results:
        for i in range(len(result) - 1):
            if result[i] + 1 == result[i + 1]:
                consecutive_counts[(result[i], result[i + 1])] += 1
    most_common_consecutive = consecutive_counts.most_common()
    return most_common_consecutive

def plot_number_distribution_over_time(number_distribution):
    plt.figure(figsize=(12, 8))
    for number, appearances in number_distribution.items():
        plt.plot(appearances, [number] * len(appearances), 'o', label=f'Number {number}')
    
    plt.xlabel('Draw Number')
    plt.ylabel('Lottery Number')
    plt.title('Number Distribution Over Time')
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    plt.grid(True)
    plt.show()

def analyze_odd_even_distribution(results):
    odd_count = 0
    even_count = 0
    for result in results:
        for number in result:
            if number % 2 == 0:
                even_count += 1
            else:
                odd_count += 1
    return odd_count, even_count

def analyze_number_position(results):
    position_counts = [Counter() for _ in range(len(results[0]))]
    for result in results:
        for i, number in enumerate(result):
            position_counts[i][number] += 1
    return position_counts

def analyze_gaps_between_numbers(results):
    gap_counts = Counter()
    for result in results:
        sorted_result = sorted(result)
        for i in range(len(sorted_result) - 1):
            gap = sorted_result[i + 1] - sorted_result[i]
            gap_counts[gap] += 1
    return gap_counts

def analyze_clusters(results):
    low_cluster = range(1, 16)
    medium_cluster = range(16, 31)
    high_cluster = range(31, 46)
    cluster_counts = {'low': 0, 'medium': 0, 'high': 0}
    for result in results:
        for number in result:
            if number in low_cluster:
                cluster_counts['low'] += 1
            elif number in medium_cluster:
                cluster_counts['medium'] += 1
            elif number in high_cluster:
                cluster_counts['high'] += 1
    return cluster_counts

def analyze_time_between_appearances(results):
    last_seen = {}
    time_between = defaultdict(list)
    for draw_index, result in enumerate(results):
        for number in result:
            if number in last_seen:
                time_between[number].append(draw_index + 1 - last_seen[number])
            last_seen[number] = draw_index + 1
    average_time_between = {number: sum(times) / len(times) for number, times in time_between.items()}
    return average_time_between

def analyze_sum_of_numbers(results):
    sums = [sum(result) for result in results]
    sum_counts = Counter(sums)
    most_common_sums = sum_counts.most_common()
    return most_common_sums

def predict_results(results):
    # Analyze most common winning numbers
    most_common_numbers = analyze_most_common_winning_numbers(results)
    top_common_numbers = [number for number, count in most_common_numbers[:10]]

    # Analyze time between appearances
    average_time_between = analyze_time_between_appearances(results)
    top_time_between_numbers = sorted(average_time_between, key=average_time_between.get)[:10]

    # Analyze sum of numbers
    most_common_sums = analyze_sum_of_numbers(results)
    target_sum = most_common_sums[0][0]

    # Analyze odd and even distribution
    odd_count, even_count = analyze_odd_even_distribution(results)
    target_odd_count = odd_count // len(results)
    target_even_count = even_count // len(results)

    # Combine analyses to predict results
    predicted_numbers = set()
    while len(predicted_numbers) < 6:
        if len(predicted_numbers) < target_odd_count:
            number = random.choice([num for num in top_common_numbers if num % 2 != 0])
        else:
            number = random.choice([num for num in top_common_numbers if num % 2 == 0])
        predicted_numbers.add(number)

    # Adjust to match the target sum
    current_sum = sum(predicted_numbers)
    while current_sum != target_sum:
        if current_sum < target_sum:
            number = random.choice([num for num in top_time_between_numbers if num not in predicted_numbers])
            predicted_numbers.add(number)
        else:
            predicted_numbers.pop()
        current_sum = sum(predicted_numbers)

    return sorted(predicted_numbers)

def main():
    parser = argparse.ArgumentParser(description="Analyze Vietlott results")
    subparsers = parser.add_subparsers(dest="command")

    dist_parser = subparsers.add_parser("distribution", help="Analyze number distribution over time")
    common_parser = subparsers.add_parser("common", help="Analyze most common winning numbers")
    consecutive_parser = subparsers.add_parser("consecutive", help="Analyze consecutive numbers")
    odd_even_parser = subparsers.add_parser("odd_even", help="Analyze odd and even number distribution")
    position_parser = subparsers.add_parser("position", help="Analyze number position frequencies")
    gap_parser = subparsers.add_parser("gap", help="Analyze gaps between consecutive numbers")
    cluster_parser = subparsers.add_parser("cluster", help="Analyze number clusters")
    time_between_parser = subparsers.add_parser("time_between", help="Analyze time between appearances of numbers")
    predict_parser = subparsers.add_parser("predict", help="Predict lottery results")

    args = parser.parse_args()

    file_path = 'result.csv'
    results = read_results(file_path)

    if args.command == "distribution":
        number_distribution = analyze_number_distribution_over_time(results)
        plot_number_distribution_over_time(number_distribution)
    elif args.command == "common":
        most_common_numbers = analyze_most_common_winning_numbers(results)
        print("Most Common Winning Numbers:")
        for number, count in most_common_numbers:
            print(f"Number {number}: {count} times")
    elif args.command == "consecutive":
        consecutive_numbers = analyze_consecutive_numbers(results)
        print("Consecutive Number Analysis:")
        for pair, count in consecutive_numbers:
            print(f"Consecutive Pair {pair}: {count} times")
    elif args.command == "odd_even":
        odd_count, even_count = analyze_odd_even_distribution(results)
        print(f"Odd Numbers: {odd_count} times")
        print(f"Even Numbers: {even_count} times")
    elif args.command == "position":
        position_counts = analyze_number_position(results)
        for i, counter in enumerate(position_counts):
            print(f"Position {i + 1} Analysis:")
            for number, count in counter.most_common():
                print(f"Number {number}: {count} times")
    elif args.command == "gap":
        gap_counts = analyze_gaps_between_numbers(results)
        print("Gap Analysis:")
        for gap, count in gap_counts.most_common():
            print(f"Gap {gap}: {count} times")
    elif args.command == "cluster":
        cluster_counts = analyze_clusters(results)
        print("Cluster Analysis:")
        for cluster, count in cluster_counts.items():
            print(f"{cluster.capitalize()} Cluster: {count} times")
    elif args.command == "time_between":
        average_time_between = analyze_time_between_appearances(results)
        print("Time Between Appearances Analysis:")
        for number, avg_time in sorted(average_time_between.items()):
            print(f"Number {number}: {avg_time:.2f} draws")
    elif args.command == "predict":
        predicted_numbers = predict_results(results)
        print("Predicted Numbers:")
        print(predicted_numbers)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
