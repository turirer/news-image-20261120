// News image for Friday 20 November 2026, make.fun bounty news-image-20261120.
// Node 22, standard library only. The entry is the PNG sitting next to this
// file; the program's whole job is to place a copy of it at
// $MAKEFUN_OUTPUT_DIR/entry.png. When that variable is not set it uses the
// ./out folder beside this file instead, creating it if needed.

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? join(here, "out");

if (!existsSync(outDir)) {
  mkdirSync(outDir, { recursive: true });
}

const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");
copyFileSync(src, dst);

// The gate only accepts a whole PNG: check the signature bytes of what
// we just wrote, and report its size so a bad copy fails loudly.
const head = readFileSync(dst).subarray(0, 8);
const pngSig = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!head.equals(pngSig)) {
  throw new Error("entry.png is not a PNG file");
}
console.log(`wrote ${dst} (${statSync(dst).size} bytes)`);
