# Compose Kotlin MVI Agent Skill — Demo

**TL;DR:** A Claude Code skill that enforces strict MVI architecture, Kotlin 2.x K2 conventions, and 2026 Compose best practices whenever you scaffold Android features. This demo generates a complete feature module and validates it against the skill's CI checklist.

## Headline Result

```
--- Generating feature: TaskList ---
    [+] task_list/presentation/TaskListState.kt
    [+] task_list/presentation/TaskListIntent.kt
    [+] task_list/presentation/TaskListSideEffect.kt
    [+] task_list/presentation/TaskListViewModel.kt
    [+] task_list/presentation/TaskListScreen.kt
    [+] task_list/domain/repository/TaskListRepository.kt
    [+] task_list/data/repository/TaskListRepositoryImpl.kt
    [+] task_list/di/TaskListModule.kt
    [OK] All CI validation checks passed
```

One command scaffolds 8 production-ready Kotlin files per feature, all following unidirectional data flow with immutable state, sealed interfaces, and Hilt DI.

## Quick Links

- [HOW_TO_USE.md](HOW_TO_USE.md) — Install the skill, trigger phrases, run the demo
- [TECH_DETAILS.md](TECH_DETAILS.md) — Architecture, data flow, limitations
- Source: [haidrrrry/compose-kotlin-agent-skills](https://github.com/haidrrrry/compose-kotlin-agent-skills)
