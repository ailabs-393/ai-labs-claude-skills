# 🚀 ai-labs-claude-skills  

[![npm version](https://img.shields.io/npm/v/ai-labs-claude-skills.svg?color=blue)](https://www.npmjs.com/package/ai-labs-claude-skills)
[![npm downloads](https://img.shields.io/npm/dt/ai-labs-claude-skills.svg?color=brightgreen)](https://www.npmjs.com/package/ai-labs-claude-skills)
[![license](https://img.shields.io/npm/l/ai-labs-claude-skills.svg)](https://github.com/ailabs-393/ai-labs-claude-skills/blob/main/LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D18-green)](https://nodejs.org)

> 🧠 A collection of reusable **"skills"** for Claude AI and developer tooling.  
> Each skill is a focused, modular package that brings automation to your dev workflows — from SEO analysis to document parsing, CI/CD generation, Docker automation, and more.

---

## ✨ Key Benefits

- ⚙️ **Modular:** Pick and use only the skills you need.  
- 🚀 **Ready-to-run Scripts:** Includes tools for SEO analysis, sitemap generation, document unpacking, resume creation, and more.  
- 🤖 **Automations:** Automatically generates index and package files on build.  
- 🔁 **Reproducible Builds:** Ensures clean and consistent skill packaging.  
- 🧩 **Extensible:** Easily add new skills by following existing folder patterns.  

---

## ⚡️ Installation

```bash
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
