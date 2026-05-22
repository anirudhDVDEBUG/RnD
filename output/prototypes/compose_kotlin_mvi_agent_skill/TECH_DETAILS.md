# Technical Details

## What It Does

The Compose Kotlin MVI Agent Skill is a `.SKILL.md` file that instructs Claude Code (and 27+ other AI agents) to enforce strict MVI (Model-View-Intent) architecture when generating Jetpack Compose and Kotlin Android code. It is not a library or runtime dependency — it is a prompt-engineering artifact that shapes how AI agents write Android code.

When triggered, the skill ensures every feature follows unidirectional data flow: a single immutable `State` data class, a `sealed interface` of `Intent`s for user actions, a `sealed interface` of `SideEffect`s for one-shot events, a `@HiltViewModel` that processes intents and emits state updates, and a stateless `@Composable` screen that receives state and emits intents. The skill also enforces Kotlin 2.x K2 compiler conventions (sealed interfaces over sealed classes, data objects, value classes) and 2026 Compose best practices (lifecycle-aware collection, Material 3, preview annotations).

## Architecture

### Skill File

The core is a single `SKILL.md` markdown file. It contains:

- **Trigger conditions** — when the skill activates (Compose UI, Kotlin Android, MVI patterns)
- **MVI contract** — the 5-part structure every feature must follow
- **Kotlin 2.x rules** — K2 compiler conventions
- **Compose conventions** — lifecycle-aware state, previews, Material 3
- **DI patterns** — Hilt annotations and scoping
- **Project structure** — directory layout for clean architecture
- **CI checklist** — validation rules for generated code

### Demo Generator (`mvi_scaffold.py`)

The Python generator in this repo demonstrates the skill's output:

```
mvi_scaffold.py
  ├── FeatureConfig          # Input: feature name, package
  ├── Templates (8)          # Kotlin source templates with MVI pattern
  ├── generate_feature()     # Renders templates → .kt files
  └── validate_feature()     # CI checks: immutability, no Context, previews
```

**Data flow:** `FeatureConfig` → template rendering → file writing → validation

**Dependencies:** Python 3.10+ stdlib only. No external packages.

### Generated Feature Structure

```
feature_name/
├── presentation/
│   ├── FeatureState.kt          # Immutable data class
│   ├── FeatureIntent.kt         # Sealed interface of user actions
│   ├── FeatureSideEffect.kt     # Sealed interface of one-shot events
│   ├── FeatureViewModel.kt      # @HiltViewModel processing intents
│   └── FeatureScreen.kt         # Stateless @Composable
├── domain/
│   └── repository/
│       └── FeatureRepository.kt # Interface (abstraction)
├── data/
│   └── repository/
│       └── FeatureRepositoryImpl.kt  # Implementation
└── di/
    └── FeatureModule.kt         # Hilt @Module binding
```

## Limitations

- **Not a library.** This is a prompt/skill file — it shapes AI output but does not execute at runtime. The generated code requires a standard Android project with Compose, Hilt, and coroutines dependencies.
- **No Compose Multiplatform templates yet.** The current templates target Android-only (Hilt, `hiltViewModel()`). CMP would need `expect`/`actual` patterns and Koin/Kodein instead of Hilt.
- **No Room/Retrofit templates.** The data layer stubs are minimal. A production setup would add DAO, entity, API, and DTO templates.
- **Single-module only.** Does not generate Gradle module configs, `build.gradle.kts`, or multi-module dependency graphs.
- **Validation is structural, not semantic.** The CI checks look for patterns (`var`, `Context`, `@Preview`) but cannot verify actual Compose correctness or type safety.

## Why It Matters

For teams building Claude-driven products:

- **Agent Factories:** If you're building systems that spawn specialized coding agents, this skill shows how a single markdown file can enforce complex architectural patterns across any AI agent. The pattern applies beyond Android — you could write equivalent skills for SwiftUI, Flutter, or React.
- **Code Quality at Scale:** When AI agents write most of your feature code, skills like this replace style guides and code review checklists. The MVI contract becomes a verifiable constraint rather than a suggestion.
- **Rapid Prototyping:** For marketing/lead-gen apps that need Android frontends, this skill lets a single developer scaffold production-quality features in minutes — each with consistent architecture, DI, and testing hooks.
- **CI Integration:** The validation checklist (immutable state, no Context in ViewModels, preview coverage) translates directly into linter rules or CI checks, closing the loop between AI-generated code and automated quality gates.

## References

- Source: [haidrrrry/compose-kotlin-agent-skills](https://github.com/haidrrrry/compose-kotlin-agent-skills)
- [Jetpack Compose docs](https://developer.android.com/jetpack/compose)
- [Kotlin K2 migration guide](https://kotlinlang.org/docs/k2-compiler-migration-guide.html)
- [Android architecture guide](https://developer.android.com/topic/architecture)
