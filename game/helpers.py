def apply_card(card, current_value, current_term):
    # Assume card is of card class
    if card.operator == "+":
        current_value += current_term
        current_term = card.value
    elif card.operator == "-":
        current_value += current_term
        current_term = -1 * card.value
    elif card.operator == "*":
        current_term *= card.value
    elif card.operator == "/":
        current_term /= card.value
    else:
        print("Error, unknown operator: ", end="")
        print(card.operator)

    return current_value, current_term