from config import SHUTDOWN_COMMANDS


def get_help(command_groups):
    lines = ["Available commands:", ""]

    for group_name, group in command_groups.items():
        aliases = ", ".join(group["aliases"])

        lines.append(f"{group_name}:")
        lines.append(f"  {aliases}")
        lines.append("")

    lines.append("System:")
    lines.append(
        f"  help, status, version, about, history, mode, "
        f"{', '.join(SHUTDOWN_COMMANDS)}"
    )

    return "\n".join(lines)