# Wedding invitation audit

Audited: 2026-11-12. Scope: static, read-only inspection of this project. No project files were changed during inspection. Browser screenshots were not produced because Playwright/Puppeteer and a browser executable are unavailable; visual notes are inferred from source, not rendered appearance.

## 1. File inventory

Project tree (excluding `node_modules` and `.git`):

```text
web-wedding-invitation/
├── index.html
└── assets/
    ├── images/
    │   ├── curtains.webp
    │   ├── football-pitch.webp
    │   ├── henna.webp
    │   └── royal-door.webp
    └── videos/
        ├── flying-doves.webm
        ├── hand-catching.webm
        ├── rings.webm
        └── roses.webm
```

Only `index.html` exists as project code. `ffprobe` is not installed. Image dimensions are from Pillow; video resolution, duration, and codec identification are from OpenCV/container FOURCC. Alpha status is **unknown** because these tools do not reliably report VP9 alpha encoding and ffprobe was unavailable.

### Images

| File | Size | Dimensions | Mode | >500 KB |
|---|---:|---:|---|---|
| `assets/images/curtains.webp` | 858,996 B (839 KB) | 1536×2752 | RGB | Yes |
| `assets/images/football-pitch.webp` | 506,284 B (495 KB) | 1536×2752 | RGB | No (under 500 KiB; over 500,000 decimal bytes) |
| `assets/images/henna.webp` | 576,942 B (563 KB) | 1536×2752 | RGB | Yes |
| `assets/images/royal-door.webp` | 1,379,164 B (1.32 MiB) | 1536×2752 | RGB | Yes |

Threshold interpretation: 500 KB is treated as 500 KiB (512,000 bytes); the football image is just below that threshold. All images share a tall 9:16-like aspect ratio (1536:2752, about 0.558).

### Videos

| File | Size | Resolution | Duration | Codec | Alpha channel |
|---|---:|---:|---:|---|---|
| `assets/videos/flying-doves.webm` | 718,908 B (702 KB) | 1280×720 | 10.04 s | VP9 (VP90) | Unknown |
| `assets/videos/hand-catching.webm` | 480,023 B (469 KB) | 720×1280 | 10.04 s | VP9 (VP90) | Unknown |
| `assets/videos/rings.webm` | 1,138,709 B (1.09 MiB) | 720×1280 | 10.04 s | VP9 (VP90) | Unknown |
| `assets/videos/roses.webm` | 853,216 B (833 KB) | 720×1280 | 10.04 s | VP9 (VP90) | Unknown |

All are below 3 MiB (3,145,728 bytes). They report 24 fps and 241 frames in local decoding. Alpha encoding is not inferable from the filename or the decoded color frames.

### Expected asset names

| Expected name | Status | On disk / detail |
|---|---|---|
| `images/door-left.webp` | DIFFERENTLY NAMED | `images/royal-door.webp` is used for both door halves |
| `images/door-right.webp` | DIFFERENTLY NAMED | Same shared `images/royal-door.webp` |
| `images/curtain-left.webp` | DIFFERENTLY NAMED | Shared `images/curtains.webp` is mirrored for right |
| `images/curtain-right.webp` | DIFFERENTLY NAMED | Same shared `images/curtains.webp` |
| `images/henna-hands-bg.webp` | DIFFERENTLY NAMED | `images/henna.webp` |
| `images/football-pitch-bg.webp` | DIFFERENTLY NAMED | `images/football-pitch.webp` |
| `images/banquet-hall-bg.webp` | MISSING | No banquet image; dinner uses a CSS radial gradient |
| `images/walima-pencil-art.webp` | DIFFERENTLY NAMED | No image file; inline SVG illustration in `index.html` line 31 |
| `videos/holding-hands-loop.webm` | DIFFERENTLY NAMED | `videos/hand-catching.webm` |
| `videos/interlocking-rings.webm` | DIFFERENTLY NAMED | `videos/rings.webm` |
| `videos/flying-doves.webm` | PRESENT | `videos/flying-doves.webm` |
| `videos/falling-roses.webm` | DIFFERENTLY NAMED | `videos/roses.webm` |

No referenced local asset path was found missing from disk. There are no image poster attributes. Video elements have `aria-label`, but that is not a substitute for a poster or visual fallback.

