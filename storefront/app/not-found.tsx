import Link from "next/link";

export default function NotFound() {
  return (
    <div className="container-x py-24 text-center">
      <p className="text-6xl">🐾</p>
      <h1 className="mt-4 text-3xl font-extrabold">This page wandered off</h1>
      <p className="mt-2 text-ink/60">We couldn't find what you were looking for.</p>
      <Link href="/" className="btn-primary mt-6">Back home</Link>
    </div>
  );
}
