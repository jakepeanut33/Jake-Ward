// =============================================================
//  SNUGPAW — SITE CONFIG
//  Edit these values once your real accounts are set up.
// =============================================================

export const site = {
  brand: "Snugpaw",
  tagline: "Cozy, personalized comfort for the pets you love.",
  // After you create your Shopify store, put your *.myshopify.com OR custom
  // domain here (no https://, no trailing slash). All "Add to cart" / "Buy"
  // buttons send shoppers to your real Shopify checkout.
  //   Example: "snugpaw.com"  or  "snugpaw-co.myshopify.com"
  shopifyDomain: process.env.NEXT_PUBLIC_SHOPIFY_DOMAIN || "your-store.myshopify.com",
  supportEmail: "support@snugpaw.co",
  // Used in the footer / legal pages. Replace with your real details before launch.
  legalName: "Snugpaw Co.",
  // Free-shipping threshold shown in the announcement bar.
  freeShippingThreshold: 45,
  currency: "USD",
  currencySymbol: "$",
};

// Build a link to a product or to checkout on your real Shopify store.
export function shopifyProductUrl(handle: string): string {
  return `https://${site.shopifyDomain}/products/${handle}`;
}

export function shopifyCartAddUrl(variantId: string, quantity = 1): string {
  // Shopify permalink that adds an item and goes straight to checkout.
  // Replace each product's `variantId` once you create it in Shopify admin.
  return `https://${site.shopifyDomain}/cart/${variantId}:${quantity}`;
}
