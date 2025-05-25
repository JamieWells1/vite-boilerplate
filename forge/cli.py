import sys
import re
import json
from pathlib import Path

from typing import Dict, cast
from forge import utils, path, types, constants


HEX_REGEX = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"


def help():
    print(
        """
Usage: forge <command>

Available commands:
  start       Start the customisation interface
  build       Syncs forge.config.json with runtime configs
  list        Lists all current configs. If none, prompts to run 'forge start'
  -h, --help  Show this help message
"""
    )


def start(config_manager):
    utils.prln("🔧 Start customisation of your Vite project")
    configs: Dict = config_manager.get()
    config_manager.set(configs)
    utils.prln("\033[1;32m✔ Custom configurations set!\033[0m")
    print("Run 'forge list' to view your configs.\n")


def list_configs():
    config_empty: bool = True
    configs = "{}"

    if path.ENV_PATH.exists():
        try:
            configs = utils.read_configs()
            if configs != "{}":
                config_empty = False
        except json.JSONDecodeError:
            pass

    if config_empty:
        utils.prln("You have not configured Forge yet. Run 'forge start' to do so.\n")
    else:
        utils.prln(json.dumps(configs, indent=2))


# Build what the user has put in package.json on project start
def build():
    config_manager = ConfigFactory()
    if path.ENV_PATH.exists():
        try:
            configs: types.ForgeConfigs = json.loads(utils.read_configs())
        except json.JSONDecodeError:
            return

        config_manager.update_index_css_font(
            path.INDEX_CSS_PATH, configs["fonts"]["font"]
        )
        config_manager.update_tailwind_config_font(
            path.TW_CONFIG_PATH, configs["fonts"]["font"]
        )
        config_manager.update_tailwind_config_colors(
            path.TW_CONFIG_PATH,
            configs["colours"],
        )
        config_manager.write_env(configs["env"])
        utils.prln(
            "✔ Forge configs built. Run 'npm run dev' to view your new configuration.\n"
        )


def main():
    config_manager = ConfigFactory()
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        help()
        return

    command = sys.argv[1]
    if command == "start":
        start(config_manager)
    elif command == "list":
        list_configs()
    elif command == "build":
        build()
    else:
        print(f"{command}: command not found")


