"""Track manually defined samples, alignment offsets, and measurement history.

Load into the shared Bluesky startup namespace (for example with ``%run -i``)
before using motor methods. They expect ``x2`` and ``IN_SIM_MODE``, plus ``sh``
and ``sh2`` when their offsets are used outside simulation. This module does
not initialize hardware or make real motors simulated.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import math
from pathlib import Path
import tempfile
import time


@dataclass
class Sample:
    """Store sample state independently.

    ``pos`` is the reference x2 position in mm, rounded to one decimal.
    ``counter`` identifies the next measurement and advances after recording.
    ``name_type`` is a naming suffix setting for measurement code.
    ``sh_offset`` and ``sh2_offset`` store motor user-coordinate offsets at full
    precision; None means no alignment offset has been saved for that motor.
    ``clock_o`` is the sample's creation or reset time in Unix seconds.
    Histories and offsets live in memory; only measurement records are saved
    to disk after calling configure_history().
    """

    name: str
    pos: float # x2 position
    counter: int = 0 # default counter value of 0
    name_type: str = "Time" # appendix to the sample name when saving files
    sh_offset: float | None = None
    sh2_offset: float | None = None
    clock_o: float = field(default_factory=time.time, init=False)
    measurement_history: list[dict] = field(default_factory=list, init=False)
    _history_file: Path | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        """Round the initial reference position to one decimal place in mm."""
        self.pos = round(self.pos, 1)

    def reset_clock(self) -> None:
        """Restart this sample's elapsed-time clock at the current wall time."""
        self.clock_o = time.time()

    def clock(self) -> float:
        """Return elapsed seconds since creation or the last reset_clock()."""
        return time.time() - self.clock_o

    def update_sh_offset(self, value: float | None = None, *, motor: str = "sh") -> None:
        """Update the saved user-coordinate offset for 'sh' or 'sh2'.

        If value is omitted, read the selected motor's user_offset signal.
        In IN_SIM_MODE, clear only the selected saved offset to None without
        accessing a motor. Otherwise retain full precision and reject nonfinite
        values. Invalid motor names raise ValueError. No file is written.
        """
        attributes = {"sh": "sh_offset", "sh2": "sh2_offset"}
        if motor not in attributes:
            raise ValueError("Height motor must be 'sh' or 'sh2'")
        if IN_SIM_MODE:
            setattr(self, attributes[motor], None)
            return
        if value is None:
            value = (sh if motor == "sh" else sh2).user_offset.get()
        if not math.isfinite(value):
            raise ValueError("Sample-height offset must be finite")
        setattr(self, attributes[motor], value)

    def gotoOrigin(self, *, position_motor=None, height_motor=None, height2_motor=None):
        """Yield a Bluesky plan returning the sample to its aligned origin.

        Run with ``RE(sample.gotoOrigin())``. The position motor defaults to x2
        and moves to self.pos rounded to one decimal in mm. Restore each saved
        user_offset, then move both height motors to zero. A missing saved
        offset leaves that motor's current user_offset unchanged, but does not
        skip its move to zero. IN_SIM_MODE skips both height motors, but still
        moves the supplied or session position motor.

        Optional motor arguments override x2, sh, and sh2 respectively. Required
        height signals and finite targets are checked before the first move.
        Each set operation is awaited; the counter and history are unchanged.
        """
        # import bluesky.plan_stubs as bps

        target = round(self.pos, 1)
        if not math.isfinite(target):
            raise ValueError("Target position must be finite")
        if position_motor is None:
            position_motor = x2
        in_sim_mode = IN_SIM_MODE
        height_targets = []
        for name, motor, offset in (
            ("sh", height_motor, self.sh_offset),
            ("sh2", height2_motor, self.sh2_offset),
        ):
            if in_sim_mode:
                continue
            if offset is not None and not math.isfinite(offset):
                raise ValueError("Sample-height offset must be finite")
            if motor is None:
                motor = sh if name == "sh" else sh2
            offset_signal = motor.user_offset if offset is not None else None
            height_targets.append((motor, offset_signal, offset))
        yield from bps.mv(position_motor, target)
        # Restore both coordinate systems before moving either height motor.
        for motor, offset_signal, offset in height_targets:
            if offset_signal is not None:
                yield from bps.mv(offset_signal, offset)
        for motor, offset_signal, offset in height_targets:
            yield from bps.mv(motor, 0)
    ### TODO need to do more testing for rest of the code
    def configure_history(self, history_file: str | Path) -> Path:
        """Attach a shared JSON file and return its resolved absolute path.

        Create missing parent folders and a sample entry, then replace the
        in-memory history with records keyed by self.name. Names must identify
        samples uniquely within this file. Resume the counter beyond saved
        measurement counters without decreasing its current value.

        Call before recording: pre-existing memory-only records are not merged.
        Malformed files raise an error instead of being overwritten. Shared
        files support multiple samples, but not concurrent writing processes.
        """
        history_file = Path(history_file).expanduser().resolve()
        history_file.parent.mkdir(parents=True, exist_ok=True)
        records = self._read_history(history_file)
        if self.name not in records:
            records[self.name] = []
            self._write_history(history_file, records)
        self.measurement_history = records[self.name]
        counters = [record["counter"] for record in self.measurement_history if "counter" in record]
        if counters:
            self.counter = max(self.counter, max(counters) + 1)
        self._history_file = history_file
        return history_file

    def record_measurement(self, technique: str, position: float) -> None:
        """Record one measurement at an absolute position in mm.

        Save the current counter, reference position, technique, position,
        relative offset, and Unix timestamp. Positions and relative offsets
        use one decimal. The caller decides when a measurement counts as used;
        this method neither runs a scan nor moves hardware.

        If configured, write to disk before updating memory and incrementing
        the counter. A failed save leaves those in-memory values unchanged.
        Without a configured file, keep the record in memory only.
        """
        position = round(position, 1)
        sample_pos = round(self.pos, 1)
        record = {
            "counter": self.counter,
            "sample_pos": sample_pos,
            "technique": technique,
            "position": position,
            "offset": round(position - sample_pos, 1),
            "timestamp": time.time(),
        }
        if self._history_file is None:
            self.measurement_history.append(record)
        else:
            records = self._read_history(self._history_file)
            records.setdefault(self.name, []).append(record)
            self._write_history(self._history_file, records)
            self.measurement_history = records[self.name]
        self.counter += 1

    def plot_history(self, ax=None, beam_size: float = 0.2):
        """Return Matplotlib axes showing where each technique was used.

        beam_size is a positive, finite footprint width in mm, applied to all
        records in this view. Squares span that width along x; technique sets
        their color. Overlapping footprints are stacked in recording order on
        the first available level, while touching edges may share a level.
        Levels indicate overlap packing, not an exact exposure-frequency curve.

        Draw a red dashed reference at self.pos. Create axes if ax is omitted;
        otherwise add to the supplied axes. The caller displays or saves the
        figure. Records are not changed, and empty histories are supported.
        """
        import matplotlib.pyplot as plt
        from matplotlib.patches import Patch, Rectangle
        from matplotlib.ticker import FormatStrFormatter

        if not math.isfinite(beam_size) or beam_size <= 0:
            raise ValueError("Beam size must be a positive finite width in mm")
        techniques = list(dict.fromkeys(record["technique"] for record in self.measurement_history))
        levels = []
        footprints = []
        # Pack each footprint into the lowest non-overlapping level.
        for record in self.measurement_history:
            position = round(record["position"], 1)
            left = position - beam_size / 2
            right = position + beam_size / 2
            for level, intervals in enumerate(levels):
                if all(
                    right <= start or math.isclose(right, start, rel_tol=0, abs_tol=1e-12)
                    or left >= end or math.isclose(left, end, rel_tol=0, abs_tol=1e-12)
                    for start, end in intervals
                ):
                    break
            else:
                level = len(levels)
                levels.append([])
            levels[level].append((left, right))
            footprints.append((record["technique"], left, level + 1))
        if ax is None:
            _, ax = plt.subplots(figsize=(8, max(3, 0.5 * len(levels) + 1.8)), layout="constrained")
        colors = plt.get_cmap("tab10")
        technique_colors = {technique: colors(index % 10) for index, technique in enumerate(techniques)}
        for technique, left, level in footprints:
            ax.add_patch(Rectangle((left, level - 0.4), beam_size, 0.8,
                                   facecolor=technique_colors[technique], edgecolor="white",
                                   linewidth=0.8, zorder=3))
        central_position = round(self.pos, 1)
        ax.axvline(central_position, color="red", linestyle="--", linewidth=1.2,
               label=f"central position ({central_position:.1f})", zorder=1)
        ax.xaxis.set_major_formatter(FormatStrFormatter("%.1f"))
        ax.set_yticks(range(1, len(levels) + 1))
        ax.set_ylim(0.4, max(len(levels), 1) + 0.6)
        # Match the displayed x-width and y-height so footprints look square.
        ax.set_aspect(beam_size / 0.8, adjustable="box")
        ax.set_xlabel("Position (mm)")
        ax.set_ylabel("Overlap level")
        ax.set_title("Measurement history")
        ax.set_axisbelow(True)
        ax.grid(axis="x", color="0.9")
        ax.margins(x=0.12)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        handles = [Patch(facecolor=technique_colors[technique], label=technique) for technique in techniques]
        handles.append(ax.lines[-1])
        ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.02, 1),
              frameon=False, fontsize=9)
        if not techniques:
            ax.text(0.5, 0.5, "No measurements recorded", transform=ax.transAxes,
                    ha="center", va="center", color="0.4")
        return ax

    @staticmethod
    def _read_history(path: Path) -> dict[str, list[dict]]:
        """Read histories keyed by sample name; return {} for a missing file.

        Accept the earlier flat-list format and group it in memory, removing
        redundant sample_name fields. Conversion is saved on a later write.
        Invalid JSON or an invalid container structure raises ValueError;
        individual measurement fields are not validated here.
        """
        if not path.exists():
            return {}
        with path.open(encoding="utf-8") as stream:
            records = json.load(stream)
        if isinstance(records, list):
            grouped = {}
            for record in records:
                if not isinstance(record, dict) or not isinstance(record.get("sample_name"), str):
                    raise ValueError("Legacy history records must include a sample name")
                grouped.setdefault(record["sample_name"], []).append(
                    {key: value for key, value in record.items() if key != "sample_name"}
                )
            records = grouped
        if not isinstance(records, dict) or not all(
            isinstance(history, list) and all(isinstance(record, dict) for record in history)
            for history in records.values()
        ):
            raise ValueError("Sample history must map sample names to lists of records")
        return records

    @staticmethod
    def _write_history(path: Path, records: dict[str, list[dict]]) -> None:
        """Atomically replace a history file with finite-valued JSON records.

        The parent directory must exist. Write and close a temporary file in
        that directory before replacing the destination; clean up temporary
        files on failure. This avoids partial destination writes, but does not
        lock out concurrent writers or guarantee durability after power loss.
        """
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as stream:
                temporary_path = Path(stream.name)
                json.dump(records, stream, indent=2, allow_nan=False)
                stream.write("\n")
            # Same-directory replacement keeps the old file until writing succeeds.
            temporary_path.replace(path)
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()




