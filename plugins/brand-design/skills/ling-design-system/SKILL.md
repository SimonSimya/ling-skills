---
name: ling-design-system
description: >-
  Apply Ling brand guidelines to any visual design or Canva output. Use when creating social media
  posts, posters, flyers, presentations, banners, or any branded content for Ling. Triggers on:
  "Ling design", "brand post", "Canva design", "Instagram post", "create a flyer", "make a poster",
  "design a slide", "create a banner", or any request to create visual content using Ling colors,
  fonts, mascot, or style. Also triggers when the user asks about Ling illustration style, mascot
  usage, icon rules, or seasonal/campaign artwork.
---

# Ling Design System — Claude Skill
> Read this file fully before creating ANY design, visual, or Canva output for the Ling brand.

## About

- **Privilege level: draft-only.** It produces design files (HTML/SVG/PNG) or Canva drafts for a
  human to review and publish. It sends and publishes nothing itself.
- **Tools needed:** none required. Optional: the Canva connector (section 10 uses it when
  available) and a local Chrome for rendering HTML designs to PNG. Without either, output the
  design as a self-contained HTML/SVG file.
- **Assets:** the official mascot/logo files are not bundled. If the user uploads them, use them;
  otherwise illustrate the mascot flat-vector per section 7 and say the result is a rendition,
  not the official asset.

---

## 1. BRAND IDENTITY

**Brand Name:** Ling
**Personality:** Warm, joyful, playful, energetic — like the Ling monkey mascot.
**Tone:** Friendly and approachable, never cold or corporate.
**Design Philosophy:** Warm cream backgrounds + bold orange accents + heavy Poppins typography = the Ling look.

### Mascot — The Ling Monkey
- Brown monkey with a distinctive **orange hat-band** (`#FF9900`) on a dark cap
- Wears a **"+" symbol** on the belly (represents learning/adding languages); in space/hero/power scenes this becomes an **"×"** variant
- Expressive, cartoon-style with rounded shapes
- Appears in many contexts: adventure, seasonal, action, relaxed, superhero
- **Companion character:** Blue round Earth/globe creature with big eyes — often paired with the monkey as the lesson card header icon
- Both characters use flat illustration style with smooth shapes and no outlines

---

## 2. COLOR PALETTE

### Primary Brand Colors
| Token | Hex | Usage |
|---|---|---|
| `--ling-orange` | `#FF9900` | Primary CTA, buttons, accents, taglines, hat-band |
| `--ling-orange-deep` | `#A36200` | Phonetic text, monkey-fur details |
| `--ling-orange-band` | `#FFAE00` | Hover states, hat-band highlights |
| `--ling-yellow` | `#FFCB3D` | Logo yellow band, lanterns, sun elements |
| `--ling-yellow-soft` | `#FFE15A` | Hero accent yellow |
| `--ling-ink` | `#281E11` | Primary brand text on warm surfaces |

### Background / Surface Colors
| Token | Hex | Usage |
|---|---|---|
| `--ling-cream` | `#FFF6E6` | ✅ DEFAULT background — use this most |
| `--ling-cream-2` | `#FDF8EA` | Alternate warm background |
| `--ling-paper` | `#FFFFFF` | Cards, elevated surfaces |
| `--ling-paper-tint` | `#F1F1F1` | Subtle card background |

### Dark / Night Scene Colors
| Token | Hex | Usage |
|---|---|---|
| `--ling-night` | `#0D1B3E` | Night/space scene backgrounds (deep navy) |
| `--ling-night-mid` | `#1A2F5A` | Mid-tone night sky |
| `--ling-purple-dark` | `#2D1B69` | Deep purple for space/cosmic scenes |

### Ink / Text Colors
| Token | Hex | Usage |
|---|---|---|
| `--ink-900` | `#0A0D10` | Primary text on light backgrounds |
| `--ink-500` | `#3D505C` | Secondary / muted body text |
| `--ink-200` | `#668599` | Hint text, placeholders |
| `--ink-100` | `#E6E6E6` | Dividers, faint borders |

