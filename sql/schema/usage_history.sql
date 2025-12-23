create table public.usage_history (
  id uuid primary key default gen_random_uuid(),

  vocab_id uuid not null
    references public.active_vocab(id)
    on delete cascade,

  grammar_id uuid
    references public.grammar_patterns(id)
    on delete set null,

  last_used timestamptz not null default now(),
  times_used integer not null default 1,

  unique (vocab_id, grammar_id)
);
