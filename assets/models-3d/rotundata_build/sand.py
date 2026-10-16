"""Irregular low reef-sand mound with ripples, a rhizome groove, and a solid base."""

import math

import bmesh

from .geometry import bm_to_mesh


def sand_radii(ang):
    rx = 0.22 * (1.0 + 0.09 * math.sin(3 * ang) + 0.04 * math.sin(5 * ang + 0.6))
    ry = 0.15 * (1.0 + 0.11 * math.cos(2 * ang + 0.4) + 0.04 * math.sin(4 * ang + 1.1))
    return rx, ry


def dist_to_path(x, y, path):
    best = 1e9
    for (ax, ay), (bx, by) in zip(path, path[1:]):
        dx, dy = bx - ax, by - ay
        t = max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy + 1e-12)))
        best = min(best, math.hypot(x - ax - dx * t, y - ay - dy * t))
    return best


def sand_height(x, y, path):
    """path: list of (x, y) along the rhizome. The groove follows it; ripples calm inside it."""
    rx, ry = sand_radii(math.atan2(y, x + 1e-9))
    r = math.sqrt((x / rx) ** 2 + (y / ry) ** 2)
    fall = max(0.0, 1.0 - r) ** 0.75
    d = dist_to_path(x, y, path) if path else 1.0
    calm = min(1.0, d / 0.018)
    mound = 0.012 * math.exp(-1.6 * r * r)
    ripple = (0.0016 * math.sin(x * 46.0 + y * 9.0) + 0.0010 * math.sin(-x * 14.0 + y * 58.0 + 0.7)) * calm
    lump = 0.0014 * math.sin(x * 11.0 + 0.4) * math.cos(y * 13.0)
    h = (mound + ripple + lump) * (0.25 + 0.75 * fall)
    if d < 0.014:
        h -= 0.0035 * 0.5 * (1.0 + math.cos(math.pi * d / 0.014))
    return h


def build_sand(name, path, bottom, cols=44, rows=40):
    path = path[::6] + [path[-1]] if len(path) > 12 else path
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    tile = 0.08
    grid = []
    for j in range(rows + 1):
        t = -1.0 + 2.0 * j / rows
        v = t * (0.35 + 0.65 * t * t)
        row = []
        for i in range(cols + 1):
            u = -1.0 + 2.0 * i / cols
            xd = u * math.sqrt(max(0.0, 1.0 - v * v / 2))
            yd = v * math.sqrt(max(0.0, 1.0 - u * u / 2))
            rx, ry = sand_radii(math.atan2(yd, xd + 1e-12))
            x, y = xd * rx, yd * ry
            row.append(bm.verts.new((x, y, sand_height(x, y, path))))
        grid.append(row)
    for j in range(rows):
        for i in range(cols):
            face = bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
            for loop in face.loops:
                loop[uv].uv = (loop.vert.co.x / tile, loop.vert.co.y / tile)

    rim = [grid[0][i] for i in range(cols + 1)]
    rim += [grid[j][cols] for j in range(1, rows + 1)]
    rim += [grid[rows][i] for i in range(cols - 1, -1, -1)]
    rim += [grid[j][0] for j in range(rows - 1, 0, -1)]
    low = [bm.verts.new((vert.co.x, vert.co.y, bottom)) for vert in rim]
    run = 0.0
    n = len(rim)
    for k in range(n):
        k2 = (k + 1) % n
        step = (rim[k2].co - rim[k].co).length
        face = bm.faces.new((rim[k], low[k], low[k2], rim[k2]))
        for loop, c in zip(face.loops, ((run, 1.0), (run, 0.0), (run + step, 0.0), (run + step, 1.0))):
            loop[uv].uv = (c[0] / tile, c[1] * 0.3)
        run += step
    base = bm.faces.new(tuple(reversed(low)))
    for loop in base.loops:
        loop[uv].uv = (loop.vert.co.x / tile, loop.vert.co.y / tile)
    return bm_to_mesh(bm, name)
