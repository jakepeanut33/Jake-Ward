import { PageShell } from "@/components/PageShell";
import { site } from "@/lib/config";

export const metadata = { title: "Shipping Policy" };

export default function ShippingPage() {
  return (
    <PageShell title="Shipping Policy">
      <p>
        We're proud to ship Snugpaw products to pet parents around the world. Because
        many items (especially personalized pieces) are made to order, please review
        the timelines below.
      </p>
      <h2>Processing time</h2>
      <p>
        Orders are processed within 1–3 business days. Personalized items (like the
        Custom Pet Portrait Blanket) require an additional 1–2 days for production.
      </p>
      <h2>Delivery estimates</h2>
      <ul>
        <li>United States: 5–9 business days after processing</li>
        <li>Canada, UK, EU, Australia: 7–14 business days after processing</li>
        <li>Rest of world: 10–20 business days after processing</li>
      </ul>
      <h2>Shipping cost</h2>
      <p>
        Flat-rate shipping is calculated at checkout. Orders over{" "}
        {site.currencySymbol}{site.freeShippingThreshold} ship free.
      </p>
      <h2>Tracking</h2>
      <p>
        You'll receive a tracking number by email as soon as your order ships. You
        can also use our <a className="text-clay underline" href="/pages/track">Track My Order</a> page.
      </p>
      <h2>Delays</h2>
      <p>
        Occasionally carrier or customs delays occur outside our control. If your
        order is taking longer than expected, email{" "}
        <a className="text-clay underline" href={`mailto:${site.supportEmail}`}>{site.supportEmail}</a>{" "}
        and we'll make it right.
      </p>
    </PageShell>
  );
}
