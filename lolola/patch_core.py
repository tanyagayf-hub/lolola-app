"""lolola: changes to hiddify-core made before it is built (.github/workflows/lolola-android.yml).

REALITY links without a keyshare parameter get keyshare=classical: the X25519 key share only,
whose ClientHello fits in one TCP segment. Hiddify's default, hybrid (X25519MLKEM768), is cut
by DPI in Russia, and the lolola servers (Xray 26.6.27) accept classical. A link that names its
keyshare keeps it.

Usage: python3 lolola/patch_core.py <hiddify-core folder>
"""

import pathlib
import sys

core = pathlib.Path(sys.argv[1])
path = core / "ray2sing" / "ray2sing" / "common.go"
text = path.read_text()

old = "\treturn strings.ToLower(keyShare)\n}"
new = (
    "\tif keyShare == \"\" { // lolola: classical unless the link says otherwise\n"
    "\t\tkeyShare = \"classical\"\n"
    "\t}\n"
    "\treturn strings.ToLower(keyShare)\n}"
)
if text.count(old) != 1:
    sys.exit(f"lolola patch: the keyshare code in {path} has changed, check the patch")
path.write_text(text.replace(old, new))
print(f"lolola patch: {path}: REALITY keyshare defaults to classical")
