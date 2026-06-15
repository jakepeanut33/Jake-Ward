import { Product } from "@/lib/products";
import { site, shopifyCartAddUrl, shopifyProductUrl } from "@/lib/config";

// Sends shoppers to your real Shopify checkout. If you've set a product's
// `variantId`, we go straight to a pre-filled cart; otherwise we open the
// Shopify product page. Configure your domain in lib/config.ts.
export function BuyButton({ product, className = "" }: { product: Product; className?: string }) {
  const href = product.variantId
    ? shopifyCartAddUrl(product.variantId)
    : shopifyProductUrl(product.handle);
  return (
    <a href={href} className={`btn-primary w-full ${className}`}>
      Add to Cart · {site.currencySymbol}
      {product.price.toFixed(2)}
    </a>
  );
}
