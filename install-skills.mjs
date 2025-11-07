import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Find root (avoid node_modules)
function findProjectRoot(dir) {
  while (dir !== path.parse(dir).root) {
    if (fs.existsSync(path.join(dir, "package.json")) && !dir.includes("node_modules")) {
      return dir;
    }
    dir = path.dirname(dir);
  }
  return process.cwd();
}

const projectRoot = findProjectRoot(__dirname);
const distSkills = path.join(__dirname, "dist", "skills");
const targetSkillsDir = path.join(projectRoot, ".claude", "skills");

// Recursive copy
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

// Recursive delete
function deleteRecursive(dir) {
  if (!fs.existsSync(dir)) return;
  for (const item of fs.readdirSync(dir)) {
    const p = path.join(dir, item);
    const stat = fs.statSync(p);
    if (stat.isDirectory()) deleteRecursive(p);
    else fs.unlinkSync(p);
  }
  fs.rmdirSync(dir);
}

(async () => {
  try {
    console.log("📦 Installing Claude skills to:", targetSkillsDir);
    copyRecursive(distSkills, targetSkillsDir);
    console.log("✅ Claude skills installed!");

    const packageDir = path.resolve(__dirname, "../..");
    if (packageDir.includes("node_modules")) {
      console.log("🧹 Cleaning up node_modules entry...");
      setTimeout(() => {
        try {
          deleteRecursive(packageDir);
          console.log("🧽 Package folder removed successfully!");
        } catch (err) {
          console.warn("⚠️ Cleanup failed:", err.message);
        }
      }, 1500);
    }
  } catch (err) {
    console.error("❌ Error installing Claude skills:", err);
  }
})();
