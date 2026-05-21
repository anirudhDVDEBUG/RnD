"""FastAPI bridge — HTTP/WebSocket API between the React control room and the Python runtime."""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from runtime.llm import LocalLLM
from runtime.rag import RAGPipeline
from runtime.mcp_client import MCPClient
from runtime.skills import SkillRegistry
from runtime.self_heal import SelfHealingEngine, flaky_operation

app = FastAPI(title="Zephyr Bridge", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Shared runtime singletons
llm = LocalLLM()
rag = RAGPipeline()
mcp = MCPClient()
skills = SkillRegistry()
healer = SelfHealingEngine()

# Seed some demo RAG content
rag.ingest_text("demo/intro.md", "Zephyr is a local-first AI sidekick that runs entirely on your machine.")
rag.ingest_text("demo/arch.md", "The architecture has three layers: React control room, FastAPI bridge, and Python runtime.")
rag.ingest_text("demo/rag.md", "RAG indexes local documents and augments LLM context with retrieved chunks for grounded answers.")

# Connect mock MCP servers
for srv in ("filesystem", "web_search", "database"):
    mcp.connect(srv)


# -- Request / Response models -------------------------------------------
class ChatRequest(BaseModel):
    message: str
    use_rag: bool = True


class MCPInvokeRequest(BaseModel):
    server: str
    operation: str
    params: dict | None = None


# -- REST endpoints ------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok", "model": llm.model_name, "rag_docs": len(rag.documents)}


@app.post("/chat")
def chat(req: ChatRequest):
    context = ""
    retrieved = []
    if req.use_rag:
        retrieved = rag.retrieve(req.message)
        context = " | ".join(d["text"][:150] for d in retrieved)

    result = llm.generate(req.message, context=context)
    return {**result, "retrieved_docs": len(retrieved)}


@app.get("/skills")
def list_skills():
    return skills.list_skills()


@app.get("/mcp/tools")
def list_mcp_tools():
    return mcp.list_tools()


@app.post("/mcp/invoke")
def invoke_mcp(req: MCPInvokeRequest):
    return mcp.invoke(req.server, req.operation, req.params)


@app.get("/self-heal/log")
def heal_log():
    return healer.get_log()


@app.post("/self-heal/demo")
def heal_demo():
    """Run a flaky operation through the self-healing engine."""
    result = healer.run_step("demo_flaky", flaky_operation, "network_call")
    return {"result": result, "log": healer.get_log()[-3:]}


# -- WebSocket for streaming chat ----------------------------------------
@app.websocket("/ws/chat")
async def ws_chat(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            msg = data.get("message", "")
            retrieved = rag.retrieve(msg)
            ctx = " | ".join(d["text"][:150] for d in retrieved)
            result = llm.generate(msg, context=ctx)
            await ws.send_json(result)
    except WebSocketDisconnect:
        pass