class ConfigFactory:

    def get(self):
        args = {}

        use_google_fonts, font = self.configure_font()
        colours: types.Colours = self.configure_colours()
        env: types.Env = self.configure_env()

        args["font"] = font
        args["use_google_fonts"] = use_google_fonts
        args["colours"] = colours
        args["env"] = env

        return args

    def set(self, config):
        config["font"] = self.write_font(config["use_google_fonts"], config["font"])
        self.write_colours(config["colours"])
        self.write_env(config["env"])

        if not path.FORGE_CONFIG_PATH.exists():
            path.FORGE_CONFIG_PATH.touch()

        with open(path.FORGE_CONFIG_PATH, "r+") as f:
            fonts: types.Font = {
                "font": config["font"],
                "use_google_fonts": config["use_google_fonts"],
            }
            colours: types.Colours = config["colours"]
            env: types.Env = config["env"]

            new_configs = json.dumps(
                {"fonts": fonts, "colours": colours, "env": env}, indent=2
            )
            f.seek(0)
            f.write(new_configs)

    # <================ Get Methods ================>

    def configure_font(self, font_choice: str = "") -> tuple[bool, str]:
        if not font_choice:
            font_choice = input("Use Google fonts? (y/N): ")
        font = input("-> Font name: ")

        if utils.cli_string_to_bool(font_choice):
            use_google_fonts: bool = True
        else:
            use_google_fonts: bool = False

        if not font:
            utils.prln("Please enter a font.")
            self.configure_font(font_choice)

        return use_google_fonts, font

    def configure_colours(self) -> types.Colours:
        colours: types.Colours = {}
        primary = "#" + input("Primary colour (hex): #")
        secondary = "#" + input("Secondary colour (hex): #")

        if not re.fullmatch(HEX_REGEX, primary) or not re.fullmatch(
            HEX_REGEX, secondary
        ):
            utils.prln("Please enter valid hexademical colours.")
            self.configure_colours()

        colours["primary"] = cast(
            types.ColourVariations, utils.generate_shades(primary)
        )
        colours["secondary"] = cast(
            types.ColourVariations, utils.generate_shades(secondary)
        )

        return colours

    def configure_env(self) -> types.Env:
        env: types.Env = {}
        api_integrations: types.ApiIntegrations = {}

        # Get/set domain
        domain: str = f"https://{input("Domain: https://").replace("www.", "")}"
        if not domain:
            domain = constants.DEFAULT_DOMAIN

        use_subdomain_api_base = input(
            f"Use https://api.{domain[8:]} as API base URL? (Y/n): "
        )
        if (
            utils.cli_string_to_bool(use_subdomain_api_base)
            or len(use_subdomain_api_base) == 0
        ):
            api_base_url = f"https://api.{domain[8:]}"
        else:
            api_base_url = f"{domain}/api"

        add_api = input("\nAdd API integration? (y/N): ")
        if utils.cli_string_to_bool(add_api):
            api_integrations = utils.prompt_api_keys(api_integrations)

        env["domain"] = domain
        env["api_base_url"] = api_base_url
        env["api_integrations"] = api_integrations

        return env

    # <================ Set Methods in respective files ================>

    def write_font(self, use_google_fonts: bool, font: str) -> str:
        if use_google_fonts:
            tailwind_config_font = " ".join(
                [word.capitalize() for word in font.split()]
            )
            utils.write_config(
                file_path=path.TW_CONFIG_PATH,
                example="<font>",
                new_setting=tailwind_config_font,
            )
            index_css_font = "+".join([word.capitalize() for word in font.split()])
            utils.write_config(
                file_path=path.INDEX_CSS_PATH,
                example="<font>",
                new_setting=index_css_font,
            )
            return tailwind_config_font

        utils.write_config(
            file_path=path.TW_CONFIG_PATH,
            example="<font>",
            new_setting=font,
        )
        utils.write_config(
            file_path=path.INDEX_CSS_PATH,
            example="<font>",
            new_setting=font.replace(" ", "-").lower(),
        )
        return font

    def write_colours(self, colours: types.Colours) -> None:
        js_colours: str = utils.to_tailwind_js(colours)
        with open(path.TW_CONFIG_PATH, "r+") as f:
            file = f.read().replace('"<colors>"', js_colours)
            f.seek(0)
            f.write(file)
            f.truncate()

    def write_env(self, env: types.Env) -> None:
        if not path.ENV_PATH.exists():
            path.ENV_PATH.touch()

        if not path.ENV_EXAMPLE_PATH.exists():
            path.ENV_EXAMPLE_PATH.touch()

        domain = utils.encase(env.get("domain", (constants.DEFAULT_DOMAIN)))
        api_base_url = utils.encase(
            env.get("api_base_url", (constants.DEFAULT_API_BASE_URL))
        )

        with open(path.ENV_PATH, "w") as f:
            lines = ['ENV="DEV"']
            lines.append(f"DOMAIN={domain}")
            lines.append(f"API_BASE_URL={api_base_url}")
            for key, value in env.get("api_integrations", {}).items():
                lines.append(f"{key}={utils.encase(value)}")

            f.write("\n".join(lines))

        with open(path.ENV_EXAMPLE_PATH, "w") as f:
            lines = ['ENV="DEV"']
            lines.append(f"DOMAIN={constants.DEFAULT_DOMAIN}")
            lines.append(f"API_BASE_URL={constants.DEFAULT_API_BASE_URL}")
            for key, value in env.get("api_integrations", {}).items():
                lines.append(f"{key}={utils.encase("your-api-key-here")}")

            f.write("\n".join(lines))

    # <================ Update Methods from forge.config.json to respective files ================>

    def update_index_css_font(self, file_path: Path, font_name: str) -> None:
        with open(file_path, "r+") as f:
            content = f.read()
            pattern = (
                r"(?<=/\* //forge-insert:google-font \*/\n)(@import url\([^)]+\);)"
            )
            new_import = f'@import url("https://fonts.googleapis.com/css2?family={font_name.replace(" ", "+")}:wght@400;600;700&display=swap");'
            updated = re.sub(pattern, new_import, content)
            f.seek(0)
            f.write(updated)
            f.truncate()

    def update_tailwind_config_font(self, file_path: Path, font_name: str) -> None:
        with open(file_path, "r+") as f:
            content = f.read()
            pattern = r"(//forge-insert:fonts\s*\n\s*sans:\s*\[)[^\]]+(?=\])"
            new_value = f'"{font_name}", ...defaultTheme.fontFamily.sans'
            updated = re.sub(pattern, r"\1" + new_value, content)
            f.seek(0)
            f.write(updated)
            f.truncate()

    def update_tailwind_config_colors(
        self, file_path: Path, colours: types.Colours
    ) -> None:
        js_colour_block: str = utils.to_tailwind_js(colours)
        if js_colour_block.startswith('"') and js_colour_block.endswith('"'):
            js_colour_block = js_colour_block[1:-1]

        with open(file_path, "r+") as f:
            content = f.read()
            pattern = (
                r"(//forge-insert:colors\s*\n\s*)colors:\s*\{(?:[^{}]|\{[^{}]*\})*\},?"
            )
            updated = re.sub(pattern, r"\1colors: " + js_colour_block + ",", content)
            f.seek(0)
            f.write(updated)
            f.truncate()
