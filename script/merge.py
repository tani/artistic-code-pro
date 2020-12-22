#!/usr/bin/env python3
from typing import List
import fontforge
import psMat
from fire import Fire


def merge_fonts(source_font: fontforge.font, *extra_fonts: List[fontforge.font]):
    """Merging Font

    This function merges extra_fonts to soruce_font.
    Compared to the built-in function,
    it skips to merge if the glyph is already defined.
    """
    if len(extra_fonts) == 0:
        return
    source_codepoints = set(
        g.encoding for g in source_font.glyphs() if g.isWorthOutputting()
    )
    extra_codepoints = set(
        g.encoding for g in extra_fonts[0].glyphs() if g.isWorthOutputting()
    )
    new_codepoints = set(
        c for c in extra_codepoints - source_codepoints if 0 <= c and c <= 0xFFFF
    )
    print(
        "src: {} chars, ext: {} chars, new: {} chars".format(
            len(source_codepoints), len(extra_codepoints), len(new_codepoints)
        )
    )
    extra_fonts[0].selection.select(*new_codepoints)
    extra_fonts[0].copy()
    source_font.selection.select(*new_codepoints)
    source_font.paste()
    merge_fonts(source_font, *extra_fonts[1:])


def generate_font(target_name: str, source_name: str, cjk_name: str):
    """Generating Font
    This function use the recipe to generate font
    """
    cjk_font = fontforge.open(cjk_name)
    source_font = fontforge.open(source_name)
    cjk_font.reencode("unicode")
    source_font.reencode("unicode")
    cjk_font.em = source_font.em
    merge_fonts(source_font, cjk_font)
    source_font.generate(target_name)
    cjk_font.close()
    source_font.close()


if __name__ == "__main__":
    Fire(generate_font)
