import { PageShell } from "@/components/PageShell";
import { site } from "@/lib/config";

export const metadata = { title: "Our Story" };

export default function AboutPage() {
  return (
    <PageShell title="Our Story">
      <p>
        {site.brand} started with a simple belief: the pets who give us everything
        deserve to be spoiled right back. We were tired of flimsy beds, jingling
        tags, and gifts that ended up in a drawer — so we set out to find products
        that actually make a pet's life cozier and a pet parent's heart fuller.
      </p>
      <p>
        Every item in our shop is hand-picked and tested against one question: would
        we put it in our own home, for our own dogs and cats? If the answer isn't an
        instant yes, it doesn't make the cut.
      </p>
      <h2>What we stand for</h2>
      <ul>
        <li>Comfort first — calming beds, soft blankets, and cozy nooks.</li>
        <li>Keepsakes that last — personalized pieces you'll treasure for years.</li>
        <li>Honest support — real humans, fast replies, no runaround.</li>
      </ul>
      <p>
        Thank you for letting us be a small part of the bond you share with your
        best friend. From our family to yours — welcome to {site.brand}. 🐾
      </p>
    </PageShell>
  );
}