## 2. Code structure

The site is one 50-line `index.html` with long, minified-style lines; there are no separate CSS or JS files. Main blocks:

- Lines 1–8: document head, metadata, Google Fonts, Tailwind CDN/config, GSAP and ScrollTrigger CDNs.
- Lines 9–11: inline CSS, layout, media and animation styles, mobile and reduced-motion rules.
- Lines 12–14: body/main wrapper.
- Lines 15–34: all 13 invitation sections.
- Line 35: closing main wrapper and live toast container (toast is not used by JS).
- Lines 36–48: inline JavaScript (entrance, countdown, scroll effects, calendar download and RSVP).
- Lines 49–50: close script/body/html.

Tailwind CDN: `https://cdn.tailwindcss.com` (unversioned/latest CDN URL; exact resolved version is unknown). Config at line 6 extends colors `navy #0B1D3A`, `gold #C9A227`, `offwhite #F8F7F4`, `emerald #16A34A`, `crimson #DC2626`; fonts are DM Serif Display and Figtree. Google Fonts request DM Serif Display and Figtree weights 300–700. GSAP and ScrollTrigger both use CDN version 3.12.5 (lines 7).

### Section-by-section structure and motion

| # | Section (line) | ID / notable class | Assets | Animation | Completeness |
|---:|---|---|---|---|---|
| 1 | Entrance (15) | `#entrance`, `.entrance-core` | `royal-door.webp` on both door halves; inline SVG lamp/calligraphy | GSAP entrance timeline; no ScrollTrigger | Complete interaction, but identical door halves and decorative calligraphy SVG rather than real Arabic calligraphy |
| 2 | Countdown (23) | `#countdown` | None | None | Complete; time target is hard-coded |
| 3 | Holding-hands / family invitation (24) | `#bond` | `hand-catching.webm` | ScrollTrigger reveal elements; background video runs independently | Complete; video is background atmosphere, copy is static |
| 4 | Curtains / name reveal (25) | `#unveiling` | `curtains.webp` shared and mirrored | Two scrubbed curtain tweens; each requests pin on same section | Weak: text and backdrop exist; overlapping pin triggers may interfere |
| 5 | Rings and prayer (26) | `#prayer` | `rings.webm` | None | Complete, but no specific video fallback |
| 6 | Sa Lalle & Kamu (27) | `#henna` | `henna.webp`, `flying-doves.webm` | None | Complete event card; venue/address is only “Arewa Garden · Kano, Nigeria” |
| 7 | Football match (28) | `#football` | `football-pitch.webp` | Scrubbed background scale/parallax | Complete event card |
| 8 | Wedding dinner (29) | `#dinner` | CSS radial gradient only; no banquet asset | Scrubbed gradient-background scale | Complete copy, but background is a synthetic gradient rather than hall image |
| 9 | Fatiha (30) | `#fatiha` | `roses.webm`, inline architectural SVGs | None | Complete event card; no poster/fallback |
| 10 | Walima (31) | `#walima` | Inline table SVG; no walima image | ScrollTrigger one-time reveal | Complete illustration and copy, but illustration is deliberately simple/flat |
| 11 | Save the Date (32) | `#save-date` | None | None | Complete; creates and downloads a local `.ics` calendar file |
| 12 | RSVP (33) | `#rsvp` | None | None; thank-you panel animates with GSAP after submit | Functional demo only; no backend or persistence despite fields being accepted |
| 13 | Closing blessing (34) | `#blessing` | Inline Arabic text | ScrollTrigger scrub fades inner content to 15% opacity | Complete blessing copy; fade-to-black is only an overlay/fade near the bottom, not a full terminal fade |

None is an empty stub. Some are weak relative to the requested realistic/3D direction; see the summary table.

## 3. Problems and findings

### Runtime and behavior

