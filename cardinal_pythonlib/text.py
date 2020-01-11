#!/usr/bin/env python
# cardinal_pythonlib/text.py

"""
===============================================================================

    Original code copyright (C) 2009-2020 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of cardinal_pythonlib.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

===============================================================================

**Simple text-processing functions.**

"""

from typing import Dict, List, Union

from cardinal_pythonlib.logs import get_brace_style_log_with_null_handler

log = get_brace_style_log_with_null_handler(__name__)


# =============================================================================
# Input support methods
# =============================================================================

def escape_newlines(s: str) -> str:
    """
    Escapes CR, LF, and backslashes.

    Its counterpart is :func:`unescape_newlines`.

    ``s.encode("string_escape")`` and ``s.encode("unicode_escape")`` are
    alternatives, but they mess around with quotes, too (specifically,
    backslash-escaping single quotes).
    """
    if not s:
        return s
    s = s.replace("\\", r"\\")  # replace \ with \\
    s = s.replace("\n", r"\n")  # escape \n; note ord("\n") == 10
    s = s.replace("\r", r"\r")  # escape \r; note ord("\r") == 13
    return s


def unescape_newlines(s: str) -> str:
    """
    Reverses :func:`escape_newlines`.
    """
    # See also http://stackoverflow.com/questions/4020539
    if not s:
        return s
    d = ""  # the destination string
    in_escape = False
    for i in range(len(s)):
        c = s[i]  # the character being processed
        if in_escape:
            if c == "r":
                d += "\r"
            elif c == "n":
                d += "\n"
            else:
                d += c
            in_escape = False
        else:
            if c == "\\":
                in_escape = True
            else:
                d += c
    return d


def escape_tabs_newlines(s: str) -> str:
    """
    Escapes CR, LF, tab, and backslashes.

    Its counterpart is :func:`unescape_tabs_newlines`.
    """
    if not s:
        return s
    s = s.replace("\\", r"\\")  # replace \ with \\
    s = s.replace("\n", r"\n")  # escape \n; note ord("\n") == 10
    s = s.replace("\r", r"\r")  # escape \r; note ord("\r") == 13
    s = s.replace("\t", r"\t")  # escape \t; note ord("\t") == 9
    return s


def unescape_tabs_newlines(s: str) -> str:
    """
    Reverses :func:`escape_tabs_newlines`.

    See also http://stackoverflow.com/questions/4020539.
    """
    if not s:
        return s
    d = ""  # the destination string
    in_escape = False
    for i in range(len(s)):
        c = s[i]  # the character being processed
        if in_escape:
            if c == "r":
                d += "\r"
            elif c == "n":
                d += "\n"
            elif c == "t":
                d += "\t"
            else:
                d += c
            in_escape = False
        else:
            if c == "\\":
                in_escape = True
            else:
                d += c
    return d


# =============================================================================
# Unicode constants
# =============================================================================

def _unicode_def_src_to_str(srclist: List[Union[str, int]]) -> str:
    """
    Used to create :data:`UNICODE_CATEGORY_STRINGS`.

    Args:
        srclist: list of integers or hex range strings like ``"0061-007A"``

    Returns:
        a string with all characters described by ``srclist``: either the
        character corresponding to the integer Unicode character number, or
        all characters corresponding to the inclusive range described
    """
    charlist = []  # type: List[str]
    for src in srclist:
        if isinstance(src, int):
            charlist.append(chr(src))
        else:
            # Range like "0041-005A"
            first, last = [int(x, 16) for x in src.split("-")]
            charlist += [chr(x) for x in range(first, last + 1)]
    return "".join(charlist)


