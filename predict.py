import csv
import random
from collections import Counter, defaultdict
from itertools import combinations

def read_results(file_path):
    results = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            results.append([int(num) for num in row[1:]])
    return results

def weighted_random_selection(results):
    all_numbers = [num for sublist in results for num in sublist]
    number_counts = Counter(all_numbers)
    total = sum(number_counts.values())
    weights = {num: count / total for num, count in number_counts.items()}
    return random.choices(list(weights.keys()), weights=list(weights.values()), k=1)[0]

def historical_patterns(results):
    patterns = defaultdict(int)
    for result in results:
        for combination in combinations(result, 2):
            patterns[combination] += 1
    most_common_pattern = max(patterns, key=patterns.get)
    return random.choice(most_common_pattern)

def exclude_recently_drawn_numbers(results, n=5):
    recent_numbers = set(num for result in results[-n:] for num in result)
    all_numbers = set(range(1, 46))
    available_numbers = list(all_numbers - recent_numbers)
    return random.choice(available_numbers)

def balanced_distribution(results):
    low_cluster = range(1, 16)
    medium_cluster = range(16, 31)
    high_cluster = range(31, 46)
    clusters = [low_cluster, medium_cluster, high_cluster]
    return [random.choice(cluster) for cluster in clusters]

def combination_of_analyses(results):
    return [
        weighted_random_selection(results),
        historical_patterns(results),
        exclude_recently_drawn_numbers(results),
        balanced_distribution(results)[0]
    ]

def hot_and_cold_numbers(results):
    all_numbers = [num for sublist in results for num in sublist]
    number_counts = Counter(all_numbers)
    hot_numbers = [num for num, count in number_counts.most_common(5)]
    cold_numbers = [num for num, count in number_counts.most_common()[-5:]]
    return random.choice(hot_numbers + cold_numbers)

def number_pairs_and_triplets(results):
    pairs = Counter()
    triplets = Counter()
    for result in results:
        pairs.update(combinations(result, 2))
        triplets.update(combinations(result, 3))
    most_common_pair = max(pairs, key=pairs.get)
    most_common_triplet = max(triplets, key=triplets.get)
    return random.choice(most_common_pair + most_common_triplet)

def adjust_for_target_sum(predicted_numbers, target_sum):
    current_sum = sum(predicted_numbers)
    while current_sum != target_sum:
        if current_sum < target_sum:
            predicted_numbers.append(random.randint(1, 45))
        else:
            predicted_numbers.pop()
        current_sum = sum(predicted_numbers)
    return predicted_numbers

def user_defined_constraints(results, constraints):
    all_numbers = set(range(1, 46))
    for constraint in constraints:
        all_numbers &= set(constraint)
    # if not all_numbers:
    #     all_numbers = set(range(1, 46))  # Fallback to the full range if no numbers match the constraints

    print(all_numbers)

    return random.choice(list(all_numbers))

def predict_results(results):
    predictions = set()
    predictions.add(weighted_random_selection(results))
    predictions.add(historical_patterns(results))
    predictions.add(exclude_recently_drawn_numbers(results))
    predictions.update(balanced_distribution(results))
    predictions.update(combination_of_analyses(results))
    predictions.add(hot_and_cold_numbers(results))
    predictions.add(number_pairs_and_triplets(results))
    
    # Adjust for target sum
    most_common_sums = analyze_sum_of_numbers(results)
    target_sum = most_common_sums[0][0]
    predictions = adjust_for_target_sum(list(predictions), target_sum)
    
    # Apply user-defined constraints (example constraints)
    constraints = [range(1, 46)]
    predictions.append(user_defined_constraints(results, constraints))
    
    # Ensure the predictions list has only 6 items
    predictions = list(set(predictions))[:6]
    
    return sorted(predictions)

def analyze_sum_of_numbers(results):
    sums = [sum(result) for result in results]
    sum_counts = Counter(sums)
    most_common_sums = sum_counts.most_common()
    return most_common_sums

def main():
    file_path = 'result.csv'
    results = read_results(file_path)
    predicted_numbers = predict_results(results)
    print("Predicted Numbers:")
    print(predicted_numbers)

if __name__ == "__main__":
    main()
