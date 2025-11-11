# 🚀 ai-labs-claude-skills  

<div align="center">

[![npm version](https://img.shields.io/npm/v/ai-labs-claude-skills.svg?color=blue)](https://www.npmjs.com/package/ai-labs-claude-skills)
[![npm downloads](https://img.shields.io/npm/dt/ai-labs-claude-skills.svg?color=brightgreen)](https://www.npmjs.com/package/ai-labs-claude-skills)
[![license](https://img.shields.io/npm/l/ai-labs-claude-skills.svg)](https://github.com/ailabs-393/ai-labs-claude-skills/blob/main/LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D18-green)](https://nodejs.org)

</div>

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

## 🧠 Example Use Cases

- Use these Claude “skills” to automate and extend your workflows:

1. 🔍 SEO report and metadata generation

2. 🧾 Document unpacking and validation

3. 🧱 Docker container creation and setup

4. 🧠 Resume or report generation scripts

5. ⚙️ CI/CD pipeline auto-generation

6. 📊 Developer project automation utilities

## 🤝 Contributing

- We welcome contributions from the community!
Here’s how to add a new skill:

1. Create a new folder inside packages/skills/. (or just add a new skill)

2. Include a SKILL.md file describing your skill.

3. Add your scripts, assets, or templates.
   
5. Run these commands to create index and package inside skills
    ``` bash
    node generate-index.js
    ```
    and
   ```bash
   node generate-packages.js
   ```
 so that it can actually become a scalable skill   

6. Follow the existing project structure for consistency.

7. Submit a pull request with clear details.

## License
- This project is licensed under the MIT License

## HAPPY CODING :)
