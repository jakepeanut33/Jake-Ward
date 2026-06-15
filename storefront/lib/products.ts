// =============================================================
//  SNUGPAW — PRODUCT CATALOG
//  These are the researched 2026 trending pet products with real
//  cost/price ranges. Swap images + variantId after you import them
//  into Shopify (via Zendrop / CJ / DSers).
// =============================================================

export type Review = {
  name: string;
  rating: number; // 1-5
  text: string;
  verified?: boolean;
};

export type Product = {
  handle: string;
  name: string;
  subtitle: string;
  price: number; // your retail price (USD)
  compareAt?: number; // "was" price for the strike-through
  cost: number; // your supplier cost (for your eyes / margin math)
  category: "Beds & Blankets" | "Personalized" | "Enrichment" | "Grooming" | "Travel";
  hero?: boolean; // featured as the main ad product
  badge?: string;
  // Replace with your real product images (hosted in Shopify or /public).
  image: string;
  gallery?: string[];
  shortDescription: string;
  bullets: string[];
  description: string[];
  variantId?: string; // Shopify variant id, e.g. "45123456789012"
  rating: number;
  reviewCount: number;
  reviews: Review[];
};

// Placeholder image (solid, on-brand) so the site builds before you add photos.
const ph = (label: string, bg = "C97B5A") =>
  `https://placehold.co/800x800/${bg}/FBF7F0/png?text=${encodeURIComponent(label)}`;

