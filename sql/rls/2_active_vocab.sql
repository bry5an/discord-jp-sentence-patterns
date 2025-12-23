create policy "bot can read active_vocab"
on public.active_vocab
for select
using (true);

create policy "bot can insert active_vocab"
on public.active_vocab
for insert
with check (true);

create policy "bot can delete active_vocab"
on public.active_vocab
for delete
using (true);
