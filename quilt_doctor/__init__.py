"""quilt-doctor — debugging tools on the quilt substrate.

Point it at any project; it answers "what's going on?" by projecting the
project's signals through three substrates: JEPA (does the trajectory
predict itself?), MOTHquantum (is the signal coherent — music or noise?),
and JEV (is the recorded work verifiable?). Same abstraction, ported across
substrates. Every verdict carries receipts.

The quilt WAL is the substrate under all of it: observations are written as
BIND/LINK/VIEW lines, hash-chained and replayable (fnv1a, same as the
fleet's canonical producer in SuperInstance/git-agent PR #1).
"""

from .doctor import diagnose, render_report_md, Diagnosis
from .substrate import QuiltSubstrate
from .collect import collect_repo
