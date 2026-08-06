# How to Add Collaborators — Arena + GitHub

You saw screenshots: Arena shows repo dropdown + branch arena/019fd213-the-bettor-1 + +1049 Create PR
That means Arena already has access via your logged-in GitHub.

## Two layers of access:

### A. Arena access (agents + humans using Arena) — No GitHub Settings needed

Arena uses YOUR GitHub OAuth token (you logged in via GitHub on arena.ai). Every Arena session you open inherits YOUR repo permissions and auto-creates a branch `arena/<id>-the-bettor-1`.

To let a teammate work WITH YOU on same branch via Arena:

1. Go to https://arena.ai → your project `the_bettor_1`
2. Click Share / Invite (top-right or project settings)
3. Invite by email: add teammate's email who has Arena account
4. They open Arena → they will see same repo `chickenaiforensic-crypto/the_bettor_1` in dropdown
5. **Important:** Tell them to checkout MY branch, not create new one:
   ```
   git checkout arena/019fd213-the-bettor-1
   git pull origin arena/019fd213-the-bettor-1
   ```
   If Arena auto-creates new arena/... branch for them, they should:
   ```
   git checkout arena/019fd213-the-bettor-1
   git merge their-other-branch --or-- cherry-pick
   git push origin arena/019fd213-the-bettor-1
   ```
   Or in Arena UI select branch dropdown: choose `arena/019fd213-the-bettor-1` instead of `main`

Your screenshot 2 shows main dropdown — that's where you select arena/019fd213-the-bettor-1. Screenshot 1 shows +1049 changes ready — that's my workspace setup commit.

**Result:** They push to same branch, no GitHub invite needed — Arena reuses YOUR token.

### B. GitHub direct access (humans who want to work outside Arena in VSCode / local)

If teammate wants to `git clone` locally without Arena:

1. Go to https://github.com/chickenaiforensic-crypto/the_bettor_1
2. Settings → Collaborators and teams → Manage access → Invite a collaborator
3. Enter their GitHub username → Add → they accept invite email
4. Then they run:
   ```
   git clone https://github.com/chickenaiforensic-crypto/the_bettor_1.git
   git checkout arena/019fd213-the-bettor-1
   ```

### Which to use?

- For AI agents (me + other Arena agents): Use A — automatic, uses your login.
- For human coders who live in Arena: Use A.
- For human who wants local VSCode: Use B + A (both).

### Quick Checklist Before Teammate Starts

- [ ] They have Arena account and you invited them via Share?
- [ ] They see repo `chickenaiforensic-crypto/the_bettor_1` in Arena dropdown?
- [ ] They checked out `arena/019fd213-the-bettor-1` not `main`?
- [ ] They read `START-HERE-COLD-START.md` + their role brief?
- [ ] They know handoffs/ is only door for returns?

If they already have access from Arena to your logged-in GitHub — that's expected. Arena proxy uses your OAuth, so you don't need to add anything on GitHub for Arena sessions — just invite on Arena and point to same branch.
