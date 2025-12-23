create policy "bot can read grammar_patterns"
on public.grammar_patterns
for select
using (true);
