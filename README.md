# Ling skills dojo

The shared home for Ling's skills. A skill is a repeatable process written down so a person or an
agent runs it the same way twice. Build one, publish it here, let anyone fork it.

The point is not the folder. The point is that improvements compound: when someone forks a skill and
makes it better, everyone gets the better version instead of it dying on one laptop.

## Install it (once, about 30 seconds)

Public repo, so no account or access grant needed. In Claude Code:

```
/plugin marketplace add ling-app/ling-skills
```

(If you have a local clone instead, `/plugin marketplace add ./ling-skills` works the same way.)

Then install what you want:

```
/plugin install feedback-tools@ling-skills
```

Later, to pick up everyone else's improvements:

```
/plugin marketplace update ling-skills
```

Skills from a plugin are namespaced, so the one above runs as
`/feedback-tools:user-feedback-categorizer`.

## What's in it

| Plugin | Skill | Privilege | What it does |
|---|---|---|---|
| `feedback-tools` | `user-feedback-categorizer` | read-only | Turns a pile of reviews, survey answers or churn reasons into a ranked table of themes with owners and a top 3 to act on. |

One skill is the right size to start. The library grows from the workshop, not from me
pre-filling it.

## Add yours

Read [CONTRIBUTING.md](CONTRIBUTING.md). The short version:

1. Build it in your own workspace and actually use it.
2. `python3 scripts/safety-check.py <your-skill-folder>` and fix what it flags.
3. Make it portable (no `../` paths, no absolute paths, no hardcoded IDs, no personal names).
4. Give it a definition of done. **No eval, no merge.**
5. Open a PR. One approval, then it is everyone's.

## Is anyone using it?

```bash
scripts/adoption.sh "6 weeks ago"
```

Contributors, most-touched skills, and skills nobody has touched. That last list is the useful one:
a library that only grows is a library nobody prunes. The kill test is who asked for this, does it
connect to value within two steps, and has anyone acted on its output in three weeks.

## Rules of the house

- **Portable or it does not ship.** Plugins are copied to a cache on install, so a skill that reaches outside its own folder breaks for everyone but its author.
- **No eval, no merge.** A skill without a definition of done is a prompt, and prompts are disposable.
- **Every skill declares a privilege level.** read-only, draft-only, or can-send. Anything that sends, publishes or spends needs a named owner and a second reviewer.
- **Nothing private in here.** No customer data, no credentials, no `_private` content. This repo is shared by construction; assume everyone at Ling reads it.
- **Fork freely.** Forking is the mechanism, not a defection. `CONTRIBUTING.md` explains how to keep a fork and still take upstream updates.
