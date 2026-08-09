@ The first playable Arauna release is English-only.
@ The Porto runtime script is pulled in as a top-level .include from
@ data/event_scripts.s so the first preproc pass inlines it before cpp,
@ letting its FLAG_*/VAR_* macros expand.
	.include "data/text/arauna/en/porto_das_redes.inc"
