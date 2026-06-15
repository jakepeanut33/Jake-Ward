import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import { getProduct, products } from "@/lib/products";
import { site } from "@/lib/config";
import { Stars } from "@/components/Stars";
import { BuyButton } from "@/components/BuyButton";
import { ProductCard } from "@/components/ProductCard";

export function generateStaticParams() {
  return products.map((p) => ({ handle: p.handle }));
}

export function generateMetadata({ params }: { params: { handle: string } }): Metadata {
  const product = getProduct(params.handle);
  if (!product) return { title: "Not found" };
  return {
    title: product.name,
    description: product.shortDescription,
  };
}

export default function ProductPage({ params }: { params: { handle: string } }) {
  const product = getProduct(params.handle);
  if (!product) notFound();

  const related = products.filter((p) => p.handle !== product.handle).slice(0, 3);
  const savings = product.compareAt ? product.compareAt - product.price : 0;

  return (
    <div className="container-x py-10">
      <nav className="mb-6 text-sm text-ink/50">
        <Link href="/products" className="hover:text-clay">Shop</Link> / {product.name}
      </nav>

      <div className="grid gap-10 lg:grid-cols-2">
        {/* Gallery */}
        <div className="space-y-3">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={product.image}
            alt={product.name}
            className="aspect-square w-full rounded-xl2 object-cover shadow"
          />
          {product.gallery && (
            <div className="grid grid-cols-3 gap-3">
              {product.gallery.map((g, i) => (
                // eslint-disable-next-line @next/next/no-img-element
                <img key={i} src={g} alt="" className="aspect-square w-full rounded-lg object-cover" />
              ))}
            </div>
          )}
        </div>

        {/* Buy box */}
        <div>
          {product.badge && (
            <span className="rounded-full bg-sage/20 px-3 py-1 text-xs font-semibold text-sage">
              {product.badge}
            </span>
          )}
          <h1 className="mt-3 text-3xl font-extrabold">{product.name}</h1>
          <p className="mt-1 text-lg text-ink/60">{product.subtitle}</p>

          <div className="mt-3 flex items-center gap-2">
            <Stars rating={product.rating} />
            <span className="text-sm text-ink/60">
              {product.rating} · {product.reviewCount.toLocaleString()} reviews
            </span>
          </div>

          <div className="mt-5 flex items-baseline gap-3">
            <span className="text-3xl font-bold">
              {site.currencySymbol}{product.price.toFixed(2)}
            </span>
            {product.compareAt && (
              <>
                <span className="text-lg text-ink/40 line-through">
                  {site.currencySymbol}{product.compareAt.toFixed(2)}
                </span>
                <span className="rounded-full bg-clay/10 px-2 py-0.5 text-sm font-semibold text-clay">
                  Save {site.currencySymbol}{savings.toFixed(2)}
                </span>
              </>
            )}
          </div>

          <p className="mt-5 text-ink/80">{product.shortDescription}</p>

          <ul className="mt-5 space-y-2">
            {product.bullets.map((b) => (
              <li key={b} className="flex items-start gap-2 text-sm">
                <span className="text-sage">✓</span>
                <span>{b}</span>
              </li>
            ))}
          </ul>

          <div className="mt-7">
            <BuyButton product={product} />
            <p className="mt-3 text-center text-xs text-ink/50">
              🔒 Secure checkout · Free shipping over ${site.freeShippingThreshold} · 30-day guarantee
            </p>
          </div>

          {/* Long description */}
          <div className="mt-8 space-y-3 border-t border-ink/10 pt-6 text-ink/80">
            {product.description.map((d, i) => (
              <p key={i}>{d}</p>
            ))}
          </div>
        </div>
      </div>

      {/* Reviews */}
      <section className="mt-16">
        <h2 className="text-2xl font-extrabold">
          Reviews <span className="text-ink/40">({product.reviewCount.toLocaleString()})</span>
        </h2>
        <div className="mt-6 grid gap-5 md:grid-cols-3">
          {product.reviews.map((r, i) => (
            <figure key={i} className="card p-5">
              <Stars rating={r.rating} />
              <blockquote className="mt-2 text-sm text-ink/80">"{r.text}"</blockquote>
              <figcaption className="mt-3 text-sm font-semibold">
                {r.name}{" "}
                {r.verified && <span className="font-normal text-sage">· Verified</span>}
              </figcaption>
            </figure>
          ))}
        </div>
      </section>

      {/* Related */}
      <section className="mt-16">
        <h2 className="mb-6 text-2xl font-extrabold">You might also love</h2>
        <div className="grid grid-cols-2 gap-5 lg:grid-cols-3">
          {related.map((p) => (
            <ProductCard key={p.handle} product={p} />
          ))}
        </div>
      </section>
    </div>
  );
}
