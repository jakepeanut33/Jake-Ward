# Snugpaw — Dropshipping Playbook

Everything you need to launch a cozy/personalized **pet** dropshipping brand,
run Facebook/Meta ads, and (hopefully) turn a profit. Read in order.

> ⚠️ **Honest expectations.** Dropshipping is a real business, not free money.
> Most stores that fail do so because the owner spent $0 learning and expected
> instant sales. The plan below is built for a **$150–$500/month** budget and
> assumes you'll test, lose some money learning, and iterate. Treat your first
> $300 of ad spend as tuition.

## The files

| # | File | What's inside |
| --- | --- | --- |
| 1 | [01-business-plan.md](01-business-plan.md) | The model, the brand, why pets, what success looks like |
| 2 | [02-product-research.md](02-product-research.md) | The 6 chosen products, costs, margins, suppliers, how to find more |
| 3 | [03-shopify-setup.md](03-shopify-setup.md) | Click-by-click: create the store, install apps, connect payments |
| 4 | [04-product-listings.md](04-product-listings.md) | Copy/paste titles, descriptions, prices for each product |
| 5 | [05-facebook-ads.md](05-facebook-ads.md) | Pixel setup, campaign structure, budgets, targeting, ad copy & creative briefs |
| 6 | [06-financials.md](06-financials.md) | Unit economics, breakeven, what "good" numbers look like |
| 7 | [07-launch-checklist.md](07-launch-checklist.md) | The do-not-skip pre-launch checklist |

## The 30-second version

1. **Pick the niche** → done: cozy/personalized pet goods (`Snugpaw`).
2. **Build the store** → use Shopify ($1 first month, then ~$39/mo). Import the 6 products from a supplier (Zendrop / CJ / DSers). Paste in the copy from file 4.
3. **Make it trustworthy** → logo, policies, reviews, fast support. (All drafted for you.)
4. **Install the Meta Pixel** → so Facebook can learn who buys.
5. **Run ads** → start with ~$10–20/day testing the Custom Blanket + Calming Bed (file 5).
6. **Read the data** → kill losers fast, scale winners slowly.
7. **Fulfill orders** → supplier ships directly to the customer; you keep the margin.

## What the code in `../storefront` is for

A free, fast Next.js site you can deploy as your **brand homepage and ad landing
pages**, with checkout handed off to Shopify. Optional but powerful for ads — see
file 5. Setup instructions are in `../storefront/README.md`.

## Two ways to run the store

- **Shopify-hosted (recommended to start):** everything lives on Shopify. Simplest,
  fastest, handles payments/checkout/fulfillment apps for you. Files 3–4 cover this.
- **Coded storefront + Shopify checkout (the `storefront/` app):** more control and
  better/cheaper landing pages for ads; checkout still runs on Shopify. Use once
  you're comfortable.
