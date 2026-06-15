# 5 · Facebook / Meta Ads

This is where most of your money and most of your learning happen. Read it twice.

> ⚠️ I can't run ads for you — that needs your Meta account, your ID, your card, and
> your legal agreement to Meta's terms (advertisers must generally be 18+). What
> follows is the exact plan, structure, targeting, copy, and creative to run yourself.

## 2026 cost benchmarks (so your expectations are calibrated)

- **CPM** (cost per 1,000 views): e-commerce median ~**$17–18**, ranging ~$11–23.
- **CPC** (cost per click): ~**$1.14 average**, apparel/pet often lower (~$0.45–$1).
- **Conversion rate:** e-commerce median ~**1.57%** (≈ 1–2 buyers per 100 visitors).
- **CPA** (cost to get one sale): e-commerce average ~**$45** — note that's *more*
  than some of our product prices, which is why **margin and upsells matter**.
- Costs spike 25–35% in Q4 (holidays). Cheapest months are Jan–Feb.

Translation: expect to pay roughly **$0.50–$1.50 per click** and convert **~1–2%** of
visitors. On a $39 product with ~$25 margin, you need a sale roughly every ~$25 of ad
spend just to break even — so your **creative and product page have to convert.**

Sources at the bottom.

## Step 1 — Accounts & Pixel (do before spending)

1. Create a **Meta Business Suite / Business Manager** account (business.facebook.com).
2. Create an **Ad Account** and add a payment method.
3. Create a **Facebook Page** for Snugpaw (and ideally an Instagram account) — ads
   run from the Page. Post 3–6 times first so it doesn't look empty.
4. **Install the Meta Pixel + Conversions API** on Shopify:
   - Shopify App Store → **Facebook & Instagram** app → connect your Business
     account → it installs the Pixel automatically.
   - Turn on tracking for **ViewContent, AddToCart, InitiateCheckout, Purchase.**
   - If using the coded storefront, add the Pixel base code to `app/layout.tsx` and
     fire events on product view / buy click.
5. **Verify your domain** in Business Settings (needed for accurate tracking).
6. Confirm events fire using the **Meta Pixel Helper** Chrome extension before
   spending a dollar. No Pixel = you're flying blind.

## Step 2 — Campaign structure (keep it simple)

Use **Advantage+ Shopping Campaign (ASC)** or a simple manual **Sales** campaign.
Meta's ASC tends to deliver lower CPA for e-commerce and needs less fiddling — good
for beginners. Run this structure:

```
Campaign (Objective: Sales / Conversions, optimize for "Purchase")
└── Ad set  (budget set here, broad targeting, Purchase event)
     ├── Ad 1  — Hero product video A
     ├── Ad 2  — Hero product video B (different hook)
     └── Ad 3  — Image/carousel
```

- **Optimize for Purchase** (not clicks/traffic). It may spend slowly at first while
  it learns — that's normal.
- **Placements:** Advantage+ (let Meta choose). Most spend goes to Feeds + Reels.
- **One product per ad set** while testing so you can read results cleanly.

## Step 3 — Targeting

In 2026, Meta's algorithm is strong, so **go broad and let the Pixel find buyers:**

- **Broad:** age 25–65+, your country, all genders, **no detailed interests.** Let
  Advantage+ audience expand. This is now often the best-performing setup.
- **If you prefer interest targeting to start:** stack pet interests — *Dog/Cat
  ownership, Petco, Chewy, PetSmart, "dog lover," pet adoption,* plus broad
  *Online shopping.* Keep the audience 2M+ so it can scale.
- **Gift angle** for the blanket: also test targeting *recently moved / engaged /
  gift-givers.*
- **Retargeting (set up once you have traffic):** show ads to people who viewed a
  product or added to cart but didn't buy — these are your cheapest sales.

## Step 4 — Budget plan for $150–$500/month

Pick the lane that matches your budget. **Testing = finding a winner; scaling = pouring
fuel on it.**

