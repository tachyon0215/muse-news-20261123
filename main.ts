// Entry point for the 23 November 2026 news-image entry.
//
// The finished artwork is stored in this repository as entry.png, next to
// this file. When the grader runs the program, it has to place that exact
// picture at entry.png inside the output directory, so this program simply
// performs a byte-for-byte copy. Doing it this way keeps the output
// deterministic: two runs always produce identical bytes, and there is no
// network or clock involved at any point.
//
// Where the copy lands:
//   - MAKEFUN_OUTPUT_DIR/entry.png when that variable is set (local runs)
//   - /output/entry.png otherwise (the grader's container)

import fs from "node:fs";
import path from "node:path";
import url from "node:url";

const here = path.dirname(url.fileURLToPath(import.meta.url));
const artwork = path.join(here, "entry.png");

const targetDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const destination = path.join(targetDir, "entry.png");
fs.mkdirSync(targetDir, { recursive: true });
fs.copyFileSync(artwork, destination);

// Guard against a truncated copy: the destination must end up exactly as
// large as the artwork it came from, otherwise something went wrong and
// the run should fail loudly instead of submitting a broken image.
const expected = fs.statSync(artwork).size;
const written = fs.statSync(destination).size;
if (written !== expected) {
  throw new Error(`copy incomplete: wrote ${written} of ${expected} bytes`);
}
