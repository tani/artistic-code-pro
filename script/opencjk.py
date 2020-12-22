#!/usr/bin/env python3

import fontforge
from freetype import Face

def open_cjk_font(font_name: str) -> fontforge.font:
    """Opening CJK Font

    This code is borrowed/inspired from
    https://github.com/HinTak/freetype-py/blob/fontval-diag/examples/cjk-multi-fix.py .
    It is licensed undet the MIT License.
    The most of part is different from the original code.
    """
    # Create the reverse lookup table and list of charcodes
    face = Face(font_name)
    face.set_charmap( face.charmap )
    reverse_lookup = {} # key: glyph_index, value: charcode
    charcodes = []
    charcode, glyph_index = face.get_first_char()
    while ( glyph_index ):
        charcodes.append(charcode)
        reverse_lookup[glyph_index] = [*reverse_lookup.get(glyph_index, []), charcode]
        charcode, glyph_index = face.get_next_char( charcode, glyph_index )
    del face
    # Remove duplicated glyphs
    font = fontforge.open(font_name)
    # CJK fonts usually contain subfonts
    # It is difficult to organize
    if (font.cidfontname != ""):
        font.cidFlatten()
    # As some glyphs conflists other glyphs in UTF-8,
    # we encode it to UTF-8, a.k.a. UCS4.
    font.reencode("ucs4")
    # Put same glyph to charchdes,
    # which has same glyph_ndex.
    for charcodes in reverse_lookup.values():
        main_charcode = charcodes[-1]
        if (not font[main_charcode].isWorthOutputting()):
            print("Source is empty.")
            continue
        for charcode in charcodes[:-1]:
            try:
                font[charcode]
            except TypeError:
                font.selection.select( main_charcode )
                font.copy()
                font.selection.select( charcode )
                font.paste()
            else:
               print("Destination is full.") 
    # Remove glyphs over 0xffff
    excess = sum(1 for _ in font.glyphs()) - 0xffff
    font.selection.select(*charcodes[-excess:])
    font.clear()
    # This font must contains glyphs,
    # only which charcode is less than 0xffff
    return font
