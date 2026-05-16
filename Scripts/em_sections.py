#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Render EM sections from L1 CATMAID for example lineages and soma examples.
Each section is fetched as a PIXEL bbox, saved as a PNG, then re-rendered
into a PDF panel with a scalebar.

Inputs (read-only):
    L1 CATMAID (env vars L1_USERNAME, L1_PASSWORD, L1_TOKEN, L1_SERVER)

Outputs (Figures/Figure_01/EM_Sections/):
    CP23d.{png,pdf}
    BAmv12.{png,pdf}
    BAmv3.{png,pdf}
    Soma_BAmv3_suNB_Right.{png,pdf}
    Soma_BAmv3_Diff-01_Right.{png,pdf}
    Soma_BAlc_SU-04_Right.{png,pdf}
    Soma_MB-AL_Dev_Right.{png,pdf}
"""
import os

import numpy as np
import matplotlib.pyplot as plt

from pymaid import tiles

import connectome_analysis_claude as ca

#------------------------------------------------------------------------------
FOLDER = "Analysis_Outputs/EM_Sections"

# (filename, center_xy, border, z)
SECTIONS = [
    ("CP23d",                    (7454,  7304),  700, 1156),
    ("BAmv12",                   (8653,  13721), 700, 551),
    ("BAmv3",                    (7219,  13563), 500, 510),
    ("Soma_BAmv3_suNB_Right",    (4528,  11646), 750, 249),
    ("Soma_BAmv3_Diff-01_Right", (4130,  12088), 750, 317),
    ("Soma_BAlc_SU-04_Right",    (4509,  15020), 750, 600),
    ("Soma_MB-AL_Dev_Right",     (7816,  1479),  750, 786)]


#------------------------------------------------------------------------------
def render_section(name, center, border, z, folder):
    """Fetch one EM section and write the PNG + PDF panel."""
    center = np.array(center)
    bbox   = [center[0] - border, center[0] + border,
              center[1] - border, center[1] + border,
              z]

    job = tiles.TileLoader(bbox, stack_id = 1, coords = "PIXEL")

    job.load_and_save(filepath = f"{folder}/", filename = f"{name}.png")
    job.load_in_memory()

    ax = job.render_im(figsize = (12, 12))
    ax.grid(False)
    job.scalebar(size = 1000, ax = ax, label = True, line_kws = {"color" : "w", "lw" : 5})
    # Save as pdf with axes
    plt.savefig(f"{folder}/{name}.pdf", bbox_inches = "tight", facecolor = "white",
                dpi = 1200)

    # Save as png without axes or scalebar label
    ax.axis("off")
    # Remove the text on the scalebar
    for t in list(ax.texts):
        t.remove()
    plt.savefig(f"{folder}/{name}-cbar.png", bbox_inches = "tight", pad_inches = 0,
                dpi = 1200)
    plt.close()


#------------------------------------------------------------------------------
if __name__ == "__main__":
    os.makedirs(FOLDER, exist_ok = True)

    # Connect to L1 CATMAID
    larval_analysis = ca.CATMAIDConnect(
        os.environ["L1_USERNAME"],
        os.environ["L1_PASSWORD"],
        os.environ["L1_TOKEN"],
        os.environ["L1_SERVER"])

    for name, center, border, z in SECTIONS:
        print(f"Rendering : {name}")
        render_section(name, center, border, z, FOLDER)

    print("हो गया दोस्तों!!!")