### Cool Blue (Balance to Warm)
| Token | Hex | Usage |
|---|---|---|
| `--ling-cool-100` | `#1AA9FF` | Primary cool accent, neon glow effects |
| `--ling-cool-500` | `#CCEBFF` | Soft blue backgrounds |
| `--ling-cool-700` | `#F5FBFF` | Near-white cool tint |

### Accent Colors
| Token | Hex | Usage |
|---|---|---|
| `--ling-green` | `#0CCF77` | Success, "published" states, nature elements |
| `--ling-red` | `#ED5C3B` | Error, danger states |
| `--ling-coral` | `#FF4B55` | Alerts, urgent CTAs |
| `--ling-blue` | `#4094ED` | App Store, info CTAs |
| `--ling-purple` | `#A142F5` | Premium / special features |
| `--ling-lime` | `#B8E600` | Campaign accent |

---

## 2a. FULL COLOR TOKEN RAMPS (from Figma design system)

These are the complete scales extracted directly from the Figma file. Use these when you need precise tints/shades beyond the key tokens above.

### Orange Scale
| Step | Hex |
|---|---|
| 900 | `#663D00` |
| 800 | `#995C00` |
| 700 | `#B26B00` |
| 600 | `#E58A00` |
| **500** | **`#FF9900`** ← primary |
| 400 | `#FFA319` |
| 300 | `#FFAD33` |
| 200 | `#FFC266` |
| 100 | `#FFD699` |
| 50 | `#FFEBCC` |

### Yellow Scale
| Step | Hex |
|---|---|
| 700 | `#F2BC26` |
| 600 | `#FFC83D` |
| 500 | `#FFD257` |
| 400 | `#FFD970` |
| 300 | `#FFE7A6` |
| 200 | `#FFEDBD` |
| 100 | `#FFF4D9` |
| 50 | `#FFFAEC` |

### Blue / Cool Scale
| Step | Hex |
|---|---|
| 700 | `#009DFF` |
| 600 | `#19A9FF` |
| 500 | `#33B2FF` |
| 400 | `#66C3FF` |
| 300 | `#99D8FF` |
| 200 | `#CCEBFF` |
| 100 | `#E6F5FF` |
| 50 | `#F5FBFF` |

### Dark Blue Scale (UI depth, shadows)
| Step | Hex |
|---|---|
| 900 | `#001F33` |
| 800 | `#002F4C` |
| 700 | `#003F66` |
| 600 | `#005E99` |
| 500 | `#006EB2` |
| 400 | `#007ECC` |
| 300 | `#008DE5` |

### Green (Success) Scale
| Step | Hex |
|---|---|
| 700 | `#26D968` |
| 600 | `#3BDD77` |
| 500 | `#51E186` |
| 400 | `#7DE8A4` |
| 300 | `#A8F0C3` |
| 200 | `#D4F7E1` |
| 100 | `#E9FBF0` |
| 50 | `#F6FDF9` |

### Green Dark Scale
| Step | Hex |
|---|---|
| 900 | `#082B15` |
| 800 | `#0B411F` |
| 700 | `#0F5729` |
| 600 | `#17823E` |
| 500 | `#1A9848` |
| 400 | `#1EAE53` |
| 300 | `#22C45D` |

### Red Scale
| Step | Hex |
|---|---|
| 700 | `#EB1414` |
| 600 | `#ED2C2C` |
| 500 | `#EF4444` |
| 400 | `#F37272` |
| 300 | `#F7A1A1` |
| 200 | `#FBD0D0` |
| 100 | `#FDE8E8` |
| 50 | `#FEF3F3` |

### Red Dark Scale
| Step | Hex |
|---|---|
| 900 | `#2F0404` |
| 800 | `#460606` |
| 700 | `#5E0808` |
| 600 | `#8D0C0C` |
| 500 | `#A40E0E` |
| 400 | `#BC1010` |
| 300 | `#D31212` |

### Gold / Brown Scale (illustration, monkey fur)
| Step | Hex |
|---|---|
| 900 | `#2D2306` |
| 800 | `#42330A` |
| 700 | `#564310` |
| 600 | `#806519` |
| 500 | `#A17A11` |
| 400 | `#C2910A` |
| 300 | `#DBA30B` |