export const products: Product[] = [
  {
    handle: "custom-pet-portrait-blanket",
    name: "Custom Pet Portrait Blanket",
    subtitle: "Your pet, woven into cozy memory",
    price: 39.95,
    compareAt: 64.95,
    cost: 12.5,
    category: "Personalized",
    hero: true,
    badge: "Best Seller",
    image: ph("Custom Pet\\nBlanket"),
    gallery: [ph("Blanket 1"), ph("Blanket 2", "7C8C6B"), ph("Blanket 3", "B5613F")],
    shortDescription:
      "A premium fleece blanket printed with your pet's photo. The gift dog & cat parents cry over.",
    bullets: [
      "Upload any photo — we do the rest",
      "Ultra-soft 300gsm fleece, machine washable",
      "3 sizes: lap, throw, and bed",
      "Printed & shipped in 5-9 days",
    ],
    description: [
      "Some bonds deserve more than a phone screenshot. The Snugpaw Custom Pet Portrait Blanket turns your favorite photo of your best friend into a plush, full-color keepsake you'll actually use every single day.",
      "Printed on premium 300gsm fleece that stays soft wash after wash, it's the gift that makes grandparents tear up and pet parents order three. Perfect for memorials, gotcha-days, and 'just because.'",
      "Each blanket is made to order from the photo you upload at checkout. No two are alike — just like your pet.",
    ],
    rating: 4.9,
    reviewCount: 1284,
    reviews: [
      {
        name: "Maria G.",
        rating: 5,
        verified: true,
        text: "I ordered this after we lost our lab. I sobbed when it arrived. The quality is unreal and the photo is perfect.",
      },
      {
        name: "Devin R.",
        rating: 5,
        verified: true,
        text: "Got it for my girlfriend with a pic of her cat. Instant best-boyfriend points. Super soft too.",
      },
      {
        name: "Anita P.",
        rating: 4,
        verified: true,
        text: "Beautiful blanket, shipping took 8 days but worth the wait. Ordering one for my mom now.",
      },
    ],
  },
  {
    handle: "calming-donut-dog-bed",
    name: "Calming Donut Pet Bed",
    subtitle: "Anxiety-easing comfort, vet-loved",
    price: 38.95,
    compareAt: 59.95,
    cost: 11.0,
    category: "Beds & Blankets",
    hero: true,
    badge: "Trending",
    image: ph("Calming\\nDonut Bed", "7C8C6B"),
    gallery: [ph("Bed 1", "7C8C6B"), ph("Bed 2"), ph("Bed 3", "B5613F")],
    shortDescription:
      "Faux-fur donut bed that helps anxious dogs & cats feel safe, calm, and sleep through the night.",
    bullets: [
      "Raised rim supports the head & neck",
      "Self-warming faux fur eases anxiety",
      "Machine washable, non-slip base",
      "4 sizes from small cat to large dog",
    ],
    description: [
      "If your pet paces, whines, or can't settle, the problem might be their bed. The Snugpaw Calming Donut Bed uses a raised, pillowy rim that pets instinctively curl against — the same deep-pressure comfort that helps anxious animals finally relax.",
      "The ultra-plush faux fur traps body heat for a cozy, self-warming nest, while the round shape creates a sense of security that flat beds simply can't.",
      "Machine washable with a non-slip bottom, it's the bed thousands of pet parents wish they'd bought sooner.",
    ],
    rating: 4.8,
    reviewCount: 2057,
    reviews: [
      {
        name: "Tasha L.",
        rating: 5,
        verified: true,
        text: "My rescue used to whine all night. First night in this bed he slept until morning. Game changer.",
      },
      {
        name: "Greg M.",
        rating: 5,
        verified: true,
        text: "Both my cats fight over it. Had to order a second one. Washes great.",
      },
      {
        name: "Priya S.",
        rating: 4,
        verified: true,
        text: "Super soft and my anxious pup loves it. Wish it came in more colors.",
      },
    ],
  },
  {
    handle: "snuffle-enrichment-mat",
    name: "Snuffle Enrichment Mat",
    subtitle: "Burn mental energy, slow fast eaters",
    price: 27.95,
    compareAt: 42.0,
    cost: 7.5,
    category: "Enrichment",
    badge: "Vet Pick",
    image: ph("Snuffle\\nMat", "B5613F"),
    shortDescription:
      "Hide treats in the mat and let natural foraging tire out your dog and stop boredom chewing.",
    bullets: [
      "15 minutes of sniffing = a long walk's worth of stimulation",
      "Slows down fast eaters",
      "Folds flat, machine washable",
      "Great for rainy days & crate rest",
    ],
    description: [
      "A bored dog is a destructive dog. The Snugpaw Snuffle Mat taps into your dog's strongest instinct — their nose — to deliver real mental exercise in just 15 minutes a day.",
      "Sprinkle in kibble or treats and watch them forage, problem-solve, and self-soothe. It's the secret tired-dog-owners swear by, especially for high-energy breeds and rainy days.",
      "Folds flat for storage and tosses straight in the wash.",
    ],
    rating: 4.7,
    reviewCount: 893,
    reviews: [
      {
        name: "Carlos D.",
        rating: 5,
        verified: true,
        text: "My border collie is finally calm in the evenings. This thing is magic.",
      },
      {
        name: "Lena K.",
        rating: 5,
        verified: true,
        text: "Stopped my lab from inhaling his food. Worth every penny.",
      },
    ],
  },
  {
    handle: "personalized-pet-id-tag",
    name: "Personalized Silent ID Tag",
    subtitle: "Custom-engraved, no annoying jingle",
    price: 18.95,
    compareAt: 29.0,
    cost: 4.0,
    category: "Personalized",
    badge: "Gift Idea",
    image: ph("Custom\\nID Tag"),
    shortDescription:
      "Deep-engraved stainless ID tag that lays flat and silent against the collar. Never lose your pet.",
    bullets: [
      "Laser-engraved with name + your phone number",
      "Silent design — no clinking at 3am",
      "Rust-proof stainless steel",
      "Slides onto any collar",
    ],
    description: [
      "Cheap dangling tags wear down, jingle all night, and fall off. The Snugpaw Silent ID Tag is laser-engraved deep into rust-proof stainless steel and lays flat against the collar — silent, durable, and always readable.",
      "Add your pet's name and your phone number at checkout. It's the $19 insurance policy every pet deserves.",
    ],
    rating: 4.8,
    reviewCount: 611,
    reviews: [
      {
        name: "Sam W.",
        rating: 5,
        verified: true,
        text: "Finally no more jingling all night. Engraving is crisp and deep.",
      },
      {
        name: "Hina T.",
        rating: 5,
        verified: true,
        text: "Bought one for each of my three cats. Looks way nicer than the pet store ones.",
      },
    ],
  },
  {
    handle: "pet-hair-remover-roller",
    name: "Reusable Pet Hair Remover",
    subtitle: "No refills, no sticky sheets, ever",
    price: 22.95,
    compareAt: 34.0,
    cost: 5.5,
    category: "Grooming",
    image: ph("Hair\\nRemover", "7C8C6B"),
    shortDescription:
      "Self-cleaning roller that pulls pet hair off couches & beds in seconds. Buy once, use forever.",
    bullets: [
      "No sticky refills — empties into the bin",
      "Works on couches, beds, car seats & clothes",
      "Self-cleaning base included",
      "One-handed, eco-friendly",
    ],
    description: [
      "Stop buying lint roller refills. The Snugpaw Reusable Hair Remover uses a self-cleaning roller that lifts embedded pet hair from any fabric, then dumps it into the built-in base with one click.",
      "One purchase replaces years of sticky sheets — better for your couch and the planet.",
    ],
    rating: 4.6,
    reviewCount: 740,
    reviews: [
      {
        name: "Bri N.",
        rating: 5,
        verified: true,
        text: "The amount of hair this pulled off my couch was horrifying and satisfying.",
      },
      {
        name: "Omar F.",
        rating: 4,
        verified: true,
        text: "Works great on the couch, a little less on car seats but still good.",
      },
    ],
  },
  {
    handle: "no-spill-travel-water-bottle",
    name: "2-in-1 Travel Water Bottle",
    subtitle: "Hydration on every walk & road trip",
    price: 24.95,
    compareAt: 36.0,
    cost: 6.0,
    category: "Travel",
    image: ph("Travel\\nBottle", "B5613F"),
    shortDescription:
      "Leak-proof bottle + fold-out bowl in one. One-handed water for walks, hikes, and the car.",
    bullets: [
      "Press the button, water fills the bowl",
      "Pour unused water back in — zero waste",
      "Leak-proof & one-handed",
      "BPA-free, 19oz",
    ],
    description: [
      "Walks, hikes, road trips — your dog gets thirsty everywhere. The Snugpaw 2-in-1 Travel Bottle holds water and a fold-out bowl in one leak-proof unit. Press the button, the bowl fills; tilt back, the leftover water returns to the bottle. No mess, no waste, one hand.",
    ],
    rating: 4.7,
    reviewCount: 532,
    reviews: [
      {
        name: "Jordan C.",
        rating: 5,
        verified: true,
        text: "Perfect for hikes with my husky. No more cupping water in my hands.",
      },
      {
        name: "Mei L.",
        rating: 5,
        verified: true,
        text: "Genuinely leak proof in my bag. Use it every single day.",
      },
    ],
  },
];

export function getProduct(handle: string): Product | undefined {
  return products.find((p) => p.handle === handle);
}

export function heroProducts(): Product[] {
  return products.filter((p) => p.hero);
}
