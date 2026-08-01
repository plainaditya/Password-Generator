from __future__ import annotations

import math
import random
import secrets
import string
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


DEFAULT_LENGTH = 16
MIN_LENGTH = 4
MAX_LENGTH = 128
EXPORT_FILE = Path("generated_passwords.txt")


@dataclass(frozen=True)
class PasswordOptions:
    length: int = DEFAULT_LENGTH
    use_lowercase: bool = True
    use_uppercase: bool = True
    use_digits: bool = True
    use_symbols: bool = True
    avoid_ambiguous: bool = False
    exclude_similar: bool = False
    no_repeating_chars: bool = False
    no_consecutive_duplicates: bool = False
    count: int = 1


AMBIGUOUS_CHARS = set("O0Il1|`'\"{}[]()<>/\\")
SIMILAR_CHARS = set("oO0iIlL1")


def banner() -> None:
    print("\n" + "=" * 62)
    print("🔐  PROFESSIONAL PASSWORD GENERATOR")
    print("=" * 62)
    print("Fast, secure, configurable password creation in the terminal.")
    print("Multiple presets, strong-copy output, and export support.")
    print("=" * 62)


def normalize_yes_no(value: str) -> bool:
    return value.strip().lower() in {"y", "yes", "true", "1"}


def prompt_int(prompt: str, minimum: int, maximum: int, default: int | None = None) -> int:
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        try:
            value = int(raw)
        except ValueError:
            print("❌ Please enter a valid number.")
            continue
        if value < minimum or value > maximum:
            print(f"⚠️ Enter a value between {minimum} and {maximum}.")
            continue
        return value


def prompt_bool(prompt: str, default: bool = False) -> bool:
    suffix = " [Y/n]: " if default else " [y/N]: "
    raw = input(prompt + suffix).strip()
    if raw == "":
        return default
    return normalize_yes_no(raw)


def select_preset() -> PasswordOptions:
    presets = {
        "1": ("Quick", PasswordOptions(length=12, use_lowercase=True, use_uppercase=True, use_digits=True, use_symbols=False)),
        "2": ("Strong", PasswordOptions(length=16, use_lowercase=True, use_uppercase=True, use_digits=True, use_symbols=True)),
        "3": ("Ultra", PasswordOptions(length=24, use_lowercase=True, use_uppercase=True, use_digits=True, use_symbols=True, avoid_ambiguous=True, no_consecutive_duplicates=True)),
        "4": ("Custom", None),
    }

    print("Choose a preset:")
    for key, (name, cfg) in presets.items():
        if cfg is None:
            print(f"  {key}) {name:<6} | build every option manually")
        else:
            extras = []
            if cfg.avoid_ambiguous:
                extras.append("avoid ambiguous")
            if cfg.no_consecutive_duplicates:
                extras.append("no double chars")
            extra_text = f" | {', '.join(extras)}" if extras else ""
            print(f"  {key}) {name:<6} | length {cfg.length}{extra_text}")

    while True:
        choice = input("Select 1, 2, 3, or 4: ").strip()
        if choice in presets:
            name, cfg = presets[choice]
            print(f"\nPreset selected: {name}\n")
            if cfg is not None:
                return cfg
            break
        print("❌ Invalid choice.")

    length = prompt_int(f"Length ({MIN_LENGTH}-{MAX_LENGTH}) [default {DEFAULT_LENGTH}]: ", MIN_LENGTH, MAX_LENGTH, DEFAULT_LENGTH)
    count = prompt_int("How many passwords to generate? (1-20) [default 1]: ", 1, 20, 1)
    use_lowercase = prompt_bool("Include lowercase letters?", True)
    use_uppercase = prompt_bool("Include uppercase letters?", True)
    use_digits = prompt_bool("Include digits?", True)
    use_symbols = prompt_bool("Include symbols?", True)
    avoid_ambiguous = prompt_bool("Avoid ambiguous characters (O, 0, l, 1, etc.)?", False)
    exclude_similar = prompt_bool("Exclude visually similar characters?", False)
    no_repeating_chars = prompt_bool("Do not repeat the same character?", False)
    no_consecutive_duplicates = prompt_bool("Avoid consecutive duplicate characters?", False)

    return PasswordOptions(
        length=length,
        use_lowercase=use_lowercase,
        use_uppercase=use_uppercase,
        use_digits=use_digits,
        use_symbols=use_symbols,
        avoid_ambiguous=avoid_ambiguous,
        exclude_similar=exclude_similar,
        no_repeating_chars=no_repeating_chars,
        no_consecutive_duplicates=no_consecutive_duplicates,
        count=count,
    )


def build_pool(options: PasswordOptions) -> str:
    pool = ""
    if options.use_lowercase:
        pool += string.ascii_lowercase
    if options.use_uppercase:
        pool += string.ascii_uppercase
    if options.use_digits:
        pool += string.digits
    if options.use_symbols:
        pool += string.punctuation

    if options.avoid_ambiguous:
        pool = "".join(ch for ch in pool if ch not in AMBIGUOUS_CHARS)
    if options.exclude_similar:
        pool = "".join(ch for ch in pool if ch not in SIMILAR_CHARS)

    return "".join(dict.fromkeys(pool))


