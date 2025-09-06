import { createInterface } from 'readline';
import { allTools, handleToolInvocation } from './index.js';
function send(res) {
    process.stdout.write(JSON.stringify(res) + '\n');
}
function ok(id, result) {
    return { jsonrpc: '2.0', id, result };
}
function err(id, message, code = -32603) {
    return { jsonrpc: '2.0', id, error: { code, message } };
}
async function handle(req) {
    const id = req.id ?? null;
    try {
        if (req.method === 'tools/list') {
            return ok(id, { tools: allTools });
        }
        if (req.method === 'tools/call') {
            const { name, arguments: args } = req.params ?? {};
            if (!name)
                return err(id, 'Missing tool name', -32602);
            const result = await handleToolInvocation(name, args || {});
            // MCP response shape expects content array
            return ok(id, {
                content: [
                    {
                        type: 'text',
                        text: typeof result === 'string' ? result : JSON.stringify(result, null, 2),
                    },
                ],
            });
        }
        return err(id, `Method not found: ${req.method}`, -32601);
    }
    catch (e) {
        return err(id, e?.message || 'Internal error');
    }
}
async function main() {
    console.error('MCP server "doc-foundry" (shim) started on stdio');
    const rl = createInterface({ input: process.stdin, crlfDelay: Infinity });
    rl.on('line', async (line) => {
        if (!line.trim())
            return;
        let req;
        try {
            req = JSON.parse(line);
        }
        catch {
            send(err(null, 'Parse error', -32700));
            return;
        }
        const res = await handle(req);
        send(res);
    });
    rl.on('close', () => process.exit(0));
}
main().catch((e) => {
    console.error('Fatal:', e);
    process.exit(1);
});
