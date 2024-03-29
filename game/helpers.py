def apply_card(card, locked_term, current_term):
    # Assume card is of card class
    if card.operator == "+":
        locked_term += current_term
        current_term = card.value
    elif card.operator == "-":
        locked_term += current_term
        current_term = -1 * card.value
    elif card.operator == "*":
        current_term *= card.value
    elif card.operator == "/":
        current_term /= card.value
    else:
        print("Error, unknown operator: ", end="")
        print(card.operator)

    return locked_term, current_term


def can_be_played(hand, energy, expensive_first=True):
    can_play = []
    for card in hand:
        if card.cost <= energy:
            can_play.append(card)

    can_play = sorted(can_play, key=lambda card: card.cost, reverse=expensive_first)

    return can_play