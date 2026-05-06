#!/usr/bin/env node
// Hook: on_session_start — wakes the pet when a Claude Code session begins.
import { PetClient } from "../src/pet-client.js";

const pet = new PetClient();
await pet.updateStatus("waking", "Claude Code session started — pet is awake!");
