# Global Claude Configuration
## Everything-Claude-Code Complete Setup

### Token Efficiency Rules

1. **Be Concise**: Use brief responses. Avoid preamble and unnecessary explanations.
2. **Context Awareness**: Reference previous context without restating.
3. **Progressive Disclosure**: Load details only when needed.
4. **Pattern Caching**: Reuse established patterns without re-explaining.

### Response Guidelines

- Start with direct answer/action
- Use bullet points over paragraphs
- Skip "Let me..." intros unless complex
- No trailing summaries unless asked
- Code-first explanations only when unclear

### Memory Management

- Auto-compact at 70% context threshold
- Persist key decisions to memory files
- Use file paths for navigation, not explanations
- Trust internal state, don't re-verify constantly

### Hook Integration

This configuration uses everything-claude-code hooks:
- Pre-read optimization (warns on large files)
- Post-edit lightweight verification
- Strategic context compaction
- Memory persistence across sessions

### Model Selection

- Default: Claude Sonnet 4.6 (balanced)
- Subagents: Claude Haiku 4.5 (token-efficient)
- Thinking tokens limited to 10,000
- Compaction triggered at 50% (aggressive)

### Agents Available

- **planner** — Feature implementation planning
- **code-reviewer** — Quality and security review
- **security-reviewer** — Vulnerability analysis
- **loop-operator** — Autonomous execution
- **chief-of-staff** — Communication triage
- **doc-updater** — Documentation sync

### Skills Available

- **continuous-learning** — Pattern extraction
- **strategic-compact** — Manual compaction
- **verification-loop** — Checkpoint validation

### Slash Commands

- `/plan` — Implementation planning
- `/code-review` — Quality review
- `/learn [pattern]` — Extract pattern
- `/checkpoint` — Save state

### Contexts

- **dev** — Development mode
- **research** — Exploration mode

### Rules

- See `/home/wls/.claude/rules/common/` for coding style, security, etc.
