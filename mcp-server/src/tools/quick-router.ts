import { callTool } from '../tool-caller.js';

// Readiness analyzer routes for natural language commands
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
    run: (_cmd: string, m: RegExpMatchArray) => {
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
    run: (_cmd: string, m: RegExpMatchArray) =>
      callTool('doc-foundry', 'readiness_park', { 
        question_id: m[1], 
        note: m[2] || 'Parked for later' 
      })
  },
  {
    test: /^readiness\s+draft(?:\s+to\s+(.+))?$/i,
    run: (_cmd: string, m: RegExpMatchArray) =>
      callTool('doc-foundry', 'readiness_generate_draft', {
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
    run: (_cmd: string, m: RegExpMatchArray) =>
      callTool('doc-foundry', 'readiness_answer', {
        question_id: '',
        answer: m[1].trim()
      })
  },
  {
    // "park <id>" without "readiness" prefix
    test: /^park\s+([a-z_][\w-]*)\s*:?[\s]*(.*)$/i,
    run: (_cmd: string, m: RegExpMatchArray) =>
      callTool('doc-foundry', 'readiness_park', {
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
    run: (_cmd: string, m: RegExpMatchArray) => {
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
    run: () => callTool('doc-foundry','ingest_plan', {}) 
  },
  { 
    test: /^ingest\s+status$/i,   
    run: () => callTool('doc-foundry','ingest_status', {}) 
  },
  { 
    test: /^ingest\s+refresh$/i,  
    run: () => callTool('doc-foundry','ingest_refresh', {}) 
  },
  { 
    test: /^ingest\s+apply(?:\s+dry\s*:\s*(true|false))?$/i,
    run: (_c: string, m: RegExpMatchArray) => callTool('doc-foundry','ingest_apply', { dryRun: (m[1] ?? 'true').toLowerCase() !== 'false' }) 
  }
];

// Export combined routes for integration
export const allReadinessRoutes = [...readinessRoutes, ...analyzerShortcuts, ...proposalRoutes, ...pingRoutes, ...ingestRoutes];

// Helper function to match and execute routes
export function handleReadinessCommand(command: string): any {
  for (const route of allReadinessRoutes) {
    const match = command.match(route.test);
    if (match) {
      return route.run(command, match);
    }
  }
  return null;
}

// Example integration with main router
export function integrateWithMainRouter(mainRouter: any) {
  // Add readiness routes to main router
  mainRouter.addRoutes(allReadinessRoutes);
  
  // Or use the handler function
  mainRouter.use((command: string) => {
    const result = handleReadinessCommand(command);
    if (result !== null) {
      return result;
    }
    // Continue to next handler
    return null;
  });
}