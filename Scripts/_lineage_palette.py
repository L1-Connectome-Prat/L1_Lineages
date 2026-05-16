"""
Lineage palette and ordering helpers used across the L1_Lineages figures.

Static data lives in ``Data_Helpers/`` at the repo root so the colour map
can be loaded independently (e.g. from notebooks or sibling repos) without
importing this module:

    Data_Helpers/
        Lineage_Colors.pkl
"""
import os
import pickle as pkl

#------------------------------------------------------------------------------
DATA_DIR = os.path.join(os.environ["PROJECTS_HOME"],
                        "L1_Lineages",
                        "Data_Helpers")

#------------------------------------------------------------------------------
# Canonical lineage ordering. Type I lineages first, then a blank spacer,
# then Type II lineages.
LINEAGE_ORDER = ["BAla1/2", "BAla3/4", "BAlc", "BAlp1-3", "BAlp4", "BAlv",
                 "BAmas1/2", "BAmd1", "BAmd2", "BAmv1/2", "BAmv3", "BApd", "BApv",
                 "BLAd1-4", "BLAl", "BLAv1/2", "BLAvm", "BLD1", "BLD2-4", "BLD5/6",
                 "BLP1/2", "BLP3/4", "BLVa1/2", "BLVa3/4", "BLVp1", "BLVp2",
                 "CP1d", "CP1v", "CP4",
                 "DALcl1/2d", "DALcl1/2v", "DALcm1/2m", "DALcm1/2v",
                 "DALd", "DALl1",
                 "DALv1", "DALv2/3", "DALv2/3accl", "DALv2/3accm", "DALv2/3accvm", "DALv2/3accvl",
                 "DAMd1", "DAMd2/3", "DAMv1/2",
                 "DILP",
                 "DPLal1-3", "DPLam", "DPLc1", "DPLc2", "DPLc3", "DPLc4", "DPLc5a", "DPLc5p", "DPLd",
                 "DPLl1-3", "DPLm1", "DPLm2", "DPLp1/2",
                 "DPMl1", "DPMl2", "DPMl3/4a", "DPMl3/4p", "DPMm2",
                 "DPMpl1/2", "DPMpl3",
                 "MB-AL", "MB-AM", "MB-PL", "MB-PM",
                 "OLP",
                 "TRdc", "TRdm", "TRdl-a/b", "TRdl-c", "TRdl-d", "TRdl-e", "TRvm", "TRmotor",
                 "",
                 "CP2/3d", "CP2/3v", "DPMm1", "DPMpm1", "DPMpm2", "CM4", "CM4-CM5*", "CM1/3"]


#------------------------------------------------------------------------------
# Anatomical groupings by lineage-name prefix.
ANTERIOR_PREFIXES       = ("BA", "BLA", "BLD", "BLP", "BLV", "DAL", "DAM", "DILP")
DORSO_POSTERIOR_PREFIXES = ("CM", "CP", "DPM", "DPL", "MB", "TR")

def _by_prefix(prefixes):
    return frozenset(l for l in LINEAGE_ORDER
                     if l and l.startswith(prefixes))

ANTERIOR_LINEAGES        = _by_prefix(ANTERIOR_PREFIXES)
DORSO_POSTERIOR_LINEAGES = _by_prefix(DORSO_POSTERIOR_PREFIXES)


#------------------------------------------------------------------------------
def load_lineage_colors(strip_slashes = True):
    """
    Return the lineage colour dict from Data_Helpers/Lineage_Colors.pkl.

    Parameters
    ----------
    strip_slashes : bool
        If True, replace "/" in keys (e.g. "BAla1/2" -> "BAla12") so the
        dictionary can be looked up with sanitised lineage strings.
    """
    with open(os.path.join(DATA_DIR, "Lineage_Colors.pkl"), "rb") as f:
        colors = pkl.load(f)

    if strip_slashes:
        colors = {key.replace("/", "") : value for key, value in colors.items()}

    return colors
