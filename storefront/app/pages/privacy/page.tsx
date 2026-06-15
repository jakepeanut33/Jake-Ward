import { PageShell } from "@/components/PageShell";
import { site } from "@/lib/config";

export const metadata = { title: "Privacy Policy" };

export default function PrivacyPage() {
  return (
    <PageShell title="Privacy Policy">
      <p>
        This Privacy Policy describes how {site.legalName} ("we", "us") collects,
        uses, and protects your information when you visit or make a purchase from
        our store. <em>This is a starter template — have it reviewed for your
        jurisdiction before launch.</em>
      </p>
      <h2>Information we collect</h2>
      <ul>
        <li>Contact and order details (name, email, shipping address, phone).</li>
        <li>Payment information, processed securely by our payment provider — we never store full card numbers.</li>
        <li>Usage data (pages viewed, device, approximate location) via cookies and analytics.</li>
      </ul>
      <h2>How we use it</h2>
      <ul>
        <li>To process and ship your orders and provide support.</li>
        <li>To send order updates and, if you opt in, marketing emails.</li>
        <li>To improve our store and measure advertising performance (e.g., Meta Pixel).</li>
      </ul>
      <h2>Sharing</h2>
      <p>
        We share data only with service providers needed to run the store (payment
        processors, fulfillment/shipping partners, analytics, and advertising
        platforms) and as required by law. We do not sell your personal information.
      </p>
      <h2>Your rights</h2>
      <p>
        You may request access to, correction of, or deletion of your personal data
        by emailing{" "}
        <a className="text-clay underline" href={`mailto:${site.supportEmail}`}>{site.supportEmail}</a>.
      </p>
      <h2>Cookies</h2>
      <p>
        We use cookies and similar technologies for cart functionality, analytics,
        and advertising. You can control cookies through your browser settings.
      </p>
      <p className="text-sm text-ink/50">Last updated: {new Date().getFullYear()}.</p>
    </PageShell>
  );
}
