import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
const [repo, proposalFile] = process.argv.slice(2);
if (!repo || !proposalFile) { console.error('usage: node verify-eidos.mjs <eidos-repo> <proposal.json>'); process.exit(2); }
const proposal = JSON.parse(fs.readFileSync(proposalFile,'utf8'));
const mod = await import(pathToFileURL(path.resolve(repo,'dist/experience/validate.js')).href);
const c = mod.validateExperienceContext(proposal.context);
const x = mod.validateExperienceComposition(proposal.composition);
const ok = proposal.contractVersion === '0.1.0' && typeof proposal.proposalId === 'string' && typeof proposal.producedAt === 'string' && c.ok && x.ok;
console.log(JSON.stringify({ok, outerContractVersion:proposal.contractVersion, context:c, composition:x}, null, 2));
process.exit(ok?0:1);
