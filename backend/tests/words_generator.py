import sys
from pathlib import Path
import random
import string
import itertools

sys.path.append(str(Path(__file__).parent.parent))

from app.api.usage import calculate_message_credits


def gen_word(vowels_include=False, length=None, is_palindrome=False):
    if length is None:
        length = random.randint(1, 10)

    if vowels_include:
        chars = string.ascii_lowercase
    else:
        chars = "".join(c for c in string.ascii_lowercase if c not in "aeiou")

    if is_palindrome:
        if length % 2 == 0:
            half_length = length // 2
            half_word = "".join(random.choices(chars, k=half_length))
            return half_word + half_word[::-1]
        else:
            half_length = length // 2
            half_word = "".join(random.choices(chars, k=half_length))
            middle_char = random.choice(chars)
            return half_word + middle_char + half_word[::-1]
    else:
        return "".join(random.choices(chars, k=length))


def generate_test_cases():
    test_cases = []

    # Helper function to generate words of specific lengths
    def gen_word(length):
        return "".join(random.choices(string.ascii_lowercase, k=length))

    # Base cases
    test_cases.extend(["", "a", "ab", "abc"])

    # Word length multipliers
    for length in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        test_cases.append(gen_word(length))

    # Multiple words with different length multipliers
    word_combinations = list(
        itertools.product(["a", "the", "cat", "word", "elephant"], repeat=3)
    )
    test_cases.extend(
        [" ".join(combo) for combo in word_combinations[:10]]
    )  # Limit to 10 combinations

    # Third vowels
    vowels = "aeiou"
    for i in range(1, 4):
        word = list("x" * (i * 3))
        word[2::3] = random.choices(vowels, k=i)
        test_cases.append("".join(word))

    # Length penalty
    test_cases.extend(["a" * length for length in [99, 100, 101, 105]])

    # Unique word bonus (single word)
    test_cases.extend(["Unique", "Supercalifragilisticexpialidocious"])

    # Palindromes
    palindromes = [
        "A man a plan a canal Panama",
        "race a car",
        "Madam Im Adam",
        "Able was I ere I saw Elba",
        "Never odd or even",
        "Do geese see God",
    ]
    test_cases.extend(palindromes)

    # Complex cases
    test_cases.extend(
        [
            "The quick brown fox jumps over the lazy dog",
            "Hello, world! This is a test message with punctuation.",
            "a'b-c",
            "ThisIsAVeryLongWordWithNoSpacesAndLotsOfUppercaseLetters",
        ]
    )

    # Random cases
    for _ in range(10):
        word_count = random.randint(1, 5)
        message = " ".join(gen_word(random.randint(1, 10)) for _ in range(word_count))
        test_cases.append(message)

    return test_cases


# def run_generated_tests():
#     test_cases = generate_test_cases()
#     for case in test_cases:
#         result = calculate_message_credits(case)
#         print(f"Input: {case}")
#         print(f"Result: {result}")
#         print("---")

if __name__ == "__main__":
    test_cases = generate_test_cases()
    # for case in test_cases:
    #     result = calculate_message_credits(case)
    #     print(f"Input: {case}")
    #     print(f"Result: {result}")
    #     print("---")
    # print(gen_word(False, 50, False))
    print(gen_word(False, 10, True))
