create table public.grammar_patterns (
  id uuid primary key default gen_random_uuid(),

  pattern text not null,
  function text not null,
  register text not null default 'casual',
  constraints text,
  example_en text,

  created_at timestamptz not null default now(),

  unique (pattern)
);
