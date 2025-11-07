import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 🧭 Find root directory (avoid node_modules)
function findRoot(startDir) {
  let dir = startDir;
  while (dir !== path.parse(dir).root) {
    if (fs.existsSync(path.join(dir, "package.json")) && !dir.includes("node_modules")) {
      return dir;
    }
    dir = path.dirname(dir);
  }
  return process.cwd();
}

const projectRoot = findRoot(__dirname);
const packageJsonPath = path.join(projectRoot, "package.json");

// 🪄 Auto-create package.json if it doesn’t exist
if (!fs.existsSync(packageJsonPath)) {
  const pkg = {
    name: "my-project",
    version: "1.0.0",
    private: true,
    description: "Auto-generated for Claude skills",
  };
  fs.writeFileSync(packageJsonPath, JSON.stringify(pkg, null, 2));
  console.log("🧩 Created package.json automatically.");
}

const distSkills = path.join(__dirname, "dist", "skills");
const claudeSkills = path.join(projectRoot, ".claude", "skills");

// 🔁 Recursive copy
function copyRecursive(src, dest) {
  if (!fs.existsSync(src)) return;
  fs.mkdirSync(dest, { recursive: true });
  for (const item of fs.readdirSync(src)) {
    const srcPath = path.join(src, item);
    const destPath = path.join(dest, item);
    const stat = fs.statSync(srcPath);
    if (stat.isDirectory()) copyRecursive(srcPath, destPath);
    else fs.copyFileSync(srcPath, destPath);
  }
}

// 🧹 Safe delete function
function deleteRecursive(target) {
  if (!fs.existsSync(target)) return;
  for (const item of fs.readdirSync(target)) {
    const p = path.join(target, item);
    const stat = fs.statSync(p);
    if (stat.isDirectory()) deleteRecursive(p);
    else fs.unlinkSync(p);
  }
  fs.rmdirSync(target);
}

// ⚙️ Main execution
(async () => {
  try {
    console.log(`📦 Installing Claude skills → ${claudeSkills}`);
    fs.mkdirSync(path.dirname(claudeSkills), { recursive: true });
    copyRecursive(distSkills, claudeSkills);
    console.log("✅ Claude skills copied successfully!");

    // 🧹 Delete this package from node_modules
    const packagePath = path.resolve(__dirname, "../.."); // ai-labs-claude-skills/
    if (packagePath.includes("node_modules")) {
      console.log("🧹 Cleaning up package folder to keep workspace clean...");
      setTimeout(() => {
        try {
          deleteRecursive(packagePath);
          console.log("🧽 Cleanup complete — only .claude/skills remains!");
        } catch (err) {
          console.warn("⚠️ Cleanup failed:", err.message);
        }
      }, 2000); // short delay to allow logs to print before removal
    }
  } catch (err) {
    console.error("❌ Error:", err);
  }
})();
