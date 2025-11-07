import fs from "fs";

if (!fs.existsSync("package.json")) {
  console.log("📦 No package.json found. Initializing project...");
  const { execSync } = await import("child_process");
  execSync("npm init -y", { stdio: "inherit" });
}
