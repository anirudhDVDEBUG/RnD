#!/usr/bin/env node
// Hook: on_session_end — puts the pet to sleep when the session ends.
import { PetClient } from "../src/pet-client.js";

const pet = new PetClient();
await pet.updateStatus("goodbye", "Claude Code session ended — pet waves goodbye!");
await pet.updateStatus("sleeping", "Pet goes back to sleep...");
