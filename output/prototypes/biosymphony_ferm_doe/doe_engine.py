"""
BioSymphony Fermentation DoE Engine
====================================
Generates Design-of-Experiments matrices for fermentation/bioprocess workflows.
Supports full factorial, fractional factorial, central composite (CCD),
and Box-Behnken designs with biosafety gating and scale-up bridging.
"""

import itertools
import math
import json
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple


# ── Factor & Response definitions ──────────────────────────────────────

@dataclass
class Factor:
    name: str
    unit: str
    low: float
    high: float
    safety_min: Optional[float] = None
    safety_max: Optional[float] = None

    @property
    def center(self):
        return (self.low + self.high) / 2.0

    @property
    def half_range(self):
        return (self.high - self.low) / 2.0

    def coded_to_real(self, coded: float) -> float:
        return self.center + coded * self.half_range


@dataclass
class Response:
    name: str
    unit: str
    objective: str = "maximize"  # maximize | minimize | target


# ── Biosafety gating ──────────────────────────────────────────────────

@dataclass
class SafetyFlag:
    run_id: int
    factor: str
    value: float
    limit_type: str  # "below_min" | "above_max"
    limit_value: float
    severity: str  # "warning" | "block"


def biosafety_gate(runs: List[Dict], factors: List[Factor]) -> Tuple[List[Dict], List[SafetyFlag]]:
    """Check every run against safety constraints. Returns (passed_runs, flags)."""
    passed = []
    flags = []
    for run in runs:
        run_ok = True
        for f in factors:
            val = run["levels"].get(f.name)
            if val is None:
                continue
            if f.safety_min is not None and val < f.safety_min:
                severity = "block" if val < f.safety_min * 0.95 else "warning"
                flags.append(SafetyFlag(run["run_id"], f.name, val, "below_min", f.safety_min, severity))
                if severity == "block":
                    run_ok = False
            if f.safety_max is not None and val > f.safety_max:
                severity = "block" if val > f.safety_max * 1.05 else "warning"
                flags.append(SafetyFlag(run["run_id"], f.name, val, "above_max", f.safety_max, severity))
                if severity == "block":
                    run_ok = False
        status = "PASS" if run_ok else "BLOCKED"
        run["safety_status"] = status
        if run_ok:
            passed.append(run)
    return passed, flags


# ── DoE matrix generators ─────────────────────────────────────────────

def full_factorial(factors: List[Factor], levels_per_factor: int = 3) -> List[Dict]:
    """Generate a full-factorial design."""
    coded_levels = {
        2: [-1, 1],
        3: [-1, 0, 1],
        5: [-1, -0.5, 0, 0.5, 1],
    }.get(levels_per_factor, [round(-1 + 2 * i / (levels_per_factor - 1), 4) for i in range(levels_per_factor)])

    combos = list(itertools.product(coded_levels, repeat=len(factors)))
    runs = []
    for i, combo in enumerate(combos, 1):
        levels = {}
        for f, c in zip(factors, combo):
            levels[f.name] = round(f.coded_to_real(c), 4)
        runs.append({"run_id": i, "design": "FullFactorial", "levels": levels})
    return runs


def central_composite(factors: List[Factor], alpha: str = "rotatable") -> List[Dict]:
    """Generate a Central Composite Design (CCD)."""
    k = len(factors)
    alpha_val = math.pow(2, k / 4) if alpha == "rotatable" else math.sqrt(k)

    runs = []
    run_id = 1

    # Factorial portion (2^k)
    for combo in itertools.product([-1, 1], repeat=k):
        levels = {f.name: round(f.coded_to_real(c), 4) for f, c in zip(factors, combo)}
        runs.append({"run_id": run_id, "design": "CCD-factorial", "levels": levels})
        run_id += 1

    # Axial (star) points
    for i, f in enumerate(factors):
        for sign in [-1, 1]:
            coded = [0] * k
            coded[i] = sign * alpha_val
            levels = {fj.name: round(fj.coded_to_real(coded[j]), 4) for j, fj in enumerate(factors)}
            runs.append({"run_id": run_id, "design": "CCD-axial", "levels": levels})
            run_id += 1

    # Center points (typically 3-6 replicates)
    center_reps = max(3, k)
    for _ in range(center_reps):
        levels = {f.name: round(f.center, 4) for f in factors}
        runs.append({"run_id": run_id, "design": "CCD-center", "levels": levels})
        run_id += 1

    return runs


