/** Build a readable, self-contained Markdown inventory of the standalone Django source tree. */
import fs from "node:fs";
import path from "node:path";

const projectRoot = "/home/ubuntu/taskswap";
const selectedPaths = ["manage.py", "requirements.txt", "TASKSWAP_README.md", "tasksite", "core"];
const ignoredNames = new Set(["__pycache__", "db.sqlite3"]);
const files = [];

function visit(relativePath) {
  const absolutePath = path.join(projectRoot, relativePath);
  const details = fs.statSync(absolutePath);
  if (details.isDirectory()) {
    for (const name of fs.readdirSync(absolutePath).sort()) {
      if (!ignoredNames.has(name)) visit(path.join(relativePath, name));
    }
  } else {
    files.push(relativePath);
  }
}

selectedPaths.forEach(visit);

const languageFor = (file) => {
  if (file.endsWith(".py")) return "python";
  if (file.endsWith(".html")) return "html";
  if (file.endsWith(".css")) return "css";
  if (file.endsWith(".js") || file.endsWith(".mjs")) return "javascript";
  return "text";
};

const tree = files.map((file) => `- \`${file}\``).join("\n");
const contents = files.map((file) => {
  const body = fs.readFileSync(path.join(projectRoot, file), "utf8");
  return `## \`${file}\`\n\n\`\`\`${languageFor(file)}\n${body}\n\`\`\``;
}).join("\n\n");

const output = `# TaskSwap — Complete Source Listing\n\nThis document contains the standalone Django project folder structure followed by the complete contents of every runnable source file.\n\n## Folder structure\n\n${tree}\n\n---\n\n${contents}\n`;
fs.writeFileSync(path.join(projectRoot, "TaskSwap_SOURCE_LISTING.md"), output);
