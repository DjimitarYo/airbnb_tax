import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Host Cleaner Marketplace",
    short_name: "Cleaners",
    description: "Scheduling marketplace for hosts, cleaners, and agencies in Bulgaria.",
    start_url: "/",
    display: "standalone",
    background_color: "#f7f7f2",
    theme_color: "#0f766e",
  };
}