### Lean ($150–$200/mo → ~$5–7/day)
- Test **one** hero product (Custom Blanket *or* Calming Bed).
- 1 ad set, 2–3 creatives, broad targeting, optimize for Purchase.
- Run 4–5 days before judging (don't kill it after 1 day). Expect this to be tight;
  you're mostly buying data.

### Recommended ($300–$500/mo → ~$10–17/day)
- **Week 1–2 (test):** run both heroes, $10–15/day total, 3 creatives each. Goal:
  find which product + hook gets the cheapest **cost per Add-to-Cart / Purchase.**
- **Week 3+ (scale the winner):** move budget to the best ad set. Increase budget
  **~20–30% every 2–3 days** (big jumps reset Meta's learning). Add retargeting.
- Kill any ad set with **no Add-to-Cart after ~$15–20 spend**, or no Purchase after
  ~$30–40 (≈ your CPA target). Be ruthless — protect your budget for winners.

## Step 5 — Reading the numbers (your decision rules)

Watch these in Ads Manager (add columns: CPM, CTR, CPC, ATC, Purchases, CPA, ROAS):

| Metric | Good sign | Bad sign → act |
| --- | --- | --- |
| **CTR (link)** | > 1.5% | < 1% → weak creative/hook, swap it |
| **CPC** | < $1 | > $2 → audience or creative off |
| **Add-to-Cart** | steady ATCs | clicks but no ATC → price/page problem |
| **ROAS** | > ~2.0 (profit zone for these margins) | < 1.5 after learning → cut or fix |
| **CPA** | < your margin (~$25) | > margin → not profitable yet |

**ROAS** = revenue ÷ ad spend. With ~65% margins you roughly break even around
**1.5–1.7 ROAS** and profit above ~**2.0**. Always know your break-even ROAS (file 6).

## Step 6 — Creative (the #1 lever)

On Meta, **the creative is the targeting.** A great video beats clever audience
settings. Most winning dropship ads are **short, native-looking videos** (UGC style),
not polished commercials.

### Winning ad formula (15–30s video)
1. **Hook (first 1–3s):** stop the scroll. Show the wow moment or the problem.
2. **Problem/agitate:** name the pain ("Your dog won't stop pacing at night?").
3. **Solution + demo:** show the product working, close-ups, the result.
4. **Social proof:** a review line on screen, "10,000+ happy pets."
5. **CTA:** "Tap Shop Now — 30-day guarantee, free shipping over $45."

### Where to get footage (you don't need to film much)
- Ask your supplier for their video/photo assets.
- Film your own pet using the sample you ordered (authentic UGC converts best).
- Use clips from your supplier + a tool like CapCut (free) to edit. Add captions —
  most people watch muted.

### Creative briefs (hand these to yourself or a CapCut session)

**Custom Pet Portrait Blanket — "Keepsake" (emotional)**
- Hook: a hand unrolling the blanket to reveal a dog's face → "I wasn't ready to cry."
- Beats: photo upload → production peek → reveal → owner hugging it on the couch.
- On-screen text: "Turn your best friend into a keepsake you'll use every day."
- CTA: "Make yours 🐾 Shop Now."

**Calming Donut Bed — "Finally sleeps" (problem/solution)**
- Hook: anxious dog pacing at 2am (or text "POV: your dog won't settle").
- Beats: pet steps into the donut bed → curls into the rim → asleep → morning, calm.
- On-screen text: "The bed that helped 10,000+ anxious pets finally relax."
- CTA: "Help your pet sleep → Shop Now."

### Ad copy (primary text — rotate these)

Blanket:
> They give us their whole life. The least we can do is keep them close. 🐾
> Our Custom Pet Portrait Blanket turns your favorite photo into an ultra-soft
> keepsake you'll actually use every day. Made to order. Loved by 10,000+ pet parents.
> ✅ Free shipping over $45 ✅ 30-day happiness guarantee
> 👉 Tap Shop Now

Calming bed:
> If your pet paces, whines, or can't settle… it might be their bed. 😔
> The Calming Donut Bed's raised rim gives anxious dogs & cats the deep-pressure
> comfort they crave — so they finally relax (and so do you).
> 🛏️ Self-warming faux fur · machine washable · 4 sizes
> ✅ 30-day guarantee 👉 Shop Now

**Headlines to test:** "The Gift Pet Parents Cry Over" · "Finally, A Bed Anxious Pets
Love" · "Made From Your Pet's Photo" · "10,000+ Happy Pets."

Make **3–5 variations** and let Meta find the winner. Refresh creatives every ~1–2
weeks as performance fatigues.

## Step 7 — Common beginner mistakes (avoid these)

- Killing ads after a few hours/$5 — give it data (~$15–40 per ad set).
- Optimizing for Clicks/Traffic instead of Purchases.
- Sending traffic to a slow, ugly, or untrustworthy page (fix the page first).
- One boring image ad — video + multiple hooks win.
- Scaling budget too fast (resets learning) — go ~20–30% every 2–3 days.
- No Pixel / unverified domain — you can't optimize what you can't measure.
- Health/medical claims ("cures anxiety") — gets ads rejected; say "helps pets feel calm."

## Sources
- [Facebook Ads Benchmarks 2026 — rule1](https://rule1.ai/articles/facebook-ads-benchmarks)
- [Facebook Ads Benchmarks 2026 (CPC/CPM/CTR) — Digital Applied](https://www.digitalapplied.com/blog/facebook-ads-benchmarks-2026-cpc-cpm-ctr-industry)
- [Meta Ads Cost Benchmarks — Mako Metrics](https://makometrics.com/blog/facebook-ads-cost-benchmarks)
- [Facebook Ads CPM for E-commerce — SuperAds](https://www.superads.ai/facebook-ads-costs/cpm-cost-per-mille/e-commerce)
- [Facebook Ads Cost Guide 2026 — Stackmatix](https://www.stackmatix.com/blog/facebook-ads-cost-complete-guide)
