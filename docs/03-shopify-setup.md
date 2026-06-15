# 3 · Shopify Setup (click-by-click)

Time needed: about an afternoon. Have ready: an email, a phone, and (an adult's)
bank/payment details for getting paid.

## Step 1 — Create the store

1. Go to **shopify.com** → **Start free trial**. Take the trial, then the cheapest
   "Basic" plan is fine (~$39/mo, often $1 for month one).
2. Store name: **Snugpaw** (or your chosen alternate). You can change the public name
   later in **Settings → Store details**.
3. Skip the "what do you sell" upsells; you can do everything from the admin.

## Step 2 — Buy a domain

- **Settings → Domains → Buy new domain.** Get `snugpaw.com` or `.co` (~$10–15/yr).
- A custom domain massively increases trust vs. `*.myshopify.com`. Do this before ads.

## Step 3 — Pick & customize a theme

1. **Online Store → Themes.** Start with the free **Dawn** theme (fast, clean, mobile-first).
2. Click **Customize**. Set:
   - **Logo** (see Step 8), brand colors (cream `#FBF7F0`, terracotta `#B5613F`,
     sage `#7C8C6B`), and a clean font.
   - **Homepage:** hero banner ("Cozy comfort, made personal"), featured collection,
     reviews section, trust badges, and a footer with your policy links.
   - **Announcement bar:** "Free shipping over $45 · 30-day guarantee."
3. Mobile preview matters most — **90%+ of your ad traffic is on phones.**

## Step 4 — Install your supplier app

Pick ONE to start:
- **Zendrop** (beginner-friendly, managed fulfillment, good for custom items), or
- **DSers** (best for AliExpress sourcing), or
- **CJ Dropshipping** (lowest fixed cost).

Install from the **Shopify App Store**, connect it, and import your products. For the
**personalized blanket & ID tag**, search a print-on-demand supplier (Printify,
Gelato, or a CJ custom supplier) and add their product/variant fields so customers
can upload a photo / enter a name.

## Step 5 — Add products

Create the 6 products from file 4 (copy/paste titles, descriptions, prices). For each:
- Upload **real images** (from your supplier or, better, your own sample photos).
- Set **price** and **compare-at price** (the higher "was" price).
- Set **SKU** and connect the supplier variant so orders auto-route.
- Add an **"Upload your photo"** / **"Pet's name"** field on personalized items (apps:
  Hulk Product Options, or your POD app's native option).

## Step 6 — Set up payments

- **Settings → Payments → Shopify Payments** (simplest) or PayPal. Offer both if you
  can — some buyers only trust PayPal.
- ⚠️ Payments require a real business/banking identity. If you're under 18, an adult
  must own this. Don't skip — this is how you actually get paid.

## Step 7 — Shipping & taxes

- **Settings → Shipping:** create a simple flat rate (e.g. $4.95) with **free over
  $45**. Keep it simple at launch.
- **Settings → Taxes:** enable automatic tax calculation for your region.
- Set realistic delivery times on the product pages and shipping policy (file 5 in the
  storefront / `app/pages/shipping`).

## Step 8 — Branding assets

- **Logo:** make a simple wordmark "🐾 Snugpaw" in Canva (free) — a paw icon + clean
  font is plenty. Export PNG (transparent) for the header and a square version for
  social.
- **Favicon:** the paw icon, 32×32.
- **Email sender name:** Snugpaw (Settings → Notifications).

## Step 9 — Trust elements (do not skip)

These are the difference between traffic and sales:
- **Reviews app** (Judge.me free, or Loox for photo reviews). Import a few honest
  starter reviews; collect real ones via post-purchase email.
- **Policy pages:** paste the Shipping, Returns, Privacy, and Terms text (already
  written in the storefront under `app/pages/*`). Add **Contact** and **About**.
- **Contact info** in the footer + a real support email.
- **Trust badges** near the buy button (secure checkout, guarantee, shipping).

## Step 10 — Pre-launch QA

- Place a **test order** (Shopify has a test/bogus gateway, or use a real order and
  refund it). Confirm the supplier order routes correctly.
- Click every link, view on a phone, check spelling.
- Then go to file 7 (Launch Checklist) before spending a cent on ads.

## Optional — connect the coded storefront

If you want the custom Next.js front end (`../storefront`) as your ad landing pages:
1. Deploy it on Vercel (see `../storefront/README.md`).
2. Set `NEXT_PUBLIC_SHOPIFY_DOMAIN` to your Shopify domain.
3. Fill each product's `variantId` in `lib/products.ts` (find it in the Shopify
   product URL / Admin API) so "Add to Cart" jumps straight to Shopify checkout.
