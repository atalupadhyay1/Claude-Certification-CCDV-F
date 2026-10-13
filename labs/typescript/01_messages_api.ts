// Lab 01 (TypeScript) — Messages API. Run: npx tsx 01_messages_api.ts [--mock]
import Anthropic from "@anthropic-ai/sdk";

const mock = process.argv.includes("--mock");
const request = {
  model: process.env.CLAUDE_MODEL ?? "claude-sonnet-5",
  max_tokens: 256,
  system: "You are a support triage assistant. Reply ONLY with JSON: {category, priority}.",
  messages: [{ role: "user" as const, content: "<ticket>Order #4411 was charged twice</ticket>\nClassify this ticket." }],
};

console.log("=== REQUEST ===\n", JSON.stringify(request, null, 2));
if (mock) {
  console.log('=== MOCK RESPONSE ===\n{"category":"billing","priority":"normal"} stop_reason=end_turn');
} else {
  const client = new Anthropic(); // reads ANTHROPIC_API_KEY
  const msg = await client.messages.create(request);
  console.log("=== RESPONSE ===\n", JSON.stringify(msg, null, 2));
  console.log(`stop_reason=${msg.stop_reason} usage=${JSON.stringify(msg.usage)}`);
}
