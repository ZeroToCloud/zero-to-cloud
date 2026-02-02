#!/usr/bin/env python3
import random
import re
import sys
from collections import defaultdict, Counter
from pathlib import Path


def tokenize(text: str):
    # words + keep simple punctuation as tokens
    return re.findall(r"[A-Za-z']+|[.!?]", text.lower())


def build_chain(tokens, n=2):
    """
    n=2 means bigrams: (w1, w2) -> Counter(next_word)
    """
    chain = defaultdict(Counter)
    if len(tokens) < n + 1:
        return chain

    for i in range(len(tokens) - n):
        state = tuple(tokens[i : i + n])
        nxt = tokens[i + n]
        chain[state][nxt] += 1
    return chain


def weighted_choice(counter: Counter):
    # counter: word -> count
    total = sum(counter.values())
    r = random.randint(1, total)
    cum = 0
    for word, count in counter.items():
        cum += count
        if r <= cum:
            return word
    # fallback (shouldn't happen)
    return random.choice(list(counter.keys()))


def generate(chain, n=2, max_tokens=60):
    if not chain:
        return ""

    state = random.choice(list(chain.keys()))
    out = list(state)

    for _ in range(max_tokens - n):
        options = chain.get(tuple(state))
        if not options:
            break

        nxt = weighted_choice(options)
        out.append(nxt)

        # stop nicely on sentence end
        if nxt in [".", "!", "?"] and len(out) > 8:
            break

        state = out[-n:]

    # clean spacing around punctuation
    text = " ".join(out)
    text = re.sub(r"\s+([.!?])", r"\1", text)
    return text


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 src/markov.py data/input.txt [n=2] [max_tokens=60]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    n = int(sys.argv[2]) if len(sys.argv) >= 3 else 2
    max_tokens = int(sys.argv[3]) if len(sys.argv) >= 4 else 60

    text = input_path.read_text(encoding="utf-8", errors="ignore")
    tokens = tokenize(text)
    chain = build_chain(tokens, n=n)

    print(generate(chain, n=n, max_tokens=max_tokens))


if __name__ == "__main__":
    main()
