import { notFound } from "next/navigation";

// The catalog and study pages are preserved static assets. Vinext handles misses.
export default function Page() { notFound(); }
