#!/usr/bin/env python3
"""Compatibility entrypoint. Current checks are in validate_fogueira_arcos.py.

--legacy-v1 is ONLY for an exact historical V1 checkout/package. It is not a
certificate for the current scene. The source model does not execute ARM.
"""
import sys
from pathlib import Path
if '--legacy-v1' in sys.argv:
    sys.argv.remove('--legacy-v1')
    from validate_fogueira_roda_v1_snapshot import main
    print('Historical V1 validation: requires the exact V1 snapshot.', file=sys.stderr)
else:
    from validate_fogueira_arcos import main
    print('V1 entrypoint redirected to current Fogueira/Noise Tower validation.', file=sys.stderr)
if __name__ == '__main__':
    main()