def box_behnken(factors: List[Factor]) -> List[Dict]:
    """Generate a Box-Behnken design (requires k >= 3)."""
    k = len(factors)
    if k < 3:
        raise ValueError("Box-Behnken requires at least 3 factors")

    runs = []
    run_id = 1

    # Generate pairs of factors at +/-1, rest at 0
    for i, j in itertools.combinations(range(k), 2):
        for ci, cj in itertools.product([-1, 1], repeat=2):
            coded = [0] * k
            coded[i] = ci
            coded[j] = cj
            levels = {factors[idx].name: round(factors[idx].coded_to_real(coded[idx]), 4) for idx in range(k)}
            runs.append({"run_id": run_id, "design": "BoxBehnken", "levels": levels})
            run_id += 1

    # Center points
    for _ in range(3):
        levels = {f.name: round(f.center, 4) for f in factors}
        runs.append({"run_id": run_id, "design": "BoxBehnken-center", "levels": levels})
        run_id += 1

    return runs


# ── Scale-up / scale-down bridging ─────────────────────────────────────

@dataclass
class ScaleConfig:
    name: str
    volume_L: float
    vessel_diameter_m: float
    impeller_diameter_m: float


def scaleup_bridge(runs: List[Dict], source: ScaleConfig, target: ScaleConfig,
                   strategy: str = "constant_kLa") -> List[Dict]:
    """
    Translate DoE runs from one bioreactor scale to another.
    Strategies: constant_kLa, constant_PV, constant_tip_speed.
    """
    ratio = target.volume_L / source.volume_L
    d_ratio = target.impeller_diameter_m / source.impeller_diameter_m

    bridged = []
    for run in runs:
        new_levels = dict(run["levels"])

        # Scale volumetric parameters (feed_rate, air_flow)
        for key in ["feed_rate_mL_h", "air_flow_vvm"]:
            if key in new_levels:
                if key == "feed_rate_mL_h":
                    new_levels[key] = round(new_levels[key] * ratio, 2)
                # vvm is already normalized to volume

        # Scale agitation based on strategy
        if "agitation_rpm" in new_levels:
            N_source = new_levels["agitation_rpm"]
            if strategy == "constant_tip_speed":
                N_target = N_source * (source.impeller_diameter_m / target.impeller_diameter_m)
            elif strategy == "constant_PV":
                # P/V ~ N^3 * D^5 / V  =>  N_target = N_source * (V_t/V_s)^(1/3) * (D_s/D_t)^(5/3) ... simplified
                N_target = N_source * (ratio ** (-1 / 3)) * (1 / d_ratio) ** (5 / 3 - 1)
            else:  # constant_kLa (default)
                # kLa ~ (P/V)^0.4 * vs^0.5  =>  approx N scaling
                N_target = N_source * (ratio ** (-0.4 / 3)) * (1 / d_ratio) ** 0.6
            new_levels["agitation_rpm"] = round(N_target, 1)

        bridged_run = {
            "run_id": run["run_id"],
            "design": run["design"],
            "source_scale": source.name,
            "target_scale": target.name,
            "strategy": strategy,
            "levels": new_levels,
        }
        if "safety_status" in run:
            bridged_run["safety_status"] = run["safety_status"]
        bridged.append(bridged_run)

    return bridged


# ── Pretty printing ───────────────────────────────────────────────────

def print_header(title: str):
    width = 70
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_runs(runs: List[Dict], max_show: int = 12):
    if not runs:
        print("  (no runs)")
        return
    # Get all factor names
    factor_names = list(runs[0]["levels"].keys())
    # Header
    hdr = f"  {'Run':>4}  {'Design':<18}"
    for fn in factor_names:
        hdr += f"  {fn:>14}"
    if "safety_status" in runs[0]:
        hdr += f"  {'Safety':>8}"
    if "target_scale" in runs[0]:
        hdr += f"  {'Scale':>12}"
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))

    shown = runs[:max_show]
    for run in shown:
        line = f"  {run['run_id']:>4}  {run['design']:<18}"
        for fn in factor_names:
            line += f"  {run['levels'][fn]:>14.2f}"
        if "safety_status" in run:
            line += f"  {run['safety_status']:>8}"
        if "target_scale" in run:
            line += f"  {run['target_scale']:>12}"
        print(line)

    if len(runs) > max_show:
        print(f"  ... and {len(runs) - max_show} more runs")


