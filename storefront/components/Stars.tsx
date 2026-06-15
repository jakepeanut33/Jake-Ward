export function Stars({ rating, className = "" }: { rating: number; className?: string }) {
  const full = Math.round(rating);
  return (
    <span className={`text-clay ${className}`} aria-label={`${rating} out of 5 stars`}>
      {"★".repeat(full)}
      <span className="text-ink/20">{"★".repeat(5 - full)}</span>
    </span>
  );
}
