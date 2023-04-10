#!/usr/bin/env python
#
# Usage:
# fontforge -script generate_nezen.py

import fontforge
import math
import psMat

src_name = 'ZenAntiqueSoft-Regular'
dst_name = 'Nezen'

ff = fontforge.open(src_name + '.ttf')

new_sfnt_names = tuple(
    (i[0], i[1], i[2] + ' Rotated' if i[1] in ('Family', 'Fullname', 'Preferred Family', 'Trademark', 'UniqueID') else i[2])
    for i in ff.sfnt_names
)
ff.sfnt_names = new_sfnt_names
ff.fontname = dst_name
ff.familyname = dst_name
ff.fullname = dst_name

vertical_lookups = [x for x in ff.gsub_lookups if x.startswith("'vert'") or x.startswith("'vrt2'") or x in ('gsubvert', 'j-vert')]
vertical_lookup_subtables = sum(
    [ff.getLookupSubtables(x) for x in vertical_lookups],
    ()
)

matrix = psMat.compose(
    psMat.rotate(math.radians(90)),
    psMat.translate(ff.em - ff.descent, -ff.descent),
)

for glyph in ff.glyphs():
    if glyph.width == ff.em:
        for subtable in vertical_lookup_subtables:
            tables = glyph.getPosSub(subtable)
            if len(tables):
                ff.selection.select(tables[0][2])
                ff.copy()
                ff.selection.select(glyph.glyphname)
                ff.paste()
                break
        glyph.transform(matrix)

ff.generate(dst_name + '.ttf')
