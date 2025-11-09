import Link from "next/link";

import { Button } from "../components/ui/button";

export default function Page(): JSX.Element {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 bg-background px-6 py-10">
      <section className="flex flex-col items-center gap-3 text-center">
        {/* Badge leverages Tailwind + shadcn tokens to highlight the current pilot program. */}
        <span className="rounded-full border border-border bg-muted px-3 py-1 text-xs font-medium text-muted-foreground">
          Logistics automation pilot
        </span>
        <h1 className="text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
          Container Base Portal
        </h1>
        <p className="max-w-2xl text-base text-muted-foreground">
          Manage container recognition events, billing usage, and AI model rollouts for Thai logistics
          sites in one place.
        </p>
      </section>
      <div className="flex flex-col gap-3 sm:flex-row">
        <Button asChild>
          <Link href="#">Go to dashboard</Link>
        </Button>
        <Button asChild variant="outline">
          <Link href="#">View release notes</Link>
        </Button>
      </div>
    </main>
  );
}
