"use client";

import { FormEvent, useMemo, useState } from "react";
import {
  Bell,
  Building2,
  CalendarDays,
  CheckCircle2,
  ClipboardList,
  Plus,
  Send,
  ShieldCheck,
  Sparkles,
  Star,
  Users,
  X,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

type ViewKey = "dashboard" | "calendar" | "cleaners" | "feedback";

type Job = {
  id: number;
  title: string;
  property: string;
  time: string;
  status: "Draft" | "Open" | "Assigned" | "Completed" | "Needs supply";
  applicants: number;
  price: string;
};

type Cleaner = {
  id: number;
  name: string;
  kind: "Individual" | "Agency";
  area: string;
  status: "Verified" | "Pending";
  rating: string;
};

const navItems: Array<{ key: ViewKey; label: string; icon: LucideIcon }> = [
  { key: "dashboard", label: "Dashboard", icon: ClipboardList },
  { key: "calendar", label: "Calendar", icon: CalendarDays },
  { key: "cleaners", label: "Cleaners", icon: ShieldCheck },
  { key: "feedback", label: "Feedback", icon: Star },
];

const workflow = [
  {
    title: "Post cleaning work",
    body: "Hosts create one cleaning or a monthly batch from property calendar demand.",
    icon: Building2,
  },
  {
    title: "Cleaners apply",
    body: "Verified cleaners and agencies apply only when the job fits their availability.",
    icon: Sparkles,
  },
  {
    title: "Assign and coordinate",
    body: "The host accepts one applicant, the calendar stays shared, and reminders go out.",
    icon: CalendarDays,
  },
  {
    title: "Review both sides",
    body: "After completion, host and cleaner leave feedback to build marketplace trust.",
    icon: Star,
  },
];

const initialJobs: Job[] = [
  {
    id: 1,
    title: "Turnover cleaning",
    property: "Center Apartment, Sofia",
    time: "Tomorrow, 11:00-13:00",
    status: "Draft",
    applicants: 0,
    price: "EUR 45",
  },
  {
    id: 2,
    title: "Monthly batch",
    property: "Sea View Studio, Varna",
    time: "June planning",
    status: "Open",
    applicants: 3,
    price: "Price agreed per job",
  },
  {
    id: 3,
    title: "Backup cleaner needed",
    property: "Old Town Flat, Plovdiv",
    time: "Friday, 10:30-12:30",
    status: "Needs supply",
    applicants: 0,
    price: "EUR 55",
  },
];

const initialCleaners: Cleaner[] = [
  {
    id: 1,
    name: "Mira Cleaning",
    kind: "Agency",
    area: "Sofia",
    status: "Verified",
    rating: "4.9",
  },
  {
    id: 2,
    name: "Elena Petrova",
    kind: "Individual",
    area: "Plovdiv",
    status: "Pending",
    rating: "New",
  },
  {
    id: 3,
    name: "Black Sea Turnovers",
    kind: "Agency",
    area: "Varna, Burgas",
    status: "Verified",
    rating: "4.7",
  },
];

const notifications = [
  "Mira Cleaning applied to the Varna monthly batch.",
  "Calendar sync placeholder is ready for provider integration.",
  "Two reviews are waiting after completed jobs.",
];

export default function Home() {
  const [activeView, setActiveView] = useState<ViewKey>("dashboard");
  const [jobs, setJobs] = useState<Job[]>(initialJobs);
  const [cleaners, setCleaners] = useState<Cleaner[]>(initialCleaners);
  const [selectedJobId, setSelectedJobId] = useState(1);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [form, setForm] = useState({
    title: "",
    property: "Center Apartment, Sofia",
    date: "",
    time: "",
    price: "",
  });

  const selectedJob = jobs.find((job) => job.id === selectedJobId) ?? jobs[0];
  const openJobs = jobs.filter((job) => job.status === "Open" || job.status === "Needs supply");
  const completedJobs = jobs.filter((job) => job.status === "Completed");
  const verifiedSupply = cleaners.filter((cleaner) => cleaner.status === "Verified");

  const metrics = useMemo(
    () => [
      { label: "Registered users", value: String(cleaners.length + 2), icon: Users },
      { label: "Open jobs", value: String(openJobs.length), icon: ClipboardList },
      { label: "Verified supply", value: String(verifiedSupply.length), icon: ShieldCheck },
      { label: "Completed cleanings", value: String(completedJobs.length), icon: CheckCircle2 },
    ],
    [cleaners.length, completedJobs.length, openJobs.length, verifiedSupply.length],
  );

  function createDraftCleaning(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const nextJob: Job = {
      id: Date.now(),
      title: form.title || "New cleaning",
      property: form.property,
      time: [form.date, form.time].filter(Boolean).join(", ") || "Time not set",
      status: "Draft",
      applicants: 0,
      price: form.price ? `EUR ${form.price}` : "Price to agree",
    };

    setJobs((current) => [nextJob, ...current]);
    setSelectedJobId(nextJob.id);
    setActiveView("dashboard");
    setIsModalOpen(false);
    setForm({
      title: "",
      property: "Center Apartment, Sofia",
      date: "",
      time: "",
      price: "",
    });
  }

  function publishSelectedJob() {
    setJobs((current) =>
      current.map((job) =>
        job.id === selectedJob.id && job.status === "Draft" ? { ...job, status: "Open" } : job,
      ),
    );
  }

  function verifyCleaner(cleanerId: number) {
    setCleaners((current) =>
      current.map((cleaner) =>
        cleaner.id === cleanerId ? { ...cleaner, status: "Verified" } : cleaner,
      ),
    );
  }

  return (
    <main className="app-shell">
      <aside className="sidebar" aria-label="Primary">
        <div className="brand">
          <span className="brand-mark">HC</span>
          <div>
            <strong>Host Cleaners</strong>
            <span>Bulgaria</span>
          </div>
        </div>
        <nav className="nav-list">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                className={activeView === item.key ? "active" : ""}
                key={item.key}
                onClick={() => setActiveView(item.key)}
                type="button"
              >
                <Icon size={18} aria-hidden />
                {item.label}
              </button>
            );
          })}
        </nav>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">MVP operations dashboard</p>
            <h1>{headingFor(activeView)}</h1>
          </div>
          <div className="topbar-actions">
            <button
              className="icon-button"
              type="button"
              aria-label="Notifications"
              onClick={() => setNotificationsOpen((open) => !open)}
            >
              <Bell size={20} aria-hidden />
            </button>
            {notificationsOpen ? (
              <div className="notification-popover">
                <strong>Notifications</strong>
                {notifications.map((notification) => (
                  <p key={notification}>{notification}</p>
                ))}
              </div>
            ) : null}
          </div>
        </header>

        {activeView === "dashboard" ? (
          <DashboardView
            jobs={jobs}
            metrics={metrics}
            selectedJob={selectedJob}
            onCreate={() => setIsModalOpen(true)}
            onPublish={publishSelectedJob}
            onSelectJob={setSelectedJobId}
          />
        ) : null}

        {activeView === "calendar" ? <CalendarView jobs={jobs} /> : null}
        {activeView === "cleaners" ? (
          <CleanersView cleaners={cleaners} onVerify={verifyCleaner} />
        ) : null}
        {activeView === "feedback" ? <FeedbackView /> : null}
      </section>

      {isModalOpen ? (
        <div className="modal-backdrop" role="presentation">
          <form className="modal" onSubmit={createDraftCleaning}>
            <div className="panel-heading">
              <div>
                <p className="eyebrow">New draft</p>
                <h2>Create cleaning</h2>
              </div>
              <button
                className="icon-button"
                type="button"
                aria-label="Close"
                onClick={() => setIsModalOpen(false)}
              >
                <X size={18} aria-hidden />
              </button>
            </div>

            <label>
              Title
              <input
                value={form.title}
                onChange={(event) => setForm({ ...form, title: event.target.value })}
                placeholder="Turnover cleaning"
              />
            </label>
            <label>
              Property
              <select
                value={form.property}
                onChange={(event) => setForm({ ...form, property: event.target.value })}
              >
                <option>Center Apartment, Sofia</option>
                <option>Sea View Studio, Varna</option>
                <option>Old Town Flat, Plovdiv</option>
              </select>
            </label>
            <div className="form-grid">
              <label>
                Date
                <input
                  type="date"
                  value={form.date}
                  onChange={(event) => setForm({ ...form, date: event.target.value })}
                />
              </label>
              <label>
                Time
                <input
                  type="time"
                  value={form.time}
                  onChange={(event) => setForm({ ...form, time: event.target.value })}
                />
              </label>
            </div>
            <label>
              Suggested price EUR
              <input
                inputMode="decimal"
                value={form.price}
                onChange={(event) => setForm({ ...form, price: event.target.value })}
                placeholder="45"
              />
            </label>
            <button className="primary-action" type="submit">
              <Plus size={18} aria-hidden />
              Save draft
            </button>
          </form>
        </div>
      ) : null}
    </main>
  );
}

