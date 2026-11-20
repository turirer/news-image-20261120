// News image for Friday 20 November 2026, make.fun bounty news-image-20261120.
// Node 22, standard library only. The entry is the PNG sitting next to this
// file; the program's whole job is to place a copy of it at
// $MAKEFUN_OUTPUT_DIR/entry.png. When that variable is not set it uses the
// ./out folder beside this file instead, creating it if needed.

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? join(here, "out");

if (!existsSync(outDir)) {
  mkdirSync(outDir, { recursive: true });
}

copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
