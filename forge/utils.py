from pathlib import Path
import colorsys
import json

from forge import path, types


def write_config(file_path: Path, example: str, new_setting: str):
    with open(file_path, "r+") as f:
        file = f.read().replace(example, new_setting)
        f.seek(0)
        f.write(file)
        f.truncate()


def prln(input: str):  # print with new line
    print(f"\n{input}")


def hex_to_hsl(hex_color):
    hex_color = hex_color.lstrip("#")
    r, g, b = [int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    return colorsys.rgb_to_hls(r, g, b)  # returns (H, L, S)


def hsl_to_hex(h, l, s):
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))


def generate_shades(hex_color, delta=0.15):
    h, l, s = hex_to_hsl(hex_color)
    return {
        "DEFAULT": hex_color,
        "light": hsl_to_hex(h, min(l + delta, 1), s),
        "dark": hsl_to_hex(h, max(l - delta, 0), s),
    }


def to_tailwind_js(py_obj, indent=2):
    def serialize(d, level=0):
        pad = " " * (level * indent)
        lines = ["{"]
        for i, (k, v) in enumerate(d.items()):
            key = k  # unquoted
            if isinstance(v, dict):
                val = serialize(v, level + 1)
            else:
                val = f'"{v}"'
            lines.append(f'{pad}{" " * indent}{key}: {val},')
        lines.append(f"{pad}}}")
        return "\n".join(lines)

    return serialize(py_obj)


def cli_string_to_bool(string: str) -> bool:
    if string == "y" or string == "Y":
        return True
    return False


# add double quotes around a value that's being injected into .env
def encase(string: str) -> str:
    return '"' + string + '"'


def read_configs() -> str:
    with open(path.FORGE_CONFIG_PATH, "r") as f:
        return json.loads(f.read())


def prompt_api_keys(api_integrations) -> types.ApiIntegrations:
    while True:
        env_var_name = input("\nEnvironment variable name: ")
        env_var_value = encase(input(f"Value for '{env_var_name}': "))

        api_integrations[env_var_name] = env_var_value
        prln(f"✅ API key '{env_var_name}' added")

        add_another = input("Add another API key? (y/N): ")
        if not cli_string_to_bool(add_another):
            return api_integrations
