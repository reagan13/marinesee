"""Small helpers shared by the builder modules."""

import bisect
import math

import bpy
from mathutils import Vector


def srgb(r, g, b):
    def f(u):
        return u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4

    return (f(r), f(g), f(b), 1.0)


def sock(node, identifier):
    for item in node.inputs:
        if item.identifier == identifier:
            return item
    raise KeyError(identifier)


def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def set_mode(obj, mode):
    view = bpy.context.view_layer
    view.objects.active = obj
    obj.select_set(True)
    with bpy.context.temp_override(active_object=obj, object=obj):
        bpy.ops.object.mode_set(mode=mode)


def tag(obj):
    obj["cr_plant"] = 1
    return obj


def collection(name):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    col["cr_plant"] = 1
    return col


def link(obj, col):
    for other in list(obj.users_collection):
        if other != col:
            other.objects.unlink(obj)
    if obj.name not in col.objects:
        col.objects.link(obj)
    return obj


def layer_collection(name, root=None):
    root = root or bpy.context.view_layer.layer_collection
    if root.collection.name == name:
        return root
    for child in root.children:
        found = layer_collection(name, child)
        if found:
            return found
    return None


def cubic(p0, h0, h1, p1, t):
    u = 1.0 - t
    return (u * u * u) * p0 + (3 * u * u * t) * h0 + (3 * u * t * t) * h1 + (t * t * t) * p1


def set_bezier(spline, points):
    """Write points with Catmull-Rom style handles, then let Blender keep them AUTO."""
    bps = spline.bezier_points
    if len(bps) < len(points):
        bps.add(len(points) - len(bps))
    n = len(points)
    for i, point in enumerate(points):
        if i == 0:
            d = (points[1] - points[0]) / 3.0
        elif i == n - 1:
            d = (points[-1] - points[-2]) / 3.0
        else:
            d = (points[i + 1] - points[i - 1]) / 6.0
        bp = bps[i]
        bp.co = point
        bp.handle_left = point - d
        bp.handle_right = point + d
        bp.handle_left_type = "AUTO"
        bp.handle_right_type = "AUTO"


def control_points(obj):
    world = obj.matrix_world
    return [world @ Vector(bp.co) for bp in obj.data.splines[0].bezier_points]


def dense_points(obj, per_seg=48):
    """World-space polyline along the first Bezier spline of a curve object."""
    bps = obj.data.splines[0].bezier_points
    world = obj.matrix_world
    pts = []
    for i in range(len(bps) - 1):
        p0, h0 = Vector(bps[i].co), Vector(bps[i].handle_right)
        h1, p1 = Vector(bps[i + 1].handle_left), Vector(bps[i + 1].co)
        for s in range(per_seg):
            pts.append(world @ cubic(p0, h0, h1, p1, s / per_seg))
    pts.append(world @ Vector(bps[-1].co))
    return pts


def arc_table(pts):
    cum = [0.0]
    for a, b in zip(pts, pts[1:]):
        cum.append(cum[-1] + (b - a).length)
    return cum


def point_at(pts, cum, d):
    d = max(0.0, min(cum[-1], d))
    i = min(len(pts) - 2, max(0, bisect.bisect_right(cum, d) - 1))
    seg = cum[i + 1] - cum[i]
    t = 0.0 if seg < 1e-12 else (d - cum[i]) / seg
    return pts[i].lerp(pts[i + 1], t)


def tangent_at(pts, cum, d, eps=2e-4):
    a = point_at(pts, cum, d - eps)
    b = point_at(pts, cum, d + eps)
    t = b - a
    return t.normalized() if t.length > 1e-10 else Vector((0.0, 0.0, 1.0))


def frame_at(tangent, side_hint, twist=0.0):
    """Side and normal perpendicular to the tangent, side kept close to the hint."""
    side = side_hint - tangent * side_hint.dot(tangent)
    if side.length < 1e-6:
        side = tangent.orthogonal()
    side.normalize()
    normal = tangent.cross(side).normalized()
    side = normal.cross(tangent).normalized()
    if twist:
        c, s = math.cos(twist), math.sin(twist)
        side, normal = side * c + normal * s, normal * c - side * s
    return side, normal


def safe_hint(direction, hint):
    d = direction.normalized()
    h = hint.normalized()
    if abs(d.dot(h)) > 0.95:
        h = d.orthogonal().normalized()
    return h
