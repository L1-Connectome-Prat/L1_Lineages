#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2D plots of unbound and developing neurons against the central brain
neuropil and the MB compartment meshes.

Inputs (read-only):
    $PROJECTS_HOME/L1_Compartment-Atlas/Central-Brain_Compartments/MB/MB_Right.stl
    $PROJECTS_HOME/L1_Compartment-Atlas/Central-Brain_Compartments/MB/MB_Left.stl
    $PROJECTS_HOME/L1_Skeletons/Skeletons/Diff_Skeletons/Unbound/*/*.swc
    $PROJECTS_HOME/L1_Skeletons/Skeletons/Dev_Skeletons/*/*/*.swc

"""
import os
from glob import glob
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import navis
import flybrains

import connectome_analysis_claude as ca
from prats_helpers import place_panel_label
sns.set_style("ticks")

#------------------------------------------------------------------------------
HOME             = os.environ["PROJECTS_HOME"]
SKEL_FOLDER      = f"{HOME}/L1_Skeletons/Skeletons"
COMPARTMENT_HOME = f"{HOME}/L1_Compartment-Atlas/Central-Brain_Compartments"
FOLDER           = "Analysis_Outputs/Atypical_Neurons"

# Coloring
UNBOUND_COLORS    = {"ventralLN" : "purple", "Clamp" : "red",
                     "MBE18"     : "green",  "UNK-anterior-basal" : "orange"}
DEVELOPING_COLORS = {"MB-AL" : "purple", "MB-AM" : "red",
                     "MB-PL" : "green",  "MB-PM" : "orange"}

# Params
linewidth      = 0.75
scatter_size   = 6
scatter_alpha  = 0.75
linewidth_hist = 0.5
alpha_hist     = 0.35
alpha_skel     = 0.75
title_fontsize = 8.5
label_fontsize = 7
tick_fontsize  = 6
row_gap_shrink = 0.03

#------------------------------------------------------------------------------
def load_mb_meshes():
    """Load and symmetrize the left/right MB compartment meshes."""
    mbr = ca.stl_to_navis(f"{COMPARTMENT_HOME}/MB/MB_Right.stl")
    mbl = ca.stl_to_navis(f"{COMPARTMENT_HOME}/MB/MB_Left.stl")

    mbr.color = (0.85, 0.85, 0.85, 0.35)
    mbl.color = (0.85, 0.85, 0.85, 0.35)

    mbr = navis.xform_brain(mbr, source = "PK_L1CNS", target = "PK_L1CNSsym")
    mbl = navis.xform_brain(mbl, source = "PK_L1CNS", target = "PK_L1CNSsym")

    return mbr, mbl

#------------------------------------------------------------------------------
def load_counts():
    """Load the neuron counts from the csv files."""
    
    count_df = pd.read_csv("Analysis_Outputs/Lineage_Stats/Lineage_Counts.csv")
    count_df = count_df.loc[(count_df["Category"] == "Dev") &
                            (count_df["Count"]    > 0)]
    count_df.reset_index(drop = True, inplace = True)

    return count_df

#------------------------------------------------------------------------------
def load_skeletons(pattern, color_attr, color_map):
    """Load swcs from a glob pattern, symmetrize, and assign colours."""
    skels = glob(pattern)
    skels = navis.read_swc(skels, fmt = "{id}.swc")
    skels = navis.xform_brain(skels, source = "PK_L1CNS", target = "PK_L1CNSsym")

    for skel in skels:
        skel.color = color_map[getattr(skel, color_attr)]

    color_dict = dict(zip(skels.id, skels.color))
    return skels, color_dict

#------------------------------------------------------------------------------
if __name__ == "__main__":
    os.makedirs(FOLDER, exist_ok = True)

    # Counts
    count_df = load_counts()

    # Neuropils
    brain    = flybrains.PK_L1CBNeuropilsym
    mbr, mbl = load_mb_meshes()

    # Load Unbound Neurons
    unbound, unbound_colors = load_skeletons(
        f"{SKEL_FOLDER}/Diff_Skeletons/Unbound/*/*.swc",
        color_attr = "moniker",
        color_map  = UNBOUND_COLORS)

    # Load Developing Neurons
    developing, developing_colors = load_skeletons(
        f"{SKEL_FOLDER}/Dev_Skeletons/*/*/*.swc",
        color_attr = "lineage",
        color_map  = DEVELOPING_COLORS)

    #--------------------------------------------------------------------------
    # Create Figure Panels
    fig, ax = plt.subplots(figsize = (9, 7.5),
                           ncols = 4,
                           nrows = 4,
                           gridspec_kw = {"height_ratios" : [1, 0.45, 1, 0.65]})

    # Tighten the vertical gaps: pull row 0 down toward row 1 and row 3 up
    # toward row 2. Row 2 is also nudged slightly to keep the developing
    # block visually centered. Gap(row1, row2) is left untouched.
    for a in ax[0, :]:
        pos = a.get_position()
        a.set_position([pos.x0, pos.y0 - row_gap_shrink, pos.width, pos.height])
    for a in ax[2, :]:
        pos = a.get_position()
        a.set_position([pos.x0, pos.y0 - row_gap_shrink / 2, pos.width, pos.height])
    for a in ax[3, :]:
        pos = a.get_position()
        a.set_position([pos.x0, pos.y0 + row_gap_shrink, pos.width, pos.height])

    #----------------------------------
    # Looping and plotting unbound neurons
    for i, moniker in enumerate(np.unique(unbound.moniker)):
        sub = unbound[unbound.moniker == moniker]

        # Anterior View
        navis.plot2d(
            [sub, mbr, mbl, brain],
            method    = "2d",
            alpha     = alpha_skel,
            soma      = True,
            view      = ("x", "-y"),
            color     = unbound_colors,
            ax        = ax[0, i],
            linewidth = linewidth * 0.5,
            rasterize = True
        )

        # Dorsal View
        navis.plot2d(
            [sub, mbr, mbl, brain],
            method    = "2d",
            alpha     = alpha_skel,
            soma      = True,
            view      = ("x", "z"),
            color     = unbound_colors,
            ax        = ax[1, i],
            linewidth = linewidth * 0.5,
            rasterize = True
        )

        # Add the title
        ax[0, i].set_title(f"{moniker}", fontsize = title_fontsize,
                           y = 0.825)

    # Common X-axis
    for a in ax[:2, :].flatten():
        a.set_xlim(17500, 85000)
        a.set_aspect(aspect = "equal", adjustable = "datalim")
        a.axis("off")

    # Differing Y-axes
    for a in ax[0, :]:
        a.set_ylim(93722, -2737)
    for a in ax[1, :]:
        a.set_ylim(19000, 67230)

    #----------------------------------
    # Plotting the developing neurons
    # Anterior View
    navis.plot2d(
        [developing, mbr, mbl, brain],
        method    = "2d",
        alpha     = alpha_skel,
        soma      = True,
        view      = ("x", "-y"),
        color     = developing_colors,
        ax        = ax[2, 0],
        linewidth = linewidth * 0.5,
        rasterize = True
    )

    # Dorsal View
    navis.plot2d(
        [developing, mbr, mbl, brain],
        method    = "2d",
        alpha     = alpha_skel,
        soma      = True,
        view      = ("x", "z"),
        color     = developing_colors,
        ax        = ax[3, 0],
        linewidth = linewidth * 0.5,
        rasterize = True
    )

    # Limits and axes
    ax[2, 0].set_xlim(17500, 85000)
    ax[2, 0].set_aspect(aspect = "equal", adjustable = "datalim")
    ax[2, 0].set_ylim(93722, -2737)
    ax[2, 0].axis("off")
    ax[3, 0].set_xlim(17500, 85000)
    ax[3, 0].set_aspect(aspect = "equal", adjustable = "datalim")
    ax[3, 0].set_ylim(14000, 82230)
    ax[3, 0].axis("off")

    # Add the title
    ax[2, 0].set_title(f"Developing Neurons", fontsize = title_fontsize,
                       y = 0.925)

    #----------------------------------
    # Developing Counts
    sns.barplot(count_df,
                y   = "Lineage",
                x   = "Count",
                hue = "Hemisphere",
                alpha = alpha_hist * 1.5,
                palette = {"Right" : "red", "Left" : "blue"},
                edgecolor = "black",
                ax = ax[2, 1],
                linewidth = linewidth_hist * 1.75)

    # Limit
    ax[2, 1].set_xlim(0, 15)
    ax[2, 1].set_ylabel("")
    ax[2, 1].set_xlabel("# Developing Neurons", fontsize = label_fontsize)
    ax[2, 1].legend(loc = "upper left", bbox_to_anchor = (1.05, 1), 
                title = "Hemisphere",
                fontsize = label_fontsize,
                title_fontsize = label_fontsize)
    ax[2, 1].tick_params(
        axis  = "both",
        which = "major",
        labelsize = tick_fontsize,
        rotation = 0)
    ax[2, 1].set_xticks([0, 5, 10, 15])

    # Color the Labels
    for i, label in enumerate(ax[2, 1].get_yticklabels()):
        label.set_color(DEVELOPING_COLORS.get(label.get_text(), "black"))

    # Despine
    sns.despine(ax = ax[2, 1])

    # Nudge the barplot to the right for better spacing from ax[2, 0]
    pos = ax[2, 1].get_position()
    ax[2, 1].set_position([pos.x0 + 0.085, pos.y0, pos.width, pos.height])

    #----------------------------------
    # Turn off unused axes
    for a in [ax[2, 2], ax[2, 3], ax[3, 1], ax[3, 2], ax[3, 3]]:
        a.axis("off")

    #----------------------------------
    # Panel Labels
    label_kwargs = dict(fontsize = 16, va = "top", ha = "right")

    # Unbound Anterior
    place_panel_label(fig, ax[0, 0], "Ai", shx = 0.005, shy = -0.005, label_kwargs = label_kwargs)
    place_panel_label(fig, ax[0, 1], "Bi", shx = 0.005, shy = -0.005, label_kwargs = label_kwargs)
    place_panel_label(fig, ax[0, 2], "Ci", shx = 0.005, shy = -0.005, label_kwargs = label_kwargs)
    place_panel_label(fig, ax[0, 3], "Di", shx = 0.005, shy = -0.005, label_kwargs = label_kwargs)

    # Dorsal
    for a in ax[1, :]:
        place_panel_label(fig, a, "ii", shx = 0.005, shy = 0, label_kwargs = label_kwargs)
    # Developing Dorsal
    place_panel_label(fig, ax[3, 0], "ii", shx = 0.005, shy = 0, label_kwargs = label_kwargs)
    
    # Change the vertical to align 
    label_kwargs["va"] = "bottom"
    # Developing Anterior
    place_panel_label(fig, ax[2, 0], "Ei", shx = 0.005, shy = -0.01, label_kwargs = label_kwargs)
    # Counts
    place_panel_label(fig, ax[2, 1], "F", shx = -0.06, shy = -0.01, label_kwargs = label_kwargs)

    #----------------------------------
    # Save
    plt.savefig(f"{FOLDER}/Figure_01_Supplementary-02_Unbound-Dev-Atypical-Neurons.pdf",
                bbox_inches = "tight",
                dpi         = 1200)

    #--------------------------------------------------------------------------
    print("हो गया दोस्तों!!!")
