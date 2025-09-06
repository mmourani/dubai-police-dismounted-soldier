import { callTool } from '../tool-caller.js';
// Help command routes
export const helpRoutes = [
    {
        test: /^(?:help|\?)$/i,
        run: () => ({
            content: [{
                    type: 'text',
                    text: `# MCP Proposal System Commands

## Ingest Commands
\`\`\`
ingest plan                    # Show active ingest plan and data state
ingest status                  # Show confidence, gaps, and file counts
ingest refresh                 # Re-run readiness analyzer
ingest apply [dry:true|false]  # Execute ingest steps (default: dry run)
\`\`\`

## Proposal Commands
\`\`\`
proposal outline new name:<PROJECT_ID> client:<CLIENT> project:"<PROJECT NAME>"
proposal outline show [name:<PROJECT_ID>]
proposal content draft name:<PROJECT_ID> section:<SECTION_ID>
proposal content approve name:<PROJECT_ID> section:<SECTION_ID>
proposal build name:<PROJECT_ID> format:(docx|pdf|html|md) [out:<path>] [template:<docx>]
\`\`\`

## Legacy Readiness Commands (Snapshot Mode)
\`\`\`
readiness analyze             # Analyze project documents
readiness status              # Show current readiness status
readiness answer <id>: <text> # Answer specific question
readiness park <id>: <note>   # Park question for later
generate proposal [force:true] [to <path>]  # Generate from snapshot
\`\`\`

## Health Commands
\`\`\`
ping                          # Health check
health                        # Same as ping
\`\`\`

*Each command shows what files it reads/writes in the output.*`
                }]
        })
    },
    {
        test: /^proposal\s+help$/i,
        run: () => ({ content: [{ type: 'text', text: 'Use \`help\` for all available commands.' }] })
    }
];
// Readiness analyzer routes for natural language commands (Legacy Snapshot Mode)
export const readinessRoutes = [
    {
        test: /^readiness\s+analyze\b/i,
        run: () => callTool('doc-foundry', 'readiness_analyze', {})
    },
    {
        test: /^readiness\s+status\b/i,
        run: () => callTool('doc-foundry', 'readiness_status', { verbose: true })
    },
    {
        // readiness answer <id>: <text>  OR readiness answer: <text>
        test: /^readiness\s+answer\b[:\s]+(.+)/i,
        run: (_cmd, m) => {
            const raw = m[1].trim();
            const idMatch = raw.match(/^([a-z_][\w-]*)\s*:\s*(.+)$/i);
            if (idMatch) {
                return callTool('doc-foundry', 'readiness_answer', {
                    question_id: idMatch[1],
                    answer: idMatch[2].trim()
                });
            }
            // no id → send answer to next unresolved
            return callTool('doc-foundry', 'readiness_answer', {
                question_id: '',
                answer: raw
            });
        }
    },
    {
        // readiness park <id>: <note>
        test: /^readiness\s+park\s+([a-z_][\w-]*)\s*:?[\s]*(.*)$/i,
        run: (_cmd, m) => callTool('doc-foundry', 'readiness_park', {
            question_id: m[1],
            note: m[2] || 'Parked for later'
        })
    },
    {
        test: /^readiness\s+draft(?:\s+to\s+(.+))?$/i,
        run: (_cmd, m) => callTool('doc-foundry', 'readiness_generate_draft', {
            output_file: m[1] || 'ingested_data/meta/draft.meta.yaml'
        })
    },
    {
        test: /^readiness\s+reset\s*(?:confirm)?$/i,
        run: () => callTool('doc-foundry', 'readiness_reset', { confirm: true })
    }
];
// Additional convenience routes
export const analyzerShortcuts = [
    {
        // "analyze opportunity" or just "analyze"
        test: /^(?:analyze|analyse)(?:\s+opportunity)?$/i,
        run: () => callTool('doc-foundry', 'readiness_analyze', {})
    },
    {
        // "what's our readiness" or "readiness?" 
        test: /^(?:what'?s\s+our\s+)?readiness\??$/i,
        run: () => callTool('doc-foundry', 'readiness_status', { verbose: true })
    },
    {
        // "answer: <text>" without "readiness" prefix
        test: /^answer\s*:\s*(.+)$/i,
        run: (_cmd, m) => callTool('doc-foundry', 'readiness_answer', {
            question_id: '',
            answer: m[1].trim()
        })
    },
    {
        // "park <id>" without "readiness" prefix
        test: /^park\s+([a-z_][\w-]*)\s*:?[\s]*(.*)$/i,
        run: (_cmd, m) => callTool('doc-foundry', 'readiness_park', {
            question_id: m[1],
            note: m[2] || 'Parked for later'
        })
    },
    {
        // "draft proposal" or "generate draft"
        test: /^(?:draft|generate\s+draft)(?:\s+proposal)?$/i,
        run: () => callTool('doc-foundry', 'readiness_generate_draft', {
            output_file: 'ingested_data/meta/draft.meta.yaml'
        })
    },
    {
        // "reset readiness" 
        test: /^reset\s+readiness$/i,
        run: () => callTool('doc-foundry', 'readiness_reset', { confirm: true })
    }
];
// Proposal generation routes
export const proposalRoutes = [
    {
        // "generate proposal" with optional "force:true" and optional path
        test: /^generate\s+proposal(?:\s+force\s*:\s*(true|false))?(?:\s+to\s+(.+))?$/i,
        run: (_cmd, m) => {
            const force = (m[1] ?? '').toLowerCase() === 'true';
            const out = m[2] || 'proposals/proposal.md';
            return callTool('doc-foundry', 'generate_proposal', { force, out });
        }
    },
    {
        // "draft proposal" or "generate draft"
        test: /^(?:draft\s+proposal|generate\s+draft)$/i,
        run: () => callTool('doc-foundry', 'generate_proposal', {
            force: true,
            out: 'proposals/proposal_draft.md'
        })
    },
    {
        // Simple "proposal" command
        test: /^proposal$/i,
        run: () => callTool('doc-foundry', 'generate_proposal', {
            force: false,
            out: 'proposals/proposal.md'
        })
    }
];
// Ping health check routes
export const pingRoutes = [
    {
        test: /^ping$/i,
        run: () => callTool('doc-foundry', 'ping', {})
    },
    {
        test: /^health$/i,
        run: () => callTool('doc-foundry', 'ping', {})
    },
    {
        test: /^health\s*check$/i,
        run: () => callTool('doc-foundry', 'ping', {})
    }
];
// Ingest routes
export const ingestRoutes = [
    {
        test: /^ingest\s+plan$/i,
        run: () => callTool('doc-foundry', 'ingest_plan', {})
    },
    {
        test: /^ingest\s+status$/i,
        run: () => callTool('doc-foundry', 'ingest_status', {})
    },
    {
        test: /^ingest\s+refresh$/i,
        run: () => callTool('doc-foundry', 'ingest_refresh', {})
    },
    {
        test: /^ingest\s+apply(?:\s+dry\s*:\s*(true|false))?$/i,
        run: (_c, m) => callTool('doc-foundry', 'ingest_apply', { dryRun: (m[1] ?? 'true').toLowerCase() !== 'false' })
    }
];
// Export combined routes for integration
export const allRoutes = [...helpRoutes, ...readinessRoutes, ...analyzerShortcuts, ...proposalRoutes, ...pingRoutes, ...ingestRoutes];
// Helper function to match and execute routes
export function handleCommand(command) {
    for (const route of allRoutes) {
        const match = command.match(route.test);
        if (match) {
            return route.run(command, match);
        }
    }
    return null;
}
// Legacy alias for backwards compatibility
export const handleReadinessCommand = handleCommand;
// Example integration with main router
export function integrateWithMainRouter(mainRouter) {
    // Add all routes to main router
    mainRouter.addRoutes(allRoutes);
    // Or use the handler function
    mainRouter.use((command) => {
        const result = handleCommand(command);
        if (result !== null) {
            return result;
        }
        // Continue to next handler
        return null;
    });
}
