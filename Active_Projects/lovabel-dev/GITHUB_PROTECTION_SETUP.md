# lovabel.dev — GitHub with Protection & “Hidden”

How to push lovabel.dev to GitHub with **git protection** and keep it **somewhat hidden**.

---

## Option A: Same Repo (DigitalMarketing) — Easiest

lovabel.dev lives under **Active_Projects/lovabel-dev/** in your main PLM repo.

1. **Repo is already private**  
   If your main repo (e.g. `Delta0537/DigitalMarketing` or `Delta0537/premier-lead-marketing`) is **Private**, everything in it (including this folder) is already hidden from the public.

2. **Push as usual**
   ```powershell
   cd c:\Users\dezel\DigitalMarketing
   git add Active_Projects/lovabel-dev
   git status   # confirm no .env or secrets
   git commit -m "Add lovabel.dev vibe-code project"
   git push origin <your-branch>
   ```
   Root `.gitignore` already excludes `.env`, secrets, etc., so they won’t be committed.

3. **“Hidden”**  
   - Private repo = not findable by public, not listed on your public profile.  
   - Folder is just another path (`Active_Projects/lovabel-dev`), not obviously highlighted.

**Protection:**  
- Rely on **branch protection** for your main/default branch (see “Branch protection” below).  
- Don’t commit `.env` or secrets; `.gitignore` in this folder + root handles that.

---

## Option B: Separate Private Repo (lovabel.dev only)

If you want lovabel.dev in its **own** repo (still under PLM, but separate from DigitalMarketing):

1. **Create a new repo on GitHub**
   - **New repository** → name: `lovabel-dev` (or `lovabel.dev`).
   - **Private**.
   - Do **not** add README / .gitignore / license (you already have them locally).

2. **Push only this folder**
   ```powershell
   cd c:\Users\dezel\DigitalMarketing\Active_Projects\lovabel-dev
   git init
   git remote add origin https://github.com/YOUR_USERNAME/lovabel-dev.git
   git add .
   git status   # confirm no .env or secrets
   git commit -m "Initial: lovabel.dev vibe-code"
   git branch -M main
   git push -u origin main
   ```
   Use a **Personal Access Token** or **SSH** instead of password if prompted.

3. **“Hidden”**
   - Repo is **Private** → not searchable, not on public profile.
   - Optionally: **Settings → General → Danger Zone** is not needed for hiding; just keep it Private.
   - To hide from profile: **Settings → General** → uncheck **“Show on my profile”** if that option exists for the repo.

**Protection:**  
- Use branch protection on `main` (see below).  
- This folder’s `.gitignore` + no `.env` in repo = no secrets in Git.

---

## Git protection checklist

- **.gitignore**
  - Root repo and `Active_Projects/lovabel-dev/.gitignore` both exclude:
    - `.env`, `.env.local`, `*.env`, `secrets.json`, `config.json`
  - So secrets stay local and are not pushed.

- **Branch protection (GitHub)**  
  - Repo → **Settings → Branches → Add rule** (or “Branch protection rules”).
  - Branch name: `main` (or your default).
  - Suggested:
    - **Require a pull request before merging** (optional but good for “protection”).
    - **Do not allow force pushes** (recommended).
    - **Require status checks** (optional).
  - Saves the rule.

- **Private repo**
  - Keeps the code “hidden” from the public and search engines.

- **Hide from profile (optional)**
  - Repo **Settings → General** → if you see “Show on my profile”, turn it off so the repo doesn’t appear on your public profile.

---

## Summary

| Goal              | What to do |
|-------------------|------------|
| **In PLM structure** | Use **Active_Projects/lovabel-dev** (Option A or B). |
| **Pushed to GitHub** | Option A: push with main repo. Option B: separate private repo and push from this folder. |
| **Git protection**   | `.gitignore` for secrets; branch protection on `main`; no force push. |
| **Somewhat hidden**  | Private repo; optionally turn off “Show on my profile” for that repo. |

After this, you can vibe-code in **Active_Projects/lovabel-dev**, push to GitHub with protection, and keep the repo somewhat hidden.
