import type { Metadata } from "next";
import { products } from "@/lib/products";
import { ProductCard } from "@/components/ProductCard";

export const metadata: Metadata = {
  title: "Shop All",
  description: "Every Snugpaw favorite — cozy beds, custom keepsakes, and enrichment your pet will love.",
};

export default function ProductsPage() {
  return (
    <div className="container-x py-12">
      <header className="mb-10 text-center">
        <h1 className="text-4xl font-extrabold">Shop All Snugpaw</h1>
        <p className="mt-2 text-ink/60">
          Cozy, calming, and personalized picks — loved by 10,000+ pet parents.
        </p>
      </header>
      <div className="grid grid-cols-2 gap-5 lg:grid-cols-3">
        {products.map((p) => (
          <ProductCard key={p.handle} product={p} />
        ))}
      </div>
    </div>
  );
}
