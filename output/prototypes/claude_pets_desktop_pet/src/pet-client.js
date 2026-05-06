// Mock OpenPets client — simulates the HTTP API that the real OpenPets desktop app exposes.
// In production, this sends PUT requests to http://localhost:42069/api/pet/status

const PET_STATES = {
  sleeping:  { emoji: "(-_-)zzZ", mood: "sleeping",  energy: 20 },
  waking:    { emoji: "(o_o)!",   mood: "alert",     energy: 50 },
  thinking:  { emoji: "(o_-)~",   mood: "thinking",  energy: 60 },
  coding:    { emoji: "(^_^)/",   mood: "happy",     energy: 80 },
  reading:   { emoji: "(@_@)",    mood: "focused",   energy: 70 },
  writing:   { emoji: "(>_<)/*",  mood: "busy",      energy: 75 },
  success:   { emoji: "\\(^o^)/", mood: "excited",   energy: 90 },
  error:     { emoji: "(;_;)",    mood: "sad",        energy: 40 },
  idle:      { emoji: "(-_-)",    mood: "bored",     energy: 30 },
  goodbye:   { emoji: "(^_^)/~~", mood: "waving",    energy: 10 },
};

const TOOL_TO_STATE = {
  Read:    "reading",
  Edit:    "writing",
  Write:   "writing",
  Bash:    "coding",
  Grep:    "reading",
  Glob:    "reading",
  Agent:   "thinking",
  default: "thinking",
};

class PetClient {
  constructor(baseUrl = "http://localhost:42069") {
    this.baseUrl = baseUrl;
    this.mock = true; // always mock in demo mode
    this.history = [];
  }

  async updateStatus(stateName, message) {
    const state = PET_STATES[stateName] || PET_STATES.idle;
    const entry = {
      timestamp: new Date().toISOString(),
      state: stateName,
      ...state,
      message: message || `Pet is ${state.mood}`,
    };
    this.history.push(entry);

    if (this.mock) {
      const line = `  ${state.emoji}  ${entry.message}  [${stateName}]`;
      console.log(line);
      return entry;
    }

    // Production path: PUT to OpenPets API
    const res = await fetch(`${this.baseUrl}/api/pet/status`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(entry),
    });
    return res.json();
  }

  stateForTool(toolName) {
    return TOOL_TO_STATE[toolName] || TOOL_TO_STATE.default;
  }

  getHistory() {
    return this.history;
  }
}

export { PetClient, PET_STATES, TOOL_TO_STATE };
