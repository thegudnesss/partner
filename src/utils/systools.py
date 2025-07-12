import asyncio

class ShellExceptionError(Exception):
    """
    Shell buyrug'i bajarilmasa, shu xatoni chiqaramiz.
    """
    pass


def parse_commits(log: str) -> dict:
    """
    Git log chiqishini dict ko'rinishiga o'tkazadi.
    """
    commits = {}
    last_commit = ""
    for line in log.splitlines():
        if line.startswith("commit"):
            last_commit = line.split()[1]
            commits[last_commit] = {}
        elif line.startswith("    "):
            if "title" in commits[last_commit]:
                commits[last_commit]["message"] = line[4:]
            else:
                commits[last_commit]["title"] = line[4:]
        elif ":" in line:
            key, value = line.split(": ", 1)
            commits[last_commit][key] = value
    return commits


async def shell_run(command: str) -> str:
    """
    Shell buyrug'ini asinxron bajaradi va natijani qaytaradi.
    """
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        return stdout.decode("utf-8").strip()

    msg = (
        f"Command '{command}' exited with {process.returncode}:\n"
        f"{stderr.decode('utf-8').strip()}"
    )
    raise ShellExceptionError(msg)