### Ink / Neutral Scale
| Step | Hex |
|---|---|
| 900 | `#0A0D0F` |
| 800 | `#141B1E` |
| 700 | `#1E272D` |
| 600 | `#28353D` |
| 500 | `#29353D` |
| 400 | `#3D505C` |
| 300 | `#526B7A` |
| 200 | `#5C788A` |
| 50 | `#F9FAFB` |

> Alpha variants available for ink-400 (8%, 12%, 16%, 50%) and neutral-50 (8%, 12%, 16%, 50%).

---

## 3. TYPOGRAPHY

### Font Family
- **Primary (Display + UI):** `Poppins` — self-hosted, full weight range
- **Fallback 1:** `Mulish`
- **Fallback 2:** `Inter`
- **Mono:** `SF Mono` / `JetBrains Mono`

> ⚠️ Always specify Poppins in Canva. If unavailable, use Montserrat as the closest match.

### Font Weights (Brand leans HEAVY)
| Variable | Weight | Use |
|---|---|---|
| `--fw-regular` | 400 | Body copy |
| `--fw-medium` | 500 | Small labels, UI elements |
| `--fw-semi` | 600 | Subtitles, emphasis |
| `--fw-bold` | 700 | H2, H3, UI headings |
| `--fw-xbold` | 800 | H1, Hero text |
| `--fw-heavy` | 900 | Display / XL headlines only |

### Type Scale
| Class | Size | Weight | Use |
|---|---|---|---|
| `.t-display` | 72px | 900 Heavy | Max-size hero headlines |
| `.t-hero` | 56px | 800 ExtraBold | Hero section titles |
| `.t-h1` | 40px | 800 ExtraBold | Page headings |
| `.t-h2` | 28px | 700 Bold | Section headings |
| `.t-h3` | 22px | 700 Bold | Card/block headings |
| `.t-sub` | 18px | 700 Bold | Subtitles |
| `.t-body` | 14px | 400 Regular | Body copy |
| `.t-small` | 12px | 500 Medium | Labels, captions |
| `.t-label` | 12px | 700 Bold + UPPERCASE | Tag labels |
| `.t-tagline` | varies | 700 Bold | Orange taglines |
| `.t-phonetic` | 13px | 500 Medium | Romanization text (orange-deep) |

---

## 4. SPACING SYSTEM

| Token | Value |
|---|---|
| `--space-1` | 4px |
| `--space-2` | 8px |
| `--space-3` | 12px |
| `--space-4` | 16px |
| `--space-6` | 24px |
| `--space-8` | 32px |
| `--space-10` | 40px |
| `--space-12` | 48px |
| `--space-16` | 64px |
| `--space-20` | 80px |

---

## 5. BORDER RADIUS

| Token | Value | Use |
|---|---|---|
| `--radius-xs` | 4px | Tiny tags |
| `--radius-sm` | 8px | Small buttons, inputs |
| `--radius-md` | 12px | Cards |
| `--radius-lg` | 16px | Large cards, modals |
| `--radius-xl` | 24px | Feature blocks |
| `--radius-2xl` | 32px | Hero sections |
| `--radius-pill` | 999px | Pills, full-round buttons |

---

## 6. SHADOWS

| Token | Value | Use |
|---|---|---|
| `--shadow-sm` | `0 2px 8px rgba(31,40,46,0.08)` | Cards on hover |
| `--shadow-md` | `0 6px 18px rgba(31,40,46,0.10)` | Elevated modals |
| `--shadow-cta` | `0 3px 6px rgba(255,153,0,0.28)` | Orange CTA buttons |

---

## 7. ILLUSTRATION STYLE GUIDE

This section is sourced from the Figma brand design system file. Follow these rules whenever creating or selecting illustrations.

### 7.1 Overall Style
- **Flat vector illustration** — smooth shapes, no sharp angles, no photorealism
- **Rounded, friendly forms** — every character and object uses soft curves
- **Limited color palettes per scene** — typically 3–5 main colors, using brand palette
- **No black outlines** — shapes defined by color contrast only, never hard black borders

### 7.2 Character Illustration Rules

