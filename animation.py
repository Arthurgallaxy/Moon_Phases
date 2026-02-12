import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

AU = 1.495978707e11  # meters


def load_body_csvs(folder="Sim_data", pattern="body*.csv"):
    paths = sorted(glob.glob(os.path.join(folder, pattern)))
    if not paths:
        raise FileNotFoundError(f"No files matched {os.path.join(folder, pattern)}")

    data = []
    for p in paths:
        arr = np.loadtxt(p, delimiter=",")
        if arr.ndim != 2 or arr.shape[1] < 2:
            raise ValueError(f"{p}: expected Nx2 or Nx3 numeric data, got shape {arr.shape}")

        if arr.shape[1] == 2:
            arr = np.column_stack([arr, np.zeros(arr.shape[0])])
        else:
            arr = arr[:, :3]

        # Remove non-finite rows (prevents broken limits / jitter)
        mask = np.isfinite(arr).all(axis=1)
        arr = arr[mask]
        data.append(arr)

    n = min(d.shape[0] for d in data)
    data = [d[:n] for d in data]
    return paths, np.stack(data, axis=0)  # (B, T, 3)


def animate_orbits(
    folder="Sim_data",
    pattern="body*.csv",
    labels=None,
    stride=10,
    interval=20,
    trail=800,
    viewpoint="earth",      # "system" or "earth"
    center_on=0,             # used for "system" viewpoint (0=sun)
    earth_index=1,           # used for "earth" viewpoint
    window_au=0.01,          # used for "earth" viewpoint (half-width)
):
    """
    viewpoint="system":
        - subtracts center_on body from all positions (e.g., heliocentric)
        - fixed axis limits based on whole dataset
    viewpoint="earth":
        - camera follows earth_index body
        - axis limits recentered each frame to +/- window_au around Earth
    """
    viewpoint = viewpoint.lower().strip()
    if viewpoint not in {"system", "earth"}:
        raise ValueError('viewpoint must be "system" or "earth"')

    paths, pos = load_body_csvs(folder, pattern)  # meters
    B, T, _ = pos.shape

    if labels is None:
        labels = [os.path.splitext(os.path.basename(p))[0] for p in paths]

    # Centering for system view
    if viewpoint == "system":
        pos = pos - pos[center_on:center_on + 1, :, :]

    # 2D positions in AU
    xy = pos[:, :, :2] / AU

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x (AU)")
    ax.set_ylabel("y (AU)")

    points, trails = [], []
    for i in range(B):
        (pt,) = ax.plot([], [], "o", label=labels[i])
        (tr,) = ax.plot([], [], linewidth=1, alpha=0.7)
        points.append(pt)
        trails.append(tr)

    ax.legend(loc="upper right")

    frames = list(range(0, T, stride))

    # Precompute fixed limits for "system"
    if viewpoint == "system":
        flat = xy.reshape(-1, 2)
        finite = np.isfinite(flat).all(axis=1)
        if not np.any(finite):
            raise ValueError("All positions are non-finite (nan/inf). Check your CSV files.")
        flat_f = flat[finite]
        rmax = np.max(np.sqrt(flat_f[:, 0] ** 2 + flat_f[:, 1] ** 2))
        if not np.isfinite(rmax) or rmax == 0:
            rmax = 1.0
        L = rmax * 1.05
        ax.set_xlim(-L, L)
        ax.set_ylim(-L, L)

    half = float(window_au)

    def init():
        for i in range(B):
            points[i].set_data([], [])
            trails[i].set_data([], [])
        return points + trails

    def update(k):
        # Camera control
        if viewpoint == "earth":
            cx, cy = xy[earth_index, k]
            ax.set_xlim(cx - half, cx + half)
            ax.set_ylim(cy - half, cy + half)

        # Update artists
        for i in range(B):
            x, y = xy[i, k]
            points[i].set_data([x], [y])

            start = max(0, k - trail * stride)
            xs = xy[i, start:k + 1:stride, 0]
            ys = xy[i, start:k + 1:stride, 1]
            trails[i].set_data(xs, ys)

        if viewpoint == "earth":
            ax.set_title(f"View: Earth-follow | timestep {k}/{T-1}")
        else:
            ax.set_title(f"View: System (center_on={center_on}) | timestep {k}/{T-1}")

        return points + trails

    anim = FuncAnimation(
        fig,
        update,
        frames=frames,
        init_func=init,
        interval=interval,
        blit=False,
        repeat=True,
    )

    return fig, anim


if __name__ == "__main__":
    # Full solar system view (heliocentric)
    """fig, anim = animate_orbits(
        labels=["Sun", "Earth", "Moon"],
        viewpoint="earth",
        earth_index=1,
        window_au=0.01,
        stride=10,
        interval=20,
        trail=800,
    )
    plt.show()"""
    fig, anim = animate_orbits(
        labels=["Sun", "Earth", "Moon"],
        viewpoint="system",
        center_on=0,
        stride=10,
        interval=20,
        trail=600,
    )
    plt.show()

    #Earth-follow view (zoom around Earth)

