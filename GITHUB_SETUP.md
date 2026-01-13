# GitHub Setup Instructions

Here are the steps to push this project to GitHub.

## 1. Create a new GitHub repo
**Using GitHub CLI (Recommended):**
```bash
gh repo create prompt-forge --public --source=. --remote=origin
```
*(Follow the interactive prompts if needed)*

**Using Web Interface:**
1. Go to [github.com/new](https://github.com/new).
2. Repository name: `prompt-forge`.
3. Description: `The Ultimate Local-First Prompt Optimizer`.
4. Do NOT check "Initialize with README" (we already have one).
5. Click **Create repository**.

## 2. Push to Remote (If created via Web)
Since we have already initialized the local repo and committed the files, you just need to link it.

1. **Create the repository** at [https://github.com/new](https://github.com/new)
   - Name: `prompt-forge`
   - Description: `The Ultimate Local-First Prompt Optimizer`
   - **Do not** initialize with README, .gitignore, or License.

2. **Run these commands:**

```bash
# Add the remote (with your specific username "ahmadzkn")
git remote remove origin
git remote add origin https://github.com/ahmadzkn/prompt-forge.git

# Push to GitHub
git branch -M main
git push -u origin main
```