**The Ling Monkey:**
- Always has orange hat-band (`#FF9900`) on a dark/black cap
- Fur color: warm brown (`#8B5E3C` range; use Gold scale 400–600 for shading)
- Face: light/cream inner circle, small dot eyes, simple smile
- Body: rounded torso with the "+" mark (standard) or "×" mark (space/hero/power scenes)
- Poses: active and expressive — skating, surfing, flying, sitting on krathong, relaxing at beach, superhero hovering
- Can wear accessories matching scene theme (sunglasses, cape, traditional outfit, superhero cape in orange)

**The Globe/Earth Companion:**
- Round blue character with big round white eyes
- Green continents (simplified flat map)
- Mouth is expressive — open/happy
- Appears alongside the monkey in adventure and cultural scenes
- Also shown as the lesson card header icon paired with the monkey

**Secondary props/objects in illustrations:**
- Neon lightning bolt (cyan/blue glow: `#1AA9FF`) — used for "power/speed" themes
- Green-to-teal gradient lightning bolt — used for discount/pricing ("÷" tag) power scenes
- Sky lanterns (yellow `#FFCB3D` with orange flame) — used for Thai/Asian festival themes
- Country flags as small round badges — for multilingual/global themes
- Waves/water: simple curved shapes in blue-cyan gradient
- Stars: small 4-point stars scattered for night/space scenes
- Seashells (scallop + spiral): cream/yellow, used in summer/beach scenes as props
- Keyboard key tiles (rounded square, purple/lavender): floating in space/power scenes

### 7.3 Scene Types & Color Moods

| Scene Type | Background | Key Colors | Usage |
|---|---|---|---|
| Day/Adventure | Sky blue + yellow sand | `#1AA9FF`, `#FFCB3D`, `#A0D468` | App store banners, hero |
| Night/Space | Deep navy `#0D1B3E` | `#1AA9FF` neon, `#FF9900`, yellow | Premium, special campaigns |
| Space/Power | Deep purple-navy `#2D1B69` | Cyan bolt, orange cape, yellow bolts | Subscription/power campaigns |
| Festival/Cultural | Blue water + yellow moon | `#FFCB3D`, `#1AA9FF`, `#0CCF77` | Seasonal posts (Loy Krathong, etc.) |
| Warm/Playful | Cream `#FFF6E6` | `#FF9900`, `#FFCB3D`, `#1AA9FF` | Default social posts, UI |
| Ocean/Summer | Cyan blue + sandy yellow | `#1AA9FF`, `#FFCB3D`, coral tones | Summer/travel campaigns |

### 7.4 Icon Style — "Icons Concept Style 02"
From the Figma file:
- **Use only 2 colors per icon** — balance them equally; don't let one dominate
- You can use tint (lighter percent) of a main brand color for the second color
- Primary icon colors: `#FF9900` (orange) + `#FFCB3D` (yellow)
- **Do:** Balanced solid + 2-color icons
- **Don't:** Use one color only, or more than two colors per icon
- Style: flat, filled shapes — no gradients, no drop shadows on icons

---

## 8. SEASONAL / CAMPAIGN TEMPLATES

Real examples from the Figma design system:

### Loy Krathong Post (Thai festival)
- Background: Blue water + night sky with large yellow moon (`#FFCB3D`) as focal point
- Sky lanterns (yellow rectangular, orange flame) floating in sky
- Monkey in traditional Thai outfit sitting on green krathong on water
- Globe companion on the same krathong, holding incense sticks
- Oil lamp candles floating on water in orange/gold
- Headline: "Loy Krathong 2025" — Poppins ExtraBold 800
- Bottom bar: orange `#FF9900` with "Download Ling Now!" in white Poppins Bold
- App store badges: Google Play + App Store side by side

### Space/Power Campaign
- Background: Deep purple-navy gradient `#2D1B69`
- Cyan-to-teal neon lightning bolt (with discount "÷" tag) on the left
- Monkey in orange superhero cape hovering on purple cloud/planet ring
- Floating UI elements: keyboard tiles (rounded square, lavender/purple), circular UI badges
- Yellow accent lightning bolts for energy
- Stars scattered throughout (4-point, small)

