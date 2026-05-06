/**
 * Mock OpenPets MCP Server
 *
 * Simulates the MCP server that OpenPets exposes to Claude Code.
 * In the real project, this runs alongside the Electron desktop pet app
 * and bridges agent status → pet animations via JSON-RPC over stdio.
 */

const PET_STATES = {
  idle: {
    label: "Idle",
    animation: "sitting",
    frames: ["(=^.^=)", "(=^-^=)", "(=^.^=)", "(=^o^=)"],
    description: "Pet is relaxing — agent is not active",
  },
  thinking: {
    label: "Thinking",
    animation: "head_tilt",
    frames: ["(=^.^=)?", "(=^·^=)!", "(=^.^=)?", "(=^~^=)…"],
    description: "Agent is planning or reasoning",
  },
  coding: {
    label: "Coding",
    animation: "typing",
    frames: ["(=^.^=)⌨", "(=^-^=)⌨", "(=^.^=)💻", "(=^>^=)⌨"],
    description: "Agent is actively writing code",
  },
  error: {
    label: "Error",
    animation: "alert",
    frames: ["(=^X^=)!", "(=^!^=)⚠", "(=^X^=)!", "(=^!^=)⚠"],
    description: "Agent encountered an error",
  },
  success: {
    label: "Success",
    animation: "celebrate",
    frames: ["(=^✓^=)✨", "(=^▽^=)🎉", "(=^✓^=)✨", "(=^▽^=)⭐"],
    description: "Task completed successfully",
  },
};

// MCP Tool definitions that OpenPets exposes
const MCP_TOOLS = [
  {
    name: "set_pet_status",
    description:
      "Update the desktop pet's visual state to reflect current agent activity",
    inputSchema: {
      type: "object",
      properties: {
        status: {
          type: "string",
          enum: ["idle", "thinking", "coding", "error", "success"],
          description: "The current activity state of the coding agent",
        },
        message: {
          type: "string",
          description: "Optional status message to display near the pet",
        },
      },
      required: ["status"],
    },
  },
  {
    name: "get_pet_status",
    description: "Get the current state of the desktop pet",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
  {
    name: "list_pets",
    description: "List all available pet sprites/characters",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
  {
    name: "set_pet_character",
    description: "Change the active pet character/sprite",
    inputSchema: {
      type: "object",
      properties: {
        character: {
          type: "string",
          description: "Name of the pet character to switch to",
        },
      },
      required: ["character"],
    },
  },
];

const AVAILABLE_PETS = [
  { name: "pixel-cat", style: "pixel-art", size: "32x32", default: true },
  { name: "pixel-dog", style: "pixel-art", size: "32x32", default: false },
  { name: "pixel-fox", style: "pixel-art", size: "32x32", default: false },
  { name: "pixel-owl", style: "pixel-art", size: "32x32", default: false },
];

let currentState = "idle";
let currentMessage = "";
let currentPet = "pixel-cat";

function handleToolCall(toolName, args) {
  switch (toolName) {
    case "set_pet_status": {
      const { status, message } = args;
      if (!PET_STATES[status]) {
        return { error: `Unknown status: ${status}` };
      }
      currentState = status;
      currentMessage = message || "";
      const state = PET_STATES[status];
      return {
        success: true,
        state: status,
        label: state.label,
        animation: state.animation,
        message: currentMessage,
        pet: currentPet,
      };
    }
    case "get_pet_status":
      return {
        state: currentState,
        label: PET_STATES[currentState].label,
        message: currentMessage,
        pet: currentPet,
        animation: PET_STATES[currentState].animation,
      };
    case "list_pets":
      return { pets: AVAILABLE_PETS };
    case "set_pet_character": {
      const pet = AVAILABLE_PETS.find((p) => p.name === args.character);
      if (!pet) return { error: `Unknown pet: ${args.character}` };
      currentPet = args.character;
      return { success: true, pet: currentPet };
    }
    default:
      return { error: `Unknown tool: ${toolName}` };
  }
}

function renderPetFrame(state, frameIndex, message) {
  const petState = PET_STATES[state];
  const frame = petState.frames[frameIndex % petState.frames.length];
  const statusBar = `[${petState.label}]`;
  const msgLine = message ? ` "${message}"` : "";
  return `  ${frame}  ${statusBar}${msgLine}`;
}

export {
  PET_STATES,
  MCP_TOOLS,
  AVAILABLE_PETS,
  handleToolCall,
  renderPetFrame,
};