- `index.html:44`: when ScrollTrigger is available, two separate curtain tweens each set `pin:true` for the same `#unveiling` trigger. This can create duplicate pin spacers/competing pin behavior and should be treated as a likely scroll layout defect. Use one pinned timeline/trigger for both curtains.
- `index.html:44`: scroll triggers are created as soon as the inline script runs, before window load and before media has necessarily settled. ScrollTrigger often refreshes automatically on load/resize, but there is no explicit refresh after media dimensions/layout changes. The image backgrounds are CSS backgrounds, so their intrinsic loading does not reserve or alter element size; video decoding and font swaps may still shift perceived layout.
- `index.html:42`: reduced-motion branch hides the doors and reveals hero text, but does not hide `#entranceHint`; “Tap to begin” remains over the complete entrance. More seriously, it disables all ScrollTrigger initialization and does not hide/open the curtains, so `#unveiling` curtains remain over the content and can obscure its text for reduced-motion users.
- `index.html:45`: `const pad` is declared but never used (not a runtime failure). Toast markup/style is also unused. No apparent missing selector errors with the current markup.
- `index.html:43`: countdown targets `2026-12-31 10:00 +01:00`, aligned with the Fatiha date/time and Africa/Lagos. All listed weekdays match the 2026 calendar. Since the audit date is 2026-11-12, it is counting toward a future date. Whether those names, date and event details are correct in the real world is unknown.
- `index.html:45`: Save the Date button creates a valid-looking local `.ics` download with a start at 10:00 and end at 22:00, but it represents one long event at Sapphire Event Hall, not all five events. `URL.revokeObjectURL` runs immediately after triggering the download, which can race download consumption in some browsers.
- `index.html:46`: RSVP intercepts submit, checks browser validity, hides the form and shows a thank-you panel. It does not send or save the response; this matches the visible “demo keeps your response on this device only” text, though it does not actually persist locally. No HTML form `action` fallback exists.
- No obvious JS syntax errors from static inspection. Browser console behavior was not executed/verified.

### Asset paths, accessibility and media

- The local asset paths that are actually referenced exist. Most target-spec filenames are differently named (inventory above); this is a naming/spec mismatch, not a broken path.
- `index.html:27–28`: the two background `<img>` elements have alt text even though they are decorative backgrounds. Consider empty alt text if decorative; the henna alt says only “Henna celebration detail.” The entrance CSS background images have no semantic equivalent or alt text. Inline meaningful SVGs at lines 15 and 31 do have accessible labels; decorative SVGs are hidden from assistive technology.
- `index.html:24,26–27,30`: all four video elements specify `autoplay muted loop playsinline preload="metadata"`, suitable for muted inline autoplay in many browsers. No `poster`, alternate `<source>`, or Safari/iOS fallback exists. WebM/VP9 (especially alpha VP9, if present) is not a dependable cross-browser/iOS delivery format; alpha status is unknown. Provide a compatible non-alpha fallback/poster and test on Safari/iOS.
- Four videos are eligible to play at once: bond background, ring video, doves overlay, roses overlay. They are spread across scroll sections and each has autoplay/loop with no visibility pausing. Browsers may pause offscreen video opportunistically, but code does not limit simultaneous decoding. Their combined sizes are about 3.04 MB; three are visual overlays/backgrounds. Lazy loading/visibility-based playback is absent.
- All images are 1536×2752 and have no responsive `srcset`/`sizes`; the images are oversized for many mobile displays. No explicit image loading hints. CSS background-image assets cannot be lazy-loaded through native `loading` attributes.
- Google Fonts, Tailwind Play CDN and GSAP are blocking head scripts without `defer`/async. Tailwind Play CDN is convenient for prototypes, not optimized production delivery. Network failure means no utility CSS / GSAP; custom CSS covers only a small subset of the layout.
- The document declares `lang="en"` while Arabic is correctly marked `lang="ar" dir="rtl"`.
- RSVP labels are explicitly connected for text/number fields and radio group has a legend; native required state is used. Focus styling is present via Tailwind `focus:ring-2` on text fields, but inputs use `outline-none`, and buttons have no explicit keyboard focus-visible style. The RSVP radio labels include the controls and are clickable.
- `.ornament` text is 0.65rem (about 10.4px), countdown unit labels are 9px on mobile, and several helper/footnote strings are 10px. These are small, especially with high letter spacing. Text sizes of 12–14px for some event details may also be difficult at 360px width.
- Contrast concern: gold text is used over both light and dark surfaces. In `#countdown` and `#walima`, `.ornament` is gold `#C9A227` over off-white and is low contrast. Gold labels over dark overlays vary with media. Some white helper text is set to 35–60% opacity. No contrast test was run.
- `prefers-reduced-motion` is present (line 10) but only CSS timing/snap and JS conditionals partially honor it; curtains remain closed and multiple videos still autoplay/loop. No pause controls are provided for motion media.
- No skip link, explicit main landmark label, or progress/navigation aid. `#entrance` can open on any click/tap inside it as well as the button; the control is labeled as a button, but behavior is not discoverable outside the hint.

