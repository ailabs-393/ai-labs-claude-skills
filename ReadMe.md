# ai-labs-claude-skills

A collection of reusable "skills" for Claude AI and developer tooling. Each skill is a small, focused package (under `packages/skills/`) that provides scripts, templates, and utilities for common developer tasks such as document processing, SEO analysis, CI/CD generation, Docker containerization, test analysis, and more.

## Key benefits
- Modular: Skills are organized per-folder so you can pick only what you need.
- Ready-to-run scripts: Includes CLI scripts for common workflows (SEO analysis, sitemap generation, document unpacking/validation, resume generation, etc.).
- Automations: Helpers to auto-generate package/index files and install skills into user projects.
- Reproducible builds: `build` copies packaged skills into `dist` for distribution.
- Extensible: Add new skills by creating a folder under `packages/skills/` and following the existing patterns.

## Installation Command 

```
 npm i ai-labs-claude-skills
```
## And if want to download the latest version than go for this:
```
npm i ai-labs-claude-skills@latest

```

## Quick start
1. Install (postinstall will attempt to copy skills into the host project):
   npm install
2. Build distribution:
   npm run build
3. Generate missing package or index files:
   npm run gen:pkg
   npm run gen:index

## Notable files & scripts
- Root package manifest: package.json
- Installer that copies skills into projects: install-skills.mjs
- Helpers to create packages/index files: create-packages.js, generate-index-files.js
- Skills directory: packages/skills/ (each skill contains scripts, assets, and a SKILL.md)

## Contributing
- Add a new folder in `packages/skills/` with a `SKILL.md`, scripts, and optional assets.
- Follow existing patterns for CLI usage and README documentation.

## License
MIT
