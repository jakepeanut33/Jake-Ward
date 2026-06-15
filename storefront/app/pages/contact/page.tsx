import { PageShell } from "@/components/PageShell";
import { site } from "@/lib/config";

export const metadata = { title: "Contact Us" };

export default function ContactPage() {
  return (
    <PageShell title="Contact Us">
      <p>
        Questions about your order, a product, or a custom blanket? We're real
        people and we'd love to help.
      </p>
      <h2>Email</h2>
      <p>
        <a className="text-clay underline" href={`mailto:${site.supportEmail}`}>
          {site.supportEmail}
        </a>
        <br />
        We reply within 24 hours, Monday–Friday.
      </p>
      <h2>Order help</h2>
      <p>
        Already ordered? Have your order number ready and visit{" "}
        <a className="text-clay underline" href="/pages/track">Track My Order</a> for
        the fastest update.
      </p>
      <h2>Business hours</h2>
      <p>Monday–Friday, 9am–5pm CT. Orders and emails over the weekend are answered the next business day.</p>
    </PageShell>
  );
}
