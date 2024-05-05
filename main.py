from libraries.json import massive

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)

    for i, c1 in enumerate(s1):
        current_row = [i + 1]

        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row

    return previous_row[-1]

def closest_word(target_word, word_list, used_words):
    closest = None
    min_distance = float('inf')

    for word in word_list:
        if len(word) == len(target_word) and word not in used_words:
            distance = levenshtein_distance(target_word, word)
            if distance < min_distance:
                closest = word
                min_distance = distance
            elif distance == min_distance and closest is not None:
                closest = min(closest, word)

    if closest is not None:
        used_words.add(closest)
    return closest if min_distance <= (len(target_word) - 1) else "Слово не найдено!"

words = massive().load_words_from_json()
iterations = 51
target_word = "крем"
used_words = set()

def generate_branch(iterations, target_word, used_words):
    branch = []
    for i in range(iterations):
        closest = closest_word(target_word, words, used_words)
        branch.append(closest)
        target_word = closest
    return branch

branches = {}
for i in range(1, 5):
    branches[i] = generate_branch(iterations, target_word, used_words)
    print(f"Ветка {i}:")
    for j, word in enumerate(branches[i]):
        print(f"[{j}] Ближайшее слово:", word)
    print()