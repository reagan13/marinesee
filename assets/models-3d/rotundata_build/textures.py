"""Packed images and materials. Veins and sand grain live in images so they survive glTF export."""

import bpy
import numpy as np

from .util import sock, srgb

LEAF = {"base": (0.24, 0.48, 0.22), "vein": (0.13, 0.32, 0.13), "tip": (0.40, 0.58, 0.28), "pale": (0.66, 0.70, 0.46)}
YOUNG = {"base": (0.45, 0.68, 0.34), "vein": (0.30, 0.50, 0.24), "tip": (0.56, 0.75, 0.40), "pale": (0.76, 0.80, 0.56)}


def vein_xs(vein_count):
    """Vein lane positions across the strap, -1..1 is edge to edge."""
    if vein_count <= 1:
        return [0.0]
    return [-0.9 + 1.8 * k / (vein_count - 1) for k in range(vein_count)]


def _image(name, w, h):
    img = bpy.data.images.get(name)
    if img is not None and tuple(img.size) != (w, h):
        bpy.data.images.remove(img)
        img = None
    if img is None:
        img = bpy.data.images.new(name, w, h, alpha=False, float_buffer=False)
    img.colorspace_settings.name = "sRGB"
    return img


def _fill(img, rgb):
    h, w, _ = rgb.shape
    rgba = np.ones((h, w, 4), dtype=np.float32)
    rgba[..., :3] = np.clip(rgb, 0.0, 1.0)
    img.pixels.foreach_set(rgba.ravel())
    img.update()
    img.pack()


def leaf_image(name, pal, vein_count, w=256, h=512, seed=3):
    rng = np.random.default_rng(seed)
    u = np.linspace(0.0, 1.0, w)[None, :]
    v = np.linspace(0.0, 1.0, h)[:, None]
    lanes = 0.5 + 0.5 * np.array(vein_xs(vein_count))
    stripe = np.max(np.exp(-((u[..., None] - lanes) ** 2) / (2 * 0.007 ** 2)), axis=-1)
    base, vein, tip, pale = (np.array(pal[k]) for k in ("base", "vein", "tip", "pale"))
    t = np.clip(v / 0.16, 0.0, 1.0)
    s = (t * t * (3 - 2 * t))[..., None]
    col = pale * (1 - s) + base * s
    tt = np.clip((v - 0.78) / 0.22, 0.0, 1.0)[..., None] * 0.6
    col = col * (1 - tt) + tip * tt
    col = np.broadcast_to(col, (h, w, 3)).copy()
    k = stripe[..., None] * 0.22
    col = col * (1 - k) + vein * k
    edge = np.clip((np.abs(u - 0.5) * 2 - 0.9) / 0.1, 0.0, 1.0)
    col *= (1 - 0.06 * edge)[..., None]
    streak = np.convolve(rng.normal(0, 1, w), np.ones(5) / 5, mode="same") * 0.018
    col *= (1 + streak)[None, :, None]
    img = _image(name, w, h)
    _fill(img, col)
    img["cr_veins"] = vein_count
    return img


def sand_image(name="CrSandGrain", n=256, seed=5):
    rng = np.random.default_rng(seed)
    u = np.linspace(0.0, 1.0, n, endpoint=False)[None, :]
    v = np.linspace(0.0, 1.0, n, endpoint=False)[:, None]
    tau = 2 * np.pi
    waves = 0.5 + 0.5 * (0.5 * np.sin(tau * (7 * u + 2 * v)) + 0.5 * np.sin(tau * (3 * u - 5 * v) + 1.7))
    speck = rng.random((n, n))
    base = np.array((0.84, 0.75, 0.58))
    light = np.array((0.95, 0.89, 0.74))
    shade = np.array((0.60, 0.50, 0.37))
    col = base * (0.90 + 0.10 * waves[..., None])
    col = np.where((speck > 0.93)[..., None], light, col)
    col = np.where((speck < 0.05)[..., None], shade, col)
    img = _image(name, n, n)
    _fill(img, col)
    return img


def _principled(name, color, rough, spec=0.22):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.use_backface_culling = False
    mat.diffuse_color = srgb(*color)
    bsdf = next(node for node in mat.node_tree.nodes if node.type == "BSDF_PRINCIPLED")
    sock(bsdf, "Base Color").default_value = srgb(*color)
    sock(bsdf, "Roughness").default_value = rough
    sock(bsdf, "Metallic").default_value = 0.0
    sock(bsdf, "Specular IOR Level").default_value = spec
    return mat


def _attach(mat, img):
    nodes = mat.node_tree.nodes
    bsdf = next(node for node in nodes if node.type == "BSDF_PRINCIPLED")
    tex = next((node for node in nodes if node.type == "TEX_IMAGE"), None) or nodes.new("ShaderNodeTexImage")
    tex.image = img
    mat.node_tree.links.new(tex.outputs["Color"], sock(bsdf, "Base Color"))
    return mat


def ensure_materials(vein_count):
    def leaf_img(name, pal):
        img = bpy.data.images.get(name)
        if img is None or img.get("cr_veins") != vein_count:
            img = leaf_image(name, pal, vein_count)
        return img

    sand = bpy.data.images.get("CrSandGrain") or sand_image()
    return {
        "leaf": _attach(_principled("CrLeaf", LEAF["base"], 0.52, 0.2), leaf_img("CrLeafVeins", LEAF)),
        "young": _attach(_principled("CrLeafYoung", YOUNG["base"], 0.55, 0.18), leaf_img("CrYoungVeins", YOUNG)),
        "rhizome": _principled("CrRhizome", (0.80, 0.72, 0.56), 0.5, 0.16),
        "root": _principled("CrRoot", (0.93, 0.88, 0.75), 0.72, 0.1),
        "stem": _principled("CrStem", (0.62, 0.66, 0.42), 0.55, 0.14),
        "sheath": _principled("CrSheath", (0.70, 0.74, 0.48), 0.6, 0.14),
        "scar": _principled("CrScar", (0.45, 0.36, 0.24), 0.5, 0.16),
        "sand": _attach(_principled("CrSand", (0.84, 0.75, 0.58), 0.92, 0.06), sand),
    }