def ensure_required_categories(options: PasswordOptions, pool: str) -> list[str]:
    required = []
    if options.use_lowercase:
        required.append(_pick_from_group(string.ascii_lowercase, options))
    if options.use_uppercase:
        required.append(_pick_from_group(string.ascii_uppercase, options))
    if options.use_digits:
        required.append(_pick_from_group(string.digits, options))
    if options.use_symbols:
        required.append(_pick_from_group(string.punctuation, options))

    required = [ch for ch in required if ch in pool]
    return required


def _pick_from_group(group: str, options: PasswordOptions) -> str:
    filtered = [ch for ch in group if _char_allowed(ch, options)]
    if not filtered:
        return ""
    return secrets.choice(filtered)


def _char_allowed(ch: str, options: PasswordOptions) -> bool:
    if options.avoid_ambiguous and ch in AMBIGUOUS_CHARS:
        return False
    if options.exclude_similar and ch in SIMILAR_CHARS:
        return False
    return True


def generate_password(options: PasswordOptions, pool: str) -> str:
    if not pool:
        raise ValueError("No characters available after applying filters.")

    if options.no_repeating_chars and options.length > len(pool):
        raise ValueError("Password length exceeds the available unique character pool.")

    required = ensure_required_categories(options, pool)
    if len(required) > options.length:
        raise ValueError("Password length is too short for the chosen character categories.")

    remaining = options.length - len(required)
    password_chars = required[:]

    used = set(password_chars) if options.no_repeating_chars else None
    last_char = password_chars[-1] if password_chars else None

    for _ in range(remaining):
        candidates = list(pool)
        if options.no_repeating_chars and used is not None:
            candidates = [ch for ch in candidates if ch not in used]
        if options.no_consecutive_duplicates and last_char is not None:
            candidates = [ch for ch in candidates if ch != last_char]
        if not candidates:
            raise ValueError("Could not satisfy the selected constraints.")

        ch = secrets.choice(candidates)
        password_chars.append(ch)
        if options.no_repeating_chars and used is not None:
            used.add(ch)
        last_char = ch

    random.SystemRandom().shuffle(password_chars)

    if options.no_consecutive_duplicates:
        password_chars = _fix_consecutive_duplicates(password_chars, pool, options)

    return "".join(password_chars)


def _fix_consecutive_duplicates(chars: list[str], pool: str, options: PasswordOptions) -> list[str]:
    if len(chars) < 2:
        return chars

    for i in range(1, len(chars)):
        if chars[i] == chars[i - 1]:
            candidates = [ch for ch in pool if ch != chars[i - 1] and _char_allowed(ch, options)]
            if not candidates:
                raise ValueError("Could not remove consecutive duplicates with the selected pool.")
            chars[i] = secrets.choice(candidates)
    return chars


def estimate_strength(password: str, options: PasswordOptions, pool: str) -> tuple[str, int, int]:
    categories = 0
    if any(c.islower() for c in password):
        categories += 1
    if any(c.isupper() for c in password):
        categories += 1
    if any(c.isdigit() for c in password):
        categories += 1
    if any(c in string.punctuation for c in password):
        categories += 1

    pool_size = max(len(pool), 1)
    entropy = int(round(len(password) * math.log2(pool_size)))

    score = 0
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1
    if categories >= 3:
        score += 1
    if categories == 4:
        score += 1
    if any(ch in string.punctuation for ch in password):
        score += 1
    if options.avoid_ambiguous or options.exclude_similar:
        score += 1

    if entropy < 50 or score <= 2:
        label = "Weak"
    elif entropy < 80 or score <= 4:
        label = "Medium"
    else:
        label = "Strong"

    return label, score, entropy


def format_output(passwords: Iterable[str], options: PasswordOptions, pool: str) -> None:
    passwords = list(passwords)
    print("\n" + "=" * 62)
    print("Generated Password(s)")
    print("=" * 62)

    for index, password in enumerate(passwords, start=1):
        strength, score, entropy = estimate_strength(password, options, pool)
        print(f"{index:>2}. {password}")
        print(f"    Strength: {strength} | Score: {score}/6 | Entropy: ~{entropy} bits")

    print("=" * 62)


def export_passwords(passwords: Iterable[str], options: PasswordOptions) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [f"[{timestamp}] length={options.length}, count={options.count}\n"]
    lines.extend(f"{pwd}\n" for pwd in passwords)
    lines.append("\n")
    with EXPORT_FILE.open("a", encoding="utf-8") as file:
        file.writelines(lines)


def main() -> None:
    banner()

    while True:
        try:
            options = select_preset()
            pool = build_pool(options)
            if not pool:
                print("❌ You must select at least one character category.")
                continue

            passwords = []
            for _ in range(options.count):
                passwords.append(generate_password(options, pool))

            format_output(passwords, options, pool)
            export_passwords(passwords, options)
            print(f"Saved to: {EXPORT_FILE.resolve()}")

        except ValueError as error:
            print(f"❌ {error}")
            continue

        again = input("Generate more? (y/n): ").strip().lower()
        if again not in {"y", "yes"}:
            print("Goodbye 👋")
            break


if __name__ == "__main__":
    main()
