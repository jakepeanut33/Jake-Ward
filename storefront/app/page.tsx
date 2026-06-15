import Link from "next/link";
import { products, heroProducts } from "@/lib/products";
import { ProductCard } from "@/components/ProductCard";
import { Stars } from "@/components/Stars";
import { site } from "@/lib/config";

export default function HomePage() {
  const hero = heroProducts()[0];
  return (
    <>
      {/* HERO */}
      <section className="bg-gradient-to-b from-sand to-cream">
        <div className="container-x grid items-center gap-10 py-16 md:grid-cols-2 lg:py-24">
          <div>
            <p className="mb-3 inline-flex items-center gap-2 rounded-full bg-white px-3 py-1 text-xs font-semibold text-clay ring-1 ring-clay/20">
              ★ 4.9/5 from 10,000+ happy pet parents
            </p>
            <h1 className="text-4xl font-extrabold leading-tight sm:text-5xl lg:text-6xl">
              Cozy comfort, <span className="text-clay">made personal.</span>
            </h1>
            <p className="mt-5 max-w-md text-lg text-ink/70">
              {site.tagline} From custom photo blankets to anxiety-easing beds,
              Snugpaw turns everyday moments into ones your pet (and you) will love.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link href="/products" className="btn-primary">Shop Best Sellers</Link>
              <Link href={`/products/${hero.handle}`} className="btn-secondary">
                Make a Custom Blanket
              </Link>
            </div>
            <div className="mt-6 flex flex-wrap gap-x-6 gap-y-2 text-sm text-ink/60">
              <span>✓ Free shipping over ${site.freeShippingThreshold}</span>
              <span>✓ 30-day guarantee</span>
              <span>✓ Tracked worldwide</span>
            </div>
          </div>
          <div className="relative">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={hero.image}
              alt={hero.name}
              className="aspect-square w-full rounded-xl2 object-cover shadow-lg"
            />
            <div className="absolute -bottom-4 -left-4 hidden rounded-xl2 bg-white p-4 shadow-lg ring-1 ring-ink/5 sm:block">
              <Stars rating={hero.rating} />
              <p className="mt-1 text-sm font-semibold">{hero.name}</p>
              <p className="text-xs text-ink/60">"I sobbed when it arrived." — Maria G.</p>
            </div>
          </div>
        </div>
      </section>

      {/* TRUST BAR */}
      <section className="border-y border-ink/10 bg-white">
        <div className="container-x grid grid-cols-2 gap-6 py-8 text-center md:grid-cols-4">
          {[
            ["🚚", "Fast, tracked shipping"],
            ["💝", "Made-to-order & personalized"],
            ["🛡️", "30-day happiness guarantee"],
            ["💬", "Real human support"],
          ].map(([icon, label]) => (
            <div key={label}>
              <div className="text-2xl">{icon}</div>
              <p className="mt-2 text-sm font-medium text-ink/70">{label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* BEST SELLERS */}
      <section className="container-x py-16">
        <div className="mb-8 flex items-end justify-between">
          <div>
            <h2 className="text-3xl font-extrabold">Loved by pet parents</h2>
            <p className="mt-1 text-ink/60">Our most-gifted, most-reordered favorites.</p>
          </div>
          <Link href="/products" className="hidden text-sm font-semibold text-clay hover:underline sm:block">
            View all →
          </Link>
        </div>
        <div className="grid grid-cols-2 gap-5 lg:grid-cols-4">
          {products.slice(0, 4).map((p) => (
            <ProductCard key={p.handle} product={p} />
          ))}
        </div>
      </section>

      {/* STORY STRIP */}
      <section className="bg-sage/15">
        <div className="container-x grid items-center gap-10 py-16 md:grid-cols-2">
          <div>
            <h2 className="text-3xl font-extrabold">Started by pet people, for pet people</h2>
            <p className="mt-4 text-ink/70">
              We believe the bond with your pet deserves more than a cracked phone
              screen and a chewed-up toy. Every Snugpaw product is chosen to make
              your pet calmer, happier, and a little more spoiled — and to give you
              keepsakes worth holding onto.
            </p>
            <Link href="/pages/about" className="btn-secondary mt-6">Read our story</Link>
          </div>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={products[1].image}
            alt="Happy pet"
            className="aspect-[4/3] w-full rounded-xl2 object-cover shadow"
          />
        </div>
      </section>

      {/* REVIEWS */}
      <section className="container-x py-16">
        <h2 className="text-center text-3xl font-extrabold">What pet parents are saying</h2>
        <div className="mt-10 grid gap-6 md:grid-cols-3">
          {products
            .flatMap((p) => p.reviews.map((r) => ({ ...r, product: p.name })))
            .slice(0, 3)
            .map((r, i) => (
              <figure key={i} className="card p-6">
                <Stars rating={r.rating} />
                <blockquote className="mt-3 text-ink/80">"{r.text}"</blockquote>
                <figcaption className="mt-4 text-sm font-semibold">
                  {r.name}{" "}
                  {r.verified && <span className="font-normal text-sage">· Verified Buyer</span>}
                </figcaption>
              </figure>
            ))}
        </div>
      </section>

      {/* CTA */}
      <section className="container-x pb-20">
        <div className="rounded-xl2 bg-ink px-8 py-14 text-center text-cream">
          <h2 className="text-3xl font-extrabold">Spoil your best friend today</h2>
          <p className="mx-auto mt-3 max-w-xl text-cream/70">
            Free shipping over ${site.freeShippingThreshold}. Loved by 10,000+ pet
            parents. Backed by our 30-day happiness guarantee.
          </p>
          <Link href="/products" className="btn-primary mt-7 bg-clay">Shop the collection</Link>
        </div>
      </section>
    </>
  );
}
