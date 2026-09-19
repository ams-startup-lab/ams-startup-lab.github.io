// Schemas for every data file. A file that breaks a schema fails the build,
// so a bad edit never reaches the live site.
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const slug = z.string().regex(/^[a-z0-9-]+$/);
const isoDate = z.coerce.date();

const members = defineCollection({
  loader: glob({ pattern: '*.yaml', base: './data/members' }),
  schema: z.object({
    name: z.string(),
    title: z.string(), // academic title, e.g. "Assistant Professor"
    lab_role: z.string().optional(), // e.g. "Lab Director"
    group: z.enum(['faculty', 'phd', 'affiliate']),
    order: z.number().int().default(100),
    joined: isoDate.optional(), // papers before this date are not proposed
    left: isoDate.optional(), // set when a member leaves; they move to alumni
    orcid: z.string().regex(/^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$/).optional(),
    openalex_ids: z.array(z.string().regex(/^A\d+$/)).default([]),
    uva_url: z.string().url().optional(),
    scholar_url: z.string().url().optional(),
    linkedin_url: z.string().url().optional(),
    photo: z.string().optional(), // path under public/
  }).strict(),
});

const publications = defineCollection({
  loader: glob({ pattern: '*.yaml', base: './data/publications' }),
  schema: z.object({
    title: z.string(),
    authors: z.string(), // as printed, e.g. "Chila, V., & Devarakonda, S."
    members: z.array(slug).default([]), // lab members among the authors
    year: z.number().int().min(2000).max(2100),
    journal: z.string(),
    status: z.enum(['published', 'in_press']).default('published'),
    volume: z.string().optional(),
    issue: z.string().optional(),
    pages: z.string().optional(),
    doi: z.string().regex(/^10\.\d{4,9}\/\S+$/).optional(),
    url: z.string().url(),
    added: isoDate.optional(),
  }).strict(),
});

const news = defineCollection({
  loader: glob({ pattern: '*.yaml', base: './data/news' }),
  schema: z.object({
    title: z.string(),
    date: isoDate,
    outlet: z.string(),
    url: z.string().url(),
    summary: z.string().optional(),
    members: z.array(slug).default([]),
  }).strict(),
});

const events = defineCollection({
  loader: glob({ pattern: '*.yaml', base: './data/events' }),
  schema: z.object({
    title: z.string(),
    date: isoDate,
    end_date: isoDate.optional(),
    location: z.string().optional(),
    url: z.string().url().optional(),
    description: z.string().optional(),
  }).strict(),
});

const projects = defineCollection({
  loader: glob({ pattern: '*.md', base: './data/projects' }),
  schema: z.object({
    title: z.string(),
    status: z.enum(['active', 'completed']).default('active'),
    order: z.number().int().default(100),
    partners: z.array(z.string()).default([]),
    members: z.array(slug).default([]),
    summary: z.string(),
    url: z.string().url().optional(),
  }).strict(),
});

// Site-wide texts (hero, about, contact). Free-form on purpose.
const site = defineCollection({
  loader: glob({ pattern: 'site.yaml', base: './data' }),
  schema: z.object({ name: z.string() }).passthrough(),
});

export const collections = { site, members, publications, news, events, projects };
