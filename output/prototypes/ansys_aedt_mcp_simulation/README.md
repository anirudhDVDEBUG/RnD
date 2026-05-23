# Ansys AEDT MCP Simulation

**TL;DR:** An MCP server that lets Claude drive Ansys Electronics Desktop (HFSS, Maxwell, Q3D, Icepak) through PyAEDT -- create geometries, assign materials, configure sweeps, run simulations, and extract results, all via natural-language conversation.

## Headline Result

```
  S11 (dB) vs Frequency (GHz)  --  2.4 GHz Patch Antenna
  ────────────────────────────────────────────────
    -2.0 |*  *                              *  *  *|
    -5.0 |      *                        *         |
   -10.0 |         *                  *            |
   -15.0 |            *           *                |
   -20.0 |               *     *                   |
   -25.0 |                  *                      |
          1.0 GHz ──────────────────────── 4.0 GHz

  Resonance: 2.4 GHz  |  Return Loss: -26.8 dB
```

Claude built the antenna geometry, set up the simulation, solved it, and plotted results -- entirely through MCP tool calls.

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** -- Install, configure, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** -- Architecture, data flow, limitations
- **[Source repo](https://github.com/LaplaceYoung/ansys-aedt-mcp)** -- Upstream MCP server

## Run the Demo

```bash
bash run.sh
```

No Ansys installation or API keys needed -- the demo uses a mock AEDT session to show the complete MCP tool-call sequence.
