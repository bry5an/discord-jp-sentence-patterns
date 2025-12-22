insert into public.grammar_patterns
  (pattern, function, register, constraints, example_en)
values
  -- Core conversational patterns
  ('～てる', 'describing current state', 'casual',
    'spoken Japanese, contraction of ～ている, first-person preferred',
    'I’m doing / I’ve been doing'),

  ('～てるんだけど', 'soft topic introduction', 'casual',
    'spoken Japanese, first-person, used to gently start a topic or question',
    'I was kind of wondering…'),

  ('～かな', 'expressing uncertainty or wondering', 'casual',
    'used for first-person thoughts, soft uncertainty',
    'I wonder if…'),

  ('～と思う', 'soft opinion or belief', 'casual',
    'used to avoid sounding too assertive',
    'I think…'),

  ('～かもしれない', 'hedging / uncertainty', 'casual',
    'used when unsure, avoids strong claims',
    'It might be…'),

  ('～てなくて', 'explaining why something is not done', 'casual',
    'used to give a reason casually',
    'I didn’t do it, so…'),

  ('まだ～てない', 'not yet', 'casual',
    'very common spoken structure',
    'I haven’t done it yet'),

  ('～てみる', 'trying something', 'casual',
    'used when attempting or experimenting',
    'I’ll try doing…'),

  ('～ておく', 'doing something in advance', 'casual',
    'used when preparing ahead of time',
    'I’ll do it beforehand'),

  ('～ほうがいい', 'gentle advice or suggestion', 'casual',
    'used to give advice softly, not commanding',
    'It’s probably better to…'),

  -- Interaction & reactions
  ('～って', 'quoting or reacting casually', 'casual',
    'used for quoting speech or reacting informally',
    'They said… / Like…'),

  ('なるほど', 'acknowledgment or understanding', 'casual',
    'used to show understanding, often alone or with follow-up',
    'I see'),

  ('そういうことか', 'realization', 'casual',
    'used when something finally makes sense',
    'Oh, that’s what it is'),

  ('～らしい', 'hearsay', 'casual',
    'used when information is second-hand',
    'Apparently…'),

  ('～みたい', 'impression or resemblance', 'casual',
    'used for impressions, guesses, or resemblance',
    'It seems like…'),

  -- Softening / framing
  ('ちょっと', 'softening statements or requests', 'casual',
    'used to soften tone or reduce directness',
    'A little / kind of'),

  ('一応', 'hedging or provisional action', 'casual',
    'used to mean just in case or for now',
    'Just in case'),

  ('正直', 'framing honesty', 'casual',
    'used to preface honest opinions',
    'Honestly'),

  ('別に～ない', 'downplaying or minimizing', 'casual',
    'used to indicate something is not a big deal',
    'It’s not like…')
on conflict (pattern) do nothing;