function DashboardView({
  jobs,
  metrics,
  selectedJob,
  onCreate,
  onPublish,
  onSelectJob,
}: {
  jobs: Job[];
  metrics: Array<{ label: string; value: string; icon: LucideIcon }>;
  selectedJob: Job;
  onCreate: () => void;
  onPublish: () => void;
  onSelectJob: (id: number) => void;
}) {
  return (
    <>
      <section className="metric-grid" aria-label="Marketplace metrics">
        {metrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <article className="metric-card" key={metric.label}>
              <Icon size={20} aria-hidden />
              <span>{metric.label}</span>
              <strong>{metric.value}</strong>
            </article>
          );
        })}
      </section>

      <section className="content-grid">
        <div className="panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">Marketplace workflow</p>
              <h2>From calendar demand to completed work</h2>
            </div>
            <button type="button" className="primary-action" onClick={onCreate}>
              <ClipboardList size={18} aria-hidden />
              New cleaning
            </button>
          </div>
          <div className="workflow-grid">
            {workflow.map((item) => {
              const Icon = item.icon;
              return (
                <article className="workflow-card" key={item.title}>
                  <Icon size={22} aria-hidden />
                  <h3>{item.title}</h3>
                  <p>{item.body}</p>
                </article>
              );
            })}
          </div>
          <SelectedJobCard job={selectedJob} onPublish={onPublish} />
        </div>

        <div className="panel compact-panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">Pipeline</p>
              <h2>Cleaning jobs</h2>
            </div>
          </div>
          <div className="job-list">
            {jobs.map((job) => (
              <button
                className={`job-row ${selectedJob.id === job.id ? "selected" : ""}`}
                key={job.id}
                onClick={() => onSelectJob(job.id)}
                type="button"
              >
                <div>
                  <h3>{job.title}</h3>
                  <p>{job.property}</p>
                  <span>{job.time}</span>
                </div>
                <strong>{job.status}</strong>
              </button>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}

function CalendarView({ jobs }: { jobs: Job[] }) {
  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Shared schedule</p>
          <h2>Upcoming cleaning calendar</h2>
        </div>
      </div>
      <div className="timeline">
        {jobs.map((job) => (
          <article key={job.id}>
            <CalendarDays size={18} aria-hidden />
            <div>
              <h3>{job.title}</h3>
              <p>{job.property}</p>
            </div>
            <span>{job.time}</span>
          </article>
        ))}
      </div>
    </section>
  );
}

function CleanersView({
  cleaners,
  onVerify,
}: {
  cleaners: Cleaner[];
  onVerify: (id: number) => void;
}) {
  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Verified supply</p>
          <h2>Cleaner and agency network</h2>
        </div>
      </div>
      <div className="cleaner-grid">
        {cleaners.map((cleaner) => (
          <article className="workflow-card" key={cleaner.id}>
            <ShieldCheck size={22} aria-hidden />
            <h3>{cleaner.name}</h3>
            <p>
              {cleaner.kind} in {cleaner.area}
            </p>
            <span className="meta-line">
              {cleaner.status} · Rating {cleaner.rating}
            </span>
            {cleaner.status === "Pending" ? (
              <button className="secondary-action" type="button" onClick={() => onVerify(cleaner.id)}>
                Verify cleaner
              </button>
            ) : null}
          </article>
        ))}
      </div>
    </section>
  );
}

