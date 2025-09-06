import { createInterface } from 'readline';
import { allTools, handleToolInvocation } from './index.js';

type JsonRpcReq = {
  jsonrpc: '2.0';
  id?: string | number | null;
  method: string;
  params?: any;
};

type JsonRpcRes =
  | { jsonrpc: '2.0'; id: string | number | null; result: any }
  | { jsonrpc: '2.0'; id: string | number | null; error: { code: number; message: string } };

function send(res: JsonRpcRes) {
  process.stdout.write(JSON.stringify(res) + '\n');
}

function ok(id: JsonRpcRes['id'], result: any): JsonRpcRes {
  return { jsonrpc: '2.0', id, result };
}

function err(id: JsonRpcRes['id'], message: string, code = -32603): JsonRpcRes {
  return { jsonrpc: '2.0', id, error: { code, message } };
}

async function handle(req: JsonRpcReq) {
  const id = req.id ?? null;

  try {
    if (req.method === 'tools/list') {
      return ok(id, { tools: allTools });
    }

    if (req.method === 'tools/call') {
      const { name, arguments: args } = req.params ?? {};
      if (!name) return err(id, 'Missing tool name', -32602);

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
  } catch (e: any) {
    return err(id, e?.message || 'Internal error');
  }
}

async function main() {
  console.error('MCP server "doc-foundry" (shim) started on stdio');
  const rl = createInterface({ input: process.stdin, crlfDelay: Infinity });

  rl.on('line', async (line) => {
    if (!line.trim()) return;
    let req: JsonRpcReq;
    try {
      req = JSON.parse(line);
    } catch {
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