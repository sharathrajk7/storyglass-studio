# Studio site — design spec (Direction D, "Sea Sparkle")

- **Date:** 2026-10-09
- **Status:** draft for your review
- **Name:** Storyglass Studio (chosen 2026-10-11). Logo: the Kinetic Aperture (seven glass blades, one kicked out, three shards) with "Storyglass" in Bodoni Moda italic using the site's ivory-to-grey fade; 2D, 3D and circular-emblem versions live in `~/Downloads/Storyglassstudio/`.
- **References:**
  - Live hero prototype: `hero-prototype/` ([live link](https://claude.ai/artifact/PFtp89STAbBos5C9h3KfUR))
  - Mockup canvas, board D: [Studio Website Mockups](https://claude.ai/artifact/SDzH99gphPbLTz9AJcdWey)

---

## 1. What we are building

The site is a sales website for a video studio that makes story-led motion films for startups,
companies and founders worldwide:
- product demos
- explainers
- about-the-company and founder films
- customer case studies
- launch films
- LinkedIn series
- 3D websites

The site has one job. It should convince a founder or marketer that **one good film will explain their
product better than anything they have now**, and get them to send a brief. There are no prices on the
site. Every path ends at the brief form, and the studio replies with an approach and a quote.

The site is also the proof. Its 3D hero is the kind of work the studio sells, so a visitor who
asks "can you build us something like this?" is a lead too.

## 2. Success criteria

| Measure | Target |
|---|---|
| Brief submissions | Every submission reaches the studio inbox **and** the Google Sheet within 1 minute |
| Mobile experience | Hero works and the page is fully usable on iPhone Safari, Android Chrome and iPad, portrait and landscape |
| Speed | Largest Contentful Paint < 2.5 s on a mid-range phone over 4G; Lighthouse mobile performance ≥ 85 (stretch 90), desktop ≥ 95 |
| Quality | Lighthouse accessibility ≥ 95, SEO = 100; no console errors on any page |
| Editability | Adding, removing or reordering a film is a one-file edit plus one script run, with no code changes |
| Honesty | Every statistic on the site has a named source; any missing fact shows as a visible placeholder until filled |

## 3. Decisions already made

These came out of the brainstorming and the mockup rounds:
- **Direction D:**
  - Black + ivory with one sea-cyan glow (`#4FE3D0`).
  - Bodoni Moda italic for display, Hanken Grotesk for body, IBM Plex Mono for labels.
  - Headlines fade from ivory to transparent ("half-fade") and carry a soft glow.
- **The hero is real-time 3D, not a pre-rendered video.**
  - It is lighter than a video background and responds to the visitor.
  - Runway is not needed for the hero; a screen-recorded teaser of the hero for LinkedIn is a later use.
- **The narrative is a sales page,** in this order:
  1. problem
  2. what one film does
  3. sourced proof
  4. which film you need
  5. case study
  6. what you get
  7. objections
  8. brief
- **Full films are hosted on Gumlet.** The short silent loops on the crystal ship with the site. The player adds
  no caption tracks; films play exactly as published.
- **Hosting: Railway behind Cloudflare.**
  - Railway runs the site and the brief endpoint, auto-deploying from GitHub like Gillfins.
  - Cloudflare (free) sits in front for DNS, a worldwide cache, SSL, bot protection and analytics.
- **No pricing on the site.** Content Lab (research, ideas, scripts) is offered in the form and quoted on the call.

## 4. Site map

| Page | Purpose |
|---|---|
| `/` | The sales page with the 3D hero (sections in §5) |
| `/work` | Every film, filterable by type (product demo, explainer, …, 3D website) |
| `/work/<slug>` | One case study per film: problem → angle → film → results |
| `/brief` | The full brief builder on its own page (the link to put in LinkedIn DMs and bios) |
| `/thanks` | Shown after a brief is sent: what happens next, plus the booking link |
| `/privacy` | What the form collects, where it goes, how long it is kept, how to delete it |
| `404` | On-brand "lost at sea" page with a link home |

The navigation shows Films we make · Work · Case study · **Start a brief**. The brief button
appears in the nav, in the hero, after the proof section and at the end of the page. It is the same action every time.

## 5. Home page, section by section

The copy is the board D copy, which is approved in direction. Items in `[brackets]` are placeholders
you need to fill (see §18).

1. **Hero (3D).**
   - On screen: "Videos that make your company" (HTML), then the giant "make sense." drawn inside the 3D scene and bent by the glass.
   - Pitch line: *"Your buyers won't read the page. They will watch ninety seconds. We make those ninety seconds."*
   - Buttons: Start a brief / Which film do you need?
   - The film info block shows the current film; the crystal turns to it (§7).
   - The real `<h1>` holds the full sentence for search engines and screen readers.
2. **The quiet problem.** Headline: "Great products lose to clearer ones." Three pains follow:
   - The homepage lists features but the buyer wants the outcome.
   - The founder repeats the same pitch on every call.
   - Posts get a scroll, not a stop.
3. **What one film does.** Headline: "One film. Four jobs, every day." The four cards are **Explains · Travels · Converts · Repeats**.
4. **Proof.** Headline: "People already use video to decide. The question is whose." Four figures with
   their source line:
   - 96%: people who have watched an explainer to learn about a product.
   - 85%: people convinced to buy by a video.
   - 85%: marketers who say video generated leads.
   - 83%: marketers who say video increased sales.
   - Source line: Wyzowl 2026 (§Appendix). No other numbers appear without a source.
5. **Which film do you need?** Six film types, each labelled by funnel stage:
   - Awareness: LinkedIn series, Launch film.
   - Understanding: Explainer, Product demo.
   - Trust: About the company.
   - Decision: Customer case study.
   - Each item links to `/brief?film=<type>` so the form arrives pre-filled.
6. **Case study teaser.** Jev vs Laya: problem / angle / film, a result row `[impressions] [comments] [inbound DMs]`, and a link to `/work/jev-vs-laya`.
7. **What you get + how it works.**
   - Deliverables: one film **up to 3 minutes** (most 60–120 s; longer is out of scope), four shapes (16:9, 1:1, 4:5, 9:16), burned-in captions, thumbnail and post copy, the script.
   - Process: discovery call → story & script → style frames → film & delivery, with `[two]` rounds of changes.
   - Content Lab callout.
8. **Objections.** Six short answers:
   - No footage needed.
   - Don't know what to say → Content Lab.
   - Style frames first, so it looks like you.
   - "How long is a film?": up to 3 minutes, with Wyzowl 2026's figure that 71% find 30 s–2 min most effective, and the `[2–4 weeks]` turnaround.
   - Any time zone.
   - You own the film.
9. **Final call to action + brief.** Headline: "Your next customer is one film away." The full brief builder (§9) is embedded here.
10. **Footer.**
    - Big half-faded wordmark (the 3D metal logo comes after the logo is designed).
    - Social links, `[hello@yourstudio.com]`.
    - The line "Named after the sea sparkle that glows at night" (changes with the name).

## 6. Visual design system

All values live in one `tokens.css`. No colour or font is written inline in components.

- **Colour:**
  - `--ink #030405` (ground)
  - `--ivory #ECEAE4` (text)
  - `--mist #A9ADAB` (secondary text)
  - `--dim #8E9496` (labels)
  - `--sea #4FE3D0` (the only accent: glow, active states, focus rings)
  - `--line rgba(236,234,228,.14)` (hairlines)
  - The site is dark-only by design.
- **Type:**
  - Display: Bodoni Moda italic. Body: Hanken Grotesk 300–600. Labels: IBM Plex Mono uppercase with 0.16–0.2em tracking.
  - Fonts are **self-hosted** (woff2 subsets) instead of Google Fonts, for speed and EU privacy.
  - Scale: display `clamp(40px, 5vw, 76px)`, section titles in the same family, body 16–19px, labels 11–12px.
- **Glow system (site-wide):**
  - Every box, field and button shares the lit edge of the brief's choice wheel.
  - Shape: 14–18 px rounded corners and a sea-cyan border.
  - Resting glow (`--glow-soft`): a faint outer halo plus a faint inner glow.
  - Active glow (`--glow`, used on hover, focus and selected items): a 22 px cyan halo, a wide 64 px soft halo and an inner glow.
  - Inputs are rounded glowing boxes, not underlines.
  - List rows ("Which film", "Every film") light up as rounded glowing boxes on hover.
  - Tokens: `--radius`, `--glow-edge`, `--glow-edge-soft`, `--glow`, `--glow-soft`.
- **Signature treatments:**
  - Half-fade headline (ivory → transparent gradient clipped to text).
  - Sea-cyan text glow on the italic words.
  - Hairline-ruled lists instead of cards.
  - The ivory primary button with a cyan halo.
- **Motion:**
  - One orchestrated moment: the hero intro (the crystal rises, rings ripple out).
  - Elsewhere, only small fades on scroll, which start from a visible state.
  - Everything respects `prefers-reduced-motion`.
- **Layout:**
  - Content max-width 1360px, side gutter `clamp(20px, 4vw, 56px)`.
  - Grids collapse to one column on phones.
  - No horizontal scroll at any width.

## 7. The 3D hero

The prototype in `hero-prototype/page.html` is the behaviour reference. Its logic is ported into
modules, not redesigned.

### 7.1 Scene

| Part | How |
|---|---|
| Night sea | Large mirror plane (three.js `Reflector`) with a custom shader: slow anisotropic ripples, fresnel, distance fade. It reflects only the crystal; the particles and headline sit on a layer the mirror ignores. |
| Plankton | Points on the water surface (4.5k / 8k / 12k by device). Each glows from a base level, a twinkle, the cursor trail (last 32 positions, age-decayed) and expanding rings. Intensity is capped so bloom stays round. |
| Crystal | A box with four video faces (the first four films in the list) inside a rounded glass box. The glass is `MeshPhysicalMaterial` with transmission, thickness and dispersion (desktop only). It uses its own studio-light environment map. |
| Headline | "make sense." drawn to a canvas texture behind the crystal, so the glass refracts real type. It is one line on wide screens and stacked on portrait screens, sized by both screen width and height. |
| Post | Bloom (UnrealBloomPass) and Neutral tone mapping, so film colours stay true. |

### 7.2 Interactions

- **Move:**
  - The sea lights up wherever the pointer or finger passes.
  - After 3 seconds idle, an automatic "swimmer" path demonstrates the effect.
- **Hover the crystal:** it turns toward the pointer (±0.5 rad), and the cursor shows "grab".
- **Drag the crystal:**
  - It spins with the drag. On release it settles on the nearest film.
  - A flick can carry it at most one extra film.
  - A tap (under 6 px of movement) opens the film.
- **Scroll:**
  - The hero is pinned for 280vh. Scrolling down turns forward and scrolling up turns back.
  - The films loop, so the crystal never gets stuck.
  - At the very top of the page, scrolling up still steps back one film.
- **Each turn:** a ring of light crosses the water, and the film info block updates (title, type, length, 4 ticks).
- **Tap / "Watch this film":**
  1. The facing film flies to the front, the glass thins out and the rest of the scene dims.
  2. A real `<video>` player lands exactly on the screen, with title, previous / next and close.
  3. Arrow keys move between films and Esc closes.
  4. Closing returns the crystal to the sea, still facing the last film watched.
  5. The page does not jump.

### 7.3 Device tiers and performance

| Tier (detected from pointer type + screen size) | Particles | Glass colour split | Films decoding | Max pixel ratio / pixel budget |
|---|---|---|---|---|
| Phone | 4,500 | off | only the facing film | 1.5 / 1.6 MP |
| Tablet / iPad | 8,000 | off | all four | 1.5 / 2.6 MP |
| Laptop / desktop | 12,000 | on | all four | 1.75 / 3.7 MP |

- **Adaptive quality:** if the average frame time over 90 frames exceeds 24 ms, resolution drops by 15% (floor 60%) and the glass colour split turns off.
- **Pausing:** rendering stops when the hero is off-screen or the tab is hidden.
- **Framing by screen shape:**
  - Portrait: stacked headline, centred crystal.
  - Near-square (iPad landscape): smaller crystal.
  - Wide: crystal to the right.
  - Ultrawide: headline capped at about 1.4× screen height.
  - Short landscape (phone on its side): compact UI.
- **Loading order:**
  1. The page first paints a still poster frame of the hero plus the HTML text. This poster is the LCP element.
  2. The 3D code loads as a deferred module and cross-fades in when the first frame is ready.
  3. The film loops load after the scene is up.

### 7.4 Fallbacks and accessibility

- **No WebGL** (old devices, blocked GPU): the poster frame stays, and everything else works.
- **Reduced motion:** no intro rise, no swimmer, no easing; scroll still changes films.
- **Text and controls:**
  - All hero text and controls are real HTML.
  - The canvas is `aria-hidden`.
  - "Watch this film" is a real button, and the player is a labelled dialog with focus moved to its close button.

## 8. Films: content model and how to change them

Films live in one ordered list, `src/content/films.json`, loaded as an Astro content collection. **The
first four films sit on the crystal, in order.** `/work` shows them all.

```json
{
  "slug": "jev-vs-laya",
  "title": "Jev vs Laya",
  "type": "product-comparison",
  "length": "1:53",
  "loop": "/media/loops/jev-vs-laya.mp4",
  "poster": "/media/posters/jev-vs-laya.jpg",
  "full": "https://video.gumlet.io/<collection>/<asset>/main.m3u8",
  "caseStudy": true
}
```

- **To add a film:**
  1. Run `tools/make_highlight.sh <video> <slug> <t1> <t2> <t3>`. It writes the crystal loop: the film's three best moments, 3.2 s each, joined with soft fades (≈ 9 s, 960×540, silent, ≈ 300–450 KB), plus a poster. For a single moment, `tools/make_loop.sh` still works.
  2. Add an entry to the list and paste the Gumlet link.
- **To remove or reorder:** edit the list.
- **The schema is validated at build time,** so a missing field or bad link type fails the build instead of shipping a broken page.
- **Case studies** are Markdown files in `src/content/cases/<slug>.md` with frontmatter for problem, angle, results (each result either a number or a placeholder) and an optional client quote.

## 9. Lead capture: the brief

### 9.0 Where visitors fill it in

There is **one** brief form, and it lives in two places:
- **The end of the home page** (`#brief`), so a reader who scrolls the whole sales page never leaves it.
- **Its own page, `/brief`,** for sending directly in LinkedIn DMs, email signatures, your bio and ads.

Every route leads to that same form:

| Entry point | Where | What it does |
|---|---|---|
| "Start a brief" button | Nav on every page, the hero, after the proof section, the footer | Scrolls to `#brief` on the home page; opens `/brief` on other pages |
| "Which film do you need?" items | Home section 5 | Opens the form with that film type already ticked (`?film=product-demo`) |
| Case study pages | End of each `/work/<slug>` page ("Want a film like this?") | Opens `/brief?film=<that film's type>` |
| Content Lab callouts | Home sections 7 and 8 | Opens the form with "I need research and ideas" ticked |
| Direct link | `/brief` shared anywhere | Same form; UTM tags show where the lead came from |

After sending, every brief goes to three places at once: your inbox, the Google Sheet, and an
auto-reply to the lead. The visitor lands on `/thanks`.

### 9.1 The choice wheel (how every list in the form works)

Every pick-one or pick-several question is a **wheel**, not a dropdown or a row of buttons:
- **Layout:**
  - The options sit in a vertical list five rows tall (three rows for the WhatsApp code).
  - A lit box in the middle marks the answer. It has **rounded corners (16 px radius)**, a sea-cyan border with a visible glow (inner glow plus a wide outer halo) and a small glowing dot at each end.
- **Motion:**
  - Scrolling, dragging with a thumb, using the trackpad or tapping an option rolls the list. It snaps so one option always sits in the box.
  - Options above and below fade out toward the top and bottom edges, and tilt back slightly like a drum.
  - The option in the box turns ivory with a cyan glow; the rest stay grey.
- **Multi-pick lists** (the film types):
  - Each option has a small tick box. Tapping the option in the lit box adds or removes it.
  - Picked films also show as removable tags under the wheel.
  - If the visitor moves on without ticking anything, the option in the box counts as picked.
- **Text that can't be picked from a list** (name, email, company, website, links, notes) stays as plain underlined inputs.
- **Accessibility:**
  - Each wheel is a real `listbox`; options are `option` items with `aria-selected`.
  - Keys: ↑/↓ move, Home/End jump to the ends, Enter or Space ticks on multi-pick wheels.
  - Focus is shown on the lit box.
  - With reduced motion, the tilt and smooth scrolling turn off but the list still works.
- **Reliability:**
  - The answer is read from the wheel's actual position when the visitor moves between steps or sends, so a half-finished scroll still counts.
  - Hidden steps keep their answers.
- **Phones:** rows are 50 px tall and text is 21 px; on desktop, 56 px and 24 px.
- **Reference:** the working version is in `hero-prototype/page.html` (section `#brief`), and board "Brief · five steps" on the canvas.

### 9.2 The form (five short steps, one screen each on phones)

1. **You**:
   - Wheel: Startup / Established company / Founder or CEO (personal brand) / Agency / Other
   - Company name
   - Website or LinkedIn
2. **The film**:
   - Multi-pick wheel: Product demo, Explainer, About the company, Customer case study, Launch film, LinkedIn series, 3D website, Not sure yet.
   - Then a **Goal** wheel: More leads / Launch / Fundraising / Hiring / Brand awareness / Sales enablement / Other.
3. **Content**:
   - Wheel: I have a script / I have an idea / I need research and ideas (Content Lab).
   - Link to logo and assets (optional).
   - Anything else (optional).
4. **Timing** (wheel): As soon as possible / 2–4 weeks / 1–2 months / Just exploring.
5. **Contact**:
   - Name and work email (plain inputs).
   - **Country** (optional): **type it or scroll**. A text box with suggestions sits above a wheel listing every country (≈ 245, names from the browser in English, alphabetical, with "Choose your country" first).
     - Typing (a name, a short name such as UAE, USA, UK or KSA, or a dialling code) snaps the wheel to the match.
     - Scrolling the wheel fills in the box.
     - Long jumps land instantly; short moves glide.
     - It starts on the visitor's own country when their browser language includes a country (e.g. en-AE).
   - **WhatsApp** (optional):
     - A typed code box ("+971", with suggestions) and the number box sit in one row. Below them is a three-row wheel of every dialling code, shown as "+971 · United Arab Emirates" in the body font. Typing and scrolling stay in step.
     - **Every time the country changes, the code switches to that country's code.** If the visitor then changes the code by hand, their choice stays until they pick another country.
     - An unknown typed code shows "We don't recognise that code".
     - Shared codes go to the main country first (+1 → United States, +44 → United Kingdom, +7 → Russia).
     - A number without a code shows "Pick your country code".
   - Consent checkbox linking to `/privacy`.

Further behaviour:
- **Pre-fill:** `?film=<type>` from the "Which film" links.
- **Tracking source:** UTM parameters from the visitor's landing URL ride along with the submission, so you can see which LinkedIn post a lead came from.
- **Drafts:** a refresh does not lose answers (draft saved in the visitor's browser only).
- **Validation:**
  - Inline, on each step.
  - Email format is checked.
  - URLs are normalised (`acme.com` → `https://acme.com`).

### 9.3 Where a brief goes

```
browser ──POST /api/brief──▶ Cloudflare (not cached) ──▶ Railway: Astro server endpoint
                               1. verify Turnstile token (invisible bot check) + honeypot field
                               2. validate and clean every field
                               3. in parallel:
                                  a. email the studio ("New brief: Acme · Product demo")      ── Resend
                                  b. append a row to the "Briefs" Google Sheet                ── Apps Script webhook
                                  c. auto-reply to the lead: what happens next + booking link  ── Resend
                               4. answer { ok: true } ──▶ browser goes to /thanks
```

- **Duplicates:** each submission carries a client-made ID, so a double click is stored once.
- **Partial failure counts as success** if either the studio email (a) or the Sheet row (b) succeeded. The failure is logged, and the lead still sees `/thanks`.
- **Total failure** (both a and b fail): the form stays filled and shows:
  - "We couldn't send this. Please email `[hello@…]`."
  - The address as copyable text.
  - A "Try again" button.
- **Secrets** (Resend key, Sheet webhook URL and token, Turnstile secret) live only in Railway's environment variables, never in the site code.
- **Privacy:**
  - `/privacy` states what is collected, that it goes to the studio inbox and a private Sheet, a 24-month retention period, and deletion on request.
  - Analytics are cookieless, so no cookie banner is needed.

### 9.4 After sending

`/thanks` shows:
- "We reply within `[24 hours]`".
- The three next steps.
- A **Book a 30-minute call** link (Cal.com), which is optional and can be added later.

## 10. Video hosting and playback

- **Full films:**
  - Hosted on Gumlet (adaptive HLS, plus MP4 if enabled).
  - The player uses Gumlet's `.m3u8` link with native HLS on Safari/iOS and hls.js elsewhere. hls.js is loaded only when a film is first opened (≈ 150 KB).
  - If a stream fails, the player falls back to the film's loop and shows a quiet "Couldn't load the full film" note.
- **No caption tracks:** the player adds no subtitles or caption files; films play exactly as published.
- **Loops and posters** ship with the site (≈ 1 MB for four films) and are cached worldwide by Cloudflare.
- **Prerequisite:** upload the four masters to Gumlet (the "Demo Collection" workspace) with public playback.

## 11. Architecture and stack

| Concern | Choice | Why |
|---|---|---|
| Site framework | **Astro 5** with the Node adapter | Every page is pre-built as plain HTML (fast, readable by search engines); only `/api/brief` runs on the server. Content collections hold films and case studies |
| 3D | three.js (pinned version) as one hero module, loaded deferred | Same engine as the prototype |
| Hosting | **Railway** (one service, auto-deploys on every push to GitHub, like Gillfins) | Familiar setup; runs the site and the form endpoint together |
| In front of Railway | **Cloudflare** (free plan), proxying the domain | DNS, a worldwide cache for pages, images, loops and fonts, SSL, DDoS protection. `/api/*` is never cached |
| Form backend | Astro server endpoint `src/pages/api/brief.ts` on Railway | No separate server to maintain |
| Email | Resend (free tier: 3,000 emails/month) | Needs DNS records on the final domain (added in Cloudflare) |
| Lead list | Google Sheet + Apps Script webhook | The Sheet is the CRM, so no database is needed |
| Bot protection | Cloudflare Turnstile (invisible) + honeypot | No puzzles for real visitors |
| Analytics | Cloudflare Web Analytics (cookieless, free) | Page views and sources at launch; funnel events can be added later |
| Domain | Registered at Namecheap (as for gillfins.com); its nameservers point to Cloudflare | The domain itself stays at Namecheap |
| Code | Private GitHub repo `studio-site` | |

**How the two connect:**
- Cloudflare's DNS points the domain to the Railway service, with the proxy (orange cloud) on and SSL mode
  "Full (strict)", so Railway's own certificate is used end to end.
- A cache rule caches `/_astro/*`, `/media/*`, `/fonts/*` and images for a long time. HTML gets a short cache
  that is purged on each deploy. `/api/*` bypasses the cache.
- Until the final domain exists, previews run on the `*.up.railway.app` address without Cloudflare.

### Folder layout

```
Studio-Site/
  site/
    src/
      config/site.ts          ← studio name, email, city, reply time, turnaround: one place to change
      content/films.json      ← the film list (§8)
      content/cases/*.md      ← case studies
      components/hero/        ← sea.ts, plankton.ts, crystal.ts, headline.ts, player.ts, tiers.ts, hero.ts
      components/sections/    ← one .astro file per home section
      components/brief/       ← the five-step form
      pages/                  ← index, work/index, work/[slug], brief, thanks, privacy, 404
      pages/api/brief.ts      ← the only server-run route
      styles/tokens.css
    public/media/loops/, public/media/posters/, public/fonts/, public/og/
    tests/                    ← Playwright + unit tests
    tools/make_loop.sh
  hero-prototype/             ← frozen reference
  mockups/                    ← canvas sources and stills
  docs/superpowers/specs/     ← this file
```

## 12. Performance budget (home page)

| Item | Budget |
|---|---|
| HTML + CSS + fonts before first paint | < 120 KB compressed |
| Hero poster (LCP) | < 90 KB (AVIF, JPEG fallback) |
| 3D code (three.js + hero) | < 200 KB compressed, deferred |
| Film loops | ≈ 1 MB, loaded after the scene; phones fetch only the facing film first |
| Total before any click | Desktop < 2.5 MB, phone < 1.5 MB |
| Layout shift | CLS < 0.05 |

## 13. Search and sharing

- Every page gets its own title and description.
- The home page has `Organization` structured data. Each film page has `VideoObject` data (name, thumbnail, duration, content URL).
- Share preview: a 1200×630 still of the hero, plus each case study's own still.
- `sitemap.xml`, `robots.txt` and canonical URLs. The site is English only for v1.

## 14. Accessibility

- Text contrast is at least 4.5:1 (the `--mist` and `--dim` tokens are checked against `--ink`).
- Visible cyan focus rings, a skip link to the main content, and 44 px minimum touch targets.
- The form uses real labels, `fieldset`/`legend` for each choice group, and announces errors.
- The player is keyboard-operable (play/pause, previous/next, Esc to close).

## 15. Testing and how we know it works

1. **Unit tests:**
   - Form validation and URL clean-up.
   - The `/api/brief` handler with the email and Sheet calls mocked: success, partial failure, total failure, duplicate ID, bot rejection.
2. **Browser tests** (Playwright: Chromium desktop, iPhone WebKit, Android Chrome emulation). Each run checks:
   - Every page loads with zero console errors.
   - The hero canvas is not blank.
   - Scrolling, dragging and the "Watch" button each change or open the right film.
   - The brief flow completes against a mock endpoint and lands on `/thanks`.
   - axe accessibility scan passes.
3. **Hero at seven screen sizes:** 375×812, 844×390, 768×1024, 1024×768, 1366×768, 1440×900 and 2560×1080. Screenshots are compared by eye, the same matrix as the prototype.
4. **Real devices:** iPhone Safari, an Android phone, iPad, and a Mac and a Windows laptop if available. Includes a Lighthouse run on mobile and desktop against §2.
5. **Live form test after launch:** one test brief must land in the inbox and the Sheet, and the auto-reply must arrive. The test row is then deleted.
6. **Cloudflare check after launch:**
   - Static files come back with a cache HIT.
   - `/api/brief` is never cached.
   - The site answers over HTTPS with no redirect loop.

## 16. Build phases

| Phase | Delivers | Ends when |
|---|---|---|
| 1. Foundation | Astro project, tokens, self-hosted fonts, every home section with real copy (poster image in place of 3D), `/privacy`, preview deploy on Railway | Preview link (`*.up.railway.app`) works on phone and desktop |
| 2. Hero | Prototype ported into modules, film list collection, poster-to-3D hand-off, device tiers, Gumlet HLS player | Hero passes the seven-size check and the real-device check |
| 3. Brief | Five-step form, `/api/brief`, Resend emails, Sheet, Turnstile, `/thanks`, `/brief` page | A real test brief arrives in the inbox and Sheet |
| 4. Work | `/work` with filters, case study pages, `VideoObject` data | Jev vs Laya case study page complete |
| 5. Launch | Search and sharing, analytics, performance pass, full test matrix; domain nameservers moved to Cloudflare, proxy and cache rules on, email DNS for Resend | Lighthouse targets met on the live domain; the Cloudflare check passes |
| Later | Final name and logo, 3D metal logo in the footer, hero teaser video for LinkedIn, more case studies | n/a |

The name is not needed until phase 5. Until then the site runs under the working name, which is a
single config value.

## 17. Not in v1

- Prices or packages.
- A blog.
- An admin screen for editing content (films are edited in the list file).
- Multiple languages.
- A client portal.
- Online payments.
- Making the 4:5 and 9:16 social cuts of the portfolio films. That's production work, not site work, but it is recommended before marketing starts.

Legal and privacy groundwork (privacy notice, contract clauses, asset rights, business set-up) lives in the separate *Studio Legal & Privacy Guide* doc.


> **Brief delivery (2026-10-12):** until the Astro server exists, the form posts to a Google Apps Script web app in storyglassstudio@gmail.com (`hero-prototype/tools/apps-script/Code.gs`, setup in `SETUP.md`). It appends to a 'Briefs' Sheet, emails the studio with Reply-To set to the lead, and sends the lead a confirmation. Spam: honeypot, 2.5 s minimum fill time, 3 briefs per email per hour, formula-safe cells. With no endpoint set, the form falls back to a prefilled mailto:. Resend on Railway can replace it later without changing the form.

## 18. Inputs needed from you

| # | Needed | Needed by |
|---|---|---|
| 1 | Domain for Storyglass Studio (name chosen) | Phase 5 |
| 2 | The inbox that receives briefs, and the address replies come from | Phase 3 |
| 3 | Reply-time promise, usual turnaround, number of revision rounds, your city | Phase 1 (placeholders until then) |
| 4 | Real LinkedIn numbers for Jev vs Laya (impressions, comments, inbound DMs), or drop the results row | Phase 4 |
| 5 | A free Cloudflare account (needed for the bot check in phase 3 and the domain in phase 5); Railway is already set up | Phase 3 |
| 6 | Four masters uploaded to Gumlet with public playback | Phase 2 |
| 7 | Cal.com booking link, or no booking step for now | Phase 3 |
| 8 | Should the brief ask for a budget range? Default: **no** | Phase 3 |
| 9 | OK to show the Gillfins site and your 3D portfolio as "3D website" work? | Phase 4 |
| 10 | Show a WhatsApp contact publicly? Default: only an optional field in the form | Phase 3 |

**Recommended, not blocking:** before marketing starts, add one B2C product film (Gillfins is ready-made) and
one on-camera founder film to the portfolio, plus vertical cuts. These close the gaps from the video
review.

## Appendix: sources

- Wyzowl, *Video Marketing Statistics 2026* (survey of 266 marketers and consumers, late 2025):
  https://wyzowl.com/video-marketing-statistics/. The page was checked on 2026-10-09 and the figures were quoted
  verbatim: 96% watched an explainer to learn about a product, 85% convinced to buy by a video, 85% of
  video marketers say video helped generate leads, 83% say it directly increased sales.
