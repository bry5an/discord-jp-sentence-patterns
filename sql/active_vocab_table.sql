create table public.active_vocab (
  id uuid primary key default gen_random_uuid(),

  word text not null,
  reading text,
  meaning text,

  priority integer not null default 1,
  status text not null default 'active'
    check (status in ('active', 'paused')),

  added_at timestamptz not null default now(),

  unique (word)
);
