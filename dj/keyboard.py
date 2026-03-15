import subprocess


def _run_osascript(lines: list[str]) -> None:
    cmd = ["osascript"]
    for line in lines:
        cmd.extend(["-e", line])
    subprocess.run(cmd, check=True)


def _escaped(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


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

    escaped_query = _escaped(safe_query)
    escaped_app = _escaped(app_name)

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


def virtualdj_select_result(
    result_index: int,
    app_name: str = "VirtualDJ",
    reset_to_top: bool = True,
) -> str:
    """
    Select a result row in the current VirtualDJ browser list.

    Result index is 1-based.
    """
    safe_index = int(result_index)
    if safe_index < 1:
        raise ValueError("Result index must be >= 1.")

    escaped_app = _escaped(app_name)
    lines = [
        f'tell application "{escaped_app}" to activate',
        "delay 0.10",
        'tell application "System Events"',
    ]

    if reset_to_top:
        lines.append("  key code 115")  # Home
        lines.append("  delay 0.03")

    for _ in range(safe_index - 1):
        lines.append("  key code 125")  # Down arrow
        lines.append("  delay 0.02")

    lines.append("end tell")

    try:
        _run_osascript(lines)
    except Exception as exc:
        raise RuntimeError(
            "Failed to move VirtualDJ browser selection. "
            "Ensure Accessibility permissions are enabled."
        ) from exc

    return f"Selected result index {safe_index} in {app_name}"
