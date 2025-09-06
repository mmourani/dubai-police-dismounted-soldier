// Separate module to avoid circular dependencies
export async function callTool(_server: string, toolName: string, args: any): Promise<any> {
  // Import dynamically to avoid circular dependency
  const { handleToolInvocation } = await import('./index.js');
  
  // We only host doc-foundry tools locally for now
  return handleToolInvocation(toolName, args);
}