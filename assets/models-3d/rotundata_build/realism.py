"""Photoreal shading for the realistic variant.

The aquarium cutaway and the growth stay the same. These settings only change
how the surfaces read: wet leaves, grainy sand, and a little light through
the blade. Subsurface does not survive the phone export; the shape does.
"""

import bpy

from .util import sock


def _bsdf(mat):
    return next(node for node in mat.node_tree.nodes if node.type == "BSDF_PRINCIPLED")


def _set(bsdf, names, value):
    for name in names:
        try:
            sock(bsdf, name).default_value = value
            return True
        except KeyError:
            continue
    return False


def _bump(mat, strength):
    nodes = mat.node_tree.nodes
    if any(node.type == "BUMP" for node in nodes):
        return
    tex = next((node for node in nodes if node.type == "TEX_IMAGE"), None)
    if tex is None:
        return
    bump = nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = strength
    bump.inputs["Distance"].default_value = 0.001
    mat.node_tree.links.new(tex.outputs["Color"], bump.inputs["Height"])
    mat.node_tree.links.new(bump.outputs["Normal"], sock(_bsdf(mat), "Normal"))


def _leaf(mat, weight):
    bsdf = _bsdf(mat)
    _set(bsdf, ("Roughness",), 0.34)
    _set(bsdf, ("Specular IOR Level", "Specular"), 0.32)
    _set(bsdf, ("Subsurface Weight", "Subsurface"), weight)
    _set(bsdf, ("Subsurface Radius",), (0.15, 0.45, 0.08))
    _set(bsdf, ("Subsurface Scale",), 0.002)
    _bump(mat, 0.18)


def lesson_shade():
    """A little light through the blade and grain in the sand. Roughness stays matte."""
    leaves = bpy.data.materials.get("CrLeaf")
    young = bpy.data.materials.get("CrLeafYoung")
    if leaves:
        _leaf(leaves, 0.18)
        _set(_bsdf(leaves), ("Roughness",), 0.55)
        _set(_bsdf(leaves), ("Specular IOR Level", "Specular"), 0.16)
    if young:
        _leaf(young, 0.22)
        _set(_bsdf(young), ("Roughness",), 0.52)
        _set(_bsdf(young), ("Specular IOR Level", "Specular"), 0.16)
    sand = bpy.data.materials.get("CrSand")
    if sand:
        _set(_bsdf(sand), ("Roughness",), 0.82)
        _bump(sand, 0.35)
    sheath = bpy.data.materials.get("CrSheath")
    if sheath:
        _set(_bsdf(sheath), ("Roughness",), 0.48)
        _set(_bsdf(sheath), ("Subsurface Weight", "Subsurface"), 0.12)
        _set(_bsdf(sheath), ("Subsurface Scale",), 0.001)
    print("lesson shade applied")


def apply():
    leaves = bpy.data.materials.get("CrLeaf")
    young = bpy.data.materials.get("CrLeafYoung")
    if leaves:
        _leaf(leaves, 0.42)
    if young:
        _leaf(young, 0.55)
    for name, rough, bump in (
        ("CrSand", 0.78, 0.55),
        ("CrRhizome", 0.42, 0.0),
        ("CrRoot", 0.62, 0.0),
        ("CrStem", 0.4, 0.0),
        ("CrSheath", 0.38, 0.0),
    ):
        mat = bpy.data.materials.get(name)
        if mat is None:
            continue
        bsdf = _bsdf(mat)
        _set(bsdf, ("Roughness",), rough)
        if name == "CrSheath":
            _set(bsdf, ("Subsurface Weight", "Subsurface"), 0.2)
            _set(bsdf, ("Subsurface Scale",), 0.001)
        if bump:
            _bump(mat, bump)
    sun = bpy.data.objects.get("Light")
    if sun and sun.type == "LIGHT":
        sun.data.energy = 4.2
        sun.data.angle = 0.35
    print("realistic shading applied")
