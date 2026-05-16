#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Per-lineage point clouds of differentiated and SU neuron tracts, pruned to
the central brain neuropil. Skeletons and the lineage annotation list come
from L1_Skeletons.

Inputs (read-only):
    $PROJECTS_HOME/L1_Skeletons/Data_Summary/L1_Annotations-Lineages_PK.npy
    $PROJECTS_HOME/L1_Skeletons/Skeletons/Diff_Tracts/<lineage>/<hemisphere>/*.swc
    $PROJECTS_HOME/L1_Skeletons/Skeletons/SU_Skeletons/<lineage>/<hemisphere>/*.swc

Outputs (Analysis_Outputs/Volumes/Lineage_Tracts/):
    <category>/<lineage>/<lineage>_<category>_<hemisphere>.pcd
"""
import os

import numpy as np
import open3d as o3d

import flybrains
import navis

#------------------------------------------------------------------------------
HOME            = os.environ["PROJECTS_HOME"]
SKELETON_FOLDER = f"{HOME}/L1_Skeletons/Skeletons"
ANNOTATION_FILE = f"{HOME}/L1_Skeletons/Data_Summary/L1_Annotations-Lineages_PK.npy"
SAVE_FOLDER     = "Analysis_Outputs/Volumes/Lineage_Tracts"

NEUROPIL = flybrains.PK_L1CBNeuropil.mesh

#------------------------------------------------------------------------------
def save_point_cloud(neurons, annot_name, category, hemisphere, folder):
    """Generate and save the point cloud for the neuron collection."""
    neuron_nodes = np.array(neurons.nodes[["x", "y", "z"]])

    # Convert to PCD
    neuron_pcd        = o3d.geometry.PointCloud()
    neuron_pcd.points = o3d.utility.Vector3dVector(neuron_nodes)

    # Check if folder exists
    out_folder = f"{folder}/{category}/{annot_name}"
    os.makedirs(out_folder, exist_ok = True)

    # Write the Cloud
    o3d.io.write_point_cloud(
        filename       = f"{out_folder}/{annot_name}_{category}_{hemisphere}.pcd",
        pointcloud     = neuron_pcd,
        print_progress = True)


#------------------------------------------------------------------------------
def run(annot, category, hemisphere, in_volume = NEUROPIL,
        skeleton_folder = SKELETON_FOLDER, save_folder = SAVE_FOLDER):
    """Load neurons, prune to the neuropil and write the point cloud."""
    # Annotation
    annot_name = annot.replace("/", "")

    # Check which folder to load
    if category == "Diff":
        folder = f"{skeleton_folder}/Diff_Tracts/{annot_name}/{hemisphere}"
    elif category == "SU":
        folder = f"{skeleton_folder}/SU_Skeletons/{annot_name}/{hemisphere}"
    else:
        raise ValueError("Please input valid neuron category : (1) Diff (2) SU")

    # Load the neurons
    neurons = navis.read_swc(folder, fmt = "{id}.swc")

    # Prune
    neurons = navis.in_volume(neurons, volume = in_volume, mode = "IN")

    # Save point cloud
    save_point_cloud(neurons, annot_name, category, hemisphere, save_folder)


#------------------------------------------------------------------------------
if __name__ == "__main__":
    annotations = np.load(ANNOTATION_FILE)

    # Run over each annotation
    for annot in annotations:
        # Status
        print(f"\nWorking on {annot}")
        for hemisphere in ["Right", "Left"]:
            for category in ["Diff", "SU"]:
                print(f"\t{hemisphere} | {category}")
                # Run the point cloud generation
                try:
                    run(annot, category = category, hemisphere = hemisphere)
                except Exception as e:
                    print(e)
                    print(f"Error in : {annot} {hemisphere} {category}")

    # Status
    print("हो गया दोस्तों!!!")
