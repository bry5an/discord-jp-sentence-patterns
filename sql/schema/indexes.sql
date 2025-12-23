-- Run after table schemas are created
create index idx_active_vocab_status
  on public.active_vocab(status);

create index idx_example_phrases_vocab
  on public.example_phrases(vocab_id);

create index idx_example_phrases_grammar
  on public.example_phrases(grammar_id);

create index idx_usage_history_last_used
  on public.usage_history(last_used);
