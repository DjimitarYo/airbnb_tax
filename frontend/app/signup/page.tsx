"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { Building2, Home, Sparkles, UserRoundCheck, UserPlus } from "lucide-react";
import { UserRole, apiFetch } from "../../lib/api";

type SignupRole = Extract<UserRole, "host" | "cleaner" | "agency">;

const roles: Array<{
  value: SignupRole;
  label: string;
  description: string;
  icon: typeof Home;
}> = [
  {
    value: "host",
    label: "Property owner",
    description: "Post cleaning jobs after admin approval.",
    icon: Home,
  },
  {
    value: "cleaner",
    label: "Cleaner",
    description: "Join verified supply and accept work.",
    icon: Sparkles,
  },
  {
    value: "agency",
    label: "Agency",
    description: "Invite cleaners and assign agency work.",
    icon: Building2,
  },
];

export default function SignupPage() {
  const [role, setRole] = useState<SignupRole>("host");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [city, setCity] = useState("");
  const [preferredLanguage, setPreferredLanguage] = useState<"bg" | "en">("bg");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function submitSignup(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      const response = await apiFetch("/api/accounts/signup/", {
        method: "POST",
        body: JSON.stringify({
          role,
          name,
          email,
          phone_number: phoneNumber,
          city,
          preferred_language: preferredLanguage,
          password,
        }),
      });
      if (!response.ok) {
        const data = (await response.json().catch(() => null)) as { detail?: string } | null;
        setError(data?.detail ?? "Check the signup details and try again.");
        return;
      }
      window.location.href = "/app";
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-panel wide-auth-panel">
        <Link className="site-brand auth-brand" href="/">
          <span className="brand-symbol">
            <UserPlus size={18} aria-hidden />
          </span>
          <strong>Host Cleaners</strong>
        </Link>
        <div className="auth-heading">
          <p className="eyebrow">Manual approval MVP</p>
          <h1>Create account</h1>
          <p>Signup requests open an onboarding account. Marketplace rights start after admin approval.</p>
        </div>

        <form className="auth-form" onSubmit={submitSignup}>
          <div className="role-grid" role="radiogroup" aria-label="Account type">
            {roles.map((option) => {
              const Icon = option.icon;
              return (
                <button
                  aria-checked={role === option.value}
                  className={role === option.value ? "role-option selected" : "role-option"}
                  key={option.value}
                  onClick={() => setRole(option.value)}
                  role="radio"
                  type="button"
                >
                  <Icon size={20} aria-hidden />
                  <span>{option.label}</span>
                  <small>{option.description}</small>
                </button>
              );
            })}
          </div>

          <div className="form-grid">
            <label>
              <span>{role === "agency" ? "Agency name" : "Name"}</span>
              <input
                autoComplete="name"
                required
                value={name}
                onChange={(event) => setName(event.target.value)}
              />
            </label>
            <label>
              <span>Email</span>
              <input
                autoComplete="email"
                required
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
              />
            </label>
            <label>
              <span>Phone</span>
              <input
                autoComplete="tel"
                value={phoneNumber}
                onChange={(event) => setPhoneNumber(event.target.value)}
              />
            </label>
            <label>
              <span>City</span>
              <input
                autoComplete="address-level2"
                value={city}
                onChange={(event) => setCity(event.target.value)}
              />
            </label>
            <label>
              <span>Language</span>
              <select
                value={preferredLanguage}
                onChange={(event) => setPreferredLanguage(event.target.value as "bg" | "en")}
              >
                <option value="bg">Bulgarian</option>
                <option value="en">English</option>
              </select>
            </label>
            <label>
              <span>Password</span>
              <input
                autoComplete="new-password"
                minLength={8}
                required
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
              />
            </label>
          </div>

          {error ? <p className="form-error">{error}</p> : null}
          <button className="primary-link auth-submit" type="submit" disabled={submitting}>
            <UserRoundCheck size={18} aria-hidden />
            {submitting ? "Creating account" : "Create account"}
          </button>
        </form>

        <p className="auth-switch">
          Already registered? <Link href="/login">Log in</Link>
        </p>
      </section>
    </main>
  );
}
