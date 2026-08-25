#!/usr/bin/env python3
"""Named waypoints through the opening, driven by the game's own state.

Every step waits on a task or callback symbol read out of memory rather than
on a timer, so it does not matter how long a fade takes on this machine. The
opening is the awkward part -- Anahi's speech, the gender choice and the
naming screen all run as tasks under CB2_MainMenu, so the main callback never
changes and cannot be followed.

    python3 tools/audit/route.py opening --checkpoint
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from play import CHECKPOINTS, Session                          # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]


def has_task(name: str):
    return lambda p: name in p.active_tasks()


def opening(s: Session, shots: bool = True) -> None:
    # Boot -> title. Start skips the intro; the title's own callback is MainCB2.
    # Phase 3 is the settled, interactive title -- phases 1 and 2 are still
    # sliding the logo in, which is why a plain wait caught a bare logo.
    s.wait_callback("MainCB2", button="start", timeout=180)
    s.wait_for(has_task("Task_TitleScreenPhase3"), timeout=60, label="title settled")
    s.probe.run(1.5)
    if shots:
        s.shot("01_title")
    print("  title screen")

    s.wait_for(has_task("Task_HandleMainMenuInput"), button="start", timeout=90,
               label="main menu")
    s.probe.run(1.5)
    if shots:
        s.shot("02_main_menu")
    print("  main menu")

    # NEW GAME is already selected.
    s.wait_for(has_task("Task_NewGameBirchSpeech_MainSpeech"), button="a",
               timeout=120, label="Anahi's speech")
    s.probe.run(1.0)
    if shots:
        s.shot("03_anahi_speech")
    print("  Anahi's speech")

    s.wait_for(has_task("Task_NewGameBirchSpeech_ChooseGender"), button="a",
               timeout=120, label="gender choice")
    s.probe.run(1.0)
    if shots:
        s.shot("04_gender")
    print("  gender choice")

    s.wait_callback("CB2_NamingScreen", button="a", timeout=120)
    s.probe.run(1.5)
    if shots:
        s.shot("05_naming")
    print("  naming screen")

    # Type one letter, then Start confirms via OK.
    s.press("a")
    s.press("start")
    s.wait_for(has_task("Task_NewGameBirchSpeech_ProcessNameYesNoMenu"),
               button="a", timeout=90, label="name confirmation")
    s.probe.run(1.0)
    if shots:
        s.shot("06_name_confirm")
    print("  name confirmation")

    # CB2_Overworld comes up while the screen is still black inside the truck;
    # the truck tasks retiring is what means "the player can see and move".
    s.wait_callback("CB2_Overworld", button="a", timeout=180)
    s.wait_for(lambda p: not any(t.startswith(("Task_Truck", "Task_HandleTruck"))
                                 for t in p.active_tasks()),
               button="a", timeout=180, label="truck sequence to finish")
    s.probe.run(2.0)
    if shots:
        s.shot("07_overworld")
    print("  overworld:", s.probe.summary())


ROUTES = {"opening": opening}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("route", choices=sorted(ROUTES))
    ap.add_argument("--resume", help="checkpoint name or path to resume from")
    ap.add_argument("--checkpoint", action="store_true",
                    help="save an mGBA savestate at the end of the route")
    ap.add_argument("--no-shots", action="store_true")
    args = ap.parse_args()

    resume = None
    if args.resume:
        resume = pathlib.Path(args.resume)
        if not resume.is_file():
            resume = CHECKPOINTS / f"{args.resume}.ss1"
        if not resume.is_file():
            raise SystemExit(f"no checkpoint at {resume}")
    session = Session(savestate=resume)
    try:
        ROUTES[args.route](session, shots=not args.no_shots)
        if args.checkpoint:
            path = session.savestate(args.route)
            print(f"  checkpoint: {path.relative_to(ROOT)}")
        return 0
    finally:
        session.close()


if __name__ == "__main__":
    raise SystemExit(main())
