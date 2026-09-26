# Run the full pipeline end-to-end.
#
# Task 12 correction: the original STEPS list referenced stale bronze
# ingestion scripts (ingest_pwt.py, ingest_gfdd.py, ingest_cinc.py,
# ingest_hyde.py) from an earlier plan revision that commit 49b0057
# ("docs: update Phase 1 plan -- replace Tasks 4-6 with NMC/V-Dem/COW...")
# superseded. The scripts that actually exist under scripts/bronze/ are
# listed below. Steps are also invoked via `python -m <module>` rather than
# as bare file paths, since none of scripts/bronze, scripts/silver, etc.
# are installed on sys.path outside of pytest's conftest.py -- running them
# as file paths raises ModuleNotFoundError: No module named 'scripts.utils'.
import subprocess, sys

STEPS = [
    "scripts/bronze/ingest_maddison.py",
    "scripts/bronze/ingest_jst.py",
    "scripts/bronze/ingest_nmc.py",
    "scripts/bronze/ingest_vdem.py",
    "scripts/bronze/ingest_polity5.py",
    "scripts/bronze/ingest_cow_trade.py",
    "scripts/silver/compute_phi.py",
    "scripts/silver/compute_psi.py",
    "scripts/silver/compute_omega.py",
    "scripts/gold/calibrate.py",
    "scripts/validation/backtesting.py",
    "scripts/dashboard/run_dashboard.py",
]

if __name__ == "__main__":
    for step in STEPS:
        module = step.replace("/", ".").replace(".py", "")
        print(f"\n--- {step} ---")
        result = subprocess.run([sys.executable, "-m", module], check=True)