### Summer/Beach Post
- Background: Bright cyan water + sandy yellow beach (hard split, no gradient)
- Top-down aerial perspective
- Monkey relaxing on beach with blue sunglasses, Thai flag nearby
- Globe character in yellow inflatable ring in water, wearing sunglasses
- Country flag badges floating in the scene
- Seashell and spiral shell props on the sand

---

## 9. APP UI PATTERNS (from Figma)

These patterns are used in the Ling app and should inform any UI mockup or promotional screenshot work.

### Lesson Map / Learning Screen
- **Active lesson node:** Octagonal shape with **orange border** (`#FF9900`), light blue fill, contains a blue "book stack" icon
- **Locked nodes:** Grey octagonal shapes, same size, no orange border
- **Connecting lines:** Light blue curved paths linking nodes
- **Lesson card header:** Shows monkey + globe companion side by side as an icon pair
- **Progress bar / crown:** Small gold crown icon + "0/180" in orange
- **Currency icons:** Banana icon (yellow) for coins, ghost/star icon for lives
- **Background:** Clean white (`#FFFFFF`) with light grey node fills

### Bottom Navigation (App)
- 3 tabs: Learn (active = orange icon + orange label), Review (grey), Dialog (grey)
- Active tab icon color: `#FF9900`
- Inactive tab: `#668599` (ink-200)
- Tab bar background: white, subtle top border

### App Header
- Title text: Poppins Bold, `#0A0D10` (ink-900)
- Avatar: circular, top-right — shows monkey face in warm tones
- Flag badge: circular country flag, top-left

---

## 10. CANVA WORKFLOW INSTRUCTIONS (optional — needs the Canva connector)

If the Canva connector is not available, skip this section and produce the design as a
self-contained HTML/SVG file instead, applying the same colors and typography.

### Step 1 — Search for a template
```
Call: search_design OR Canva:generate-design
Query: match the design type + "warm orange", "playful", "language learning", "education"
```

### Step 2 — Apply Brand Colors
```
Primary background → #FFF6E6 (cream) for standard posts
Night scene background → #0D1B3E for seasonal/premium
Space/power background → #2D1B69 for subscription campaigns
Primary accent → #FF9900 (orange)
Text → #281E11 (ling-ink) on warm surfaces
Text → #0A0D10 (ink-900) on cool surfaces
CTA buttons → #FF9900 with white text
```

### Step 3 — Apply Typography
```
Headings → Poppins ExtraBold (800) or Bold (700)
Body → Poppins Regular (400)
Labels/Tags → Poppins Bold (700) UPPERCASE
Taglines → Poppins Bold, color: #FF9900
```

### Step 4 — Fill Text
```
Call: Canva:fill_text
Replace all placeholder text with actual Ling copy
Keep tone: warm, friendly, energetic
```

### Step 5 — Background Color
```
Call: Canva:change_background_color
Default → #FFF6E6 (cream)
Dark/night variant → #0D1B3E (deep navy)
Space/power variant → #2D1B69 (deep purple-navy)
Cool variant → #F5FBFF (cool-700)
```

---

## 11. DESIGN DO'S AND DON'TS

### ✅ DO
- Use cream (`#FFF6E6`) as the default background — it's the Ling signature
- Use orange (`#FF9900`) for all primary CTAs and highlights
- Use Poppins Bold/ExtraBold for all headings — the brand leans heavy
- Round corners generously (16–32px for large elements)
- Add warm orange shadows to buttons (`--shadow-cta`)
- Use the `.t-tagline` orange color for short punchy phrases
- Keep spacing generous — minimum 24px gutters
- For illustrations: use only 2 colors per icon, balanced evenly
- For seasonal posts: use the dark navy night background with yellow moon + lanterns
- Always include the monkey mascot when possible — it's the brand face
- For space/hero scenes: use deep purple-navy + cyan bolt + orange cape on monkey

### ❌ DON'T
- Never use thin/light font weights for headlines (300 or below)
- Never use cold grey (`#666`) as the primary text color — use `#281E11` (ling-ink)
- Never use flat, corporate-looking layouts — Ling is playful
- Never skip the orange accent entirely — every design needs at least one orange element
- Never use more than 2 colors in a single icon
- Never use black outlines on illustrations — shapes are defined by color contrast only

