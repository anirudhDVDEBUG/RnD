"""FastAPI REST server for Seidr-Smidja avatar generation."""


def start_server(port=8080):
    """Start the API server (requires fastapi and uvicorn)."""
    try:
        from fastapi import FastAPI
        import uvicorn
    except ImportError:
        print("[ERROR] FastAPI/uvicorn not installed. Run: pip install fastapi uvicorn")
        return

    from seidr_smidja import create_avatar

    app = FastAPI(title="Seidr-Smidja API", version="0.3.0")

    @app.post("/create")
    async def api_create(request: dict):
        result = create_avatar(
            name=request.get("name", "api_avatar"),
            style=request.get("style", "anime"),
            hair=request.get("hair"),
            eyes=request.get("eyes"),
            outfit=request.get("outfit"),
            accessories=request.get("accessories"),
        )
        return result

    @app.get("/styles")
    async def api_styles():
        from style_presets import PRESETS
        return {"styles": list(PRESETS.keys())}

    @app.get("/health")
    async def health():
        return {"status": "ok", "version": "0.3.0"}

    uvicorn.run(app, host="0.0.0.0", port=port)
