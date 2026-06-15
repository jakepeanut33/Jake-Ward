import { PageShell } from "@/components/PageShell";
import { site } from "@/lib/config";

export const metadata = { title: "Terms of Service" };

export default function TermsPage() {
  return (
    <PageShell title="Terms of Service">
      <p>
        These Terms of Service govern your use of {site.legalName}'s website and your
        purchases. By using our store you agree to these terms.{" "}
        <em>This is a starter template — have it reviewed before launch.</em>
      </p>
      <h2>Orders</h2>
      <p>
        We reserve the right to refuse or cancel any order. Prices and availability
        are subject to change. You're responsible for providing accurate shipping and
        personalization details.
      </p>
      <h2>Pricing & payment</h2>
      <p>
        All prices are listed in {site.currency}. Payment is captured at checkout
        through our secure payment provider.
      </p>
      <h2>Intellectual property</h2>
      <p>
        All content on this site (text, images, logos) is owned by or licensed to{" "}
        {site.legalName} and may not be reused without permission.
      </p>
      <h2>Limitation of liability</h2>
      <p>
        Our products are provided "as is." To the fullest extent permitted by law,
        {site.legalName} is not liable for indirect or incidental damages arising
        from use of our products or site.
      </p>
      <h2>Contact</h2>
      <p>
        Questions about these terms? Email{" "}
        <a className="text-clay underline" href={`mailto:${site.supportEmail}`}>{site.supportEmail}</a>.
      </p>
      <p className="text-sm text-ink/50">Last updated: {new Date().getFullYear()}.</p>
    </PageShell>
  );
}
