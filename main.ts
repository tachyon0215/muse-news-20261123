// Entry program for the news-image competition (Node 22, no dependencies).
//
// The artwork for this entry lives in the entry.png file stored next to this
// script. Running the program publishes that image as the entry by copying
// it, byte for byte, to a file named entry.png inside the output folder.
//
// The output folder comes from the MAKEFUN_OUTPUT_DIR environment variable
// when it is set; otherwise it defaults to /output, which is where the
// grader expects to find the finished image.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Resolve the folder this script sits in, so the source image is found
// relative to the script itself rather than the caller's working directory.
const scriptDir = dirname(fileURLToPath(import.meta.url));
const sourceImage = join(scriptDir, "entry.png");

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const destination = join(outputDir, "entry.png");

// Make sure the target folder exists, then copy the image across unchanged
// so repeated runs always produce identical bytes.
mkdirSync(outputDir, { recursive: true });
copyFileSync(sourceImage, destination);
