---
name: claude_mythos_app_setup
description: |
  Set up and configure the Claude Mythos AI Anthropic App, including API key configuration, prompt formatting, and creative writing workflows.
  Triggers: mythos app, claude mythos, mythos setup, roleplay client, mythos creative writing, claude frontend app
---

# Claude Mythos AI App Setup

Assist users with setting up, configuring, and using the Claude Mythos AI Anthropic App — an open-source frontend client for Claude that supports creative writing, roleplay, and custom prompt formatting.

## When to use

- "Help me set up Claude Mythos AI app"
- "Configure my Anthropic API key for the Mythos client"
- "Set up prompt formatting for Claude roleplay in Mythos"
- "How do I install and run Claude Mythos on my platform?"
- "Configure a custom system prompt in the Mythos app"

## How to use

### 1. Clone and prepare the repository

```bash
git clone https://github.com/AbhishekK130804/Claude-Mythos-AI-Anthropic-App.git
cd Claude-Mythos-AI-Anthropic-App
```

### 2. API key configuration

Set your Anthropic API key in the app's configuration:

- Locate the settings or configuration file in the project.
- Add your `ANTHROPIC_API_KEY` to the appropriate config field.
- Supported models: Claude 3.5 Sonnet, Claude Opus 4.6, and other Anthropic models.

### 3. Build and run

The project is built with C#. Open the solution in Visual Studio or build via the .NET CLI:

```bash
dotnet build
dotnet run
```

For platform-specific builds (PC, Android APK, iOS), follow the build instructions in the repository README.

### 4. Custom prompt formatting

- Navigate to the prompt configuration section in the app.
- Set up system prompts for your desired use case (creative writing, roleplay, general assistant).
- The app supports SillyTavern-compatible prompt formatting for Claude models.

### 5. Key features

- **Multi-platform**: PC (Windows), Android (APK), iOS support.
- **Creative writing**: Optimized prompt templates for fiction and roleplay.
- **Custom system prompts**: Full control over system prompt configuration.
- **Model selection**: Switch between Claude Sonnet and Opus models.
- **Open-source frontend**: Extensible and self-hostable.

## References

- Source repository: https://github.com/AbhishekK130804/Claude-Mythos-AI-Anthropic-App
- Anthropic API documentation: https://docs.anthropic.com/
