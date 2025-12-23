create policy "bot can read example_phrases"
on public.example_phrases
for select
using (true);

create policy "bot can insert example_phrases"
on public.example_phrases
for insert
with check (true);

create policy "bot can delete example_phrases"
on public.example_phrases
for delete
using (true);
