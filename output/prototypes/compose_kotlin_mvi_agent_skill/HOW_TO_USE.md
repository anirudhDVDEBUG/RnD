# How to Use

## Option A: Install as a Claude Code Skill

### 1. Clone the skill

```bash
git clone https://github.com/haidrrrry/compose-kotlin-agent-skills.git
```

### 2. Copy to your Claude skills directory

```bash
mkdir -p ~/.claude/skills/compose-kotlin-mvi
cp compose-kotlin-agent-skills/SKILL.md ~/.claude/skills/compose-kotlin-mvi/SKILL.md
```

### 3. Trigger phrases

The skill activates automatically when you ask Claude Code to:

- "Create a new Compose screen with MVI architecture"
- "Scaffold a Kotlin Android feature module"
- "Set up a Compose Multiplatform shared UI component"
- "Write a ViewModel with unidirectional data flow"
- "Add a new feature following clean architecture with Hilt DI"

Any prompt involving Jetpack Compose UI, Kotlin Android features, or MVI/MVVM patterns will trigger it.

### 4. What happens when triggered

Claude Code will generate feature modules that strictly follow:

- **MVI pattern**: State (immutable data class) + Intent (sealed interface) + SideEffect (sealed interface) + ViewModel + Stateless Composable
- **Kotlin 2.x**: `sealed interface` over `sealed class`, `data object` for singletons, `value class` for wrappers
- **Compose 2026**: `collectAsStateWithLifecycle()`, `@PreviewLightDark`, Material 3, `LazyColumn` for lists
- **Hilt DI**: `@HiltViewModel`, `@Inject constructor`, proper scoping
- **Clean Architecture**: domain/data/presentation layer separation

## Option B: Run the Demo Generator

This prototype includes a Python scaffold generator that shows exactly what the skill produces.

### Prerequisites

- Python 3.10+

### Install & Run

```bash
git clone <this-repo>
cd compose_kotlin_mvi_agent_skill
bash run.sh
```

No external dependencies or API keys required.

### First 60 Seconds

**Input:** Run `bash run.sh`

**Output:** The generator scaffolds two complete feature modules (`TaskList` and `UserProfile`) into `generated_output/`, printing each file created and running validation checks:

```
=== Generating feature: TaskList ===
    Package: com.example.taskapp.task_list

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

Then it prints the full `TaskListViewModel.kt` source so you can see the actual generated Kotlin code — complete with `@HiltViewModel`, `MutableStateFlow`, `Channel<SideEffect>`, and the `onIntent()` dispatch pattern.

Browse `generated_output/` afterward to inspect the full feature tree.

## Verification

After running, check that:

1. `generated_output/task_list/presentation/` has 5 files (State, Intent, SideEffect, ViewModel, Screen)
2. `generated_output/task_list/domain/repository/` has the interface
3. `generated_output/task_list/data/repository/` has the implementation
4. `generated_output/task_list/di/` has the Hilt module
5. All validation checks show `[OK]`
