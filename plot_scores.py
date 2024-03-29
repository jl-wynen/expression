import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def plot_results():
    # Loading lists
    with open('data.json', 'r') as f:
        loaded_lists = json.load(f)


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


    longest_history = 0
    longest_plotted_history = 0
    data_set = loaded_lists

    for score_history in data_set:
        longest_history = max([longest_history, len(score_history)])

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6))

    positive_win_lengths = []
    negative_win_lengths = []


    history_plot_limit = 60

    for index, score_history in enumerate(data_set):
        length = len(score_history)
        length_frac = length/longest_history
        length_frac = 1 - length_frac*0.8

        if score_history[-1] > 100:
            color_sign = 1
            positive_win_lengths.append(length)
        else:
            color_sign = -1
            negative_win_lengths.append(length)

        color = get_color(color_sign*length_frac)

        if index < history_plot_limit:
            ax1.plot(score_history, color=color, alpha=0.6)
            #ax1.stairs(score_history, color=color, alpha=0.6)
            longest_plotted_history = max([longest_plotted_history, len(score_history)])

    ax1.set_xlabel("Turns")
    ax1.set_ylabel("Score")

    ax1.plot([0, longest_plotted_history], [100, 100], "--k")
    ax1.plot([0, longest_plotted_history], [-100, -100], "--k")

    ax1.set_ylim([-115, 115])
    #ax1.set_xlim([0, 20])

    """
    # Create a list of labels for each bar (optional)
    labels = [f'List {i+1}' for i in range(len(loaded_lists))]
    
    # Plotting
    ax2.hist(positive_win_lengths, color='blue')
    ax2.hist(negative_win_lengths, color='red')
    
    ax2.set_xlabel('List')
    ax2.set_ylabel('Length')
    ax2.set_title('Length of Lists')
    """

    """
    lengths_set1 = positive_win_lengths
    lengths_set2 = negative_win_lengths
    
    print(positive_win_lengths)
    print(negative_win_lengths)
    
    # Find the number of bars for each set
    n_bars = max(max(positive_win_lengths), max(negative_win_lengths))
    
    # Generate a set of indices for the bars
    indices = np.arange(n_bars)
    
    # Bar width
    bar_width = 0.35
    
    # Plotting both sets
    bars_set1 = ax2.bar(indices - bar_width/2, lengths_set1 + [0]*(n_bars - len(positive_win_lengths)), bar_width, label='Set 1', color='blue')
    bars_set2 = ax2.bar(indices + bar_width/2, lengths_set2 + [0]*(n_bars - len(negative_win_lengths)), bar_width, label='Set 2', color='red')
    
    # Adding some text for labels, title, and axes ticks
    ax2.set_xlabel('List Index')
    ax2.set_ylabel('Length')
    ax2.set_title('Comparison of List Lengths')
    #ax2.set_xticks(indices)
    #ax2.set_xticklabels([f'List {i+1}' for i in range(n_bars)])
    ax2.legend()
    
    # Ensure the y-axis is scaled to accommodate the longest list
    ax2.set_ylim(0, max(max(lengths_set1), max(lengths_set2)) + 1)  # Adding 1 for a little extra space
    """

    # Calculate the length of each list
    lengths_set1 = positive_win_lengths
    lengths_set2 = negative_win_lengths

    if len(lengths_set1) > 0:
        max_set1 = max(lengths_set1)
    else:
        max_set1 = 0

    if len(lengths_set2) > 0:
        max_set2 = max(lengths_set2)
    else:
        max_set2 = 0

    bins = np.arange(0, max(max_set1, max_set2) + 2) - 0.5

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
    #ax2.grid(True, which='both', linestyle='--', linewidth=0.5)
    #ax2.set_xticks(np.arange(0, max(lengths_set1 + lengths_set2) + 1))  # Setting x-ticks to show every possible list length


    positive_win_rate = len(positive_win_lengths)/len(data_set)
    negative_win_rate = len(negative_win_lengths)/len(data_set)
    labels = f'Positive wins {100*positive_win_rate} %', f"Negative wins {100*negative_win_rate} %"
    sizes = [positive_win_rate, negative_win_rate]

    ax3.pie(sizes, labels=labels, colors=["blue", "red"])

    plt.show(block=True)

if __name__ == "__main__":
    plot_results()