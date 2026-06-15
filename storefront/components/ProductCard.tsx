import Link from "next/link";
import { Product } from "@/lib/products";
import { site } from "@/lib/config";
import { Stars } from "./Stars";

export function ProductCard({ product }: { product: Product }) {
  return (
    <Link href={`/products/${product.handle}`} className="group card overflow-hidden">
      <div className="relative aspect-square overflow-hidden bg-sand">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={product.image}
          alt={product.name}
          className="h-full w-full object-cover transition duration-300 group-hover:scale-105"
        />
        {product.badge && (
          <span className="absolute left-3 top-3 rounded-full bg-ink/85 px-3 py-1 text-xs font-semibold text-cream">
            {product.badge}
          </span>
        )}
      </div>
      <div className="space-y-1 p-4">
        <h3 className="font-semibold leading-tight group-hover:text-clay">{product.name}</h3>
        <p className="text-sm text-ink/60">{product.subtitle}</p>
        <div className="flex items-center gap-2 pt-1 text-sm">
          <Stars rating={product.rating} />
          <span className="text-ink/50">({product.reviewCount.toLocaleString()})</span>
        </div>
        <div className="flex items-baseline gap-2 pt-1">
          <span className="text-lg font-bold">
            {site.currencySymbol}
            {product.price.toFixed(2)}
          </span>
          {product.compareAt && (
            <span className="text-sm text-ink/40 line-through">
              {site.currencySymbol}
              {product.compareAt.toFixed(2)}
            </span>
          )}
        </div>
      </div>
    </Link>
  );
}
