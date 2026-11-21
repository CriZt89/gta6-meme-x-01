// gta6-meme-x-01 entry: the post itself is the entry, so this program only
// carries POST.json (the X post's address) into /output for the gate.
// The house reads the post from X and builds the judge's dossier from it.
// Deterministic by construction: same POST.json in, same POST.json out, no
// network, no clock, no files outside the repository.
import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(outDir, { recursive: true });
try {
  copyFileSync(join(botDir, 'POST.json'), join(outDir, 'POST.json'));
} catch (err) {
  console.error(`could not copy POST.json: ${(err as Error).message}`);
  process.exit(1);
}