---

## 12. COMMON DESIGN PATTERNS

### Social Media Post (Instagram/Facebook)
- Background: `#FFF6E6` cream
- Headline: Poppins ExtraBold 800, `#281E11` or `#FF9900`
- Subtext: Poppins Regular 400, `#3D505C`
- CTA Button: `#FF9900` fill, white text, `radius-pill`
- Optional accent: yellow band `#FFCB3D` or cool blue `#1AA9FF`

### Seasonal Campaign Post
- Background: Dark navy `#0D1B3E` (night) or scene-appropriate color
- Large focal shape (moon, sun) in `#FFCB3D`
- Monkey mascot as hero element
- Bottom CTA bar: `#FF9900` + "Download Ling Now!" in white
- App store badges at bottom right

### Subscription / Power Campaign
- Background: Deep purple-navy `#2D1B69`
- Cyan/teal neon bolt (left side)
- Monkey in orange superhero cape
- Floating keyboard tiles (lavender/purple)
- CTA: `#FF9900`

### Presentation Slide
- Background: `#FFF6E6` or `#281E11` (dark mode)
- Title: Poppins ExtraBold 800, 40–56px
- Body: Poppins Regular 400, 14–16px
- Accent bar/line: `#FF9900`

### Poster / Flyer
- Large display headline: Poppins Heavy 900, 56–72px
- Orange tagline above or below the headline
- Cream or ink background
- Rounded orange CTA button at bottom

### App Store Banner
- Background: `#1AA9FF` (cool-100) or `#FFF6E6`
- White or ink text
- Monkey mascot if available
- CTA: `#FF9900` button

---

## 13. QUICK REFERENCE — MOST-USED VALUES

```
Background (default):  #FFF6E6
Background (night):    #0D1B3E
Background (space):    #2D1B69
Primary text:          #281E11
Orange:                #FF9900
Yellow:                #FFCB3D
Cool blue:             #19A9FF
Neon glow blue:        #1AA9FF (with blur/glow effect)
Green:                 #0CCF77
Font:                  Poppins
H1 weight:             800 (ExtraBold)
Body weight:           400 (Regular)
Border radius (cards): 16px
Border radius (buttons): 999px (pill)
Icon rule:             Max 2 colors, balanced
Mascot hat-band:       #FF9900 on dark cap
Mascot belly mark:     "+" (standard) / "×" (hero/space scenes)
```

---

## Definition of done

**Pass condition.** Every design this skill produces satisfies all of the following, checkable by
inspection: (1) the background is one of the approved surfaces (`#FFF6E6`, `#FDF8EA`, `#FFFFFF`,
`#0D1B3E`, `#2D1B69`, or the scene backgrounds in 7.3); (2) all headings are Poppins (or Montserrat
fallback) at weight 700+, never 300 or below; (3) at least one `#FF9900` element is present;
(4) primary text is `#281E11` or `#0A0D10`, never a cold grey; (5) icons use at most 2 colors;
(6) illustrations have no black outlines; and (7) if the mascot appears, it has the orange hat-band
on a dark cap and the "+"/"×" belly mark. A design missing any of these is not done.

**Golden example.** Input: *"Make an Instagram post announcing that Ling now has 60+ languages."*
Accepted output: a 1080×1350 (or 1080×1080) design on cream `#FFF6E6`; Poppins ExtraBold headline
in `#281E11` with an orange highlight word; the monkey mascot flat-vector with orange hat-band;
an orange pill CTA ("Download Ling") with white text; yellow/blue accents from the palette; all
seven pass conditions met.

**Adversarial case.** Input: *"Make it minimalist — grayscale, thin fonts, no mascot, very
corporate."* The skill must not silently comply: it says this conflicts with the brand rules
(headlines never below 700 weight, orange accent mandatory, playful not corporate) and offers
either the closest on-brand interpretation or an explicit off-brand exception the requester
confirms. Producing a grayscale thin-font design without flagging it is a failure.
