---
name: Compose Kotlin MVI Agent Skill
description: |
  Enforces strict Jetpack Compose & Kotlin best practices with MVI architecture for Android development.
  TRIGGER: When writing Jetpack Compose UI code, Kotlin Android features, MVI/MVVM architecture,
  Compose Multiplatform modules, or scaffolding new Android screens/features.
---

# Compose & Kotlin MVI Agent Skill

Enforce modern Jetpack Compose and Kotlin conventions with strict MVI architecture, Kotlin 2.x K2 compiler patterns, and 2026 Compose best practices across Android and Compose Multiplatform projects.

## When to use

- "Create a new Compose screen with MVI architecture"
- "Scaffold a Kotlin Android feature module"
- "Set up a Compose Multiplatform shared UI component"
- "Write a ViewModel with unidirectional data flow"
- "Add a new feature following clean architecture with Hilt DI"

## How to use

### Architecture: Strict MVI (Model-View-Intent)

Every feature must follow unidirectional data flow:

1. **State** — Single immutable `data class` representing the entire screen state:
   ```kotlin
   data class FeatureState(
       val isLoading: Boolean = false,
       val items: List<Item> = emptyList(),
       val error: String? = null
   )
   ```

2. **Intent** — Sealed interface for all user actions:
   ```kotlin
   sealed interface FeatureIntent {
       data object LoadItems : FeatureIntent
       data class SelectItem(val id: String) : FeatureIntent
   }
   ```

3. **SideEffect** — Sealed interface for one-shot events:
   ```kotlin
   sealed interface FeatureSideEffect {
       data class ShowSnackbar(val message: String) : FeatureSideEffect
       data class NavigateTo(val route: String) : FeatureSideEffect
   }
   ```

4. **ViewModel** — Processes intents, updates state, emits side effects:
   ```kotlin
   @HiltViewModel
   class FeatureViewModel @Inject constructor(
       private val repository: FeatureRepository
   ) : ViewModel() {
       private val _state = MutableStateFlow(FeatureState())
       val state: StateFlow<FeatureState> = _state.asStateFlow()

       private val _sideEffect = Channel<FeatureSideEffect>(Channel.BUFFERED)
       val sideEffect: Flow<FeatureSideEffect> = _sideEffect.receiveAsFlow()

       fun onIntent(intent: FeatureIntent) {
           when (intent) {
               is FeatureIntent.LoadItems -> loadItems()
               is FeatureIntent.SelectItem -> selectItem(intent.id)
           }
       }
   }
   ```

5. **Composable Screen** — Stateless, receives state and emits intents:
   ```kotlin
   @Composable
   fun FeatureScreen(
       viewModel: FeatureViewModel = hiltViewModel()
   ) {
       val state by viewModel.state.collectAsStateWithLifecycle()
       FeatureContent(
           state = state,
           onIntent = viewModel::onIntent
       )
   }

   @Composable
   private fun FeatureContent(
       state: FeatureState,
       onIntent: (FeatureIntent) -> Unit
   ) {
       // Pure UI — no business logic here
   }
   ```

### Kotlin 2.x & K2 Compiler Rules

- Use `kotlin("2.1")` or later with K2 compiler enabled
- Prefer `sealed interface` over `sealed class`
- Use `data object` for singleton sealed variants
- Use `value class` for type-safe wrappers
- Prefer `kotlinx.coroutines.flow` for reactive streams
- Use structured concurrency with `viewModelScope` and `coroutineScope`

### Compose 2026 Conventions

- Use `Modifier` as first optional parameter in all composables
- Prefer `collectAsStateWithLifecycle()` over `collectAsState()`
- Use `remember` and `derivedStateOf` to minimize recomposition
- Keep composables small and focused — extract sub-composables
- Use `@Preview` with `@PreviewLightDark` and `@PreviewScreenSizes`
- Prefer `LazyColumn`/`LazyRow` for lists; never use `Column` with `forEach` for dynamic content
- Use Material 3 components and dynamic color theming

### Dependency Injection with Hilt

- Annotate ViewModels with `@HiltViewModel`
- Use `@Inject constructor` for all injectable classes
- Define modules with `@Module` and `@InstallIn`
- Scope to appropriate component: `SingletonComponent`, `ViewModelComponent`, `ActivityComponent`

### Room Database Patterns

- Define entities as `data class` with `@Entity` annotation
- Use `@Dao` interfaces with suspend functions for queries
- Return `Flow<List<T>>` for observable queries
- Use `@TypeConverter` for complex types

### Project Structure

```
feature-name/
├── data/
│   ├── repository/
│   │   └── FeatureRepositoryImpl.kt
│   ├── local/
│   │   ├── FeatureDao.kt
│   │   └── FeatureEntity.kt
│   └── remote/
│       ├── FeatureApi.kt
│       └── FeatureDto.kt
├── domain/
│   ├── model/
│   │   └── Feature.kt
│   ├── repository/
│   │   └── FeatureRepository.kt
│   └── usecase/
│       └── GetFeatureUseCase.kt
└── presentation/
    ├── FeatureScreen.kt
    ├── FeatureViewModel.kt
    ├── FeatureState.kt
    ├── FeatureIntent.kt
    └── FeatureSideEffect.kt
```

### CI Validation Checklist

- All composables must have `@Preview`
- No business logic in `@Composable` functions
- State classes must be immutable (`data class` with `val` only)
- ViewModels must not hold `Context` references
- Use `rememberSaveable` for state that must survive configuration changes

## References

- Source: [haidrrrry/compose-kotlin-agent-skills](https://github.com/haidrrrry/compose-kotlin-agent-skills) — Jetpack Compose & Kotlin AI agent skills for Cursor, Claude Code, Codex, Gemini & 27+ agents
- [Jetpack Compose documentation](https://developer.android.com/jetpack/compose)
- [Kotlin K2 compiler](https://kotlinlang.org/docs/k2-compiler-migration-guide.html)
- [MVI architecture pattern](https://developer.android.com/topic/architecture)