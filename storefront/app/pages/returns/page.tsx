import { PageShell } from "@/components/PageShell";
import { site } from "@/lib/config";

export const metadata = { title: "Returns & Refunds" };

export default function ReturnsPage() {
  return (
    <PageShell title="Returns & Refunds">
      <p>
        Your happiness (and your pet's) is guaranteed. If something isn't right,
        we'll make it right.
      </p>
      <h2>30-day happiness guarantee</h2>
      <p>
        If you're not in love with your order, contact us within 30 days of delivery
        for a replacement or refund.
      </p>
      <h2>How to start a return</h2>
      <p>
        Email{" "}
        <a className="text-clay underline" href={`mailto:${site.supportEmail}`}>{site.supportEmail}</a>{" "}
        with your order number and a photo if the item arrived damaged. We'll send
        next steps within 24 hours.
      </p>
      <h2>Damaged or wrong items</h2>
      <p>
        If your item arrives damaged or incorrect, we'll replace it free of charge —
        no need to ship anything back.
      </p>
      <h2>Personalized items</h2>
      <p>
        Custom/personalized products can't be resold, so they're only eligible for
        replacement or refund if there's a defect or an error on our end. Please
        double-check spelling and uploaded photos at checkout.
      </p>
      <h2>Refund timing</h2>
      <p>Approved refunds are issued to your original payment method within 5–10 business days.</p>
    </PageShell>
  );
}
