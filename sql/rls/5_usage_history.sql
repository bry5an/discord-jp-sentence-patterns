create policy "bot can read usage_history"
on public.usage_history
for select
using (true);

create policy "bot can insert usage_history"
on public.usage_history
for insert
with check (true);

create policy "bot can update usage_history"
on public.usage_history
for update
using (true)
with check (true);

create policy "bot can delete usage_history"
on public.usage_history
for delete
using (true);
