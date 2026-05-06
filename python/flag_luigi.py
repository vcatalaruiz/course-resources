import os
import time
import sys
import random

def hard_clear():
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()

# Canvas width: 50 chars
# Pit is columns 20-35  (~16 wide)
# Rope anchor is at column 27 (center of pit)
# Left bank: cols 0-19, Right bank: cols 36-49

CANOPY = "-"*22

def draw_scene(swing_phase=0, state="idle", msg=""):
    """
    swing_phase: 0=left, 1=center, 2=right
    state: idle | swinging | falling | safe
    """

    # Rope anchor hangs from canopy at col ~26
    # swing_phase shifts the rope bottom left/center/right over the pit

    # rope bottom x offset from anchor: left=-6, center=0, right=+6
    offsets = [-6, 0, 6]
    dx = offsets[swing_phase]

    # Prebuilt rope lines  (each string is exactly 50 chars wide using spaces)
    # Rope anchor at col 26 from left
    # Line 1 (top of rope, near canopy): always straight down
    # Lines 2-4: lean with dx

    def rope_line(row, dx, anchor=26):
        """Return a 50-char string with rope char at interpolated position."""
        x = anchor + (dx * row) // 4
        line = list(" " * 50)
        line[max(0, min(49, x))] = "|" if dx == 0 else ("\\" if dx > 0 else "/")
        return "".join(line)

    # Player char
    p_hang  = "O"   # hanging on rope
    p_walk  = "O"   # standing
    p_fall  = "X"   # falling/dead

    # rope bottom position
    rope_bottom_x = 26 + dx

    # Build the 8-row scene as a list of 50-char strings
    rows = [list(" " * 50) for _ in range(8)]

    if state in ("swinging",):
        # Draw rope from row 0 to row 4
        for row in range(5):
            x = 26 + (dx * row) // 4
            x = max(0, min(49, x))
            rows[row][x] = "|" if dx == 0 else ("\\" if dx > 0 else "/")
        # Player hangs at bottom of rope (row 4)
        px = 26 + dx
        if 0 <= px < 49:
            rows[4][max(0,px-1)] = "("
            rows[4][px]          = p_hang
            rows[4][min(49,px+1)]= ")"

    elif state == "falling":
        # Rope swings back empty
        for row in range(5):
            rows[row][26] = "|"
        # Player falling into pit row 5-6
        rows[5][27] = p_fall
        rows[6][27] = "|"

    elif state == "idle":
        # Rope hangs still at center
        for row in range(5):
            rows[row][26] = "|"
        # Player stands on left bank (col 10)
        rows[6][10] = p_walk
        rows[7][10] = "|"

    elif state == "safe":
        # Rope hangs center, player on right bank
        for row in range(5):
            rows[row][26] = "|"
        rows[6][38] = p_walk
        rows[7][38] = "|"

    # Ground row (row 7): left bank, pit, right bank
    ground = list("=" * 50)
    for i in range(20, 36):
        ground[i] = "~" if state == "falling" else " "
    if state in ("swinging", "idle", "safe"):
        for i in range(20, 36):
            ground[i] = " "
    # pit walls
    ground[19] = "|"
    ground[36] = "|"

    # Merge ground into row 7
    rows[7] = ground

    # Print everything
    print(CANOPY)
    print(f"  {'PITFALL':^20}  {msg}")
    print()
    for row in rows:
        print("".join(row))
    print()
    print("  LEFT BANK            PIT              RIGHT BANK")
    print("  " + "=" * 19 + "  " + "~" * 14 + "  " + "=" * 12)


def animate_swing(success):
    """Animate the player swinging over the pit."""
    # Phase sequence: idle left -> swing left -> swing center -> swing right -> land/fall
    if success:
        steps = [
            ("idle",     1, "JUMP!"),
            ("swinging", 0, "HANG ON!"),
            ("swinging", 1, "FLYING!"),
            ("swinging", 2, "ALMOST!"),
            ("safe",     1, "SAFE!!"),
        ]
    else:
        steps = [
            ("idle",     1, "JUMP!"),
            ("swinging", 0, "HANG ON!"),
            ("swinging", 1, "SLIP!"),
            ("falling",  1, "AHHHHH!"),
            ("falling",  1, "SPLASH!"),
        ]

    for state, phase, msg in steps:
        hard_clear()
        draw_scene(swing_phase=phase, state=state, msg=msg)
        time.sleep(0.35)