function FeedbackView() {
  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Reputation</p>
          <h2>Two-way feedback queue</h2>
        </div>
      </div>
      <div className="feedback-list">
        <article>
          <Star size={20} aria-hidden />
          <div>
            <h3>Host review pending</h3>
            <p>Center Apartment turnover cleaning was completed. Host can rate cleaner reliability.</p>
          </div>
          <button className="secondary-action" type="button">
            Draft review
          </button>
        </article>
        <article>
          <Send size={20} aria-hidden />
          <div>
            <h3>Cleaner feedback pending</h3>
            <p>Cleaner can privately report unclear instructions or property access issues.</p>
          </div>
          <button className="secondary-action" type="button">
            Open form
          </button>
        </article>
      </div>
    </section>
  );
}

function SelectedJobCard({ job, onPublish }: { job: Job; onPublish: () => void }) {
  return (
    <article className="selected-job-card">
      <div>
        <p className="eyebrow">Selected job</p>
        <h3>{job.title}</h3>
        <p>{job.property}</p>
      </div>
      <div className="selected-job-meta">
        <span>{job.time}</span>
        <span>{job.price}</span>
        <span>{job.applicants} applicants</span>
      </div>
      <button
        className="secondary-action"
        type="button"
        onClick={onPublish}
        disabled={job.status !== "Draft"}
      >
        Publish draft
      </button>
    </article>
  );
}

function headingFor(view: ViewKey) {
  const headings: Record<ViewKey, string> = {
    dashboard: "Cleaning marketplace control center",
    calendar: "Shared calendar",
    cleaners: "Cleaner verification and supply",
    feedback: "Feedback and trust",
  };

  return headings[view];
}
