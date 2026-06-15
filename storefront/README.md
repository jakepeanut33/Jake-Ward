# Snugpaw Storefront

A fast, conversion-focused storefront and ad-landing site for the **Snugpaw** pet
brand, built with Next.js 14 (App Router) + Tailwind CSS. Use it as your branded
front end and as dedicated landing pages for Facebook/Meta ads, with checkout
handed off to your real Shopify store.

## Quick start

```bash
cd storefront
npm install
npm run dev      # http://localhost:3000
```

Build for production:

```bash
npm run build && npm start
```

## Deploy (free)

The easiest path is [Vercel](https://vercel.com):

1. Push this repo to GitHub (already done if you're reading this there).
2. In Vercel, "Add New Project" → import the repo → set the **Root Directory** to
   `storefront`.
3. Add an environment variable `NEXT_PUBLIC_SHOPIFY_DOMAIN` = your store domain
   (e.g. `snugpaw.com` or `snugpaw-co.myshopify.com`).
4. Deploy. You get a free `*.vercel.app` URL; add your custom domain later.

## How checkout works

This storefront is the *marketing* layer. Real money is collected by **Shopify**.
- Edit `lib/config.ts` → set `shopifyDomain` (or the env var above).
- Every "Add to Cart" button links to your Shopify product page, or — if you fill in
  each product's `variantId` in `lib/products.ts` — straight to a pre-filled Shopify
  cart/checkout.

## Where to edit things

| What | File |
| --- | --- |
| Brand name, domain, support email, free-ship threshold | `lib/config.ts` |
| Products, prices, copy, reviews, images | `lib/products.ts` |
| Home page | `app/page.tsx` |
| Product page template | `app/products/[handle]/page.tsx` |
| Policies (shipping/returns/privacy/terms) | `app/pages/*` |
| Colors & fonts | `tailwind.config.ts` |

## Replacing placeholder images

Product images use a placeholder service so the site builds out of the box. Replace
the `image`/`gallery` URLs in `lib/products.ts` with your real product photos (host
them in `/public` or paste your Shopify CDN URLs).

See the `../docs/` folder for the full business + Facebook ads playbook.
