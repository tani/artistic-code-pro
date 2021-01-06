#!/usr/bin/env python3
from tempfile import NamedTemporaryFile
from shutil import copy2
from fontTools.ttLib.ttFont import TTFont
from fontTools.misc import etree
from fire import Fire


def update_matadata(font_path: str, weight: str, version: float):
    """Updating Metadata
    This function updates the metadata by TTF -> TTX -> TTF
    """
    font = TTFont(font_path)
    with NamedTemporaryFile() as xml:
        font.saveXML(xml.name)
        tree = etree.parse(xml.name)
        root = tree.getroot()
        fontRevision = root.find(".//fontRevision")
        fontRevision.set("value", str(version))
        for record in root.findall('.//namerecord[@nameID="0"]'):
            record.text = "\n".join(
                [
                    "Copyright (c) 2020, TANIGUCHI Masaya (https://github.com/tani/artistic-code-pro)",
                    "Copyright (c) 2014-2020 The Fira Code Project Authors (https://github.com/tonsky/FiraCode)",
                    "Copyright (c) 2014, 2015 Adobe Systems Incorporated (http://www.adobe.com/), with Reserved Font Name 'Source'",
                    "Copyright (c) 2019 M+ FONTS PROJECT",
                ]
            )
        for record in root.findall('.//namerecord[@nameID="1"]'):
            record.text = "Artistic Code Pro"
        for record in root.findall('.//namerecord[@nameID="2"]'):
            record.text = weight
        for record in root.findall('.//namerecord[@nameID="3"]'):
            record.text = "{};TANI;ArtisticCodePro-{}".format(version, weight)
        for record in root.findall('.//namerecord[@nameID="4"]'):
            record.text = "Artistic Code Pro {}".format(weight)
        for record in root.findall('.//namerecord[@nameID="5"]'):
            record.text = "Version {}".format(version)
        for record in root.findall('.//namerecord[@nameID="6"]'):
            record.text = "ArtisticCodePro-{}".format(weight)
        for record in root.findall('.//namerecord[@nameID="11"]'):
            record.text = "https://github.com/tani"
        for record in root.findall('.//namerecord[@nameID="12"]'):
            record.text = "https://github.com/tani"
        for record in root.findall('.//namerecord[@nameID="16"]'):
            record.text = "Artistic Code Pro"
        for record in root.findall('.//namerecord[@nameID="18"]'):
            record.text = "Artistic Code Pro {}".format(weight)
        tree.write(xml.name)
        font.importXML(xml.name)
    with NamedTemporaryFile() as ttf:
        font.save(ttf.name)
        font.close()
        copy2(ttf.name, font_path)


if __name__ == "__main__":
    Fire(update_matadata)
