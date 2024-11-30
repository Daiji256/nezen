#!/usr/bin/env python
#
# Usage:
# fontforge -script generate_nezen.py

import fontforge
import math
import psMat

sources = [
    {"name": "Zen Antique", "weight": "Regular"},
    {"name": "Zen Antique Soft", "weight": "Regular"},
    {"name": "Zen Kaku Gothic Antique", "weight": "Light"},
    {"name": "Zen Kaku Gothic Antique", "weight": "Regular"},
    {"name": "Zen Kaku Gothic Antique", "weight": "Medium"},
    {"name": "Zen Kaku Gothic Antique", "weight": "Bold"},
    {"name": "Zen Kaku Gothic Antique", "weight": "Black"},
    {"name": "Zen Kaku Gothic New", "weight": "Light"},
    {"name": "Zen Kaku Gothic New", "weight": "Regular"},
    {"name": "Zen Kaku Gothic New", "weight": "Medium"},
    {"name": "Zen Kaku Gothic New", "weight": "Bold"},
    {"name": "Zen Kaku Gothic New", "weight": "Black"},
    {"name": "Zen Kurenaido", "weight": "Regular"},
    {"name": "Zen Maru Gothic", "weight": "Light"},
    {"name": "Zen Maru Gothic", "weight": "Regular"},
    {"name": "Zen Maru Gothic", "weight": "Medium"},
    {"name": "Zen Maru Gothic", "weight": "Bold"},
    {"name": "Zen Maru Gothic", "weight": "Black"},
    {"name": "Zen Old Mincho", "weight": "Regular"},
    {"name": "Zen Old Mincho", "weight": "Medium"},
    {"name": "Zen Old Mincho", "weight": "SemiBold"},
    {"name": "Zen Old Mincho", "weight": "Bold"},
    {"name": "Zen Old Mincho", "weight": "Black"},
]

for source in sources:
    name = source["name"]
    weight = source["weight"]
    file_name = name.replace(" ", "")
    nezen_name = name.replace("Zen", "Nezen", 1)
    nezen_file_name = nezen_name.replace(" ", "")

    ff = fontforge.open(
        "sources/" + file_name + "/" + file_name + "-" + weight + ".ttf"
    )

    new_sfnt_names = tuple(
        (
            i[0],
            i[1],
            (
                i[2] + " Rotated"
                if i[1]
                in ("Family", "Fullname", "Preferred Family", "Trademark", "UniqueID")
                else i[2]
            ),
        )
        for i in ff.sfnt_names
    )
    ff.sfnt_names = new_sfnt_names
    ff.fontname = nezen_name
    ff.familyname = nezen_name
    ff.fullname = nezen_name + " " + weight

    vertical_lookups = [
        x
        for x in ff.gsub_lookups
        if x.startswith("'vert'")
        or x.startswith("'vrt2'")
        or x in ("gsubvert", "j-vert")
    ]
    vertical_lookup_subtables = sum(
        [ff.getLookupSubtables(x) for x in vertical_lookups], ()
    )

    for glyph in ff.glyphs():
        unicode = glyph.unicode
        if (
            0x04E00 <= unicode <= 0x09FFF  # CJK Unified Ideographs
            or 0x03400 <= unicode <= 0x04DBF  # CJK Unified Ideographs Extension A
            or 0x20000 <= unicode <= 0x2A6DF  # CJK Unified Ideographs Extension B
            or 0x2A700 <= unicode <= 0x2B739  # CJK Unified Ideographs Extension C
            or 0x2B740 <= unicode <= 0x2B81D  # CJK Unified Ideographs Extension D
            or 0x2B820 <= unicode <= 0x2CEA1  # CJK Unified Ideographs Extension E
            or 0x2CEB0 <= unicode <= 0x2EBE0  # CJK Unified Ideographs Extension F
            or 0x30000 <= unicode <= 0x3134A  # CJK Unified Ideographs Extension G
            or 0x31350 <= unicode <= 0x323AF  # CJK Unified Ideographs Extension H
            or 0x2EBF0 <= unicode <= 0x2EE5D  # CJK Unified Ideographs Extension I
            or 0x0F900 <= unicode <= 0x0FAFF  # CJK Compatibility Ideographs
            or 0x2F800 <= unicode <= 0x2FA1F  # CJK Compatibility Ideographs Supplement
            or 0x02F00 <= unicode <= 0x02FDF  # Kangxi Radicals
            or 0x02E80 <= unicode <= 0x02EFF  # CJK Radicals Supplement
            or 0x031C0 <= unicode <= 0x031EF  # CJK Strokes
            or 0x02FF0 <= unicode <= 0x02FFF  # Ideographic Description Characters
            or 0x03040 <= unicode <= 0x0309F  # Hiragana
            or 0x1B100 <= unicode <= 0x1B12F  # Kana Extended-A
            or 0x1AFF0 <= unicode <= 0x1AFFF  # Kana Extended-B
            or 0x1B000 <= unicode <= 0x1B0FF  # Kana Supplement
            or 0x1B130 <= unicode <= 0x1B16F  # Small Kana Extension
            or 0x03190 <= unicode <= 0x0319F  # Kanbun
            or 0x030A0 <= unicode <= 0x030FF  # Katakana
            or 0x031F0 <= unicode <= 0x031FF  # Katakana Phonetic Extensions
            or 0x0FF00 <= unicode <= 0x0FF5A  # Fullwidth Forms 1
            or 0x0FFE0 <= unicode <= 0x0FFFF  # Fullwidth Forms 2
            or 0x18B00 <= unicode <= 0x18CFF  # Khitan Small Script
            or 0x03000 <= unicode <= 0x0303F  # CJK Symbols and Punctuation
            or 0x03200 <= unicode <= 0x032FF  # Enclosed CJK Letters and Months
            or 0x03300 <= unicode <= 0x033FF  # CJK Compatibility
        ):
            for subtable in vertical_lookup_subtables:
                tables = glyph.getPosSub(subtable)
                if len(tables):
                    ff.selection.select(tables[0][2])
                    ff.copy()
                    ff.selection.select(glyph.glyphname)
                    ff.paste()
                    break
            matrix = psMat.compose(
                psMat.rotate(math.radians(90)),
                psMat.translate(
                    ff.em - ff.descent, (ff.em - glyph.width) / 2 - ff.descent
                ),
            )
            glyph.transform(matrix)
            glyph.width = ff.em

    ff.generate(
        "fonts/" + nezen_file_name + "/" + nezen_file_name + "-" + weight + ".ttf"
    )
