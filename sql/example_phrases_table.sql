create table public.example_phrases (
  id uuid primary key default gen_random_uuid(),

  vocab_id uuid not null
    references public.active_vocab(id)
    on delete cascade,

  grammar_id uuid not null
    references public.grammar_patterns(id)
    on delete restrict,

  sentence_ja text not null,
  sentence_en text,
  usage_note text,

  register text not null default 'casual',

  created_at timestamptz not null default now()
);
