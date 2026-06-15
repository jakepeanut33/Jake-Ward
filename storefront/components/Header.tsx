import Link from "next/link";
import { site } from "@/lib/config";

export function Header() {
  return (
    <header className="sticky top-0 z-40 border-b border-ink/10 bg-cream/90 backdrop-blur">
      <div className="container-x flex h-16 items-center justify-between">
        <Link href="/" className="flex items-center gap-2 text-xl font-extrabold tracking-tight">
          <span aria-hidden>🐾</span>
          <span>{site.brand}</span>
        </Link>
        <nav className="hidden items-center gap-8 text-sm font-medium md:flex">
          <Link href="/products" className="hover:text-clay">Shop All</Link>
          <Link href="/products/custom-pet-portrait-blanket" className="hover:text-clay">Custom Blanket</Link>
          <Link href="/products/calming-donut-dog-bed" className="hover:text-clay">Calming Bed</Link>
          <Link href="/pages/about" className="hover:text-clay">Our Story</Link>
        </nav>
        <div className="flex items-center gap-3">
          <Link href="/products" className="btn-primary !px-5 !py-2.5 text-xs sm:text-sm">
            Shop Now
          </Link>
        </div>
      </div>
    </header>
  );
}