### Mobile layout

- `index.html:9–10`: uses `100dvh`, not `100vh`; this is a good mobile viewport choice in current browsers. Sections use `min-height`, so content can exceed a viewport and scroll vertically.
- `body` has `overflow-x:hidden`; this masks horizontal overflow rather than proving no child overflows. Likely narrow-screen pressure points at 360px include RSVP radio labels on one line (`flex` with `gap-5` and no wrapping), long ornament copy with `.45em` letter spacing, Arabic line wrapping, and the team labels plus VS group. There are no 360×640 or 390×844 browser measurements because browser tooling is unavailable.
- At max-width 380px hero title is set to 3rem, but most section title sizes remain 2.25rem. The RSVP form plus section vertical padding is likely taller than 640px; `min-height` allows scrolling, so content should not be clipped vertically, but interaction/composition is not visually verified.
- Tap targets: entrance and calendar buttons have padding; RSVP submit button is 3rem tall. Radio controls/labels are small (text 14px) and the label click areas are only their text/content. No global touch-target sizing is applied.
- The initial entrance overlays the full screen with doors and requires a click/tap. Automatic opening is delayed until `load` plus 500ms, so slow font/CDN/media loads can prolong the covered state.

### Visual quality (source-only; no browser screenshots)

- Entrance: symmetric halves reuse one identical door image; no separately composed left/right doors, camera movement, dimensional hinges, or layered scene geometry. Visual richness comes mainly from gradients, borders and grain.
- Countdown: clean but generic four-cell layout; unit labels are tiny and there is no illustrative/3D element.
- Family invitation: a full-screen portrait video sits behind text and a dark gradient. Contrast is aided by the shade; exact footage crop/contrast is unknown.
- Curtains: same curtain image mirrored; the contents sit behind curtains and depend on ScrollTrigger to reveal. Without JS/reduced motion the text can be hidden. Pinning behavior is suspect.
- Prayer/rings: single square video floats in a flat light gradient panel; no depth beyond `translateZ` and drop shadow. Video framing is unknown.
- Henna: background photo with a broad dark overlay and glass event card; dove overlay may compete with copy. Video alpha/visual treatment unknown.
- Football: background photo plus strong dark gradient; card is legible by intent but heavily boxed and generic. Team naming is placeholder-like (“TEAM GROOM/TEAM BRIDE”).
- Dinner: explicitly no venue visual; radial gradient and blur replace the requested banquet hall scene, making it the most obvious synthetic/empty visual.
- Fatiha: rose video, two decorative SVG columns and glass card; the overlay effect may look flat if the WebM has no alpha (alpha unknown).
- Walima: inline single-color vector table drawing inside a framed panel. It is a clear placeholder for a premium realistic illustration/photo and contains no 3D depth.
- Save the Date: gradient-only background and centered text/button; spacious but generic.
- RSVP: functional compact glass card; dense labels/form controls against an atmospheric gradient, no decorative narrative or guest count explanation.
- Blessing: typography-led ending with Arabic text, quote and a fade overlay. The fade only dims inner content; the gradient overlay becomes black at the bottom, but does not transition the entire section uniformly to black.

## 4. Content status

No literal `A & B`, `lorem ipsum`, TODO or FIXME strings occur. The visible couple and family names are filled with Al-Amin Bello, Aisha Yusuf, Ibrahim Bello and Musa Yusuf. Whether these are approved real details or sample data is **unknown**. Items that should be confirmed as real, not assumed placeholders:

