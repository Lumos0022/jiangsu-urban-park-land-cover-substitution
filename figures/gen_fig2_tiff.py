# -*- coding: utf-8 -*-
"""Regenerate Fig2 tiff (600 dpi, uncompressed) from the new PNG; sync to all figure dirs."""
from PIL import Image
from pathlib import Path

dirs = [
    Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\AAA投稿前最终版本\P01_FULL_SUBMISSION_PACKAGE_20260915\05_Figures"),
    Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\09_Manuscript\投稿前\P01_v4_FINAL_SUBMISSION_PACKAGE_20260914\05_Figures"),
]
for d in dirs:
    png = d / "Fig2_composition_associations.png"
    tif = d / "Fig2_composition_associations.tiff"
    im = Image.open(png)
    im.save(tif, format="TIFF", compression=None, dpi=(600, 600))
    print(tif, im.size, tif.stat().st_size)
