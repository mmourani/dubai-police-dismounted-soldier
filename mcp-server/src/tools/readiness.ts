import { Tool } from '@modelcontextprotocol/sdk/types.js';
import { exec } from 'child_process';
import { promisify } from 'util';
import * as path from 'path';
import * as fs from 'fs/promises';

const execAsync = promisify(exec);

// Path to the Python readiness analyzer
const ANALYZER_PATH = path.join(process.cwd(), 'ingested_data', 'meta', 'readiness_analyzer.py');
const PROJECT_ROOT = process.cwd();

export const readinessTools: Tool[] = [
  {
    name: 'readiness_analyze',
    description: 'Analyze project readiness and identify gaps. Returns confidence score and missing information.',
    inputSchema: {
      type: 'object',
      properties: {
        mode: {
          type: 'string',
          enum: ['analyze', 'draft'],
          description: 'Mode: analyze (identify gaps) or draft (generate with assumptions)',
          default: 'analyze'
        },
        force_rescan: {
          type: 'boolean',
          description: 'Force rescan of files even if session exists',
          default: false
        }
      }
    }
  },
  {
    name: 'readiness_answer',
    description: 'Answer a specific readiness question by ID',
    inputSchema: {
      type: 'object',
      properties: {
        question_id: {
          type: 'string',
          description: 'The ID of the question to answer'
        },
        answer: {
          type: 'string',
          description: 'The answer to provide'
        }
      },
      required: ['question_id', 'answer']
    }
  },
  {
    name: 'readiness_status',
    description: 'Get current readiness status, confidence score, and pending questions',
    inputSchema: {
      type: 'object',
      properties: {
        verbose: {
          type: 'boolean',
          description: 'Include detailed question status',
          default: false
        }
      }
    }
  },
  {
    name: 'readiness_park',
    description: 'Park a question for later (mark as pending with a note)',
    inputSchema: {
      type: 'object',
      properties: {
        question_id: {
          type: 'string',
          description: 'The ID of the question to park'
        },
        note: {
          type: 'string',
          description: 'Note about why this is parked (e.g., "Waiting for supplier quote")'
        }
      },
      required: ['question_id']
    }
  },
  {
    name: 'readiness_reset',
    description: 'Reset the readiness analyzer session',
    inputSchema: {
      type: 'object',
      properties: {
        confirm: {
          type: 'boolean',
          description: 'Confirm reset (will lose all answers)',
          default: false
        }
      }
    }
  },
  {
    name: 'readiness_generate_draft',
    description: 'Generate draft metadata with explicit assumptions for unanswered questions',
    inputSchema: {
      type: 'object',
      properties: {
        output_file: {
          type: 'string',
          description: 'Output file path for draft metadata',
          default: 'draft.meta.yaml'
        }
      }
    }
  }
];

export async function handleReadinessTool(name: string, args: any): Promise<any> {
  try {
    // Ensure Python analyzer exists
    await fs.access(ANALYZER_PATH);
    
    let command: string;
    
    switch (name) {
      case 'readiness_analyze':
        command = `python3 "${ANALYZER_PATH}" analyze`;
        if (args.mode === 'draft') {
          command += ' --draft';
        }
        if (args.force_rescan) {
          command += ' --force-rescan';
        }
        break;
        
      case 'readiness_answer':
        // Escape single quotes in answer
        const escapedAnswer = args.answer.replace(/'/g, "'\\''");
        command = `python3 "${ANALYZER_PATH}" answer '${args.question_id}' '${escapedAnswer}'`;
        break;
        
      case 'readiness_status':
        command = `python3 "${ANALYZER_PATH}" status`;
        if (args.verbose) {
          command += ' --verbose';
        }
        break;
        
      case 'readiness_park':
        const escapedNote = args.note ? args.note.replace(/'/g, "'\\''") : '';
        command = `python3 "${ANALYZER_PATH}" park '${args.question_id}'`;
        if (escapedNote) {
          command += ` '${escapedNote}'`;
        }
        break;
        
      case 'readiness_reset':
        if (!args.confirm) {
          return {
            error: 'Reset requires confirmation. Set confirm: true to proceed.',
            warning: 'This will lose all answered questions!'
          };
        }
        command = `python3 "${ANALYZER_PATH}" reset --confirm`;
        break;
        
      case 'readiness_generate_draft':
        command = `python3 "${ANALYZER_PATH}" draft`;
        if (args.output_file) {
          command += ` --output '${args.output_file}'`;
        }
        break;
        
      default:
        throw new Error(`Unknown readiness tool: ${name}`);
    }
    
    // Execute Python command
    const { stdout, stderr } = await execAsync(command, {
      cwd: PROJECT_ROOT,
      env: { ...process.env, PYTHONPATH: PROJECT_ROOT }
    });
    
    if (stderr && !stderr.includes('Warning')) {
      console.error('Python stderr:', stderr);
    }
    
    // Parse JSON output from Python
    try {
      return JSON.parse(stdout);
    } catch (e) {
      // If not JSON, return as text
      return { output: stdout, stderr: stderr || undefined };
    }
    
  } catch (error: any) {
    return {
      error: error.message,
      details: error.stderr || error.stdout || 'Unknown error'
    };
  }
}

// Helper function to get question routing suggestions
export function getQuestionRouting(question: any): string {
  const who = question.who_to_ask || 'Unknown';
  const routingSuggestions: Record<string, string> = {
    'Customer': 'Route to Dubai Police procurement team or project manager',
    'SupplierINVISIO': 'Contact INVISIO sales team for audio equipment specs/pricing',
    'SupplierSamsung': 'Contact Samsung Enterprise for device specifications',
    'SupplierMount': 'Contact tactical equipment suppliers for mount systems',
    'Engineering': 'Internal engineering team review required',
    'End-User': 'SWAT team feedback needed on operational requirements',
    'Market Intelligence': 'Research competitive solutions and pricing',
    'Legal': 'Legal/compliance review for export controls or regulations',
    'Finance': 'Finance team for budget approval or payment terms'
  };
  
  return routingSuggestions[who] || `Route to ${who}`;
}

// Helper to format confidence score with color coding
export function formatConfidence(confidence: number): string {
  if (confidence >= 95) {
    return `✅ ${confidence}% (Ready for final generation)`;
  } else if (confidence >= 80) {
    return `🟨 ${confidence}% (Can generate draft with assumptions)`;
  } else if (confidence >= 60) {
    return `🟧 ${confidence}% (Many gaps, draft will have high risk)`;
  } else {
    return `🔴 ${confidence}% (Critical gaps, need more information)`;
  }
}