// Redis Array Playground — In-browser emulator of the Redis Array data type
// Emulates the commands from https://github.com/redis/redis/pull/15162

(function () {
  "use strict";

  // ── In-memory store ──────────────────────────────────────────────────
  const store = {}; // key → Array of strings

  function getArr(key) {
    if (!store[key]) return null;
    return store[key];
  }
  function ensureArr(key) {
    if (!store[key]) store[key] = [];
    return store[key];
  }

  // ── Command definitions ──────────────────────────────────────────────
  const COMMANDS = {
    ARSET: {
      desc: "Set one or more values at specific indices in an array.",
      params: [
        { name: "key", type: "text", required: true },
        { name: "index", type: "text", required: true, placeholder: "0" },
        { name: "value", type: "text", required: true },
      ],
      run(args) {
        const arr = ensureArr(args.key);
        const idx = parseInt(args.index, 10);
        if (isNaN(idx) || idx < 0) return err("ERR invalid index");
        while (arr.length <= idx) arr.push("");
        arr[idx] = args.value;
        return ok("OK");
      },
    },
    ARGET: {
      desc: "Get the value at a specific index in an array.",
      params: [
        { name: "key", type: "text", required: true },
        { name: "index", type: "text", required: true, placeholder: "0" },
      ],
      run(args) {
        const arr = getArr(args.key);
        if (!arr) return nil();
        const idx = parseInt(args.index, 10);
        if (isNaN(idx) || idx < 0 || idx >= arr.length) return nil();
        return ok(JSON.stringify(arr[idx]));
      },
    },
    ARLEN: {
      desc: "Return the number of elements in the array.",
      params: [{ name: "key", type: "text", required: true }],
      run(args) {
        const arr = getArr(args.key);
        return ok(`(integer) ${arr ? arr.length : 0}`);
      },
    },
    ARCOUNT: {
      desc: "Return the count of non-empty elements in the array.",
      params: [{ name: "key", type: "text", required: true }],
      run(args) {
        const arr = getArr(args.key);
        if (!arr) return ok("(integer) 0");
        return ok(`(integer) ${arr.filter((v) => v !== "").length}`);
      },
    },
    ARDEL: {
      desc: "Delete a value at a specific index (sets it to empty string).",
      params: [
        { name: "key", type: "text", required: true },
        { name: "index", type: "text", required: true, placeholder: "0" },
      ],
      run(args) {
        const arr = getArr(args.key);
        if (!arr) return ok("(integer) 0");
        const idx = parseInt(args.index, 10);
        if (isNaN(idx) || idx < 0 || idx >= arr.length) return ok("(integer) 0");
        arr[idx] = "";
        return ok("(integer) 1");
      },
    },
    ARDELRANGE: {
      desc: "Delete a range of elements from start to end index (inclusive).",
      params: [
        { name: "key", type: "text", required: true },
        { name: "start", type: "text", required: true, placeholder: "0" },
        { name: "end", type: "text", required: true, placeholder: "5" },
      ],
      run(args) {
        const arr = getArr(args.key);
        if (!arr) return ok("(integer) 0");
        const s = parseInt(args.start, 10),
          e = parseInt(args.end, 10);
        if (isNaN(s) || isNaN(e)) return err("ERR invalid range");
        let count = 0;
        for (let i = Math.max(0, s); i <= Math.min(e, arr.length - 1); i++) {
          if (arr[i] !== "") count++;
          arr[i] = "";
        }
        return ok(`(integer) ${count}`);
      },
    },
    ARGETRANGE: {
      desc: "Get a range of values from start to end index (inclusive).",
      params: [
        { name: "key", type: "text", required: true },
        { name: "start", type: "text", required: true, placeholder: "0" },
        { name: "end", type: "text", required: true, placeholder: "9" },
      ],
      run(args) {
        const arr = getArr(args.key);
        if (!arr) return ok("(empty array)");
        const s = parseInt(args.start, 10),
          e = parseInt(args.end, 10);
        const slice = arr.slice(Math.max(0, s), e + 1);
        return ok(formatList(slice));
      },
    },
    ARINSERT: {
      desc: "Insert a value at a specific index, shifting subsequent elements.",
      params: [
        { name: "key", type: "text", required: true },
        { name: "index", type: "text", required: true, placeholder: "0" },
        { name: "value", type: "text", required: true },
      ],
      run(args) {
        const arr = ensureArr(args.key);
        const idx = parseInt(args.index, 10);
        if (isNaN(idx) || idx < 0) return err("ERR invalid index");
        arr.splice(idx, 0, args.value);
        return ok(`(integer) ${arr.length}`);
      },
    },
    ARMSET: {
      desc: "Set multiple index-value pairs at once. Provide pairs as 'idx1 val1 idx2 val2 ...'.",
      params: [
        { name: "key", type: "text", required: true },
        { name: "pairs", type: "text", required: true, placeholder: "0 apple 1 banana 2 cherry" },
      ],
      run(args) {
        const arr = ensureArr(args.key);
        const parts = args.pairs.split(/\s+/);
        if (parts.length % 2 !== 0) return err("ERR odd number of arguments");
        for (let i = 0; i < parts.length; i += 2) {
          const idx = parseInt(parts[i], 10);
          if (isNaN(idx) || idx < 0) return err(`ERR invalid index '${parts[i]}'`);
          while (arr.length <= idx) arr.push("");
          arr[idx] = parts[i + 1];
        }
        return ok("OK");
      },
    },
    ARMGET: {
      desc: "Get values at multiple indices. Provide indices separated by spaces.",
      params: [
        { name: "key", type: "text", required: true },
        { name: "indices", type: "text", required: true, placeholder: "0 2 4" },
      ],
      run(args) {
        const arr = getArr(args.key);
        if (!arr) return ok("(empty array)");
        const idxs = args.indices.split(/\s+/).map(Number);
        const vals = idxs.map((i) => (i >= 0 && i < arr.length ? arr[i] : null));
        return ok(formatList(vals));
      },
    },
    ARINFO: {
      desc: "Return metadata about the array: length, count of non-empty, memory usage estimate.",
      params: [{ name: "key", type: "text", required: true }],
      run(args) {
        const arr = getArr(args.key);
        if (!arr) return nil();
        const count = arr.filter((v) => v !== "").length;
        const mem = arr.reduce((s, v) => s + v.length * 2 + 16, 64);
        return ok(
          `length: ${arr.length}\ncount: ${count}\nestimated-memory: ${mem} bytes`
        );
      },
    },
    ARLASTITEMS: {
      desc: "Return the last N non-empty items from the array.",
      params: [
        { name: "key", type: "text", required: true },
        { name: "count", type: "text", required: true, placeholder: "3" },
      ],
      run(args) {
        const arr = getArr(args.key);
        if (!arr) return ok("(empty array)");
        const n = parseInt(args.count, 10);
        const nonEmpty = arr.filter((v) => v !== "");
        return ok(formatList(nonEmpty.slice(-n)));
      },
    },
    ARNEXT: {
      desc: "Return the next non-empty value at or after the given index.",
      params: [
        { name: "key", type: "text", required: true },
        { name: "index", type: "text", required: true, placeholder: "0" },
      ],
      run(args) {
        const arr = getArr(args.key);
        if (!arr) return nil();
        const start = parseInt(args.index, 10);
        for (let i = Math.max(0, start); i < arr.length; i++) {
          if (arr[i] !== "") return ok(`${i}) ${JSON.stringify(arr[i])}`);
        }
        return nil();
      },
    },
    ARSEEK: {
      desc: "Find the first index of an exact value in the array.",
      params: [
        { name: "key", type: "text", required: true },
        { name: "value", type: "text", required: true },
      ],
      run(args) {
        const arr = getArr(args.key);
        if (!arr) return ok("(integer) -1");
        const idx = arr.indexOf(args.value);
        return ok(`(integer) ${idx}`);
      },
    },
    AROP: {
      desc: "Perform an arithmetic operation on a numeric value at an index. Ops: INCR, DECR, ADD, SUB, MUL.",
      params: [
        { name: "key", type: "text", required: true },
        { name: "index", type: "text", required: true, placeholder: "0" },
        { name: "op", type: "select", options: ["INCR", "DECR", "ADD", "SUB", "MUL"], required: true },
        { name: "operand", type: "text", required: false, placeholder: "(for ADD/SUB/MUL)" },
      ],
      run(args) {
        const arr = ensureArr(args.key);
        const idx = parseInt(args.index, 10);
        if (isNaN(idx) || idx < 0) return err("ERR invalid index");
        while (arr.length <= idx) arr.push("0");
        let val = parseFloat(arr[idx]) || 0;
        const operand = parseFloat(args.operand) || 0;
        switch (args.op) {
          case "INCR": val++; break;
          case "DECR": val--; break;
          case "ADD": val += operand; break;
          case "SUB": val -= operand; break;
          case "MUL": val *= operand; break;
        }
        arr[idx] = String(val);
        return ok(JSON.stringify(val));
      },
    },
    ARRING: {
      desc: "Treat the array as a ring buffer — append value, wrapping at max-length.",
      params: [
        { name: "key", type: "text", required: true },
        { name: "maxlen", type: "text", required: true, placeholder: "10" },
        { name: "value", type: "text", required: true },
      ],
      run(args) {
        const arr = ensureArr(args.key);
        const maxlen = parseInt(args.maxlen, 10);
        if (isNaN(maxlen) || maxlen < 1) return err("ERR invalid maxlen");
        arr.push(args.value);
        while (arr.length > maxlen) arr.shift();
        return ok(`(integer) ${arr.length}`);
      },
    },
    ARSCAN: {
      desc: "Scan the array for elements matching a glob-style pattern.",
      params: [
        { name: "key", type: "text", required: true },
        { name: "pattern", type: "text", required: true, placeholder: "*berry*" },
      ],
      flags: [{ name: "WITHVALUES", label: "WITHVALUES" }],
      run(args) {
        const arr = getArr(args.key);
        if (!arr) return ok("(empty array)");
        const re = globToRegex(args.pattern);
        const results = [];
        for (let i = 0; i < arr.length; i++) {
          if (arr[i] !== "" && re.test(arr[i])) {
            if (args.WITHVALUES) results.push(`${i}) ${JSON.stringify(arr[i])}`);
            else results.push(`${i}`);
          }
        }
        return ok(results.length ? results.join("\n") : "(empty array)");
      },
    },
    ARGREP: {
      desc: "Server-side grep: search array values using predicates (MATCH, PREFIX, SUFFIX, CONTAINS). Supports AND/OR logic, LIMIT, WITHVALUES, NOCASE.",
      params: [
        { name: "key", type: "text", required: true },
        { name: "predicate", type: "select", options: ["MATCH", "PREFIX", "SUFFIX", "CONTAINS"], required: true },
        { name: "pattern", type: "text", required: true, placeholder: "cherry" },
      ],
      flags: [
        { name: "AND", label: "AND (all predicates)" },
        { name: "OR", label: "OR (any predicate)" },
        { name: "LIMIT", label: "LIMIT", hasValue: true, placeholder: "10" },
        { name: "WITHVALUES", label: "WITHVALUES" },
        { name: "NOCASE", label: "NOCASE" },
      ],
      run(args) {
        const arr = getArr(args.key);
        if (!arr) return ok("(empty array)");
        const pattern = args.NOCASE ? args.pattern.toLowerCase() : args.pattern;
        const limit = args.LIMIT ? parseInt(args.LIMIT_val, 10) || Infinity : Infinity;
        const results = [];
        for (let i = 0; i < arr.length && results.length < limit; i++) {
          if (arr[i] === "") continue;
          const val = args.NOCASE ? arr[i].toLowerCase() : arr[i];
          let match = false;
          switch (args.predicate) {
            case "MATCH": match = val === pattern; break;
            case "PREFIX": match = val.startsWith(pattern); break;
            case "SUFFIX": match = val.endsWith(pattern); break;
            case "CONTAINS": match = val.includes(pattern); break;
          }
          if (match) {
            if (args.WITHVALUES) results.push(`${i}) ${JSON.stringify(arr[i])}`);
            else results.push(`${i}`);
          }
        }
        return ok(results.length ? results.join("\n") : "(empty array)");
      },
    },
  };

  // ── Helpers ──────────────────────────────────────────────────────────
  function ok(msg) { return { type: "ok", text: msg }; }
  function err(msg) { return { type: "err", text: msg }; }
  function nil() { return { type: "ok", text: "(nil)" }; }

  function formatList(arr) {
    if (!arr.length) return "(empty array)";
    return arr.map((v, i) => `${i + 1}) ${v === null || v === "" ? "(nil)" : JSON.stringify(v)}`).join("\n");
  }

  function globToRegex(glob) {
    const escaped = glob.replace(/[.+^${}()|[\]\\]/g, "\\$&");
    const re = escaped.replace(/\*/g, ".*").replace(/\?/g, ".");
    return new RegExp(`^${re}$`, "i");
  }

  // ── UI Rendering ────────────────────────────────────────────────────
  const sidebar = document.getElementById("sidebar");
  const fieldsEl = document.getElementById("fields");
  const cmdTitle = document.getElementById("cmd-title");
  const cmdDesc = document.getElementById("cmd-desc");
  const preview = document.getElementById("command-preview");
  const reply = document.getElementById("reply");

  let activeCmd = null;

  // Build sidebar buttons
  for (const name of Object.keys(COMMANDS)) {
    const btn = document.createElement("button");
    btn.className = "cmd-btn";
    btn.textContent = name;
    btn.addEventListener("click", () => selectCommand(name));
    sidebar.appendChild(btn);
  }

  function selectCommand(name) {
    activeCmd = name;
    const cmd = COMMANDS[name];
    // Update sidebar active state
    sidebar.querySelectorAll(".cmd-btn").forEach((b) => b.classList.toggle("active", b.textContent === name));
    cmdTitle.textContent = name;
    cmdDesc.textContent = cmd.desc;
    fieldsEl.innerHTML = "";

    // Render parameter fields
    for (const p of cmd.params) {
      const div = document.createElement("div");
      div.className = "field";
      const label = document.createElement("label");
      label.textContent = p.name;
      div.appendChild(label);

      if (p.type === "select") {
        const sel = document.createElement("select");
        sel.id = `param-${p.name}`;
        for (const opt of p.options) {
          const o = document.createElement("option");
          o.value = opt;
          o.textContent = opt;
          sel.appendChild(o);
        }
        sel.addEventListener("change", updatePreview);
        div.appendChild(sel);
      } else {
        const inp = document.createElement("input");
        inp.type = "text";
        inp.id = `param-${p.name}`;
        inp.placeholder = p.placeholder || p.name;
        inp.addEventListener("input", updatePreview);
        div.appendChild(inp);
      }
      fieldsEl.appendChild(div);
    }

    // Render flags
    if (cmd.flags && cmd.flags.length) {
      const wrap = document.createElement("div");
      wrap.className = "field";
      const label = document.createElement("label");
      label.textContent = "flags";
      wrap.appendChild(label);
      const flagsDiv = document.createElement("div");
      flagsDiv.className = "flags";
      for (const f of cmd.flags) {
        const fl = document.createElement("label");
        const cb = document.createElement("input");
        cb.type = "checkbox";
        cb.id = `flag-${f.name}`;
        cb.addEventListener("change", updatePreview);
        fl.appendChild(cb);
        fl.appendChild(document.createTextNode(f.label));
        flagsDiv.appendChild(fl);
        if (f.hasValue) {
          const vi = document.createElement("input");
          vi.type = "text";
          vi.id = `flagval-${f.name}`;
          vi.placeholder = f.placeholder || "";
          vi.style.width = "60px";
          vi.addEventListener("input", updatePreview);
          flagsDiv.appendChild(vi);
        }
      }
      wrap.appendChild(flagsDiv);
      fieldsEl.appendChild(wrap);
    }
    updatePreview();
  }

  function collectArgs() {
    if (!activeCmd) return null;
    const cmd = COMMANDS[activeCmd];
    const args = {};
    for (const p of cmd.params) {
      const el = document.getElementById(`param-${p.name}`);
      args[p.name] = el ? el.value : "";
    }
    if (cmd.flags) {
      for (const f of cmd.flags) {
        const cb = document.getElementById(`flag-${f.name}`);
        args[f.name] = cb ? cb.checked : false;
        if (f.hasValue) {
          const vi = document.getElementById(`flagval-${f.name}`);
          args[`${f.name}_val`] = vi ? vi.value : "";
        }
      }
    }
    return args;
  }

  function buildCommandString() {
    if (!activeCmd) return "...";
    const cmd = COMMANDS[activeCmd];
    const args = collectArgs();
    const parts = [activeCmd];
    for (const p of cmd.params) {
      const v = args[p.name];
      if (v) parts.push(v.includes(" ") ? `"${v}"` : v);
    }
    if (cmd.flags) {
      for (const f of cmd.flags) {
        if (args[f.name]) {
          parts.push(f.name);
          if (f.hasValue && args[`${f.name}_val`]) parts.push(args[`${f.name}_val`]);
        }
      }
    }
    return parts.join(" ");
  }

  function updatePreview() {
    preview.textContent = buildCommandString();
  }

  // ── Execution ───────────────────────────────────────────────────────
  function runCommand() {
    if (!activeCmd) {
      appendReply("Select a command first.", "err");
      return;
    }
    const args = collectArgs();
    const cmd = COMMANDS[activeCmd];

    // Validate required params
    for (const p of cmd.params) {
      if (p.required && !args[p.name]) {
        appendReply(`ERR missing required parameter: ${p.name}`, "err");
        return;
      }
    }

    const cmdStr = buildCommandString();
    appendReply(`> ${cmdStr}`, "info");
    const result = cmd.run(args);
    appendReply(result.text, result.type === "err" ? "err" : "ok");
  }

  function appendReply(text, cls) {
    const span = document.createElement("div");
    span.className = `reply-${cls}`;
    span.textContent = text;
    reply.appendChild(span);
    reply.scrollTop = reply.scrollHeight;
  }

  function loadSampleData() {
    store["fruits"] = [
      "apple", "banana", "cherry", "date", "elderberry",
      "fig", "grape", "honeydew", "kiwi", "lemon",
      "mango", "nectarine", "orange", "papaya", "quince",
      "raspberry", "strawberry", "tangerine", "ugli", "watermelon",
    ];
    store["scores"] = ["100", "85", "92", "78", "95", "88", "91", "76", "83", "97"];
    store["cities"] = [
      "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
      "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
    ];
    appendReply("> [loaded sample data]", "info");
    appendReply('Created arrays: "fruits" (20 items), "scores" (10 items), "cities" (10 items)', "ok");
  }

  // ── Event bindings ──────────────────────────────────────────────────
  document.getElementById("run-btn").addEventListener("click", runCommand);
  document.getElementById("seed-btn").addEventListener("click", loadSampleData);
  document.getElementById("clear-btn").addEventListener("click", () => {
    reply.innerHTML = '<span class="reply-info">Output cleared.</span>';
  });

  // Keyboard shortcut: Enter to run
  document.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && e.ctrlKey) runCommand();
  });

  // Auto-select first command
  selectCommand("ARSET");
})();
