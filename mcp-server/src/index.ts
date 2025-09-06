import { Tool } from '@modelcontextprotocol/sdk/types.js';
import { readinessTools, handleReadinessTool } from './tools/readiness.js';
import { allRoutes, handleCommand as handleRouterCommand } from './tools/quick-router.js';
import { generateProposalTools, handleGenerateProposalTool } from './tools/generate-proposal.js';
import { pingTools, handlePingTool } from './tools/ping.js';
import { ingestTools, handleIngestTool } from './tools/ingest.js';

// Aggregate all tools
export const allTools: Tool[] = [
  ...readinessTools,
  ...generateProposalTools,
  ...pingTools,
  ...ingestTools,
];

// Tool invocation dispatcher
export async function handleToolInvocation(name: string, args: any): Promise<any> {
  // Handle readiness tools
  if (readinessTools.find(t => t.name === name)) {
    return handleReadinessTool(name, args);
  }
  
  // Handle proposal generation
  if (generateProposalTools.find(t => t.name === name)) {
    return handleGenerateProposalTool(name, args);
  }
  
  // Handle ping health check
  if (pingTools.find(t => t.name === name)) {
    return handlePingTool(name, args);
  }
  
  // Handle ingest tools
  if (ingestTools.find(t => t.name === name)) {
    return handleIngestTool(name, args);
  }
  
  // Fallback
  throw new Error(`Unknown tool: ${name}`);
}

// Command router for natural language
export function handleCommand(command: string): any {
  // Try all routed commands
  const result = handleRouterCommand(command);
  if (result !== null) {
    return result;
  }
  
  // No match
  return null;
}

// Export for MCP server registration
export const mcpServerConfig = {
  tools: allTools,
  handleToolCall: handleToolInvocation,
  handleCommand: handleCommand,
};

// Export tools and handlers for use by other modules