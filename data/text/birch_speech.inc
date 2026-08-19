@ Arauna introduction language selector.
@ 0 = English, 1 = Portuguese (Brazil).
@ Normal builds default to Portuguese so the current main behavior is preserved.
#ifndef ARAUNA_LANGUAGE
#define ARAUNA_LANGUAGE 1
#endif

#if ARAUNA_LANGUAGE == 1
#include "data/text/arauna/pt_br/birch_speech.inc"
#elif ARAUNA_LANGUAGE == 0
#include "data/text/arauna/en/birch_speech.inc"
#else
#error Unsupported ARAUNA_LANGUAGE; use 0 (English) or 1 (Portuguese)
#endif
