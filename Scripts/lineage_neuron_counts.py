#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Per-lineage neuron-count bars for the Differentiated and SU categories,
ordered by the canonical lineage ordering. Also writes the long-form
count table that downstream lineage-stats scripts read back in.

Inputs (read-only):
    $PROJECTS_HOME/L1_Skeletons/Data_Summary/L1_NeuronInformation_PK.csv

Outputs:
    Analysis_Outputs/Lineage_Stats/Lineage_Counts.csv
    Figures/Figure_01/Lineage_Stats/Lineage_Neuron-Counts.{pdf,png}
"""
import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("ticks")

from prats_helpers import place_panel_label
from Scripts._lineage_palette import LINEAGE_ORDER

plt.rcParams["savefig.facecolor"] = "white"

#------------------------------------------------------------------------------
HOME          = os.environ["PROJECTS_HOME"]
SKELETON_PATH = f"{HOME}/L1_Skeletons/Data_Summary"
FOLDER        = "Analysis_Outputs/Lineage_Stats"
HEMI_PALETTE  = {"Right" : "red", "Left" : "blue"}

# Params
linewidth      = 0.75
scatter_size   = 6
scatter_alpha  = 0.75
linewidth_hist = 0.5
alpha_hist     = 0.35
title_fontsize = 8.5
label_fontsize = 7
tick_fontsize  = 6
ylim           = 60

#------------------------------------------------------------------------------
def build_count_df():
    """Pivot the neuron-information CSV to a long lineage-count DataFrame."""
    neuron_info = pd.read_csv(f"{SKELETON_PATH}/L1_NeuronInformation_PK.csv")
    neuron_info["Count"] = 1

    pivot = pd.pivot_table(
        neuron_info,
        values     = "Count",
        index      = ["Lineage", "Hemisphere"],
        columns    = "Category",
        aggfunc    = "sum",
        fill_value = 0)

    count_df = pivot.reset_index().melt(
        id_vars    = ["Lineage", "Hemisphere"],
        var_name   = "Category",
        value_name = "Count")

    return count_df

#------------------------------------------------------------------------------
def _draw_bars(ax, sub_df, ylim, ylabel):
    """Single-category bar panel."""
    sns.barplot(sub_df, x = "Lineage", y = "Count", hue = "Hemisphere", ax = ax,
                alpha   = alpha_hist * 1.5,
                palette = HEMI_PALETTE,
                order   = LINEAGE_ORDER)

    ax.set_xlim(-1, 87)
    ax.set_ylim(0, ylim)

    legend = ax.legend(title = "Hemisphere")
    legend.set_bbox_to_anchor((78, ylim), transform = ax.transData)

    ax.text(39, ylim - 5, "Type I",  color = "magenta", fontsize = label_fontsize, ha = "center", va = "bottom")
    ax.text(82.5, ylim - 5, "Type II", color = "magenta", fontsize = label_fontsize, ha = "center", va = "bottom")

    ax.set_xticks(ticks = ax.get_xticks(), labels = ax.get_xticklabels(), rotation = 90)

    ax.set_xlabel("Lineage",  fontsize = label_fontsize)
    ax.set_ylabel(ylabel,     fontsize = label_fontsize)
    ax.yaxis.labelpad = 10
    ax.xaxis.labelpad = 10

    ax.axvline(x = 78, color = "grey", linestyle = "--", linewidth = 0.5)


def plot_neuron_counts(count_df):
    """Two-panel figure: Diff bars (A) on top, SU bars (B) on bottom."""
    fig, ax = plt.subplots(figsize = (8.5, 7), nrows = 2, ncols = 1,
                       sharex = False)
    plt.subplots_adjust(hspace = 0.4, top = 1, bottom = 0,
                        left = 0, right = 0.95)

    _draw_bars(ax[0], count_df.loc[count_df["Category"] == "Diff"],
               ylim = ylim, ylabel = "# Differentiated Neurons")
    _draw_bars(ax[1], count_df.loc[count_df["Category"] == "SU"],
               ylim = ylim, ylabel = "# SU Neurons")

    # Despine
    for a in ax:
        sns.despine(ax = a)
        a.tick_params(axis = "x", which = "major", labelsize = tick_fontsize, rotation = 90)
        a.tick_params(axis = "y", which = "major", labelsize = tick_fontsize)
        a.set_xlim(-1, 87)

    # Legend
    ax[0].legend(loc = "upper left",
                 bbox_to_anchor = (0.8, 1),
                 title = "Hemisphere",
                 fontsize = label_fontsize,
                 title_fontsize = label_fontsize)
    ax[1].legend().remove()

    # Label
    ax[0].set_xlabel("")

    # Panel Labels
    label_kwargs = dict(fontsize = 16, va = "center", ha = "left")
    place_panel_label(fig, ax[0], "A", shx = -0.075, shy = 0, label_kwargs = label_kwargs)
    place_panel_label(fig, ax[1], "B", shx = -0.075, shy = 0, label_kwargs = label_kwargs)

    plt.savefig(f"{FOLDER}/Figure_01_Supplementary-01_Neuron-Counts.pdf", bbox_inches = "tight", dpi = 1200)
    plt.close(fig)

#------------------------------------------------------------------------------
if __name__ == "__main__":
    os.makedirs(FOLDER, exist_ok = True)

    count_df = build_count_df()
    count_df.to_csv(f"{FOLDER}/Lineage_Counts.csv", index = False)

    plot_neuron_counts(count_df)

    print("हो गया दोस्तों!!!")
