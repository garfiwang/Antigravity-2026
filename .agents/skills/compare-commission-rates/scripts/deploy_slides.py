import subprocess
import os
import sys

project_dir = "/Users/garfiwang/Documents/Antigravity-2026/壽險佣金-2026/three-year-commissions"
repo_name = "three-year-commissions"
username = "garfiwang"

def run_cmd(args, cwd=project_dir):
    print(f"Running command: {' '.join(args)} in {cwd}")
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing command: {result.stderr}")
        return False, result.stderr
    print(f"Success: {result.stdout}")
    return True, result.stdout

# 1. git init
print("\n--- Initializing Git ---")
if not os.path.exists(os.path.join(project_dir, ".git")):
    success, out = run_cmd(["git", "init"])
    if not success:
        sys.exit(1)
else:
    print("Git already initialized.")

# 2. Check and configure git user
print("\n--- Configuring Git User ---")
success, name = run_cmd(["git", "config", "user.name"])
if not success or not name.strip():
    run_cmd(["git", "config", "user.name", "garfiwang"])
    
success, email = run_cmd(["git", "config", "user.email"])
if not success or not email.strip():
    run_cmd(["git", "config", "user.email", "richnews168@gmail.com"])

# 3. git add
print("\n--- Adding Files ---")
success, _ = run_cmd(["git", "add", "."])
if not success:
    sys.exit(1)

# 4. git commit
print("\n--- Committing ---")
# Check if there is anything to commit
success, status = run_cmd(["git", "status", "--porcelain"])
if success and status.strip():
    success, _ = run_cmd(["git", "commit", "-m", "Initialize Three-Year Insurance Commissions Presentation"])
    if not success:
        sys.exit(1)
else:
    print("Nothing to commit.")

# Ensure we are on main branch
success, _ = run_cmd(["git", "branch", "-M", "main"])

# 5. gh repo create and push
print("\n--- Creating GitHub Repo and Pushing ---")
# Check if repo already exists on remote
success, remote_list = run_cmd(["git", "remote", "-v"])
if success and "origin" in remote_list:
    print("Remote 'origin' already exists. Pushing directly...")
    success, _ = run_cmd(["git", "push", "-u", "origin", "main"])
else:
    # Use gh repo create
    success, _ = run_cmd([
        "gh", "repo", "create", 
        f"{username}/{repo_name}", 
        "--public", 
        "--source=.", 
        "--push", 
        "--description", "Three-Year Life Insurance Commissions Presentation"
    ])
    # If it failed because it already exists, let's try setting remote and pushing
    if not success:
        print("gh repo create failed (it may already exist). Trying to add remote manually...")
        run_cmd(["git", "remote", "add", "origin", f"https://github.com/{username}/{repo_name}.git"])
        success, _ = run_cmd(["git", "push", "-u", "origin", "main", "--force"])

# 6. Enable GitHub Pages
print("\n--- Enabling GitHub Pages ---")
branch_name = "main"
success, _ = run_cmd([
    "gh", "api", 
    f"repos/{username}/{repo_name}/pages", 
    "--method", "POST", 
    "-f", f"source[branch]={branch_name}", 
    "-f", "source[path]=/"
])

if success:
    print("\n==============================================")
    print("✅ Deployment completed successfully!")
    print(f"🔗 GitHub Pages URL: https://{username}.github.io/{repo_name}/")
    print(f"📦 Repository URL: https://github.com/{username}/{repo_name}")
    print("==============================================")
else:
    print("\n⚠️ Pages API returned an error, it might already be enabled or setting up.")
    print(f"🔗 GitHub Pages URL: https://{username}.github.io/{repo_name}/")
