# Contributing a skill to the Ling dojo

A skill is a repeatable process written down so a person or an agent can run it the same way twice.
If you do something more than once, it should probably be a skill. If you built one that works,
it belongs here so someone else can fork it.

## The loop

1. **Build it in your own workspace** (`.claude/skills/<name>/SKILL.md`). Get it working on real work first. A skill you have not actually used is not ready.
2. **Run the safety check.** `python3 scripts/safety-check.py <your-skill-folder-or-submission.zip>`. Fix everything it flags.

   It reports three levels. **LEAK** (exit 2) is a secret, credential or internal id: stop, and rotate the key if it was real. **GAP** (exit 1) is a missing `SKILL.md` or definition of done: a quality problem, not a security one. **read** never fails the build; it marks a passage a human must read. These are deliberately different, because a reviewer who overrides a BLOCK for a missing heading learns to override the next one for a Stripe key. Do not "publish now and clean later"; that is how keys leak.

   It blocks on two kinds of thing. **Things that break the installer:** personal file paths, references escaping the skill folder, destructive commands, anything writing into `~/.claude`. **Things that leak Ling:** vendor keys (Stripe, GCP/Firebase service accounts, SendGrid, Twilio, HubSpot, database URLs), and internal identifiers such as Stripe account ids, Google Sheet and Drive file ids, Slack channel ids, ClickUp list ids, GA4 property ids and Firebase project ids. An id is not a password, but a public repo hands an outsider the map, so read ids from config or ask the user for them.

   It also **warns**, without failing, on things only a person can judge: external email addresses and phone numbers (a skill is a process, not the rows it was tested on), revenue and compensation figures, and anything marked confidential. Read every warning before you merge.

   **The check is a floor, not a clearance.** It matches patterns; it cannot recognise a customer name, an unreleased roadmap or a screenshot. Its own regression suite is `tests/run.py`, and every case in `tests/fixtures.md` is one it got wrong once. If you change a pattern, run it. `git log -p` your own diff before opening the PR, and remember the repo is public.
3. **Make it portable.** See the checklist below. This is the step people skip and it is the reason forked skills break on other machines.
4. **Give it a definition of done.** See "No eval, no merge" below. This is a hard gate.
5. **Open a PR.** Add your skill under `plugins/<pack>/skills/<name>/`, add or update the entry in `.claude-plugin/marketplace.json`, and describe in the PR what the skill does and what you used it for.
6. **CI runs the safety check on your PR automatically.** A LEAK fails the build. You do not have to remember to run it, and neither does your reviewer. Run `./scripts/install-hooks.sh` once and it also runs before every local commit, which is better: a key caught pre-commit is deleted, a key caught in CI is already in your branch history and has to be rotated.
7. **One reviewer approves**, then merge. Everyone who has added the marketplace gets it on their next `/plugin marketplace update`.

## Portability checklist

Plugins are copied to a local cache when installed, so **a skill cannot reference files outside its
own folder**. Paths like `../../../00-brain/customers.md` break for everyone but you.

- No `../` paths. Reference workspace files relatively from the project root (`00-brain/customers.md`), and treat them as optional.
- No absolute paths. `/Users/yourname/...` exists only on your machine.
- No hardcoded IDs, tokens, channel IDs, or spreadsheet keys. Read them from the environment or ask the user.
- No personal names in the instructions. Write "you", not the name of whoever built it.
- Say which tools it needs. If it requires Google Workspace or ClickUp, say so at the top, so someone without that connection knows before they install.

## No eval, no merge

A skill enters the library only with a written definition of done. This is the single rule that
keeps the library from filling up with vague prompt blobs.

Your skill needs a `## Definition of done` section containing at least:

- **A pass condition** you could check without arguing about it. "The page loads in under 50ms" is a definition of done. "The output is good" is not.
- **One golden example**: an input and the output you would accept for it.
- **One adversarial case**: an input you expect it to handle badly, and what it should do instead (usually: say it cannot).

If you cannot write the pass condition, the skill is not finished, it is a prompt. That is fine,
keep using it privately until you can name what "done" means.

Demystifier for anyone who thinks evals are an engineering thing: when you read a draft and think
"that headline is weak", you are running an eval in your head. Write that down.

## Privilege level

Every skill declares one, in its `## About` section:

- **read-only**: reads data, writes nothing. Default. Install without thinking about it.
- **draft-only**: produces drafts, messages, or files for a human to send or keep. The right level for most useful skills.
- **can-send**: writes to an external system, sends, publishes, or spends. Needs a named owner and a second reviewer on the PR.

## If you push a secret by accident

Delete it from the repo, rotate the key immediately, and clean the git history if the commit
already synced to anyone. Do not just delete the line and pretend the internet forgot: a deleted
line still lives in every prior commit until history is rewritten, and git history is exactly what
this repo is for.

## Forking without losing updates

Forking is encouraged; that is the point of the library. To customize a skill and still get
upstream improvements: keep your renamed fork, install the updated original alongside it, have
Claude read the original's changes and merge what you want into your fork, then uninstall the
original. The changelog in each PR is what makes this possible, so write a real one.
