import numpy as np
import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p
import textwrap
from matplotlib.colors import LinearSegmentedColormap

def plot_sparsity(
        sparsity: np.ndarray,
        input_labels: list[str] = None,
        output_labels: list[str] = None,
        base_label_fontsize: float = 8,
        max_line_length: int = 20,
        color="k",
):
    fig, ax = plt.subplots(figsize=(6, 6), dpi=600)
    plt.imshow(
        sparsity,
        # cmap="Grays",
        cmap=LinearSegmentedColormap.from_list("custom", [np.ones(3) * 1, color]),
        origin="upper",
        alpha=0.7
    )
    ax.set_facecolor(np.ones(3))
    plt.hlines(np.arange(sparsity.shape[0] + 1) - 0.5, -0.5, sparsity.shape[1] - 0.5, color=np.ones(3) * 0.9,
               linewidth=0.5)
    plt.vlines(np.arange(sparsity.shape[1] + 1) - 0.5, -0.5, sparsity.shape[0] - 0.5, color=np.ones(3) * 0.9,
               linewidth=0.5)
    ax.xaxis.set_label_position('top')
    ax.xaxis.tick_top()
    ax.yaxis.tick_left()
    ax.tick_params(which='both', length=0)
    if input_labels is not None:
        input_labels = [textwrap.fill(label, max_line_length, break_long_words=False) for label in input_labels]

        locs, labels = plt.xticks(range(len(input_labels)), input_labels, rotation=90, ha="center", va="bottom", alpha=0.5)
        for i, label in enumerate(labels):
            label.set_fontsize(base_label_fontsize / (input_labels[i].count("\n") + 1))
            if ", " in label._text:
                label.set_alpha(1)

    if output_labels is not None:
        output_labels = [textwrap.fill(label, max_line_length, break_long_words=False) for label in output_labels]

        locs, labels = plt.yticks(range(len(output_labels)), output_labels, ha="right", va="center", alpha=0.5)
        for i, label in enumerate(labels):
            label.set_fontsize(base_label_fontsize / (output_labels[i].count("\n") + 1))
            if ", " in label._text:
                label.set_alpha(1)

    plt.xlabel(f"Inputs (n={sparsity.shape[1]})")
    plt.ylabel(f"Outputs\n(m={sparsity.shape[0]})")
    plt.grid(False)


if __name__ == '__main__':
    sparsity = np.random.random((30, 40)) < 0.2
    input_labels = [f"Inputs {i}" for i in range(sparsity.shape[1])]
    input_labels[0] = "This is a really long label that should wrap around and be fine with it I hope"
    output_labels = [f"Output {i}" for i in range(sparsity.shape[0])]
    plot_sparsity(sparsity, input_labels, output_labels, color="b")
    # p.show_plot(
    #     "Sparsity pattern",
    #     set_ticks=False,
    # )
    plt.tight_layout()
    plt.show()
