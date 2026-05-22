#!/usr/bin/env python3
"""
Compose Kotlin MVI Scaffold Generator

Demonstrates the Compose Kotlin MVI Agent Skill by generating a complete
feature module following strict MVI architecture, Kotlin 2.x conventions,
and 2026 Compose best practices.
"""

import os
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class FeatureConfig:
    """Configuration for generating a feature module."""
    feature_name: str
    package_base: str = "com.example.app"
    include_room: bool = True
    include_remote: bool = True

    @property
    def class_name(self) -> str:
        return self.feature_name.replace("_", " ").title().replace(" ", "")

    @property
    def package_path(self) -> str:
        return self.package_base.replace(".", "/")


# --- Templates ---

STATE_TEMPLATE = '''package {package}.{feature}.presentation

/**
 * Single immutable state for {class_name} screen.
 * All fields use val — no mutable state allowed.
 */
data class {class_name}State(
    val isLoading: Boolean = false,
    val items: List<{class_name}Item> = emptyList(),
    val selectedItemId: String? = null,
    val error: String? = null
)

data class {class_name}Item(
    val id: String,
    val title: String,
    val description: String
)
'''

INTENT_TEMPLATE = '''package {package}.{feature}.presentation

/**
 * Sealed interface for all user actions on {class_name} screen.
 * Uses sealed interface (not sealed class) per Kotlin 2.x conventions.
 */
sealed interface {class_name}Intent {{
    data object LoadItems : {class_name}Intent
    data object Refresh : {class_name}Intent
    data class SelectItem(val id: String) : {class_name}Intent
    data class DeleteItem(val id: String) : {class_name}Intent
    data object DismissError : {class_name}Intent
}}
'''

SIDE_EFFECT_TEMPLATE = '''package {package}.{feature}.presentation

/**
 * One-shot events that don't belong in persistent state.
 * Consumed once by the UI layer.
 */
sealed interface {class_name}SideEffect {{
    data class ShowSnackbar(val message: String) : {class_name}SideEffect
    data class NavigateTo(val route: String) : {class_name}SideEffect
    data object NavigateBack : {class_name}SideEffect
}}
'''

VIEWMODEL_TEMPLATE = '''package {package}.{feature}.presentation

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject
import {package}.{feature}.domain.repository.{class_name}Repository

/**
 * ViewModel processing intents and producing state updates.
 * No Context references. Uses structured concurrency via viewModelScope.
 */
@HiltViewModel
class {class_name}ViewModel @Inject constructor(
    private val repository: {class_name}Repository
) : ViewModel() {{

    private val _state = MutableStateFlow({class_name}State())
    val state: StateFlow<{class_name}State> = _state.asStateFlow()

    private val _sideEffect = Channel<{class_name}SideEffect>(Channel.BUFFERED)
    val sideEffect: Flow<{class_name}SideEffect> = _sideEffect.receiveAsFlow()

    init {{
        onIntent({class_name}Intent.LoadItems)
    }}

    fun onIntent(intent: {class_name}Intent) {{
        when (intent) {{
            is {class_name}Intent.LoadItems -> loadItems()
            is {class_name}Intent.Refresh -> loadItems()
            is {class_name}Intent.SelectItem -> selectItem(intent.id)
            is {class_name}Intent.DeleteItem -> deleteItem(intent.id)
            is {class_name}Intent.DismissError -> dismissError()
        }}
    }}

    private fun loadItems() {{
        viewModelScope.launch {{
            _state.update {{ it.copy(isLoading = true, error = null) }}
            repository.getItems()
                .onSuccess {{ items ->
                    _state.update {{ it.copy(isLoading = false, items = items) }}
                }}
                .onFailure {{ throwable ->
                    _state.update {{ it.copy(isLoading = false, error = throwable.message) }}
                }}
        }}
    }}

    private fun selectItem(id: String) {{
        _state.update {{ it.copy(selectedItemId = id) }}
        viewModelScope.launch {{
            _sideEffect.send({class_name}SideEffect.NavigateTo("detail/$id"))
        }}
    }}

    private fun deleteItem(id: String) {{
        viewModelScope.launch {{
            repository.deleteItem(id)
                .onSuccess {{
                    _state.update {{ state ->
                        state.copy(items = state.items.filter {{ it.id != id }})
                    }}
                    _sideEffect.send({class_name}SideEffect.ShowSnackbar("Item deleted"))
                }}
                .onFailure {{ throwable ->
                    _sideEffect.send({class_name}SideEffect.ShowSnackbar(
                        throwable.message ?: "Delete failed"
                    ))
                }}
        }}
    }}

    private fun dismissError() {{
        _state.update {{ it.copy(error = null) }}
    }}
}}
'''