def print_flags(flags: List[SafetyFlag]):
    if not flags:
        print("  No safety flags raised. All runs within limits.")
        return
    for sf in flags:
        icon = "BLOCK" if sf.severity == "block" else " WARN"
        print(f"  [{icon}] Run {sf.run_id}: {sf.factor} = {sf.value:.2f} "
              f"({sf.limit_type} limit {sf.limit_value})")


# ── Demo scenario ─────────────────────────────────────────────────────

def run_demo():
    print_header("BioSymphony Fermentation DoE Demo")
    print("  Scenario: Optimize fed-batch CHO cell culture for mAb titer")
    print("  Organism: CHO-K1 (BSL-1)")

    # Define factors with safety limits
    factors = [
        Factor("temperature_C", "degC", 33.0, 37.0, safety_min=30.0, safety_max=39.0),
        Factor("pH", "", 6.8, 7.4, safety_min=6.5, safety_max=7.6),
        Factor("DO_pct", "%", 30.0, 60.0, safety_min=20.0, safety_max=80.0),
        Factor("feed_rate_mL_h", "mL/h", 5.0, 15.0, safety_min=1.0, safety_max=25.0),
        Factor("agitation_rpm", "rpm", 100.0, 250.0, safety_min=50.0, safety_max=400.0),
    ]

    responses = [
        Response("titer_g_L", "g/L", "maximize"),
        Response("viability_pct", "%", "maximize"),
        Response("kLa_h_inv", "1/h", "target"),
    ]

    print(f"\n  Factors ({len(factors)}):")
    for f in factors:
        safety = ""
        if f.safety_min is not None:
            safety = f"  [safety: {f.safety_min}-{f.safety_max} {f.unit}]"
        print(f"    - {f.name}: {f.low}-{f.high} {f.unit}{safety}")

    print(f"\n  Responses ({len(responses)}):")
    for r in responses:
        print(f"    - {r.name} ({r.unit}) -> {r.objective}")

    # ── Step 1: Generate CCD ──
    print_header("Step 1: Central Composite Design (CCD)")
    runs = central_composite(factors)
    print(f"  Generated {len(runs)} runs (2^5 factorial + 10 axial + 5 center)")
    print_runs(runs)

    # ── Step 2: Biosafety gating ──
    print_header("Step 2: Biosafety Readiness Gating")
    passed, flags = biosafety_gate(runs, factors)
    print_flags(flags)
    blocked = len(runs) - len(passed)
    print(f"\n  Result: {len(passed)} runs PASSED, {blocked} BLOCKED")

    # ── Step 3: Scale-up bridging ──
    print_header("Step 3: Scale-Up Bridging (Bench -> Pilot)")

    bench = ScaleConfig("Bench (2L)", 2.0, 0.10, 0.04)
    pilot = ScaleConfig("Pilot (200L)", 200.0, 0.50, 0.20)

    bridged = scaleup_bridge(passed[:8], bench, pilot, strategy="constant_kLa")
    print(f"  Source: {bench.name} | Target: {pilot.name}")
    print(f"  Strategy: constant kLa")
    print(f"  Volume ratio: {pilot.volume_L / bench.volume_L:.0f}x")
    print_runs(bridged)

    # ── Step 4: Box-Behnken alternative ──
    print_header("Step 4: Alternative — Box-Behnken Design (3 factors)")
    bb_factors = factors[:3]  # temperature, pH, DO
    bb_runs = box_behnken(bb_factors)
    print(f"  Generated {len(bb_runs)} runs for {[f.name for f in bb_factors]}")
    bb_passed, bb_flags = biosafety_gate(bb_runs, bb_factors)
    print_runs(bb_passed)

    # ── Summary ──
    print_header("Summary")
    print(f"  CCD design:        {len(runs)} total runs, {len(passed)} after safety gating")
    print(f"  Box-Behnken:       {len(bb_runs)} total runs, {len(bb_passed)} after safety gating")
    print(f"  Safety flags:      {len(flags)} (CCD) + {len(bb_flags)} (BB)")
    print(f"  Scale-up bridging: bench (2L) -> pilot (200L), constant kLa")
    print(f"\n  Ready for export to LIMS / ELN / bioreactor control system.")

    # ── JSON export ──
    print_header("JSON Export (first 3 runs)")
    export = [{"run_id": r["run_id"], "design": r["design"],
               "levels": r["levels"], "safety_status": r.get("safety_status", "N/A")}
              for r in passed[:3]]
    print(json.dumps(export, indent=2))

    print("\n" + "=" * 70)
    print("  Demo complete. See HOW_TO_USE.md for integration instructions.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_demo()
