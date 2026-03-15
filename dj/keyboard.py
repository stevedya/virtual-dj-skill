import subprocess


def _run_osascript(lines: list[str]) -> None:
    cmd = ["osascript"]
    for line in lines:
        cmd.extend(["-e", line])
    subprocess.run(cmd, check=True)


def virtualdj_search(
    query: str,
    app_name: str = "VirtualDJ",
    open_search_shortcut: bool = True,
    submit: bool = True,
) -> str:
    """
    Focus VirtualDJ and type into its search box via keyboard automation.

    Requires macOS Accessibility permissions for the terminal app running this script.
    """
    safe_query = (query or "").strip()
    if not safe_query:
        raise ValueError("Search query cannot be empty.")

    # Escape quote/backslash for AppleScript string literals.
    escaped_query = safe_query.replace("\\", "\\\\").replace('"', '\\"')
    escaped_app = app_name.replace("\\", "\\\\").replace('"', '\\"')

    lines = [
        f'tell application "{escaped_app}" to activate',
        "delay 0.15",
        'tell application "System Events"',
    ]

    if open_search_shortcut:
        lines.append('  keystroke "f" using command down')
        lines.append("  delay 0.05")

    lines.append(f'  keystroke "{escaped_query}"')

    if submit:
        lines.append("  key code 36")

    lines.append("end tell")

    try:
        _run_osascript(lines)
    except Exception as exc:
        raise RuntimeError(
            "Failed to send search keystrokes. "
            "Ensure VirtualDJ is installed/running and Accessibility permissions are enabled."
        ) from exc

    return (
        f'Sent search query "{safe_query}" to {app_name} '
        f"(shortcut={'on' if open_search_shortcut else 'off'}, submit={'on' if submit else 'off'})"
    )
