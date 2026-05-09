import { spawn } from "child_process";
import { NextRequest, NextResponse } from "next/server";
import path from "path";

const ALLOWED_TOOLS = new Set([
  "generate_plan",
  "generate_section_content",
  "answer_with_rag",
]);

function runPythonTool(
  tool: string,
  args: Record<string, unknown>
): Promise<unknown> {
  return new Promise((resolve, reject) => {
    const serverDir = path.resolve(process.cwd(), "../server");

    const child = spawn(
      "uv",
      ["run", "--env-file", ".env", "python", "-c", buildScript(tool, args)],
      {
        cwd: serverDir,
        env: { ...process.env },
      }
    );

    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (chunk: Buffer) => {
      stdout += chunk.toString();
    });

    child.stderr.on("data", (chunk: Buffer) => {
      stderr += chunk.toString();
    });

    child.on("close", (code) => {
      if (code !== 0) {
        reject(new Error(stderr || `Process exited with code ${code}`));
        return;
      }

      try {
        resolve(JSON.parse(stdout.trim()));
      } catch {
        reject(new Error(`Invalid JSON from tool: ${stdout}`));
      }
    });

    child.on("error", reject);
  });
}

function buildScript(tool: string, args: Record<string, unknown>): string {
  const argsJson = JSON.stringify(args);
  return [
    "import asyncio, json",
    `from podagent_server.mcp.tools.learnflow import ${tool}`,
    `args = json.loads(${JSON.stringify(argsJson)})`,
    `result = asyncio.run(${tool}(**args))`,
    "print(json.dumps(result))",
  ].join("; ");
}

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ tool: string }> }
): Promise<NextResponse> {
  const { tool } = await params;

  if (!ALLOWED_TOOLS.has(tool)) {
    return NextResponse.json(
      { success: false, error: `Unknown tool: ${tool}` },
      { status: 400 }
    );
  }

  let body: Record<string, unknown>;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json(
      { success: false, error: "Invalid JSON body" },
      { status: 400 }
    );
  }

  try {
    const data = await runPythonTool(tool, body);
    return NextResponse.json({ success: true, data });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json(
      { success: false, error: message },
      { status: 500 }
    );
  }
}
