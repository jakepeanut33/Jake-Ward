import Link from "next/link";
import { site } from "@/lib/config";

export function Footer() {
  return (
    <footer className="mt-24 border-t border-ink/10 bg-sand">
      <div className="container-x grid gap-10 py-14 sm:grid-cols-2 lg:grid-cols-4">
        <div>
          <div className="flex items-center gap-2 text-lg font-extrabold">
            <span aria-hidden>🐾</span> {site.brand}
          </div>
          <p className="mt-3 max-w-xs text-sm text-ink/70">{site.tagline}</p>
        </div>
        <div>
          <h3 className="text-sm font-semibold uppercase tracking-wide text-ink/60">Shop</h3>
          <ul className="mt-4 space-y-2 text-sm">
            <li><Link href="/products" className="hover:text-clay">All Products</Link></li>
            <li><Link href="/products/custom-pet-portrait-blanket" className="hover:text-clay">Custom Blanket</Link></li>
            <li><Link href="/products/calming-donut-dog-bed" className="hover:text-clay">Calming Bed</Link></li>
          </ul>
        </div>
        <div>
          <h3 className="text-sm font-semibold uppercase tracking-wide text-ink/60">Help</h3>
          <ul className="mt-4 space-y-2 text-sm">
            <li><Link href="/pages/track" className="hover:text-clay">Track My Order</Link></li>
            <li><Link href="/pages/shipping" className="hover:text-clay">Shipping</Link></li>
            <li><Link href="/pages/returns" className="hover:text-clay">Returns & Refunds</Link></li>
            <li><Link href="/pages/contact" className="hover:text-clay">Contact Us</Link></li>
          </ul>
        </div>
        <div>
          <h3 className="text-sm font-semibold uppercase tracking-wide text-ink/60">Company</h3>
          <ul className="mt-4 space-y-2 text-sm">
            <li><Link href="/pages/about" className="hover:text-clay">Our Story</Link></li>
            <li><Link href="/pages/privacy" className="hover:text-clay">Privacy Policy</Link></li>
            <li><Link href="/pages/terms" className="hover:text-clay">Terms of Service</Link></li>
          </ul>
        </div>
      </div>
      <div className="border-t border-ink/10">
        <div className="container-x flex flex-col items-center justify-between gap-2 py-6 text-xs text-ink/60 sm:flex-row">
          <p>© {new Date().getFullYear()} {site.legalName}. All rights reserved.</p>
          <p>Made with love for pets everywhere.</p>
        </div>
      </div>
    </footer>
  );
}