QUESTIONS = [
    # --- mkdir ---
    {"q": "Create a directory called 'logs'?",          "opts": ["A. touch logs",   "B. mkdir logs",     "C. cat logs",      "D. grep logs"],    "a": "B"},
    {"q": "Create nested dirs in one command?",         "opts": ["A. mkdir -r",     "B. mkdir --deep",   "C. mkdir -p a/b",  "D. mkdir -n a/b"], "a": "C"},
    {"q": "mkdir stands for...?",                       "opts": ["A. make dir",     "B. modify dir",     "C. move dir",      "D. mount dir"],     "a": "A"},
    {"q": "Create multiple dirs at once?",              "opts": ["A. mkdir a b c",  "B. touch a b c",    "C. cat a b c",     "D. grep a b c"],    "a": "A"},
    {"q": "Which flag lets mkdir create parents?",      "opts": ["A. -v",           "B. -m",             "C. -p",            "D. -r"],            "a": "C"},

    # --- touch ---
    {"q": "Create an empty file called 'notes.txt'?",   "opts": ["A. mkdir notes.txt","B. grep notes.txt","C. cat notes.txt", "D. touch notes.txt"],"a": "D"},
    {"q": "touch on an existing file does what?",       "opts": ["A. Deletes it",   "B. Updates timestamp","C. Prints it",   "D. Renames it"],    "a": "B"},
    {"q": "Create 3 files at once with touch?",         "opts": ["A. touch a+b+c",  "B. touch a,b,c",    "C. touch a b c",   "D. touch [a,b,c]"], "a": "C"},
    {"q": "touch mainly manipulates file...?",          "opts": ["A. Size",         "B. Permissions",    "C. Content",       "D. Timestamp"],     "a": "D"},
    {"q": "Which creates a file if it doesn't exist?",  "opts": ["A. grep",         "B. cat",            "C. touch",         "D. mkdir"],         "a": "C"},

    # --- cat ---
    {"q": "Print contents of file.txt?",                "opts": ["A. grep file.txt","B. cat file.txt",   "C. touch file.txt","D. mkdir file.txt"],"a": "B"},
    {"q": "Concatenate two files into one?",            "opts": ["A. touch a b>c",  "B. grep a b>c",     "C. cat a b > c",   "D. mkdir a b > c"], "a": "C"},
    {"q": "cat stands for...?",                         "opts": ["A. copy and trim","B. concatenate",    "C. catalog",       "D. capture"],       "a": "B"},
    {"q": "Show line numbers with cat?",                "opts": ["A. cat -l",       "B. cat -n",         "C. cat -v",        "D. cat -c"],        "a": "B"},
    {"q": "cat -A shows what extra info?",              "opts": ["A. File size",    "B. Permissions",    "C. Hidden chars",  "D. Line count"],    "a": "C"},

    # --- grep ---
    {"q": "Find 'error' in server.log?",                "opts": ["A. cat error server.log","B. touch error","C. grep error server.log","D. mkdir error"],"a": "C"},
    {"q": "grep -i means...?",                          "opts": ["A. Invert match", "B. Case-insensitive","C. Include files","D. Interactive"],   "a": "B"},
    {"q": "grep -r searches...?",                       "opts": ["A. Remotely",     "B. In reverse",     "C. Recursively",   "D. With regex only"],"a": "C"},
    {"q": "Invert a grep match (non-matching lines)?",  "opts": ["A. grep -n",      "B. grep -x",        "C. grep -v",       "D. grep -i"],       "a": "C"},
    {"q": "grep -c returns...?",                        "opts": ["A. Colored output","B. Match count",   "C. Character pos", "D. Copied matches"],"a": "B"},
]

def game_loop():
    score = 0
    total = len(QUESTIONS)

    for idx, q in enumerate(QUESTIONS):
        hard_clear()
        draw_scene(swing_phase=1, state="idle", msg=f"Q {idx+1}/{total}  SCORE:{score}")

        print(f"\n  CHALLENGE: {q['q']}\n")
        for opt in q["opts"]:
            print(f"    {opt}")

        ans = input("\n  Your move (A/B/C/D): ").strip().upper()
        correct = ans == q["a"]

        animate_swing(correct)

        if correct:
            score += 1
            hard_clear()
            draw_scene(swing_phase=1, state="safe", msg=f"CORRECT! +1")
            print(f"\n  Score: {score}/{total}")
            time.sleep(1.2)
        else:
            hard_clear()
            draw_scene(swing_phase=1, state="falling", msg="GAME OVER")
            print(f"\n  SPLASH! Correct answer was: {q['a']}")
            print(f"  Final score: {score}/{total}")
            print("\n  Better luck next time, adventurer.\n")
            return

    # All questions cleared
    hard_clear()
    print()
    print("  " + "=" * 22)
    print()
    print("   ██████╗  ██████╗ ███╗   ██╗███████╗ ██╗")
    print("   ██╔══██╗██╔═══██╗████╗  ██║██╔════╝ ██║")
    print("   ██║  ██║██║   ██║██╔██╗ ██║█████╗   ██║")
    print("   ██║  ██║██║   ██║██║╚██╗██║██╔══╝   ╚═╝")
    print("   ██████╔╝╚██████╔╝██║ ╚████║███████╗ ██╗")
    print("   ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═╝")
    print()
    print(f"   TREASURE RECOVERED!  SCORE: {score}/{total}")
    print()
    print("   FLAG: CTF{JUNGLE_MASTER_2026}")
    print()
    print("  " + "=" * 22)
    print()


if __name__ == "__main__":
    random.shuffle(QUESTIONS)
    QUESTIONS = QUESTIONS[:10]
    game_loop()