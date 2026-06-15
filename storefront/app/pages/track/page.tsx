import { PageShell } from "@/components/PageShell";
import { site } from "@/lib/config";

export const metadata = { title: "Track My Order" };

export default function TrackPage() {
  return (
    <PageShell title="Track My Order">
      <p>
        As soon as your order ships, we email you a tracking link. Most orders ship
        within 1–3 business days (a little longer for personalized items).
      </p>
      <h2>Can't find your tracking?</h2>
      <ul>
        <li>Check your spam/promotions folder for an email from {site.brand}.</li>
        <li>Personalized orders take 1–2 extra days to produce before shipping.</li>
        <li>
          Still stuck? Email{" "}
          <a className="text-clay underline" href={`mailto:${site.supportEmail}`}>{site.supportEmail}</a>{" "}
          with your order number and we'll track it down for you.
        </li>
      </ul>
      <p className="text-sm text-ink/50">
        Tip: once your store is live, connect a tracking app (e.g. Shopify's built-in
        order status page, AfterShip, or 17TRACK) and embed it here.
      </p>
    </PageShell>
  );
}
