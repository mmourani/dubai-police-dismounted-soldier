import { exec } from 'child_process';
import { promisify } from 'util';
import * as path from 'path';
import * as fs from 'fs/promises';
const execAsync = promisify(exec);
const PROJECT_ROOT = process.cwd();
const BUILDER_PATH = path.join(PROJECT_ROOT, 'ingested_data', 'meta', 'proposal_builder.py');
export const generateProposalTools = [
    {
        name: 'generate_proposal',
        description: 'Generate proposals from readiness snapshot (legacy mode) in various formats. Blocks if confidence < 95% unless force:true. Use --spec for content-first mode.',
        inputSchema: {
            type: 'object',
            properties: {
                force: {
                    type: 'boolean',
                    description: 'Force generation even if confidence < 95%',
                    default: false
                },
                out: {
                    type: 'string',
                    description: 'Output file path for the proposal',
                    default: 'proposals/proposal.md'
                },
                format: {
                    type: 'string',
                    enum: ['md', 'html', 'pdf', 'docx'],
                    description: 'Output format (md/html/pdf/docx)',
                    default: 'md'
                },
                template: {
                    type: 'string',
                    description: 'Path to DOCX template (for docx format)'
                }
            }
        }
    }
];
export async function handleGenerateProposalTool(name, args) {
    if (name !== 'generate_proposal') {
        throw new Error(`Unknown tool: ${name}`);
    }
    // Check if builder script exists
    try {
        await fs.access(BUILDER_PATH);
    }
    catch {
        throw new Error(`proposal_builder.py not found at ${BUILDER_PATH}`);
    }
    // Build command with proper escaping
    const forceFlag = args.force ? '--force' : '';
    const outArg = args.out ? `--out '${args.out.replace(/'/g, "'\\''")}'` : '';
    const formatArg = args.format ? `--format ${args.format}` : '';
    const templateArg = args.template ? `--template '${args.template.replace(/'/g, "'\\''")}'` : '';
    const cmd = `python3 "${BUILDER_PATH}" ${forceFlag} ${formatArg} ${templateArg} ${outArg}`.trim();
    try {
        const { stdout, stderr } = await execAsync(cmd, {
            cwd: PROJECT_ROOT,
            env: { ...process.env, PYTHONPATH: PROJECT_ROOT }
        });
        // Log stderr if present (for debugging)
        if (stderr && !/^\s*$/.test(stderr)) {
            console.error('Python stderr:', stderr);
        }
        // Parse JSON response
        try {
            const result = JSON.parse(stdout);
            // Add helpful formatting for success cases
            if (result.success) {
                result.message = result.message || `Proposal generated successfully at ${result.output_file}`;
                if (result.forced) {
                    result.message += ' (DRAFT with assumptions)';
                }
            }
            return result;
        }
        catch (e) {
            // If not JSON, return raw output
            return {
                output: stdout,
                stderr: stderr || undefined,
                success: false,
                error: 'Failed to parse builder output'
            };
        }
    }
    catch (error) {
        return {
            success: false,
            error: error.message || 'Unknown error running proposal builder',
            details: error.stderr || error.stdout || undefined
        };
    }
}