- Couple names in title/sections and downloadable calendar: Al-Amin Bello and Aisha Yusuf (`index.html:1,15,24–25,34,45`).
- Parent names: Mr. & Mrs. Ibrahim Bello and Mr. & Mrs. Musa Yusuf (`index.html:24`).
- Wedding date/time: December 31, 2026, Fatiha 10:00 AM, countdown target and Save the Date span (`index.html:15,23,30,32,43,45`).
- RSVP deadline December 15, 2026 (`index.html:33`).
- Event schedule/venues: Arewa Garden, Kano; Unity Sports Ground, Kano; Sapphire Event Hall, Kano; Masjid Al-Noor, Kano (`index.html:27–31,45`). No street addresses, map links, venue contacts, or postal addresses are provided.
- “TEAM GROOM” and “TEAM BRIDE” (`index.html:28`) are generic team labels and may be intended copy or placeholders.
- Event-specific phrases, generic names and demo behavior are clearly present; the RSVP explicitly says it is a demo (`index.html:33`).
- No placeholder initials were found. “Ameen” and the blessing text are intentional devotional copy, not placeholders.

## 5. Summary table

| Section | Status (OK / Weak / Broken / Missing) | Main issue | Suggested fix |
|---|---|---|---|
| Entrance | Weak | Both door halves share one image; reduced-motion branch leaves “Tap to begin” visible | Compose distinct door panels and ensure the reduced-motion state is fully open and clear |
| Countdown | Weak | Valid hard-coded target, but unit labels are tiny and date requires confirmation | Confirm event data and improve mobile label size/contrast |
| Holding-hands / family invitation | Weak | Background video autoplay has no fallback/poster or visibility control | Add poster and compatible fallback; pause offscreen playback |
| Curtains / names | Broken | Two pinned ScrollTriggers target the same section; curtains can stay closed when reduced motion is on | Use one coordinated trigger/timeline and expose content in reduced-motion mode |
| Rings and prayer | Weak | WebM-only, no poster/fallback; shallow scene depth | Add cross-browser fallback and build layered scene treatment |
| Sa Lalle & Kamu | Weak | Expected asset name differs; no venue street address; overlay video could compete | Confirm venue details and balance the card/overlay against media |
| Football match | Weak | Generic team names; no exact ground address; likely tight labels on 360px | Confirm event copy/location and wrap or stack team labels on narrow screens |
| Wedding dinner | Weak | No banquet-hall image; gradient is a synthetic substitute | Add a real venue scene with lighting and depth |
| Fatiha | Weak | WebM-only petals without fallback; alpha is unknown | Verify alpha and provide poster/fallback; check text contrast on actual media |
| Walima | Weak | Flat inline SVG substitutes for expected artwork; no confirmed street address | Replace with approved premium illustration/scene and complete venue details |
| Save the Date | Weak | Calendar download is one 12-hour event, not a full schedule | Confirm desired calendar scope and include accurate venue/event details |
| RSVP | Weak | Submission is only an in-page demo; response is not stored or sent | Connect to the intended RSVP destination or clearly label the interaction as a preview |
| Closing blessing | Weak | Fade dims only the inner content and motion reduction disables scroll animation | Fade the complete section to black and provide a static reduced-motion end state |

### Top 10 improvements by impact

1. Fix the curtain reveal: consolidate the duplicate pinning into one controlled pinned timeline and make curtains open for reduced-motion users.
2. Replace the dinner gradient with a real banquet scene; build coherent layered depth across all sections for the premium, realistic 3D goal.
3. Confirm names, family names, dates, venues, RSVP deadline, and exact addresses with the couple; current correctness is unknown.
4. Add Safari/iOS-compatible video fallbacks and poster images; verify which WebM files actually contain alpha.
5. Reduce video decode/bandwidth cost by pausing offscreen videos and loading media near the viewport.
6. Optimize 1536×2752 assets for mobile and use responsive image sizes; each current image is large for a 9:16 phone screen.
7. Replace shared/mirrored entrance and curtain imagery with separately composed assets; replace the flat Walima SVG with final approved art.
8. Improve mobile typography and spacing: increase tiny ornament/unit/footnote text, wrap dense labels, and verify 360×640 and 390×844 layouts.
9. Improve accessibility: explicit focus-visible styles, high-contrast gold on light backgrounds, reduced-motion-complete behavior, and meaningful/empty alt text as appropriate.
10. Make the calendar and RSVP behavior match the actual event workflow (calendar scope, real response delivery/persistence) and avoid immediately revoking the calendar object URL.
