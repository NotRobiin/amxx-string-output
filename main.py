import os
import time
import subprocess
import config as cfg


def get_plugins() -> list:
    out = []
    search = ".amxx"

    for f in os.listdir(cfg.plugins_path):
        if not os.path.isfile(os.path.join(cfg.plugins_path, f)):
            continue

        if f[-len(search) :] != search:
            continue

        out.append(f)

    return out


def uncompress(plugin: str) -> bool:
    start = time.time()
    cmd = f"{cfg.uncompress_path} {cfg.plugins_path}/{plugin} >> trash.txt"
    mem = f"{cfg.plugins_path}/{plugin.replace('.amxx', '.memory')}"
    proc = subprocess.Popen(cmd, stdout=None, shell=False)

    while True:
        if time.time() - start > cfg.uncompress_timeout:
            proc.terminate()
            return False

        if not os.path.isfile(mem) or os.path.getsize(mem) == 0:
            time.sleep(cfg.uncompress_delay)
        else:
            break

    proc.terminate()

    return True


def remove_raw(plugin: str) -> None:
    raw = f"{cfg.plugins_path}/{plugin.replace('.amxx', '.raw')}"

    if os.path.isfile(raw):
        try:
            os.remove(raw)

        except PermissionError:
            time.sleep(cfg.file_remove_delay)
            remove_raw(plugin)


def remove_memory(plugin: str) -> None:
    memory = f"{cfg.plugins_path}/{plugin.replace('.amxx', '.memory')}"

    if os.path.isfile(memory):
        try:
            os.remove(memory)

        except PermissionError:
            time.sleep(cfg.file_remove_delay)
            remove_memory(plugin)


def read_memory(plugin: str, out: dict) -> None:
    memory = f"{cfg.plugins_path}/{plugin.replace('.amxx', '.memory')}"

    if not os.path.isfile(memory):
        print(f'Missing .memory file for plugin "{plugin}"')
        return

    for line in open(memory, "r", encoding="utf8", errors="ignore").readlines():
        line = line[cfg.truncate :]
        out[plugin].append(line)


def write_output(out: dict, failed: list) -> None:
    output_file = cfg.output_path

    # Remove output file if it already exists
    if os.path.isfile(output_file):
        os.remove(output_file)

    # Write output
    with open(output_file, "w+") as f:
        for k in out:
            f.write(f"{k}:\n")

            for v in out[k]:
                f.write(f"\t{v}")

        f.write("\n\nFailed to read:\n")

        for fail in failed:
            f.write(f"\t{fail}")

        f.write("\n\n\n")


def display_stats(
    iteration: int, start, plugin: str, plugins: list, failed: list
) -> None:
    os.system("cls")

    te = time.strftime("%H:%M:%S", time.gmtime(time.time() - start))
    s = time.strftime("%H:%M:%S", time.gmtime(start))

    print(f"Started: {s} Elapsed: {te}")
    print(f'Working on "{plugin}" ({iteration + 1} / {len(plugins)})')
    print(f"Failed: {len(failed)}")

    print("\n\n")


def setup() -> None:
    if not os.path.isfile(cfg.uncompress_path):
        print(f"Missing uncompresser on path {cfg.uncompress_path}")
        exit()

    if len(get_plugins()) == 0:
        print(f"No .amxx files were found on path {cfg.plugins_path}")
        exit()


def main() -> None:
    setup()

    plugins = get_plugins()
    output = {k: [] for k in plugins}
    start = time.time()
    failed = []

    for i, p in enumerate(plugins):
        if not uncompress(p):
            failed.append(p)

        remove_raw(p)
        read_memory(p, output)
        remove_memory(p)
        display_stats(i, start, p, plugins, failed)

    write_output(output, failed)


if __name__ == "__main__":
    main()
