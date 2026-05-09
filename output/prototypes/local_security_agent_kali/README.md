# Local Security Agent on Kali Linux

An autonomous security-testing agent powered by a locally-hosted Qwen 2.5-7B model via LM Studio. It runs a plan-act-observe loop — the LLM decides which Kali tools to run (nmap, nikto, searchsploit), executes them, and synthesizes findings. Everything runs offline; no data leaves your machine.

**Headline result:** Agent autonomously discovers 3 open ports, identifies a vulnerable Apache 2.4.49, and recommends patching — zero cloud API calls.

```
$ bash run.sh

[Step 1] Querying LLM for next action...
  -> Running: nmap_scan(target='192.168.1.100', flags='-sV -sC -T4')
[Step 2] Querying LLM for next action...
  -> Running: nikto_scan(target='192.168.1.100', port='80')
[Step 3] Querying LLM for next action...
  -> Running: searchsploit(query='Apache 2.4.49')

  AGENT COMPLETE
Summary:
Target has 3 open ports. Apache 2.4.49 vulnerable to CVE-2021-41773.
```

See [HOW_TO_USE.md](HOW_TO_USE.md) for setup and [TECH_DETAILS.md](TECH_DETAILS.md) for architecture.
