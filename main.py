"""news-23 b122 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
Validates the PNG by parsing its header with struct: signature, IHDR 1024x1024,
bit depth 8, colour type 2/6, compression/filter/interlace 0, IHDR CRC, per-chunk
CRCs, non-empty IDAT payload, IEND 0-byte as the last chunk, size 10_000..1MiB.
"""
import hashlib
import os
import struct
import sys
import zlib

MIN_SIZE = 10_000
MAX_SIZE = 1_048_576
WANT_W, WANT_H = 1024, 1024

def fail(msg):
    print("ERROR:", msg, file=sys.stderr)
    return 1

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not outdir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    outdir_abs = os.path.abspath(outdir)
    if outdir_abs == os.path.abspath(here):
        return fail("MAKEFUN_OUTPUT_DIR must not be the repo dir")
    if os.path.commonpath([outdir_abs, os.path.abspath(here)]) == os.path.abspath(here):
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if os.path.isfile(outdir_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    if not os.path.isfile(src):
        return fail("entry.png missing next to main.py")
    data = open(src, "rb").read()
    if len(data) < MIN_SIZE or len(data) > MAX_SIZE:
        return fail("entry.png size %d out of range" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("bad PNG signature")
    # chunk walk: 8-byte signature, then chunks (4 len + 4 type + data + 4 CRC).
    # First chunk must be IHDR, 13 bytes, starting at offset 8.
    pos = 8
    if len(data) < pos + 25:
        return fail("truncated PNG")
    ln = struct.unpack(">I", data[pos:pos + 4])[0]
    typ = data[pos + 4:pos + 8]
    if typ != b"IHDR" or ln != 13:
        return fail("first chunk is not a 13-byte IHDR")
    ihdr = data[pos + 8:pos + 21]
    w, h, depth, ctype, comp, filt, inter = struct.unpack(">IIBBBBB", ihdr)
    if (w, h) != (WANT_W, WANT_H):
        return fail("dimensions %dx%d, want 1024x1024" % (w, h))
    if depth != 8 or ctype not in (2, 6):
        return fail("bad bit depth/colour type")
    if comp != 0 or filt != 0 or inter != 0:
        return fail("bad compression/filter/interlace")
    crc_stored = struct.unpack(">I", data[pos + 21:pos + 25])[0]
    if zlib.crc32(b"IHDR" + ihdr) & 0xFFFFFFFF != crc_stored:
        return fail("IHDR CRC mismatch")
    # walk remaining chunks from offset 33: 8-byte signature + 25-byte IHDR
    # chunk (4 length + 4 type + 13 data + 4 CRC). The next chunk starts
    # at 33, not 37 — the IHDR data is 13 bytes, not 17.
    pos = 33
    idat_total = 0
    seen_iend = False
    while pos < len(data):
        if len(data) < pos + 12:
            return fail("truncated chunk header")
        ln = struct.unpack(">I", data[pos:pos + 4])[0]
        typ = data[pos + 4:pos + 8]
        end = pos + 12 + ln
        if end > len(data):
            return fail("truncated chunk " + typ.decode("latin1"))
        crc_stored = struct.unpack(">I", data[pos + 8 + ln:pos + 12 + ln])[0]
        if zlib.crc32(typ + data[pos + 8:pos + 8 + ln]) & 0xFFFFFFFF != crc_stored:
            return fail("CRC mismatch in chunk " + typ.decode("latin1"))
        if typ == b"IDAT":
            if ln == 0:
                return fail("empty IDAT chunk")
            idat_total += ln
        if typ == b"IEND":
            if ln != 0:
                return fail("IEND must be 0 bytes")
            if end != len(data):
                return fail("trailing data after IEND")
            seen_iend = True
            break
        pos = end
    if not seen_iend:
        return fail("missing IEND")
    if idat_total < 1000:
        return fail("IDAT payload too small")
    os.makedirs(outdir_abs, exist_ok=True)
    dst = os.path.join(outdir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        return fail("output would overwrite the source")
    with open(dst, "wb") as f:
        f.write(data)
    back = open(dst, "rb").read()
    if back != data:
        return fail("re-read mismatch")
    print("wrote %s (%d bytes) sha256=%s" % (dst, len(data),
          hashlib.sha256(data).hexdigest()))
    return 0

if __name__ == "__main__":
    sys.exit(main())