SCREEN_TEMPLATE = '''package {package}.{feature}.presentation

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.tooling.preview.PreviewLightDark
import androidx.compose.ui.tooling.preview.PreviewScreenSizes
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import kotlinx.coroutines.flow.collectLatest

/**
 * Screen-level composable — connects ViewModel to stateless content.
 */
@Composable
fun {class_name}Screen(
    viewModel: {class_name}ViewModel = hiltViewModel()
) {{
    val state by viewModel.state.collectAsStateWithLifecycle()
    val snackbarHostState = remember {{ SnackbarHostState() }}

    LaunchedEffect(Unit) {{
        viewModel.sideEffect.collectLatest {{ effect ->
            when (effect) {{
                is {class_name}SideEffect.ShowSnackbar -> {{
                    snackbarHostState.showSnackbar(effect.message)
                }}
                is {class_name}SideEffect.NavigateTo -> {{
                    // Handle navigation
                }}
                is {class_name}SideEffect.NavigateBack -> {{
                    // Handle back navigation
                }}
            }}
        }}
    }}

    {class_name}Content(
        state = state,
        snackbarHostState = snackbarHostState,
        onIntent = viewModel::onIntent
    )
}}

/**
 * Stateless content composable — pure UI, no business logic.
 * Receives state, emits intents. Testable in isolation.
 */
@Composable
private fun {class_name}Content(
    state: {class_name}State,
    snackbarHostState: SnackbarHostState = remember {{ SnackbarHostState() }},
    onIntent: ({class_name}Intent) -> Unit,
    modifier: Modifier = Modifier
) {{
    Scaffold(
        snackbarHost = {{ SnackbarHost(snackbarHostState) }},
        modifier = modifier
    ) {{ padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {{
            when {{
                state.isLoading -> {{
                    CircularProgressIndicator(
                        modifier = Modifier.align(Alignment.Center)
                    )
                }}
                state.error != null -> {{
                    Column(
                        modifier = Modifier.align(Alignment.Center),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {{
                        Text(
                            text = state.error,
                            style = MaterialTheme.typography.bodyLarge,
                            color = MaterialTheme.colorScheme.error
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Button(onClick = {{ onIntent({class_name}Intent.Refresh) }}) {{
                            Text("Retry")
                        }}
                    }}
                }}
                else -> {{
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(16.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {{
                        items(
                            items = state.items,
                            key = {{ it.id }}
                        ) {{ item ->
                            {class_name}ItemCard(
                                item = item,
                                onSelect = {{ onIntent({class_name}Intent.SelectItem(item.id)) }},
                                onDelete = {{ onIntent({class_name}Intent.DeleteItem(item.id)) }}
                            )
                        }}
                    }}
                }}
            }}
        }}
    }}
}}

@Composable
private fun {class_name}ItemCard(
    item: {class_name}Item,
    onSelect: () -> Unit,
    onDelete: () -> Unit,
    modifier: Modifier = Modifier
) {{
    Card(
        onClick = onSelect,
        modifier = modifier.fillMaxWidth()
    ) {{
        Row(
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {{
            Column(modifier = Modifier.weight(1f)) {{
                Text(
                    text = item.title,
                    style = MaterialTheme.typography.titleMedium
                )
                Text(
                    text = item.description,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }}
            IconButton(onClick = onDelete) {{
                Icon(
                    imageVector = Icons.Default.Delete,
                    contentDescription = "Delete"
                )
            }}
        }}
    }}
}}

@PreviewLightDark
@PreviewScreenSizes
@Composable
private fun {class_name}ContentPreview() {{
    MaterialTheme {{
        {class_name}Content(
            state = {class_name}State(
                items = listOf(
                    {class_name}Item("1", "First Item", "Description of first item"),
                    {class_name}Item("2", "Second Item", "Description of second item"),
                    {class_name}Item("3", "Third Item", "Description of third item")
                )
            ),
            onIntent = {{}}
        )
    }}
}}
'''

