-- Get all grammar patterns
select pattern, function, register, constraints, example_en
from public.grammar_patterns
order by created_at;

-- Get all active vocabulary
select word, definition, example_en
from public.active_vocab
order by created_at;

-- Edit a grammar pattern constraint for a given pattern
update public.grammar_patterns
set constraints = 'new constraints'
where pattern = 'pattern to edit';
