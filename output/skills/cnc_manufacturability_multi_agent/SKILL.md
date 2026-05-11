---
name: CNC Manufacturability Multi-Agent System
description: |
  Build a multi-agent pipeline that analyzes CAD/STEP files for CNC manufacturability.
  TRIGGER: user wants to build a manufacturability checker, CNC feasibility analyzer,
  multi-agent CAD analysis system, or DFM (Design for Manufacturing) automation tool.
---

# CNC Manufacturability Multi-Agent System

Build a multi-agent system that takes STEP/CAD files and determines whether a CNC machine shop can manufacture the part — replacing 30-60 minute manual feasibility reviews with ~30 second automated assessments.

## When to use

- "Build a system that checks if a part is manufacturable on our CNC machines"
- "Create a multi-agent pipeline to analyze STEP files for manufacturing feasibility"
- "Automate DFM checks against our shop's tool inventory"
- "I need an AI system that extracts features from CAD files and determines required tooling"
- "Build a manufacturability report generator for machine shop quoting"

## How to use

### Architecture: 5-Stage Pipeline

1. **STEP File Parser** (Pure Python, no LLM)  
   Use `cadquery` (OpenCASCADE backend) for exact geometry extraction:
   - Cylindrical holes (diameter, depth)
   - Flat surfaces, chamfers, fillets
   - Bounding box, volume, surface area

   ```python
   import cadquery as cq
   from OCP.BRepAdaptor import BRepAdaptor_Surface
   from OCP.GeomAbs import GeomAbs_Cylinder

   def extract_features(step_file_path: str) -> dict:
       model = cq.importers.importStep(step_file_path)
       shape = model.val()
       bb = shape.BoundingBox()
       holes = {}
       for face in model.faces().vals():
           adaptor = BRepAdaptor_Surface(face.wrapped)
           if adaptor.GetType() == GeomAbs_Cylinder:
               radius = adaptor.Cylinder().Radius()
               diameter = round(radius * 2, 3)
               holes[diameter] = holes.get(diameter, 0) + 1
       return {
           "bounding_box": [bb.xlen, bb.ylen, bb.zlen],
           "holes": holes,
           "volume": shape.Volume(),
           "surface_area": shape.Area()
       }
   ```

2. **Agent 1: Operations Classifier** (LLM)  
   Determines required CNC operations and tools from extracted geometry, material, tolerances, and thread specs. Uses manufacturing domain knowledge (e.g., Steel 304 → carbide tooling).

3. **Agent 2: Tool Matcher** (Pure Python — no LLM)  
   Deterministic database lookup comparing shop tool inventory against requirements. Avoids hallucination risk.

4. **Agent 3: Feasibility Decision Agent** (LLM)  
   Produces structured JSON output:
   ```json
   {
     "decision": "CONDITIONAL",
     "confidence": "HIGH",
     "reason": "All tools available except M10x1.5 tap",
     "action_items": ["Purchase M10x1.5 tap ($15)"],
     "risk_flags": ["Verify spindle speed for Steel 304"],
     "estimated_setup_hours": 2.5
   }
   ```

5. **Agent 4: Report Generator** (LLM)  
   Synthesizes a professional manufacturability report with executive summary, part analysis, tool/machine status, and final recommendation.

### Technology Stack

| Layer | Technology |
|-------|------------|
| LLM | Qwen 2.5 7B Instruct (or any OpenAI-compatible model) |
| Inference | vLLM with OpenAI-compatible API |
| Orchestration | LangChain |
| API | FastAPI |
| CAD Processing | cadquery (OpenCASCADE) |
| Frontend | Next.js |
| GPU | AMD MI300X (or any ROCm/CUDA GPU) |

### LLM Setup with vLLM

```bash
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-7B-Instruct \
  --host 0.0.0.0 --port 8000 \
  --dtype float16 --gpu-memory-utilization 0.5
```

```python
from langchain_community.llms import VLLMOpenAI

llm = VLLMOpenAI(
    openai_api_base="http://localhost:8000/v1",
    openai_api_key="EMPTY",
    model_name="Qwen/Qwen2.5-7B-Instruct",
    temperature=0.1,
    max_tokens=1000
)
```

### Inputs

- STEP file (CAD geometry)
- Material type (e.g., Steel 304, Aluminum 6061)
- Required tolerance
- Thread specifications

### Outputs

- Manufacturability decision: YES / NO / CONDITIONAL
- Required tools list with availability status
- Missing tools with estimated procurement costs
- Risk assessment and flags
- Action items
- Setup time estimate
- Professional report (PDF/HTML)

### Key Design Principles

1. **LLMs only for reasoning** — Use pure Python for geometry extraction and tool matching (speed + reliability)
2. **Structured output** — Enforce JSON schemas via prompt engineering with manufacturing constraints
3. **Privacy by design** — On-premise inference keeps proprietary CAD data local
4. **Mathematical exactness** — Extract exact geometry from STEP files, not approximations

### Performance Targets

- Feature extraction: <1 second
- Full pipeline (all agents): 25-40 seconds end-to-end
- Zero external data transmission

## References

- [MachinaCheck Blog Post](https://huggingface.co/blog/lablab-ai-amd-developer-hackathon/machinacheck)
- [GitHub: Manufacturing-Agent](https://github.com/SyedMuhammadSarmad/Manufacturing-Agent)
- [Live Demo on HF Spaces](https://huggingface.co/spaces/lablab-ai-amd-developer-hackathon/MachinaCheck)
