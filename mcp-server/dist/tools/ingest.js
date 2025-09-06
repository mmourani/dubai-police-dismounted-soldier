import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { exec as _exec } from 'child_process';
import { promisify } from 'util';
const exec = promisify(_exec);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '../../..');
async function pickPlan() {
    const candidates = [
        path.join(ROOT, 'Dubai_Police_Ingest_Plan.md'),
        path.join(ROOT, 'Data_Ingestion_Plan.md')
    ];
    for (const p of candidates) {
        try {
            await fs.access(p);
            return p;
        }
        catch { }
    }
    return '';
}
export const ingestTools = [
    {
        name: 'ingest_plan',
        description: 'Show the active ingest plan (prefers Dubai_Police_Ingest_Plan.md) and a state audit.',
        inputSchema: { type: 'object', properties: {} }
    },
    {
        name: 'ingest_status',
        description: 'Summarize ingested_data/ (evidence, processed, meta) and snapshot confidence.',
        inputSchema: { type: 'object', properties: {} }
    },
    {
        name: 'ingest_refresh',
        description: 'Re-run readiness analyzer to refresh snapshot.',
        inputSchema: { type: 'object', properties: {} }
    },
    {
        name: 'ingest_apply',
        description: 'Execute basic steps from the plan: (a) analyze, (b) list processed artifacts. (Non-destructive).',
        inputSchema: {
            type: 'object',
            properties: {
                dryRun: { type: 'boolean', description: 'If true, only report what would run', default: true }
            }
        }
    }
];
export async function handleIngestTool(name, args) {
    if (name === 'ingest_plan') {
        const planPath = await pickPlan();
        const planHead = planPath
            ? (await fs.readFile(planPath, 'utf-8')).split('\n').slice(0, 80).join('\n')
            : '(No plan file found)';
        const dirs = ['ingested_data/evidence', 'ingested_data/processed', 'ingested_data/meta'];
        const listings = [];
        for (const d of dirs) {
            const p = path.join(ROOT, d);
            try {
                listings.push(`• ${d}:\n` + (await fs.readdir(p)).slice(0, 100).join('\n'));
            }
            catch {
                listings.push(`• ${d}: (missing)`);
            }
        }
        const summary = [
            `Plan file: ${planPath || '—'}`,
            '',
            '=== PLAN (first 80 lines) ===',
            planHead,
            '',
            '=== DATA STATE ===',
            ...listings,
        ].join('\n');
        return { content: [{ type: 'text', text: summary }] };
    }
    if (name === 'ingest_status') {
        // snapshot + quick counts
        const snapPath = path.join(ROOT, 'ingested_data/meta/opportunity.readiness.json');
        let confidence = 'unknown', gaps = 'unknown';
        try {
            const j = JSON.parse(await fs.readFile(snapPath, 'utf-8'));
            confidence = String(Math.round((j.confidence || 0) * 100)) + '%';
            gaps = String((j.gaps || []).filter((g) => !g.resolved).length);
        }
        catch { }
        async function count(d) { try {
            return (await fs.readdir(path.join(ROOT, d))).length;
        }
        catch {
            return 0;
        } }
        const text = [
            `Confidence: ${confidence}`,
            `Unresolved gaps: ${gaps}`,
            `evidence/: ${await count('ingested_data/evidence')}`,
            `processed/: ${await count('ingested_data/processed')}`,
            `meta/: ${await count('ingested_data/meta')}`,
        ].join('\n');
        return { content: [{ type: 'text', text }] };
    }
    if (name === 'ingest_refresh') {
        const cmd = `python3 "${path.join(ROOT, 'ingested_data/meta/readiness_analyzer.py')}" analyze`;
        const { stdout, stderr } = await exec(cmd, { cwd: ROOT });
        const text = `✅ analyzer ran\n\nstdout:\n${stdout || '(none)'}\n${stderr ? `\nstderr:\n${stderr}` : ''}`;
        return { content: [{ type: 'text', text }] };
    }
    if (name === 'ingest_apply') {
        const dry = !!args?.dryRun;
        const steps = [
            `python3 "${path.join(ROOT, 'ingested_data/meta/readiness_analyzer.py')}" analyze`,
            // (hook in any deterministic extract/normalize steps you want here)
        ];
        if (dry) {
            return { content: [{ type: 'text', text: `Dry run. Would execute:\n- ` + steps.join('\n- ') }] };
        }
        let log = '';
        for (const s of steps) {
            const { stdout, stderr } = await exec(s, { cwd: ROOT });
            log += `\n$ ${s}\n${stdout || ''}${stderr ? `\nstderr:\n${stderr}\n` : ''}`;
        }
        return { content: [{ type: 'text', text: `✅ ingest apply completed\n${log}` }] };
    }
    throw new Error(`Unknown ingest tool: ${name}`);
}
