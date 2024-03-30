import concurrent.futures
from collections import Counter
import subprocess
from pathlib import Path
import random
import json

from rich.progress import track

BASE_PATH = Path(__file__).resolve().parent
OUT_FILE = BASE_PATH / 'deck_benchmark.json'
CARD_NAMES = ('plus1', 'plus5', 'plus10', 'mult3', 'mult10', 'div5', 'div10')
N_GAMES = 15

CUSTOM_DECKS = [
    dict(
        plus1=4,
        plus5=5,
        plus10=3,
        mult3=6,
        mult10=3,
        div5=2,
        div10=1,
    ),
    dict(
        plus1=3,
        plus5=4,
        plus10=3,
        mult3=4,
        mult10=4,
        div5=4,
        div10=2,
    )
]


def serialize_deck(deck):
    return ','.join(f"{k}={v}" for k, v in deck.items())


def run_game(deck, opponent, n_runs):
    for _ in range(3):
        try:
            res = subprocess.run(
                ['python', 'benchmark_jankas.py', f'--n_runs={n_runs}',
                 f'--bottom_agent={opponent}', f'--deck={serialize_deck(deck)}'],
                stdout=subprocess.PIPE,
                timeout=20,
            )
        except subprocess.TimeoutExpired:
            continue
        res.check_returncode()
        return tuple(map(int, res.stdout.decode('utf-8').strip().split(',')))
    print(f'Failed to meet timeout for {deck=}, {opponent=}')
    return 0, 0


def make_decks(n_decks):
    for _ in range(n_decks):
        counter = Counter([CARD_NAMES[random.randint(0, len(CARD_NAMES) - 1)]
                           for _ in range(random.randint(15, 30))])
        yield dict(counter.items())


def main() -> None:
    random.seed(712)
    decks = list(make_decks(50))
    decks.extend(CUSTOM_DECKS)

    results = [
        (deck, {'template_fast': 0.0, 'template_careful': 0.0, 'template_reckless': 0.0})
        for deck in decks
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(run_game, deck, opponent, N_GAMES): (ideck, opponent)
            for ideck, deck in enumerate(decks)
            for opponent in ('template_fast', 'template_careful', 'template_reckless')
        }
        for future in track(concurrent.futures.as_completed(futures),
                            total=len(futures)):
            ideck, opponent = futures[future]
            results[ideck][1][opponent] = future.result()

    with OUT_FILE.open('w') as f:
        json.dump(results, f)


if __name__ == '__main__':
    main()
