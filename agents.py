"""One headless agent run, in the harness you pick. The loop does not care which.

    RUNNER=claude python3 loop.py ...    # Claude Code (the default)
    RUNNER=codex  python3 loop.py ...    # OpenAI Codex CLI
    RUNNER=hermes python3 loop.py ...    # Hermes Agent (open source; any model it is set up for)

Every runner writes its trace in one shape (Claude Code's stream-json), so the scorer,
the walls, `loop.py trace` and the optimizer read a Codex or Hermes run the same way.
The tool's own log is kept next to it as `<name>.raw.jsonl`.

Two roles:
    brief      runs in harness/. Shell and files. Writes nothing but scratch/.
    optimizer  runs in optimizer/. Reads the traces, edits harness/.

What each runner can fence, and what only the walls in loop.py catch:

    claude   permissions file: only `python3 tools/*`, edits only in scratch/
    codex    sandbox: writes only inside its folder (plus harness/ for the optimizer)
    hermes   no fence. It may run any command. The walls throw the run away afterwards.
"""
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HARNESS = ROOT / "harness"
RUNNER = os.environ.get("RUNNER", "claude").lower()
MAX_TURNS = 40
TIMEOUT = 1200

DEFAULT_MODELS = {             # (briefing agent, optimizer); None = the tool's own default
    "claude": ("sonnet", "opus"),
    "codex": (None, None),
    "hermes": (None, None),
}
if RUNNER not in DEFAULT_MODELS:
    raise SystemExit(f"RUNNER={RUNNER}? Use claude, codex or hermes.")
BRIEF_MODEL = os.environ.get("BRIEF_MODEL") or DEFAULT_MODELS[RUNNER][0]
OPT_MODEL = os.environ.get("OPT_MODEL") or DEFAULT_MODELS[RUNNER][1]


def run(role, prompt, cwd, trace, model=None, harness=HARNESS):
    """Run one agent to the end. Returns the final result event: result, num_turns, usage, cost."""
    trace = Path(trace)
    trace.parent.mkdir(parents=True, exist_ok=True)
    fn = {"claude": _claude, "codex": _codex, "hermes": _hermes}[RUNNER]
    try:
        fn(role, prompt, Path(cwd), trace, model, Path(harness))
    except subprocess.TimeoutExpired:
        with open(trace, "a") as f:
            f.write(json.dumps({"type": "result", "result": "", "num_turns": 0,
                                "error": f"timed out after {TIMEOUT}s"}) + "\n")
    result = {}
    for e in events(trace):
        if e.get("type") == "result":
            result = e
    why = unreached(result, trace)
    if why:
        raise NoModel(f"The {RUNNER} run could not reach its model: {why}\n"
                      f"Nothing was scored. Usually the network is blocked (an agent running loop.py\n"
                      f"for you inside its sandbox, as Codex's does) or a login has ended.\n"
                      f"Run the same command in your own terminal. Trace: {_rel(trace)}")
    return result


def _rel(path):
    try:
        return Path(path).resolve().relative_to(ROOT.resolve())
    except ValueError:
        return path


class NoModel(SystemExit):
    """A run that never reached its model. Scoring it would record a 0 that is not the setup's.
    A SystemExit, so any command stops with the message alone, from a worker thread too."""


def unreached(result, trace):
    """Why a run never reached its model, or '' if it did. Such a run made no tool call and used
    no tokens, and either says it failed (Claude Code: "Not logged in") or wrote nothing (Codex:
    "workspace routing discovery failed" in its own log). A timeout is a real run: it scores 0."""
    if result.get("error") or tokens(result) or any(True for _ in tool_inputs(trace)):
        return ""
    text = (result.get("result") or "").strip()
    if not result.get("is_error") and text:
        return ""
    raw = Path(trace).with_suffix(".raw.jsonl")
    said = [e.get("message") or (e.get("error") or {}).get("message")
            for e in (events(raw) if raw.exists() else [])
            if e.get("type") in ("error", "turn.failed")]
    said = [s for s in said if s]
    return text or (said[-1] if said else "it wrote nothing and used no tokens")


