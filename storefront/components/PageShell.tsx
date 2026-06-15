export function PageShell({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="container-x py-14">
      <h1 className="text-4xl font-extrabold">{title}</h1>
      <div className="prose mt-8 max-w-3xl space-y-4 text-ink/80 [&_h2]:mt-8 [&_h2]:text-xl [&_h2]:font-bold [&_h2]:text-ink [&_li]:ml-5 [&_li]:list-disc">
        {children}
      </div>
    </div>
  );
}
