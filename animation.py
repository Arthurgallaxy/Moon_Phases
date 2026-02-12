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

        # drop non-finite rows (prevents broken limits / single-frame weirdness)
        mask = np.isfinite(arr).all(axis=1)
        arr = arr[mask]
        data.append(arr)

    n = min(d.shape[0] for d in data)
    data = [d[:n] for d in data]
    return paths, np.stack(data, axis=0)  # (B, T, 3)


def animate_follow_earth(
    folder="Sim_data",
    pattern="body*.csv",
    labels=None,
    earth_index=1,
    stride=10,
    interval=20,
    trail=800,              # how many plotted points in the trail (in frames, not seconds)
    window_au=0.02,          # camera half-width in AU (0.02 AU ~ 3 million km)
):
    paths, pos = load_body_csvs(folder, pattern)
    B, T, _ = pos.shape

    if labels is None:
        labels = [os.path.splitext(os.path.basename(p))[0] for p in paths]

    # Use x,y only, convert to AU for readable axes
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
    half = float(window_au)

    def init():
        for i in range(B):
            points[i].set_data([], [])
            trails[i].set_data([], [])
        return points + trails

    def update(k):
        # Camera center = Earth position at frame k
        cx, cy = xy[earth_index, k]

        # Set view window centered on Earth
        ax.set_xlim(cx - half, cx + half)
        ax.set_ylim(cy - half, cy + half)

        # Update each body
        for i in range(B):
            x, y = xy[i, k]
            points[i].set_data([x], [y])

            start = max(0, k - trail * stride)
            xs = xy[i, start:k + 1:stride, 0]
            ys = xy[i, start:k + 1:stride, 1]
            trails[i].set_data(xs, ys)

        ax.set_title(f"Following Earth (body {earth_index}) | timestep {k}/{T-1}")
        return points + trails

    anim = FuncAnimation(
        fig,
        update,
        frames=frames,
        init_func=init,
        interval=interval,
        blit=False,   # more reliable across backends
        repeat=True,
    )

    return fig, anim


if __name__ == "__main__":
    fig, anim = animate_follow_earth(
        folder="Sim_data",
        pattern="body*.csv",
        labels=["Sun", "Earth", "Moon"],
        earth_index=1,
        stride=10,
        interval=20,
        trail=800,
        window_au=0.01,   # zoom: try 0.005..0.05
    )

    # IMPORTANT: keep reference to anim until after show()
    plt.show()
