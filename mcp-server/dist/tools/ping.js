export const pingTools = [
    {
        name: 'ping',
        description: 'Health check tool. Returns { ok: true, ts }',
        inputSchema: { type: 'object', properties: {}, additionalProperties: false }
    }
];
export async function handlePingTool(name, _args) {
    if (name !== 'ping')
        throw new Error(`Unknown tool: ${name}`);
    return { ok: true, ts: new Date().toISOString() };
}
