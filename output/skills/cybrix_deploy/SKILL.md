---
name: cybrix_deploy
description: |
  Deploy and host applications using Cybrix's auto-deployment platform via Claude Code.
  TRIGGER when: user wants to deploy an app, set up hosting, auto-deploy from git, use Cybrix platform, or manage deployed services.
  DO NOT TRIGGER when: user is doing local development only, using other hosting providers explicitly (Vercel, Netlify, AWS), or general devops unrelated to deployment.
---

# Cybrix Deploy

Deploy and manage hosted applications using the Cybrix platform directly from Claude Code.

## When to use

- "Deploy this app to Cybrix"
- "Set up auto-deployment for this repo"
- "Host this project with Cybrix"
- "Check my Cybrix deployment status"
- "Configure Cybrix hosting for this service"

## How to use

1. **Install the Cybrix skills plugin:**
   ```bash
   claude plugin marketplace add cybrixcc/cybrix-skills
   ```

2. **Deploy an application:**
   - Ensure your project has a valid configuration (Dockerfile, package.json, or supported build system)
   - Run the deploy command from your project root
   - Cybrix will auto-detect your framework and configure hosting

3. **Set up auto-deployment:**
   - Connect your Git repository to Cybrix
   - Pushes to the configured branch will trigger automatic deployments
   - Monitor deployment status through the Cybrix dashboard or CLI

4. **Manage deployments:**
   - View logs, restart services, and configure environment variables
   - Scale resources as needed through the Cybrix backend

## Key features

- **Auto-deployment** from Git pushes
- **Framework detection** for automatic build configuration
- **Hosted backend** managed by Cybrix
- **Shell-based skills** for integration with Claude Code workflows

## References

- Source: https://github.com/cybrixcc/cybrix-skills
- Topics: claude-code-skills, auto-deployment, devops, hosting
