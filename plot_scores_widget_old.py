import ipywidgets as widgets
from IPython.display import display
import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import json

# Create a custom colormap
cmap = LinearSegmentedColormap.from_list(
    'rwb',
    [(1, 0, 0), (1, 1, 1), (0, 0, 1)]
)

def get_color(value):
    """Return a color from the custom red-white-blue colormap for a given value between -1 and 1."""
    # Normalize value to be between 0 and 1 for the colormap
    normalized_value = (value + 1) / 2
    return cmap(normalized_value)

# Load your data
with open('data.json', 'r') as f:
    loaded_lists = json.load(f)


# Determine the full range of turns across all games
max_turns = max(len(score_history) for score_history in loaded_lists)

# Create the IntRangeSlider
turns_slider = widgets.IntRangeSlider(
    value=[0, max_turns],
    min=0,
    max=max_turns,
    step=1,
    description='Turn Range:',
    continuous_update=False
)

def plot_subset(turn_range):
    # Extract start and end turns from the turn_range
    start_turn, end_turn = turn_range

    data_set = loaded_lists[start_turn:end_turn]

    longest_history = 0
    for score_history in data_set:
        longest_history = max([longest_history, len(score_history)])

    # Your modified plotting code here
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6))

    positive_win_lengths = []
    negative_win_lengths = []

    for score_history in data_set:
        length = len(score_history)
        length_frac = length / longest_history
        length_frac = 1 - length_frac * 0.8

        if score_history[-1] > 100:
            color_sign = 1
            positive_win_lengths.append(length)
        else:
            color_sign = -1
            negative_win_lengths.append(length)

        color = get_color(color_sign * length_frac)

        ax1.plot(score_history, color=color, alpha=0.6)

    ax1.set_xlabel("Turns")
    ax1.set_ylabel("Score")

    ax1.plot([0, longest_history], [100, 100], "--k")
    ax1.plot([0, longest_history], [-100, -100], "--k")

    ax1.set_ylim([-115, 115])
    # ax1.set_xlim([0, 20])

    # Calculate the length of each list
    lengths_set1 = positive_win_lengths
    lengths_set2 = negative_win_lengths

    bins = np.arange(0, max(max(lengths_set1), max(lengths_set2)) + 2) - 0.5

    hist1, edges = np.histogram(lengths_set1, bins=bins)
    hist2, edges = np.histogram(lengths_set2, bins=bins)

    # Plot the first dataset as positive
    ax2.bar(bins[:-1] + 0.5, hist1, width=1, color='blue', label='Set 1', align='center', alpha=0.8)

    # Plot the second dataset as negative
    ax2.bar(bins[:-1] + 0.5, -hist2, width=1, color='red', label='Set 2', align='center', alpha=0.8)

    max_y_value = max([max(hist1), max(hist2)])
    ax2.set_ylim([-max_y_value, max_y_value])

    ax2.set_xlabel('Length of Lists')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Histogram of List Lengths')
    ax2.legend()

    ticks = ax2.get_yticks()
    ax2.set_yticks(ticks, [str(abs(tick)) for tick in ticks])

    ax2.stairs(hist1 - hist2, edges, color="black", alpha=0.5)
    # ax2.grid(True, which='both', linestyle='--', linewidth=0.5)
    # ax2.set_xticks(np.arange(0, max(lengths_set1 + lengths_set2) + 1))  # Setting x-ticks to show every possible list length

    positive_win_rate = len(positive_win_lengths) / len(data_set)
    negative_win_rate = len(negative_win_lengths) / len(data_set)
    labels = f'Positive wins {100 * positive_win_rate} %', f"Negative wins {100 * negative_win_rate} %"
    sizes = [positive_win_rate, negative_win_rate]

    ax3.pie(sizes, labels=labels, colors=["blue", "red"])

    plt.show(block=True)

    # You'll need to adjust your plotting to consider the selected range.
    # For ax1, as an example, you would slice the score_history like this:
    # for score_history in loaded_lists:
    #     ax1.plot(score_history[start_turn:end_turn], ...)

    # Ensure your code utilizes the start_turn and end_turn for slicing the data to plot
    # This is just an example and needs to be adjusted according to your actual plotting code.


# Display the slider
display(turns_slider)


# Function to update the plot based on the slider
def update_plot(change):
    plot_subset(change.new)


# Observe changes to the slider value
turns_slider.observe(update_plot, names='value')

# Initial plot call (if needed, you can call plot_subset with the initial slider range)
plot_subset(turns_slider.value)