REPOSITORY_INTERFACE_TEMPLATE = '''package {package}.{feature}.domain.repository

import {package}.{feature}.presentation.{class_name}Item

/**
 * Domain-layer repository interface.
 * Implementation lives in data layer — depends on abstractions, not concretions.
 */
interface {class_name}Repository {{
    suspend fun getItems(): Result<List<{class_name}Item>>
    suspend fun getItem(id: String): Result<{class_name}Item>
    suspend fun deleteItem(id: String): Result<Unit>
}}
'''

REPOSITORY_IMPL_TEMPLATE = '''package {package}.{feature}.data.repository

import {package}.{feature}.domain.repository.{class_name}Repository
import {package}.{feature}.presentation.{class_name}Item
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Repository implementation with constructor injection.
 * Coordinates data from local (Room) and remote sources.
 */
@Singleton
class {class_name}RepositoryImpl @Inject constructor(
    // private val dao: {class_name}Dao,
    // private val api: {class_name}Api
) : {class_name}Repository {{

    override suspend fun getItems(): Result<List<{class_name}Item>> {{
        return runCatching {{
            // In production: dao.getAll().map {{ it.toDomain() }}
            emptyList()
        }}
    }}

    override suspend fun getItem(id: String): Result<{class_name}Item> {{
        return runCatching {{
            // In production: dao.getById(id).toDomain()
            throw NotImplementedError()
        }}
    }}

    override suspend fun deleteItem(id: String): Result<Unit> {{
        return runCatching {{
            // In production: dao.delete(id)
        }}
    }}
}}
'''

DI_MODULE_TEMPLATE = '''package {package}.{feature}.di

import dagger.Binds
import dagger.Module
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import {package}.{feature}.data.repository.{class_name}RepositoryImpl
import {package}.{feature}.domain.repository.{class_name}Repository
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
abstract class {class_name}Module {{

    @Binds
    @Singleton
    abstract fun bind{class_name}Repository(
        impl: {class_name}RepositoryImpl
    ): {class_name}Repository
}}
'''


def generate_feature(config: FeatureConfig, output_dir: Path) -> list[str]:
    """Generate all files for a feature module. Returns list of created files."""
    created = []
    feature = config.feature_name.lower()
    class_name = config.class_name
    package = config.package_base

    fmt = {"package": package, "feature": feature, "class_name": class_name}

    structure = {
        f"presentation/{class_name}State.kt": STATE_TEMPLATE.format(**fmt),
        f"presentation/{class_name}Intent.kt": INTENT_TEMPLATE.format(**fmt),
        f"presentation/{class_name}SideEffect.kt": SIDE_EFFECT_TEMPLATE.format(**fmt),
        f"presentation/{class_name}ViewModel.kt": VIEWMODEL_TEMPLATE.format(**fmt),
        f"presentation/{class_name}Screen.kt": SCREEN_TEMPLATE.format(**fmt),
        f"domain/repository/{class_name}Repository.kt": REPOSITORY_INTERFACE_TEMPLATE.format(**fmt),
        f"data/repository/{class_name}RepositoryImpl.kt": REPOSITORY_IMPL_TEMPLATE.format(**fmt),
        f"di/{class_name}Module.kt": DI_MODULE_TEMPLATE.format(**fmt),
    }

    base = output_dir / feature
    for rel_path, content in structure.items():
        file_path = base / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        created.append(str(file_path.relative_to(output_dir)))

    return created


