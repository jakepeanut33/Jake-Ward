import { site } from "@/lib/config";

export function AnnouncementBar() {
  return (
    <div className="bg-ink text-cream">
      <div className="container-x flex items-center justify-center gap-2 py-2 text-center text-xs font-medium sm:text-sm">
        <span>
          🐾 Free shipping over {site.currencySymbol}
          {site.freeShippingThreshold} · 30-day happiness guarantee · Loved by
          10,000+ pet parents
        </span>
      </div>
    </div>
  );
}
