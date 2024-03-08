from tasopt_wing_weight_model_interface import surfw, example_inputs
import numpy as np
import networkx

n_inputs = len(example_inputs)
input_labels = list(example_inputs.keys())

# Generate nan-contaminated inputs
contaminants = np.diag(np.ones(n_inputs) * np.nan)
inputs = np.tile(list(example_inputs.values()), (n_inputs, 1)) + contaminants
input_dictionaries = [{k: v for k, v in zip(example_inputs.keys(), row)} for row in inputs]

# Call the function
output_dictionaries = [surfw(**d) for d in input_dictionaries]
n_outputs = len(output_dictionaries[0])
output_labels = list(output_dictionaries[0].keys())
outputs = np.stack(
    [np.array(list(d.values())) for d in output_dictionaries],
    axis=1
)

sparsity = np.isnan(outputs)

# Plot the sparsity pattern

import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p
from _utilities import plot_sparsity

plot_sparsity(sparsity, input_labels=input_labels, output_labels=output_labels)
# plt.subplots_adjust(top=0.7)
p.show_plot(
    "Sparsity pattern of `surfw()`, using NaN-contamination",
    set_ticks=False,
    # tight_layout=False,
)

strategy = "largest_first"
# strategy = "independent_set"

# Plot the compressed sparsity, showing reverse-mode (column-compression)
connectivity = sparsity.T @ sparsity
coloring_dict = networkx.algorithms.coloring.greedy_color(
    G=networkx.convert_matrix.from_numpy_array(connectivity),
    strategy=strategy
)
indices, colors = list(zip(*coloring_dict.items()))
coloring = np.asarray(colors)[np.argsort(indices)]
col_effective_sparsity = np.zeros((n_outputs, np.max(coloring) + 1), dtype=bool)
compressed_input_labels = [[] for _ in range(col_effective_sparsity.shape[1])]
for i in range(n_inputs):
    col_effective_sparsity[sparsity[:, i], coloring[i]] = True
    compressed_input_labels[coloring[i]].append(input_labels[i])

plot_sparsity(
    col_effective_sparsity,
    input_labels=[", ".join(labels) for labels in compressed_input_labels],
    output_labels=output_labels
)
plt.subplots_adjust(top=0.7)
p.show_plot(
    "Column-compressed sparsity pattern of `surfw()`",
    set_ticks=False,
    tight_layout=False,
)

# # Plot the compressed sparsity, showing reverse-mode (row-compression)
# connectivity = sparsity @ sparsity.T
# coloring_dict = networkx.algorithms.coloring.greedy_color(
#     G=networkx.convert_matrix.from_numpy_array(connectivity),
#     strategy=strategy
# )
# indices, colors = list(zip(*coloring_dict.items()))
# coloring = np.asarray(colors)[np.argsort(indices)]
# row_effective_sparsity = np.zeros((np.max(coloring) + 1, n_inputs), dtype=bool)
# compressed_output_labels = [[] for _ in range(row_effective_sparsity.shape[0])]
# for i in range(n_outputs):
#     row_effective_sparsity[coloring[i], sparsity[i, :]] = True
#     compressed_output_labels[coloring[i]].append(output_labels[i])
#
# plot_sparsity(
#     row_effective_sparsity,
#     input_labels=input_labels,
#     output_labels=[", ".join(labels) for labels in compressed_output_labels]
# )
# p.show_plot(
#     "Row-compressed sparsity pattern of `surfw()`",
#     set_ticks=False,
#     tight_layout=False,
# )