# ---------------------------------------------------------------- reading a trace

def events(trace):
    for line in open(trace):
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            pass


def tool_inputs(trace):
    for e in events(trace):
        if e.get("type") == "assistant":
            for c in e["message"].get("content", []):
                if c.get("type") == "tool_use":
                    yield c["name"], json.dumps(c.get("input", {}))


def tokens(result):
    u = result.get("usage", {})
    return (u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0)
            + u.get("cache_creation_input_tokens", 0) + u.get("output_tokens", 0))


# ---------------------------------------------------------------- Claude Code

def _claude(role, prompt, cwd, trace, model, harness):
    cmd = ["claude", "-p", prompt, "--model", model or "sonnet",
           "--output-format", "stream-json", "--verbose",
           "--setting-sources", "",             # nothing loaded by itself, trusted folder or not:
           "--append-system-prompt", setup_text(Path(cwd), Path(harness)),   # the setup, always
           "--settings", str(HARNESS / ".claude" / "settings.json"),
           "--strict-mcp-config",               # no connectors
           "--permission-mode", "dontAsk",      # anything not allowed is refused
           "--no-session-persistence", "--max-turns", str(MAX_TURNS)]
    if role == "brief":
        cmd += ["--tools", "Bash,Read,Write,Edit,Skill"]
    else:
        h, t, o = harness.as_posix(), (ROOT / "traces").as_posix(), (ROOT / "optimizer").as_posix()
        cmd += ["--tools", "Read,Grep,Glob,Edit,Write",
                "--add-dir", h, t,
                "--allowedTools", f"Read(/{h}/**)", f"Read(/{t}/**)",
                f"Edit(/{h}/**)", f"Edit(/{o}/proposals.md)",
                "--disallowedTools", f"Edit(/{h}/.claude/settings.json)"]
    with open(trace, "w") as out:
        subprocess.run(cmd, cwd=cwd, stdout=out, stderr=subprocess.DEVNULL,
                       stdin=subprocess.DEVNULL, timeout=TIMEOUT)


# ---------------------------------------------------------------- Codex and Hermes read the same file

def setup_text(cwd, harness):
    """The folder's CLAUDE.md with its @imports filled in, and the skills it holds.

    Every runner gets this text explicitly. Claude Code would load CLAUDE.md by itself only in a
    folder you have trusted, so a loop started from a fresh clone ran with no instructions at all.
    One file stays the source for all three tools, so the optimizer's changes reach every runner.
    (Using Codex or Hermes by hand instead? Copy CLAUDE.md to AGENTS.md.)
    """
    def expand(text, base):
        return re.sub(r"(?m)^@(\S+)\s*$",
                      lambda m: (base / m.group(1)).read_text() if (base / m.group(1)).exists() else "",
                      text)
    text = expand((cwd / "CLAUDE.md").read_text(), cwd)
    skills = sorted((harness / ".claude" / "skills").glob("*/SKILL.md")) if cwd == harness else []
    if skills:
        text += "\n\n## Skills in this folder\n\nRead one when it fits the job:\n"
        for s in skills:
            desc = re.search(r"(?m)^description:\s*(.+)$", s.read_text())
            text += f"- `{s.relative_to(harness)}`: {desc.group(1) if desc else ''}\n"
    return f"# Your instructions (CLAUDE.md in {cwd.name}/)\n\n{text}"


def instructions(cwd, prompt, harness):
    """Codex and Hermes get the setup at the top of the prompt."""
    return f"{setup_text(cwd, harness)}\n\n---\n\nWork in {cwd}. Your task:\n\n{prompt}"


