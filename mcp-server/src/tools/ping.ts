import type { Tool } from '@modelcontextprotocol/sdk/types.js';

export const pingTools: Tool[] = [
  {
    name: 'ping',
    description: 'Health check tool. Returns { ok: true, ts }',
    inputSchema: { type: 'object', properties: {}, additionalProperties: false }
  }
];

export async function handlePingTool(name: string, _args: any) {
  if (name !== 'ping') throw new Error(`Unknown tool: ${name}`);
  return { ok: true, ts: new Date().toISOString() };
}