def validate_feature(output_dir: Path, feature_name: str) -> list[str]:
    """Run CI-style validation checks on generated code."""
    issues = []
    feature = feature_name.lower()
    base = output_dir / feature

    # Check all presentation files exist
    required_suffixes = ["State.kt", "Intent.kt", "SideEffect.kt", "ViewModel.kt", "Screen.kt"]
    class_name = feature.replace("_", " ").title().replace(" ", "")
    for suffix in required_suffixes:
        path = base / "presentation" / f"{class_name}{suffix}"
        if not path.exists():
            issues.append(f"MISSING: {path.relative_to(output_dir)}")

    # Check state immutability (no var)
    state_file = base / "presentation" / f"{class_name}State.kt"
    if state_file.exists():
        content = state_file.read_text()
        if "var " in content:
            issues.append(f"MUTABLE STATE: {state_file.name} contains 'var' — state must be immutable")

    # Check ViewModel has no Context import
    vm_file = base / "presentation" / f"{class_name}ViewModel.kt"
    if vm_file.exists():
        content = vm_file.read_text()
        if "android.content.Context" in content:
            issues.append(f"CONTEXT LEAK: {vm_file.name} imports Context — forbidden in ViewModels")

    # Check Screen uses collectAsStateWithLifecycle
    screen_file = base / "presentation" / f"{class_name}Screen.kt"
    if screen_file.exists():
        content = screen_file.read_text()
        if "collectAsState()" in content and "collectAsStateWithLifecycle" not in content:
            issues.append(f"LIFECYCLE: {screen_file.name} uses collectAsState() instead of collectAsStateWithLifecycle()")
        if "@Preview" not in content:
            issues.append(f"NO PREVIEW: {screen_file.name} missing @Preview annotation")

    # Check sealed interface usage (not sealed class)
    for kt_file in (base / "presentation").glob("*.kt"):
        content = kt_file.read_text()
        if "sealed class" in content:
            issues.append(f"SEALED CLASS: {kt_file.name} uses 'sealed class' — prefer 'sealed interface'")

    return issues


def main():
    print("=" * 70)
    print("  Compose Kotlin MVI Scaffold Generator")
    print("  Demonstrates: haidrrrry/compose-kotlin-agent-skills")
    print("=" * 70)
    print()

    # Generate two example features to show the pattern
    output_dir = Path("generated_output")
    output_dir.mkdir(exist_ok=True)

    features = [
        FeatureConfig(feature_name="task_list", package_base="com.example.taskapp"),
        FeatureConfig(feature_name="user_profile", package_base="com.example.taskapp"),
    ]

    for config in features:
        print(f"--- Generating feature: {config.class_name} ---")
        print(f"    Package: {config.package_base}.{config.feature_name.lower()}")
        print()

        created = generate_feature(config, output_dir)
        for f in created:
            print(f"    [+] {f}")
        print()

        # Validate
        issues = validate_feature(output_dir, config.feature_name)
        if issues:
            print("    VALIDATION ISSUES:")
            for issue in issues:
                print(f"    [!] {issue}")
        else:
            print("    [OK] All CI validation checks passed")
        print()

    # Show a sample of generated code
    print("=" * 70)
    print("  SAMPLE OUTPUT: TaskListViewModel.kt")
    print("=" * 70)
    sample = (output_dir / "task_list" / "presentation" / "TaskListViewModel.kt")
    if sample.exists():
        print(sample.read_text())

    # Print structure summary
    print("=" * 70)
    print("  GENERATED STRUCTURE")
    print("=" * 70)
    for path in sorted(output_dir.rglob("*.kt")):
        print(f"  {path.relative_to(output_dir)}")

    print()
    print(f"Total files generated: {len(list(output_dir.rglob('*.kt')))}")
    print("All features follow strict MVI with Kotlin 2.x conventions.")


if __name__ == "__main__":
    main()