def _add(out, kind, **body):
    if kind == "text":
        out.append({"type": "assistant", "message": {"content": [{"type": "text", "text": body["text"]}]}})
    elif kind == "tool":
        out.append({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": body["name"], "input": body["input"]}]}})
        out.append({"type": "user", "message": {"content": [
            {"type": "tool_result", "content": body.get("output", "")}]}})


def _write(trace, out):
    with open(trace, "w") as f:
        for e in out:
            f.write(json.dumps(e) + "\n")


# ---------------------------------------------------------------- Codex

def _codex_home():
    """A Codex home with your login and nothing else, so your own AGENTS.md and config stay out.

    Like `--setting-sources ""` for Claude Code."""
    home = ROOT / ".runner" / "codex-home"
    home.mkdir(parents=True, exist_ok=True)
    real = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    link = home / "auth.json"
    if not link.exists() and (real / "auth.json").exists():
        link.symlink_to(real / "auth.json")
    return home, real


def _codex_default_model(real):
    cfg = real / "config.toml"
    m = re.search(r'(?m)^model\s*=\s*"([^"]+)"', cfg.read_text()) if cfg.exists() else None
    return m.group(1) if m else None


def _codex(role, prompt, cwd, trace, model, harness):
    home, real = _codex_home()
    model = model or _codex_default_model(real)
    cmd = ["codex", "exec", "--json", "--ephemeral", "--skip-git-repo-check",
           "-s", "workspace-write", "-C", str(cwd)]
    if model:
        cmd += ["-m", model]
    if role == "brief":
        cmd += ["-c", "sandbox_workspace_write.network_access=true"]   # tools/fetch.py reads links
    else:
        cmd += ["--add-dir", str(harness)]
    cmd.append(instructions(cwd, prompt, harness))
    raw = trace.with_suffix(".raw.jsonl")
    with open(raw, "w") as f:
        subprocess.run(cmd, cwd=cwd, stdout=f, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       timeout=TIMEOUT, env=dict(os.environ, CODEX_HOME=str(home)))

    out, text, steps, usage = [], "", 0, {}
    for e in events(raw):
        item = e.get("item") or {}
        kind = item.get("type")
        if e.get("type") == "item.completed" and kind == "agent_message":
            text = item.get("text", "")
            _add(out, "text", text=text)
        elif e.get("type") == "item.completed" and kind == "command_execution":
            steps += 1
            cmd_s = item.get("command", "")
            inner = re.match(r"""^/bin/\w+ -lc (['"])(.*)\1$""", cmd_s, re.S)
            _add(out, "tool", name="Bash", input={"command": inner.group(2) if inner else cmd_s},
                 output=item.get("aggregated_output", ""))
        elif e.get("type") == "item.completed" and kind == "file_change":
            steps += 1
            for ch in item.get("changes", []):
                _add(out, "tool", name="Edit", input={"file_path": ch.get("path"), "kind": ch.get("kind")},
                     output=item.get("status", ""))
        elif e.get("type") == "item.completed" and kind in ("mcp_tool_call", "web_search"):
            steps += 1
            _add(out, "tool", name=kind, input={k: v for k, v in item.items() if k not in ("id", "type")})
        elif e.get("type") == "turn.completed":
            u = e.get("usage", {})
            cached = u.get("cached_input_tokens", 0)
            usage = {"input_tokens": u.get("input_tokens", 0) - cached,
                     "cache_read_input_tokens": cached,
                     "output_tokens": u.get("output_tokens", 0)}
    out.append({"type": "result", "result": text, "num_turns": steps, "usage": usage,
                "runner": "codex", "model": model})
    _write(trace, out)


# ---------------------------------------------------------------- Hermes

HERMES_TOOLS = {"terminal": "Bash", "read_file": "Read", "write_file": "Write",
                "patch": "Edit", "search_files": "Grep"}


def _unwrap(output):
    """Hermes wraps terminal results as {"output": "...", "exit_code": 0}, and cuts long ones
    at 5,000 characters in its stream (the model itself saw them whole)."""
    if not isinstance(output, str) or not output.startswith('{"output": "'):
        return output
    try:
        return json.loads(output)["output"]
    except ValueError:
        body = output[len('{"output": "'):].rstrip(".").rstrip("\\")
        try:
            return json.loads(f'"{body}"') + " ...(cut by Hermes)"
        except ValueError:
            return output


def _hermes_home():
    """A Hermes home with your login and your model choice, and nothing else.

    Hermes guards CLAUDE.md and AGENTS.md: a write to one needs a person to approve it, every
    time. That is right for your own setup, but the optimizer's whole job is to edit
    harness/CLAUDE.md, with plain code checking it afterwards. So this home, and only this
    home, turns the guard off. Your ~/.hermes is not changed."""
    real = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
    home = ROOT / ".runner" / "hermes-home"
    home.mkdir(parents=True, exist_ok=True)
    for name in (".env", "auth.json"):
        if (real / name).exists() and not (home / name).exists():
            (home / name).symlink_to(real / name)
    model = ""
    if (real / "config.yaml").exists():      # copy only your model block
        m = re.search(r"(?m)^model:\n(?:[ \t]+.*\n?)+", (real / "config.yaml").read_text())
        model = m.group(0) if m else ""
    (home / "config.yaml").write_text(
        model.rstrip("\n") + "\nmemory:\n  memory_enabled: false\n"
        "security:\n  protected_instruction_files: false\n")
    return home


def _hermes(role, prompt, cwd, trace, model, harness):
    cmd = ["hermes", "chat", "-q", instructions(cwd, prompt, harness), "--format", "stream-json",
           # the briefing agent gets a shell and files; the optimizer files only, as in Claude Code
           "-t", "terminal,file" if role == "brief" else "file",
           "--ignore-rules",               # no AGENTS.md, SOUL.md, memory or skills from your setup
           "--max-turns", str(MAX_TURNS), "--source", "tool"]
    if model:
        cmd += ["-m", model]
    if os.environ.get("HERMES_PROVIDER"):
        cmd += ["--provider", os.environ["HERMES_PROVIDER"]]
    raw = trace.with_suffix(".raw.jsonl")
    with open(raw, "w") as f:
        subprocess.run(cmd, cwd=cwd, stdout=f, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       timeout=TIMEOUT, env=dict(os.environ, HERMES_HOME=str(_hermes_home())))

    return _hermes_trace(raw, trace, model)


def _hermes_trace(raw, trace, model=""):
    """Hermes's stream-json, rewritten in the shape every other trace has."""
    out, text, steps, usage, pending, said = [], "", 0, {}, [], ""

    def flush():          # Hermes streams its words in pieces; the trace keeps one block per turn
        nonlocal said
        if said.strip():
            _add(out, "text", text=said.strip())
        said = ""

    for e in events(raw):
        t = e.get("type")
        if t == "text":
            said += e.get("text", "")
        elif t == "tool_use":
            flush()
            steps += 1
            inp = dict(e.get("input") or {})
            if "path" in inp:
                inp["file_path"] = inp.pop("path")
            # Hermes often makes several calls at once and then returns their results in order,
            # with no ids. Queue the calls; give each result to the oldest call of the same tool.
            pending.append((e.get("name"), HERMES_TOOLS.get(e.get("name"), e.get("name")), inp))
        elif t == "tool_result" and pending:
            i = next((k for k, p in enumerate(pending) if p[0] == e.get("name")), 0)
            _, name, inp = pending.pop(i)
            _add(out, "tool", name=name, input=inp, output=_unwrap(e.get("output", "")))
        elif t == "result":
            text = e.get("text", "")
            tk = e.get("tokens", {})
            usage = {"input_tokens": tk.get("input", 0), "cache_read_input_tokens": tk.get("cache_read", 0),
                     "cache_creation_input_tokens": tk.get("cache_write", 0),
                     "output_tokens": tk.get("output", 0)}
    flush()
    for _, name, inp in pending:        # calls that never got a result still count for the walls
        _add(out, "tool", name=name, input=inp)
    out.append({"type": "result", "result": text, "num_turns": steps, "usage": usage,
                "runner": "hermes", "model": model})
    _write(trace, out)
