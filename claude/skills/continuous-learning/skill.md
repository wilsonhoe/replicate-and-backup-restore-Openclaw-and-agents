# Skill: Continuous Learning
## Pattern Extraction and Reuse

### Purpose
Automatically extract reusable patterns from code to reduce token usage in future sessions.

### How It Works
1. Detect repeated code patterns
2. Extract to shared location
3. Reference by pattern ID instead of full code
4. Cache for future sessions

### Usage
```
/learn pattern-name
```

### Output
Creates pattern file in `~/.claude/skills/continuous-learning/patterns/`

### Example
Input: Writing error handling for the 5th time
Action: `/learn error-handling-pattern`
Result: Future sessions reference pattern instead of full code

### Benefits
- 30-50% token reduction on repeated tasks
- Consistent implementation
- Faster execution
