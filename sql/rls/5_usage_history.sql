create policy "bot can read usage_history"
on public.usage_history
for select
to anon, authenticated
using (true);

create policy "bot can insert usage_history"
on public.usage_history
for insert
to anon, authenticated
with check (true);

create policy "bot can update usage_history"
on public.usage_history
for update
to anon, authenticated
using (true)
with check (true);

create policy "bot can delete usage_history"
on public.usage_history
for delete
to anon, authenticated
using (true);
