import {
  CopilotRuntime,
  OpenAIAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { AzureOpenAI } from "openai";
import { NextRequest } from "next/server";

function getRequiredEnv(key: string): string {
  const value = process.env[key];
  if (!value) {
    throw new Error(`Missing required environment variable: ${key}`);
  }
  return value;
}

function buildHandler() {
  const endpoint = getRequiredEnv("AZURE_OPENAI_ENDPOINT").replace(/\/+$/, "");
  const apiKey = getRequiredEnv("AZURE_OPENAI_API_KEY");
  const deployment = getRequiredEnv("AZURE_OPENAI_DEPLOYMENT_CHAT");
  const apiVersion =
    process.env.AZURE_OPENAI_API_VERSION ?? "2024-02-15-preview";

  const openai = new AzureOpenAI({
    apiKey,
    endpoint,
    apiVersion,
    deployment,
  });

  const serviceAdapter = new OpenAIAdapter({ openai, model: deployment });
  const runtime = new CopilotRuntime();

  return copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  }).handleRequest;
}

export const POST = async (req: NextRequest) => buildHandler()(req);
export const GET = async (req: NextRequest) => buildHandler()(req);
export const OPTIONS = async (req: NextRequest) => buildHandler()(req);
