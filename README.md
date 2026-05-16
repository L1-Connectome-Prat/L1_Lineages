# L1 Lineage Organization

Lineage-level organization and visualization of the first-instar *Drosophila*
larval (L1) connectome. This repository accompanies a larger study on L1
neural organization and produces the lineage anatomy figures.

## Overview

The pipeline takes per-lineage neuron skeletons and annotations, separates
them into Differentiated (Diff), Secondary Undifferentiated (SU),
Unbound, and Developing categories, and renders the spatial / statistical
summaries used in Figure 1. Core outputs:

- **Lineage Neuron Counts** — per-lineage Diff and SU neuron tallies,
  ordered by the canonical lineage ordering.
- **Lineage Tracts** — per-lineage 3D point clouds of Diff and SU tracts,
  pruned to the central brain neuropil, plus smoothed alpha-shape meshes.
- **Sensory Bundles** — point clouds and meshes for sensory afferent
  bundles (S-AN, S-GLN).
- **EM Sections** — example CATMAID EM cross-sections through individual
  lineage tracts and soma clusters, with scalebars.
- **Atypical Neurons** — 2D projections of Unbound and Developing neurons
  against the central brain neuropil and MB compartment meshes.

## Pipeline

Scripts are intended to run sequentially; each produces inputs consumed by
the Figure 1 notebooks.

| # | Script | Purpose |
|---|--------|---------|
| 1 | `lineage_neuron_counts.py` | Per-lineage Diff / SU neuron counts from `L1_NeuronInformation_PK.csv`; writes the long-form `Lineage_Counts.csv` and the count-bar figure. |
| 2 | `lineage_clouds.py` | Per-lineage point clouds of Diff and SU tracts, pruned to the central brain neuropil; written as `.pcd` per lineage / hemisphere. |
| 3 | `lineage_meshes.m` | MATLAB alpha-shape meshing of the point clouds with jitter, Taubin smoothing, and per-lineage size tuning; produces the smoothed `.stl` meshes used in 3D figures. |
| 4 | `em_sections.py` | Fetches pixel-bbox EM sections from L1 CATMAID for example lineages (CP23d, BAmv12, BAmv3) and soma clusters; rendered as PNG + PDF panels with scalebars. |
| 5 | `unbound_dev_neurons.py` | 2D plots of Unbound and Developing neurons against the central brain neuropil and the MB Left / Right meshes. |

Shared utilities:
- `_lineage_palette.py` — canonical lineage ordering and colour scheme used
  across all lineage figures (also pickled to `Data_Helpers/Lineage_Colors.pkl`).

## Directory Structure

```
L1_Lineages/
  Scripts/                            # Analysis scripts (Python + MATLAB)
  Notebooks/                          # Figure 1 assembly notebooks
  Data_Helpers/                       # Lineage colour palette pickle
  Analysis_Outputs/
    Lineage_Stats/                    # Neuron-count table + bar figure
    Volumes/
      Lineage_Tracts/{Diff,SU}/       # Per-lineage point clouds + meshes
      Sensory_Bundles/{S-AN,S-GLN}/   # Sensory bundle clouds + meshes
    EM_Sections/                      # CATMAID EM section panels
    Atypical_Neurons/                 # Unbound + Developing neuron figure
    Figure_01*.pdf                    # Assembled figure outputs
```