# https://stackoverflow.com/questions/13233076/determine-if-a-unicode-character-is-alphanumeric-without-using-a-regular-express  # noqa
_UNICODE_CATEGORY_SRC = {
    # From https://github.com/slevithan/xregexp/blob/master/tools/scripts/property-regex.py  # noqa
    'ASCII': ['0000-007F'],
    'Alphabetic': ['0041-005A', '0061-007A', 0x00AA, 0x00B5, 0x00BA, '00C0-00D6', '00D8-00F6', '00F8-02C1', '02C6-02D1', '02E0-02E4', 0x02EC, 0x02EE, 0x0345, '0370-0374', 0x0376, 0x0377, '037A-037D', 0x037F, 0x0386, '0388-038A', 0x038C, '038E-03A1', '03A3-03F5', '03F7-0481', '048A-052F', '0531-0556', 0x0559, '0561-0587', '05B0-05BD', 0x05BF, 0x05C1, 0x05C2, 0x05C4, 0x05C5, 0x05C7, '05D0-05EA', '05F0-05F2', '0610-061A', '0620-0657', '0659-065F', '066E-06D3', '06D5-06DC', '06E1-06E8', '06ED-06EF', '06FA-06FC', 0x06FF, '0710-073F', '074D-07B1', '07CA-07EA', 0x07F4, 0x07F5, 0x07FA, '0800-0817', '081A-082C', '0840-0858', '08A0-08B4', '08B6-08BD', '08D4-08DF', '08E3-08E9', '08F0-093B', '093D-094C', '094E-0950', '0955-0963', '0971-0983', '0985-098C', 0x098F, 0x0990, '0993-09A8', '09AA-09B0', 0x09B2, '09B6-09B9', '09BD-09C4', 0x09C7, 0x09C8, 0x09CB, 0x09CC, 0x09CE, 0x09D7, 0x09DC, 0x09DD, '09DF-09E3', 0x09F0, 0x09F1, '0A01-0A03', '0A05-0A0A', 0x0A0F, 0x0A10, '0A13-0A28', '0A2A-0A30', 0x0A32, 0x0A33, 0x0A35, 0x0A36, 0x0A38, 0x0A39, '0A3E-0A42', 0x0A47, 0x0A48, 0x0A4B, 0x0A4C, 0x0A51, '0A59-0A5C', 0x0A5E, '0A70-0A75', '0A81-0A83', '0A85-0A8D', '0A8F-0A91', '0A93-0AA8', '0AAA-0AB0', 0x0AB2, 0x0AB3, '0AB5-0AB9', '0ABD-0AC5', '0AC7-0AC9', 0x0ACB, 0x0ACC, 0x0AD0, '0AE0-0AE3', 0x0AF9, '0B01-0B03', '0B05-0B0C', 0x0B0F, 0x0B10, '0B13-0B28', '0B2A-0B30', 0x0B32, 0x0B33, '0B35-0B39', '0B3D-0B44', 0x0B47, 0x0B48, 0x0B4B, 0x0B4C, 0x0B56, 0x0B57, 0x0B5C, 0x0B5D, '0B5F-0B63', 0x0B71, 0x0B82, 0x0B83, '0B85-0B8A', '0B8E-0B90', '0B92-0B95', 0x0B99, 0x0B9A, 0x0B9C, 0x0B9E, 0x0B9F, 0x0BA3, 0x0BA4, '0BA8-0BAA', '0BAE-0BB9', '0BBE-0BC2', '0BC6-0BC8', '0BCA-0BCC', 0x0BD0, 0x0BD7, '0C00-0C03', '0C05-0C0C', '0C0E-0C10', '0C12-0C28', '0C2A-0C39', '0C3D-0C44', '0C46-0C48', '0C4A-0C4C', 0x0C55, 0x0C56, '0C58-0C5A', '0C60-0C63', '0C80-0C83', '0C85-0C8C', '0C8E-0C90', '0C92-0CA8', '0CAA-0CB3', '0CB5-0CB9', '0CBD-0CC4', '0CC6-0CC8', '0CCA-0CCC', 0x0CD5, 0x0CD6, 0x0CDE, '0CE0-0CE3', 0x0CF1, 0x0CF2, '0D01-0D03', '0D05-0D0C', '0D0E-0D10', '0D12-0D3A', '0D3D-0D44', '0D46-0D48', '0D4A-0D4C', 0x0D4E, '0D54-0D57', '0D5F-0D63', '0D7A-0D7F', 0x0D82, 0x0D83, '0D85-0D96', '0D9A-0DB1', '0DB3-0DBB', 0x0DBD, '0DC0-0DC6', '0DCF-0DD4', 0x0DD6, '0DD8-0DDF', 0x0DF2, 0x0DF3, '0E01-0E3A', '0E40-0E46', 0x0E4D, 0x0E81, 0x0E82, 0x0E84, 0x0E87, 0x0E88, 0x0E8A, 0x0E8D, '0E94-0E97', '0E99-0E9F', '0EA1-0EA3', 0x0EA5, 0x0EA7, 0x0EAA, 0x0EAB, '0EAD-0EB9', '0EBB-0EBD', '0EC0-0EC4', 0x0EC6, 0x0ECD, '0EDC-0EDF', 0x0F00, '0F40-0F47', '0F49-0F6C', '0F71-0F81', '0F88-0F97', '0F99-0FBC', '1000-1036', 0x1038, '103B-103F', '1050-1062', '1065-1068', '106E-1086', 0x108E, 0x109C, 0x109D, '10A0-10C5', 0x10C7, 0x10CD, '10D0-10FA', '10FC-1248', '124A-124D', '1250-1256', 0x1258, '125A-125D', '1260-1288', '128A-128D', '1290-12B0', '12B2-12B5', '12B8-12BE', 0x12C0, '12C2-12C5', '12C8-12D6', '12D8-1310', '1312-1315', '1318-135A', 0x135F, '1380-138F', '13A0-13F5', '13F8-13FD', '1401-166C', '166F-167F', '1681-169A', '16A0-16EA', '16EE-16F8', '1700-170C', '170E-1713', '1720-1733', '1740-1753', '1760-176C', '176E-1770', 0x1772, 0x1773, '1780-17B3', '17B6-17C8', 0x17D7, 0x17DC, '1820-1877', '1880-18AA', '18B0-18F5', '1900-191E', '1920-192B', '1930-1938', '1950-196D', '1970-1974', '1980-19AB', '19B0-19C9', '1A00-1A1B', '1A20-1A5E', '1A61-1A74', 0x1AA7, '1B00-1B33', '1B35-1B43', '1B45-1B4B', '1B80-1BA9', '1BAC-1BAF', '1BBA-1BE5', '1BE7-1BF1', '1C00-1C35', '1C4D-1C4F', '1C5A-1C7D', '1C80-1C88', '1CE9-1CEC', '1CEE-1CF3', 0x1CF5, 0x1CF6, '1D00-1DBF', '1DE7-1DF4', '1E00-1F15', '1F18-1F1D', '1F20-1F45', '1F48-1F4D', '1F50-1F57', 0x1F59, 0x1F5B, 0x1F5D, '1F5F-1F7D', '1F80-1FB4', '1FB6-1FBC', 0x1FBE, '1FC2-1FC4', '1FC6-1FCC', '1FD0-1FD3', '1FD6-1FDB', '1FE0-1FEC', '1FF2-1FF4', '1FF6-1FFC', 0x2071, 0x207F, '2090-209C', 0x2102, 0x2107, '210A-2113', 0x2115, '2119-211D', 0x2124, 0x2126, 0x2128, '212A-212D', '212F-2139', '213C-213F', '2145-2149', 0x214E, '2160-2188', '24B6-24E9', '2C00-2C2E', '2C30-2C5E', '2C60-2CE4', '2CEB-2CEE', 0x2CF2, 0x2CF3, '2D00-2D25', 0x2D27, 0x2D2D, '2D30-2D67', 0x2D6F, '2D80-2D96', '2DA0-2DA6', '2DA8-2DAE', '2DB0-2DB6', '2DB8-2DBE', '2DC0-2DC6', '2DC8-2DCE', '2DD0-2DD6', '2DD8-2DDE', '2DE0-2DFF', 0x2E2F, '3005-3007', '3021-3029', '3031-3035', '3038-303C', '3041-3096', '309D-309F', '30A1-30FA', '30FC-30FF', '3105-312D', '3131-318E', '31A0-31BA', '31F0-31FF', '3400-4DB5', '4E00-9FD5', 'A000-A48C', 'A4D0-A4FD', 'A500-A60C', 'A610-A61F', 0xA62A, 0xA62B, 'A640-A66E', 'A674-A67B', 'A67F-A6EF', 'A717-A71F', 'A722-A788', 'A78B-A7AE', 'A7B0-A7B7', 'A7F7-A801', 'A803-A805', 'A807-A80A', 'A80C-A827', 'A840-A873', 'A880-A8C3', 0xA8C5, 'A8F2-A8F7', 0xA8FB, 0xA8FD, 'A90A-A92A', 'A930-A952', 'A960-A97C', 'A980-A9B2', 'A9B4-A9BF', 0xA9CF, 'A9E0-A9E4', 'A9E6-A9EF', 'A9FA-A9FE', 'AA00-AA36', 'AA40-AA4D', 'AA60-AA76', 0xAA7A, 'AA7E-AABE', 0xAAC0, 0xAAC2, 'AADB-AADD', 'AAE0-AAEF', 'AAF2-AAF5', 'AB01-AB06', 'AB09-AB0E', 'AB11-AB16', 'AB20-AB26', 'AB28-AB2E', 'AB30-AB5A', 'AB5C-AB65', 'AB70-ABEA', 'AC00-D7A3', 'D7B0-D7C6', 'D7CB-D7FB', 'F900-FA6D', 'FA70-FAD9', 'FB00-FB06', 'FB13-FB17', 'FB1D-FB28', 'FB2A-FB36', 'FB38-FB3C', 0xFB3E, 0xFB40, 0xFB41, 0xFB43, 0xFB44, 'FB46-FBB1', 'FBD3-FD3D', 'FD50-FD8F', 'FD92-FDC7', 'FDF0-FDFB', 'FE70-FE74', 'FE76-FEFC', 'FF21-FF3A', 'FF41-FF5A', 'FF66-FFBE', 'FFC2-FFC7', 'FFCA-FFCF', 'FFD2-FFD7', 'FFDA-FFDC', '10000-1000B', '1000D-10026', '10028-1003A', 0x1003C, 0x1003D, '1003F-1004D', '10050-1005D', '10080-100FA', '10140-10174', '10280-1029C', '102A0-102D0', '10300-1031F', '10330-1034A', '10350-1037A', '10380-1039D', '103A0-103C3', '103C8-103CF', '103D1-103D5', '10400-1049D', '104B0-104D3', '104D8-104FB', '10500-10527', '10530-10563', '10600-10736', '10740-10755', '10760-10767', '10800-10805', 0x10808, '1080A-10835', 0x10837, 0x10838, 0x1083C, '1083F-10855', '10860-10876', '10880-1089E', '108E0-108F2', 0x108F4, 0x108F5, '10900-10915', '10920-10939', '10980-109B7', 0x109BE, 0x109BF, '10A00-10A03', 0x10A05, 0x10A06, '10A0C-10A13', '10A15-10A17', '10A19-10A33', '10A60-10A7C', '10A80-10A9C', '10AC0-10AC7', '10AC9-10AE4', '10B00-10B35', '10B40-10B55', '10B60-10B72', '10B80-10B91', '10C00-10C48', '10C80-10CB2', '10CC0-10CF2', '11000-11045', '11082-110B8', '110D0-110E8', '11100-11132', '11150-11172', 0x11176, '11180-111BF', '111C1-111C4', 0x111DA, 0x111DC, '11200-11211', '11213-11234', 0x11237, 0x1123E, '11280-11286', 0x11288, '1128A-1128D', '1128F-1129D', '1129F-112A8', '112B0-112E8', '11300-11303', '11305-1130C', 0x1130F, 0x11310, '11313-11328', '1132A-11330', 0x11332, 0x11333, '11335-11339', '1133D-11344', 0x11347, 0x11348, 0x1134B, 0x1134C, 0x11350, 0x11357, '1135D-11363', '11400-11441', '11443-11445', '11447-1144A', '11480-114C1', 0x114C4, 0x114C5, 0x114C7, '11580-115B5', '115B8-115BE', '115D8-115DD', '11600-1163E', 0x11640, 0x11644, '11680-116B5', '11700-11719', '1171D-1172A', '118A0-118DF', 0x118FF, '11AC0-11AF8', '11C00-11C08', '11C0A-11C36', '11C38-11C3E', 0x11C40, '11C72-11C8F', '11C92-11CA7', '11CA9-11CB6', '12000-12399', '12400-1246E', '12480-12543', '13000-1342E', '14400-14646', '16800-16A38', '16A40-16A5E', '16AD0-16AED', '16B00-16B36', '16B40-16B43', '16B63-16B77', '16B7D-16B8F', '16F00-16F44', '16F50-16F7E', '16F93-16F9F', 0x16FE0, '17000-187EC', '18800-18AF2', 0x1B000, 0x1B001, '1BC00-1BC6A', '1BC70-1BC7C', '1BC80-1BC88', '1BC90-1BC99', 0x1BC9E, '1D400-1D454', '1D456-1D49C', 0x1D49E, 0x1D49F, 0x1D4A2, 0x1D4A5, 0x1D4A6, '1D4A9-1D4AC', '1D4AE-1D4B9', 0x1D4BB, '1D4BD-1D4C3', '1D4C5-1D505', '1D507-1D50A', '1D50D-1D514', '1D516-1D51C', '1D51E-1D539', '1D53B-1D53E', '1D540-1D544', 0x1D546, '1D54A-1D550', '1D552-1D6A5', '1D6A8-1D6C0', '1D6C2-1D6DA', '1D6DC-1D6FA', '1D6FC-1D714', '1D716-1D734', '1D736-1D74E', '1D750-1D76E', '1D770-1D788', '1D78A-1D7A8', '1D7AA-1D7C2', '1D7C4-1D7CB', '1E000-1E006', '1E008-1E018', '1E01B-1E021', 0x1E023, 0x1E024, '1E026-1E02A', '1E800-1E8C4', '1E900-1E943', 0x1E947, '1EE00-1EE03', '1EE05-1EE1F', 0x1EE21, 0x1EE22, 0x1EE24, 0x1EE27, '1EE29-1EE32', '1EE34-1EE37', 0x1EE39, 0x1EE3B, 0x1EE42, 0x1EE47, 0x1EE49, 0x1EE4B, '1EE4D-1EE4F', 0x1EE51, 0x1EE52, 0x1EE54, 0x1EE57, 0x1EE59, 0x1EE5B, 0x1EE5D, 0x1EE5F, 0x1EE61, 0x1EE62, 0x1EE64, '1EE67-1EE6A', '1EE6C-1EE72', '1EE74-1EE77', '1EE79-1EE7C', 0x1EE7E, '1EE80-1EE89', '1EE8B-1EE9B', '1EEA1-1EEA3', '1EEA5-1EEA9', '1EEAB-1EEBB', '1F130-1F149', '1F150-1F169', '1F170-1F189', '20000-2A6D6', '2A700-2B734', '2B740-2B81D', '2B820-2CEA1', '2F800-2FA1D'],  # noqa
    'Any': ['0000-10FFFF'],
    # 'Assigned': [], # Defined as the inverse of category Cn
    'Default_Ignorable_Code_Point': [0x00AD, 0x034F, 0x061C, 0x115F, 0x1160, 0x17B4, 0x17B5, '180B-180E', '200B-200F', '202A-202E', '2060-206F', 0x3164, 'FE00-FE0F', 0xFEFF, 0xFFA0, 'FFF0-FFF8', '1BCA0-1BCA3', '1D173-1D17A', 'E0000-E0FFF'],  # noqa
    'Lowercase': ['0061-007A', 0x00AA, 0x00B5, 0x00BA, '00DF-00F6', '00F8-00FF', 0x0101, 0x0103, 0x0105, 0x0107, 0x0109, 0x010B, 0x010D, 0x010F, 0x0111, 0x0113, 0x0115, 0x0117, 0x0119, 0x011B, 0x011D, 0x011F, 0x0121, 0x0123, 0x0125, 0x0127, 0x0129, 0x012B, 0x012D, 0x012F, 0x0131, 0x0133, 0x0135, 0x0137, 0x0138, 0x013A, 0x013C, 0x013E, 0x0140, 0x0142, 0x0144, 0x0146, 0x0148, 0x0149, 0x014B, 0x014D, 0x014F, 0x0151, 0x0153, 0x0155, 0x0157, 0x0159, 0x015B, 0x015D, 0x015F, 0x0161, 0x0163, 0x0165, 0x0167, 0x0169, 0x016B, 0x016D, 0x016F, 0x0171, 0x0173, 0x0175, 0x0177, 0x017A, 0x017C, '017E-0180', 0x0183, 0x0185, 0x0188, 0x018C, 0x018D, 0x0192, 0x0195, '0199-019B', 0x019E, 0x01A1, 0x01A3, 0x01A5, 0x01A8, 0x01AA, 0x01AB, 0x01AD, 0x01B0, 0x01B4, 0x01B6, 0x01B9, 0x01BA, '01BD-01BF', 0x01C6, 0x01C9, 0x01CC, 0x01CE, 0x01D0, 0x01D2, 0x01D4, 0x01D6, 0x01D8, 0x01DA, 0x01DC, 0x01DD, 0x01DF, 0x01E1, 0x01E3, 0x01E5, 0x01E7, 0x01E9, 0x01EB, 0x01ED, 0x01EF, 0x01F0, 0x01F3, 0x01F5, 0x01F9, 0x01FB, 0x01FD, 0x01FF, 0x0201, 0x0203, 0x0205, 0x0207, 0x0209, 0x020B, 0x020D, 0x020F, 0x0211, 0x0213, 0x0215, 0x0217, 0x0219, 0x021B, 0x021D, 0x021F, 0x0221, 0x0223, 0x0225, 0x0227, 0x0229, 0x022B, 0x022D, 0x022F, 0x0231, '0233-0239', 0x023C, 0x023F, 0x0240, 0x0242, 0x0247, 0x0249, 0x024B, 0x024D, '024F-0293', '0295-02B8', 0x02C0, 0x02C1, '02E0-02E4', 0x0345, 0x0371, 0x0373, 0x0377, '037A-037D', 0x0390, '03AC-03CE', 0x03D0, 0x03D1, '03D5-03D7', 0x03D9, 0x03DB, 0x03DD, 0x03DF, 0x03E1, 0x03E3, 0x03E5, 0x03E7, 0x03E9, 0x03EB, 0x03ED, '03EF-03F3', 0x03F5, 0x03F8, 0x03FB, 0x03FC, '0430-045F', 0x0461, 0x0463, 0x0465, 0x0467, 0x0469, 0x046B, 0x046D, 0x046F, 0x0471, 0x0473, 0x0475, 0x0477, 0x0479, 0x047B, 0x047D, 0x047F, 0x0481, 0x048B, 0x048D, 0x048F, 0x0491, 0x0493, 0x0495, 0x0497, 0x0499, 0x049B, 0x049D, 0x049F, 0x04A1, 0x04A3, 0x04A5, 0x04A7, 0x04A9, 0x04AB, 0x04AD, 0x04AF, 0x04B1, 0x04B3, 0x04B5, 0x04B7, 0x04B9, 0x04BB, 0x04BD, 0x04BF, 0x04C2, 0x04C4, 0x04C6, 0x04C8, 0x04CA, 0x04CC, 0x04CE, 0x04CF, 0x04D1, 0x04D3, 0x04D5, 0x04D7, 0x04D9, 0x04DB, 0x04DD, 0x04DF, 0x04E1, 0x04E3, 0x04E5, 0x04E7, 0x04E9, 0x04EB, 0x04ED, 0x04EF, 0x04F1, 0x04F3, 0x04F5, 0x04F7, 0x04F9, 0x04FB, 0x04FD, 0x04FF, 0x0501, 0x0503, 0x0505, 0x0507, 0x0509, 0x050B, 0x050D, 0x050F, 0x0511, 0x0513, 0x0515, 0x0517, 0x0519, 0x051B, 0x051D, 0x051F, 0x0521, 0x0523, 0x0525, 0x0527, 0x0529, 0x052B, 0x052D, 0x052F, '0561-0587', '13F8-13FD', '1C80-1C88', '1D00-1DBF', 0x1E01, 0x1E03, 0x1E05, 0x1E07, 0x1E09, 0x1E0B, 0x1E0D, 0x1E0F, 0x1E11, 0x1E13, 0x1E15, 0x1E17, 0x1E19, 0x1E1B, 0x1E1D, 0x1E1F, 0x1E21, 0x1E23, 0x1E25, 0x1E27, 0x1E29, 0x1E2B, 0x1E2D, 0x1E2F, 0x1E31, 0x1E33, 0x1E35, 0x1E37, 0x1E39, 0x1E3B, 0x1E3D, 0x1E3F, 0x1E41, 0x1E43, 0x1E45, 0x1E47, 0x1E49, 0x1E4B, 0x1E4D, 0x1E4F, 0x1E51, 0x1E53, 0x1E55, 0x1E57, 0x1E59, 0x1E5B, 0x1E5D, 0x1E5F, 0x1E61, 0x1E63, 0x1E65, 0x1E67, 0x1E69, 0x1E6B, 0x1E6D, 0x1E6F, 0x1E71, 0x1E73, 0x1E75, 0x1E77, 0x1E79, 0x1E7B, 0x1E7D, 0x1E7F, 0x1E81, 0x1E83, 0x1E85, 0x1E87, 0x1E89, 0x1E8B, 0x1E8D, 0x1E8F, 0x1E91, 0x1E93, '1E95-1E9D', 0x1E9F, 0x1EA1, 0x1EA3, 0x1EA5, 0x1EA7, 0x1EA9, 0x1EAB, 0x1EAD, 0x1EAF, 0x1EB1, 0x1EB3, 0x1EB5, 0x1EB7, 0x1EB9, 0x1EBB, 0x1EBD, 0x1EBF, 0x1EC1, 0x1EC3, 0x1EC5, 0x1EC7, 0x1EC9, 0x1ECB, 0x1ECD, 0x1ECF, 0x1ED1, 0x1ED3, 0x1ED5, 0x1ED7, 0x1ED9, 0x1EDB, 0x1EDD, 0x1EDF, 0x1EE1, 0x1EE3, 0x1EE5, 0x1EE7, 0x1EE9, 0x1EEB, 0x1EED, 0x1EEF, 0x1EF1, 0x1EF3, 0x1EF5, 0x1EF7, 0x1EF9, 0x1EFB, 0x1EFD, '1EFF-1F07', '1F10-1F15', '1F20-1F27', '1F30-1F37', '1F40-1F45', '1F50-1F57', '1F60-1F67', '1F70-1F7D', '1F80-1F87', '1F90-1F97', '1FA0-1FA7', '1FB0-1FB4', 0x1FB6, 0x1FB7, 0x1FBE, '1FC2-1FC4', 0x1FC6, 0x1FC7, '1FD0-1FD3', 0x1FD6, 0x1FD7, '1FE0-1FE7', '1FF2-1FF4', 0x1FF6, 0x1FF7, 0x2071, 0x207F, '2090-209C', 0x210A, 0x210E, 0x210F, 0x2113, 0x212F, 0x2134, 0x2139, 0x213C, 0x213D, '2146-2149', 0x214E, '2170-217F', 0x2184, '24D0-24E9', '2C30-2C5E', 0x2C61, 0x2C65, 0x2C66, 0x2C68, 0x2C6A, 0x2C6C, 0x2C71, 0x2C73, 0x2C74, '2C76-2C7D', 0x2C81, 0x2C83, 0x2C85, 0x2C87, 0x2C89, 0x2C8B, 0x2C8D, 0x2C8F, 0x2C91, 0x2C93, 0x2C95, 0x2C97, 0x2C99, 0x2C9B, 0x2C9D, 0x2C9F, 0x2CA1, 0x2CA3, 0x2CA5, 0x2CA7, 0x2CA9, 0x2CAB, 0x2CAD, 0x2CAF, 0x2CB1, 0x2CB3, 0x2CB5, 0x2CB7, 0x2CB9, 0x2CBB, 0x2CBD, 0x2CBF, 0x2CC1, 0x2CC3, 0x2CC5, 0x2CC7, 0x2CC9, 0x2CCB, 0x2CCD, 0x2CCF, 0x2CD1, 0x2CD3, 0x2CD5, 0x2CD7, 0x2CD9, 0x2CDB, 0x2CDD, 0x2CDF, 0x2CE1, 0x2CE3, 0x2CE4, 0x2CEC, 0x2CEE, 0x2CF3, '2D00-2D25', 0x2D27, 0x2D2D, 0xA641, 0xA643, 0xA645, 0xA647, 0xA649, 0xA64B, 0xA64D, 0xA64F, 0xA651, 0xA653, 0xA655, 0xA657, 0xA659, 0xA65B, 0xA65D, 0xA65F, 0xA661, 0xA663, 0xA665, 0xA667, 0xA669, 0xA66B, 0xA66D, 0xA681, 0xA683, 0xA685, 0xA687, 0xA689, 0xA68B, 0xA68D, 0xA68F, 0xA691, 0xA693, 0xA695, 0xA697, 0xA699, 'A69B-A69D', 0xA723, 0xA725, 0xA727, 0xA729, 0xA72B, 0xA72D, 'A72F-A731', 0xA733, 0xA735, 0xA737, 0xA739, 0xA73B, 0xA73D, 0xA73F, 0xA741, 0xA743, 0xA745, 0xA747, 0xA749, 0xA74B, 0xA74D, 0xA74F, 0xA751, 0xA753, 0xA755, 0xA757, 0xA759, 0xA75B, 0xA75D, 0xA75F, 0xA761, 0xA763, 0xA765, 0xA767, 0xA769, 0xA76B, 0xA76D, 'A76F-A778', 0xA77A, 0xA77C, 0xA77F, 0xA781, 0xA783, 0xA785, 0xA787, 0xA78C, 0xA78E, 0xA791, 'A793-A795', 0xA797, 0xA799, 0xA79B, 0xA79D, 0xA79F, 0xA7A1, 0xA7A3, 0xA7A5, 0xA7A7, 0xA7A9, 0xA7B5, 0xA7B7, 'A7F8-A7FA', 'AB30-AB5A', 'AB5C-AB65', 'AB70-ABBF', 'FB00-FB06', 'FB13-FB17', 'FF41-FF5A', '10428-1044F', '104D8-104FB', '10CC0-10CF2', '118C0-118DF', '1D41A-1D433', '1D44E-1D454', '1D456-1D467', '1D482-1D49B', '1D4B6-1D4B9', 0x1D4BB, '1D4BD-1D4C3', '1D4C5-1D4CF', '1D4EA-1D503', '1D51E-1D537', '1D552-1D56B', '1D586-1D59F', '1D5BA-1D5D3', '1D5EE-1D607', '1D622-1D63B', '1D656-1D66F', '1D68A-1D6A5', '1D6C2-1D6DA', '1D6DC-1D6E1', '1D6FC-1D714', '1D716-1D71B', '1D736-1D74E', '1D750-1D755', '1D770-1D788', '1D78A-1D78F', '1D7AA-1D7C2', '1D7C4-1D7C9', 0x1D7CB, '1E922-1E943'],  # noqa
    'Noncharacter_Code_Point': ['FDD0-FDEF', 0xFFFE, 0xFFFF, 0x1FFFE, 0x1FFFF, 0x2FFFE, 0x2FFFF, 0x3FFFE, 0x3FFFF, 0x4FFFE, 0x4FFFF, 0x5FFFE, 0x5FFFF, 0x6FFFE, 0x6FFFF, 0x7FFFE, 0x7FFFF, 0x8FFFE, 0x8FFFF, 0x9FFFE, 0x9FFFF, 0xAFFFE, 0xAFFFF, 0xBFFFE, 0xBFFFF, 0xCFFFE, 0xCFFFF, 0xDFFFE, 0xDFFFF, 0xEFFFE, 0xEFFFF, 0xFFFFE, 0xFFFFF, 0x10FFFE, 0x10FFFF],  # noqa
    'Uppercase': ['0041-005A', '00C0-00D6', '00D8-00DE', 0x0100, 0x0102, 0x0104, 0x0106, 0x0108, 0x010A, 0x010C, 0x010E, 0x0110, 0x0112, 0x0114, 0x0116, 0x0118, 0x011A, 0x011C, 0x011E, 0x0120, 0x0122, 0x0124, 0x0126, 0x0128, 0x012A, 0x012C, 0x012E, 0x0130, 0x0132, 0x0134, 0x0136, 0x0139, 0x013B, 0x013D, 0x013F, 0x0141, 0x0143, 0x0145, 0x0147, 0x014A, 0x014C, 0x014E, 0x0150, 0x0152, 0x0154, 0x0156, 0x0158, 0x015A, 0x015C, 0x015E, 0x0160, 0x0162, 0x0164, 0x0166, 0x0168, 0x016A, 0x016C, 0x016E, 0x0170, 0x0172, 0x0174, 0x0176, 0x0178, 0x0179, 0x017B, 0x017D, 0x0181, 0x0182, 0x0184, 0x0186, 0x0187, '0189-018B', '018E-0191', 0x0193, 0x0194, '0196-0198', 0x019C, 0x019D, 0x019F, 0x01A0, 0x01A2, 0x01A4, 0x01A6, 0x01A7, 0x01A9, 0x01AC, 0x01AE, 0x01AF, '01B1-01B3', 0x01B5, 0x01B7, 0x01B8, 0x01BC, 0x01C4, 0x01C7, 0x01CA, 0x01CD, 0x01CF, 0x01D1, 0x01D3, 0x01D5, 0x01D7, 0x01D9, 0x01DB, 0x01DE, 0x01E0, 0x01E2, 0x01E4, 0x01E6, 0x01E8, 0x01EA, 0x01EC, 0x01EE, 0x01F1, 0x01F4, '01F6-01F8', 0x01FA, 0x01FC, 0x01FE, 0x0200, 0x0202, 0x0204, 0x0206, 0x0208, 0x020A, 0x020C, 0x020E, 0x0210, 0x0212, 0x0214, 0x0216, 0x0218, 0x021A, 0x021C, 0x021E, 0x0220, 0x0222, 0x0224, 0x0226, 0x0228, 0x022A, 0x022C, 0x022E, 0x0230, 0x0232, 0x023A, 0x023B, 0x023D, 0x023E, 0x0241, '0243-0246', 0x0248, 0x024A, 0x024C, 0x024E, 0x0370, 0x0372, 0x0376, 0x037F, 0x0386, '0388-038A', 0x038C, 0x038E, 0x038F, '0391-03A1', '03A3-03AB', 0x03CF, '03D2-03D4', 0x03D8, 0x03DA, 0x03DC, 0x03DE, 0x03E0, 0x03E2, 0x03E4, 0x03E6, 0x03E8, 0x03EA, 0x03EC, 0x03EE, 0x03F4, 0x03F7, 0x03F9, 0x03FA, '03FD-042F', 0x0460, 0x0462, 0x0464, 0x0466, 0x0468, 0x046A, 0x046C, 0x046E, 0x0470, 0x0472, 0x0474, 0x0476, 0x0478, 0x047A, 0x047C, 0x047E, 0x0480, 0x048A, 0x048C, 0x048E, 0x0490, 0x0492, 0x0494, 0x0496, 0x0498, 0x049A, 0x049C, 0x049E, 0x04A0, 0x04A2, 0x04A4, 0x04A6, 0x04A8, 0x04AA, 0x04AC, 0x04AE, 0x04B0, 0x04B2, 0x04B4, 0x04B6, 0x04B8, 0x04BA, 0x04BC, 0x04BE, 0x04C0, 0x04C1, 0x04C3, 0x04C5, 0x04C7, 0x04C9, 0x04CB, 0x04CD, 0x04D0, 0x04D2, 0x04D4, 0x04D6, 0x04D8, 0x04DA, 0x04DC, 0x04DE, 0x04E0, 0x04E2, 0x04E4, 0x04E6, 0x04E8, 0x04EA, 0x04EC, 0x04EE, 0x04F0, 0x04F2, 0x04F4, 0x04F6, 0x04F8, 0x04FA, 0x04FC, 0x04FE, 0x0500, 0x0502, 0x0504, 0x0506, 0x0508, 0x050A, 0x050C, 0x050E, 0x0510, 0x0512, 0x0514, 0x0516, 0x0518, 0x051A, 0x051C, 0x051E, 0x0520, 0x0522, 0x0524, 0x0526, 0x0528, 0x052A, 0x052C, 0x052E, '0531-0556', '10A0-10C5', 0x10C7, 0x10CD, '13A0-13F5', 0x1E00, 0x1E02, 0x1E04, 0x1E06, 0x1E08, 0x1E0A, 0x1E0C, 0x1E0E, 0x1E10, 0x1E12, 0x1E14, 0x1E16, 0x1E18, 0x1E1A, 0x1E1C, 0x1E1E, 0x1E20, 0x1E22, 0x1E24, 0x1E26, 0x1E28, 0x1E2A, 0x1E2C, 0x1E2E, 0x1E30, 0x1E32, 0x1E34, 0x1E36, 0x1E38, 0x1E3A, 0x1E3C, 0x1E3E, 0x1E40, 0x1E42, 0x1E44, 0x1E46, 0x1E48, 0x1E4A, 0x1E4C, 0x1E4E, 0x1E50, 0x1E52, 0x1E54, 0x1E56, 0x1E58, 0x1E5A, 0x1E5C, 0x1E5E, 0x1E60, 0x1E62, 0x1E64, 0x1E66, 0x1E68, 0x1E6A, 0x1E6C, 0x1E6E, 0x1E70, 0x1E72, 0x1E74, 0x1E76, 0x1E78, 0x1E7A, 0x1E7C, 0x1E7E, 0x1E80, 0x1E82, 0x1E84, 0x1E86, 0x1E88, 0x1E8A, 0x1E8C, 0x1E8E, 0x1E90, 0x1E92, 0x1E94, 0x1E9E, 0x1EA0, 0x1EA2, 0x1EA4, 0x1EA6, 0x1EA8, 0x1EAA, 0x1EAC, 0x1EAE, 0x1EB0, 0x1EB2, 0x1EB4, 0x1EB6, 0x1EB8, 0x1EBA, 0x1EBC, 0x1EBE, 0x1EC0, 0x1EC2, 0x1EC4, 0x1EC6, 0x1EC8, 0x1ECA, 0x1ECC, 0x1ECE, 0x1ED0, 0x1ED2, 0x1ED4, 0x1ED6, 0x1ED8, 0x1EDA, 0x1EDC, 0x1EDE, 0x1EE0, 0x1EE2, 0x1EE4, 0x1EE6, 0x1EE8, 0x1EEA, 0x1EEC, 0x1EEE, 0x1EF0, 0x1EF2, 0x1EF4, 0x1EF6, 0x1EF8, 0x1EFA, 0x1EFC, 0x1EFE, '1F08-1F0F', '1F18-1F1D', '1F28-1F2F', '1F38-1F3F', '1F48-1F4D', 0x1F59, 0x1F5B, 0x1F5D, 0x1F5F, '1F68-1F6F', '1FB8-1FBB', '1FC8-1FCB', '1FD8-1FDB', '1FE8-1FEC', '1FF8-1FFB', 0x2102, 0x2107, '210B-210D', '2110-2112', 0x2115, '2119-211D', 0x2124, 0x2126, 0x2128, '212A-212D', '2130-2133', 0x213E, 0x213F, 0x2145, '2160-216F', 0x2183, '24B6-24CF', '2C00-2C2E', 0x2C60, '2C62-2C64', 0x2C67, 0x2C69, 0x2C6B, '2C6D-2C70', 0x2C72, 0x2C75, '2C7E-2C80', 0x2C82, 0x2C84, 0x2C86, 0x2C88, 0x2C8A, 0x2C8C, 0x2C8E, 0x2C90, 0x2C92, 0x2C94, 0x2C96, 0x2C98, 0x2C9A, 0x2C9C, 0x2C9E, 0x2CA0, 0x2CA2, 0x2CA4, 0x2CA6, 0x2CA8, 0x2CAA, 0x2CAC, 0x2CAE, 0x2CB0, 0x2CB2, 0x2CB4, 0x2CB6, 0x2CB8, 0x2CBA, 0x2CBC, 0x2CBE, 0x2CC0, 0x2CC2, 0x2CC4, 0x2CC6, 0x2CC8, 0x2CCA, 0x2CCC, 0x2CCE, 0x2CD0, 0x2CD2, 0x2CD4, 0x2CD6, 0x2CD8, 0x2CDA, 0x2CDC, 0x2CDE, 0x2CE0, 0x2CE2, 0x2CEB, 0x2CED, 0x2CF2, 0xA640, 0xA642, 0xA644, 0xA646, 0xA648, 0xA64A, 0xA64C, 0xA64E, 0xA650, 0xA652, 0xA654, 0xA656, 0xA658, 0xA65A, 0xA65C, 0xA65E, 0xA660, 0xA662, 0xA664, 0xA666, 0xA668, 0xA66A, 0xA66C, 0xA680, 0xA682, 0xA684, 0xA686, 0xA688, 0xA68A, 0xA68C, 0xA68E, 0xA690, 0xA692, 0xA694, 0xA696, 0xA698, 0xA69A, 0xA722, 0xA724, 0xA726, 0xA728, 0xA72A, 0xA72C, 0xA72E, 0xA732, 0xA734, 0xA736, 0xA738, 0xA73A, 0xA73C, 0xA73E, 0xA740, 0xA742, 0xA744, 0xA746, 0xA748, 0xA74A, 0xA74C, 0xA74E, 0xA750, 0xA752, 0xA754, 0xA756, 0xA758, 0xA75A, 0xA75C, 0xA75E, 0xA760, 0xA762, 0xA764, 0xA766, 0xA768, 0xA76A, 0xA76C, 0xA76E, 0xA779, 0xA77B, 0xA77D, 0xA77E, 0xA780, 0xA782, 0xA784, 0xA786, 0xA78B, 0xA78D, 0xA790, 0xA792, 0xA796, 0xA798, 0xA79A, 0xA79C, 0xA79E, 0xA7A0, 0xA7A2, 0xA7A4, 0xA7A6, 0xA7A8, 'A7AA-A7AE', 'A7B0-A7B4', 0xA7B6, 'FF21-FF3A', '10400-10427', '104B0-104D3', '10C80-10CB2', '118A0-118BF', '1D400-1D419', '1D434-1D44D', '1D468-1D481', 0x1D49C, 0x1D49E, 0x1D49F, 0x1D4A2, 0x1D4A5, 0x1D4A6, '1D4A9-1D4AC', '1D4AE-1D4B5', '1D4D0-1D4E9', 0x1D504, 0x1D505, '1D507-1D50A', '1D50D-1D514', '1D516-1D51C', 0x1D538, 0x1D539, '1D53B-1D53E', '1D540-1D544', 0x1D546, '1D54A-1D550', '1D56C-1D585', '1D5A0-1D5B9', '1D5D4-1D5ED', '1D608-1D621', '1D63C-1D655', '1D670-1D689', '1D6A8-1D6C0', '1D6E2-1D6FA', '1D71C-1D734', '1D756-1D76E', '1D790-1D7A8', 0x1D7CA, '1E900-1E921', '1F130-1F149', '1F150-1F169', '1F170-1F189'],  # noqa
    'White_Space': ['0009-000D', 0x0020, 0x0085, 0x00A0, 0x1680, '2000-200A', 0x2028, 0x2029, 0x202F, 0x205F, 0x3000],  # noqa

    # From https://en.wikipedia.org/wiki/Latin_script_in_Unicode
    'Latin': [
        '0000-007F',  # Basic Latin; this block corresponds to ASCII.
        '0080-00FF',  # Latin-1 Supplement
        '0100-017F',  # Latin Extended-A
        '0180-024F',  # Latin Extended-B
        '0250-02AF',  # IPA Extensions
        '02B0-02FF',  # Spacing Modifier Letters
        '1D00-1D7F',  # Phonetic Extensions
        '1D80-1DBF',  # Phonetic Extensions Supplement
        '1E00-1EFF',  # Latin Extended Additional
        '2070-209F',  # Superscripts and Subscripts
        '2100-214F',  # Letterlike Symbols
        '2150-218F',  # Number Forms
        '2C60-2C7F',  # Latin Extended-C
        'A720-A7FF',  # Latin Extended-D
        'AB30-AB6F',  # Latin Extended-E
        'FB00-FB4F',  # Alphabetic Presentation Forms (Latin ligatures)
        'FF00-FFEF',  # Halfwidth and Fullwidth Forms
    ],

    # RNC, from the Wikipedia chart above:
    'Latin_Alphabetic': [
        # @
        '0041-005A',  # Basic Latin: A-Z
        # [\]^_`
        '0061-007A',  # Basic Latin: a-z
        # {|}~ then mishmash symbols
        0x00B5,       # Basic Latin: mu
        # more symbols
        '00C0-00D6',  # Basic Latin: accented capitals
        # multiplication symbol
        '00D8-00F6',  # Basic Latin: more accented capitals, something odd, Eszett, accented lower case  # noqa
        # division symbol
        '00F8-00FF',  # Basic Latin: more accented...

        '0100-017F',  # Latin Extended-A
        '0180-024F',  # Latin Extended-B
        # IPA Extensions
        # Spacing Modifier Letters
        # '1D00-1D7F',  # Phonetic Extensions
        # '1D80-1DBF',  # Phonetic Extensions Supplement
        '1E00-1EFF',  # Latin Extended Additional
        # '2070-209F',  # Superscripts and Subscripts
        # '2100-214F',  # Letterlike Symbols
        # '2150-218F',  # Number Forms
        '2C60-2C7F',  # Latin Extended-C
        'A720-A7AC',  # Latin Extended-D: part 1
        'A7B0-A7B7',  # Latin Extended-D: part 2
        'A7F7-A7FF',  # Latin Extended-D: part 3
        'AB30-AB65',  # Latin Extended-E: those assigned
        'FB00-FB06',  # Alphabetic Presentation Forms (Latin ligatures): those assigned  # noqa
        'FF20-FF5F',  # Halfwidth and Fullwidth Forms: those assigned
    ],
}


def get_unicode_category_strings() -> Dict[str, str]:
    """
    Returns a dictionary mapping Unicode categories (e.g. "ASCII") to a string
    containing those characters.

    This is large (~5 Mb) so don't call it unnecessarily and don't have it as a
    module-level variable.

    NB 'Alphabetic' has length 118240; 'Latin_Alphabetic' only 1022.
    """
    return {k: _unicode_def_src_to_str(v)
            for k, v in _UNICODE_CATEGORY_SRC.items()}


def get_unicode_characters(category: str) -> str:
    """
    Args:
        category:
            a Unicode category, e.g. "ASCII"

    Returns:
        str: a string containing those characters

    Raises:
        :exc:`KeyError` if the category is bad
    """
    definition_strings = _UNICODE_CATEGORY_SRC[category]
    return _unicode_def_src_to_str(definition_strings)
