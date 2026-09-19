import { getCollection, getEntry } from 'astro:content';

export const fmtDate = (d: Date) =>
  d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' });

export async function siteTexts() {
  return (await getEntry('site', 'site'))!.data as any;
}

export async function publications() {
  const all = await getCollection('publications');
  // Newest first. Within a year: most recently added first, then by title.
  return all.sort((a, b) =>
    b.data.year - a.data.year ||
    (b.data.added?.getTime() ?? 0) - (a.data.added?.getTime() ?? 0) ||
    a.data.title.localeCompare(b.data.title));
}

export async function news() {
  return (await getCollection('news')).sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
}

export async function events() {
  const all = (await getCollection('events')).sort((a, b) => a.data.date.getTime() - b.data.date.getTime());
  const today = new Date(new Date().toISOString().slice(0, 10));
  const end = (e: (typeof all)[number]) => e.data.end_date ?? e.data.date;
  return { upcoming: all.filter((e) => end(e) >= today), past: all.filter((e) => end(e) < today).reverse() };
}

export async function members() {
  const all = (await getCollection('members')).sort((a, b) => a.data.order - b.data.order);
  return { current: all.filter((m) => !m.data.left), alumni: all.filter((m) => m.data.left) };
}

export const pubMeta = (p: { journal: string; year: number; status: string; volume?: string; issue?: string; pages?: string }) => {
  let s = p.journal;
  if (p.volume) s += `, ${p.volume}${p.issue ? `(${p.issue})` : ''}`;
  if (p.pages) s += `, ${p.pages}`;
  return p.status === 'in_press' ? `${s} · In press` : `${s} · ${p.year}`;
};
