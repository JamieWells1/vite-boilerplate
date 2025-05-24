import sys
import re
import json

from typing import Dict, cast
from forge import utils, path, types


HEX_REGEX = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"


def print_help():
    print(
        """
Usage: forge <command>

Available commands:
  customise   Start the customisation interface
  list        Lists all current configs. If none, prompts to run 'forge customise'
  -h, --help  Show this help message
"""
    )


def customise(config):
    utils.prln("🔧 Customise your Vite project")
    args: Dict = config.get()
    config.set(args)


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
        utils.prln("You have not configured Forge yet. Run 'forge customise' to do so.")
    else:
        utils.prln(configs)


# Build what the user has put in package.json on project start
def build(config):
    if path.ENV_PATH.exists():
        try:
            configs = utils.read_configs()
        except json.JSONDecodeError:
            return

        config.write_font(
            configs["fonts"]["use_google_fonts"], configs["fonts"]["font"]
        )


def main():
    config = ConfigFactory()
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print_help()
        return

    command = sys.argv[1]
    if command == "customise":
        customise(config)
    elif command == "list":
        list_configs()
    elif command == "build":
        build(config)
    else:
        print(f"Unknown command: {command}\n")
        print_help()


if __name__ == "__main__":
    main()


class ConfigFactory:
    def __init__(self) -> None:
        self.font: str = ""
        self.primary: str = ""
        self.secondary: str = ""

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

    def set(self, args):
        self.write_font(args["use_google_fonts"], args["font"])
        self.write_colours(args["colours"])
        self.write_env(args["env"])

        with open(path.FORGE_CONFIG_PATH, "r+") as f:
            fonts: types.Font = {
                "font": args["font"],
                "use_google_fonts": args["use_google_fonts"],
            }
            colours: types.Colours = args["colours"]
            env: types.Env = args["env"]

            new_configs = json.dumps({"fonts": fonts, "colours": colours, "env": env})
            f.seek(0)
            f.write(new_configs)

    # <================ Get Methods ================>

    def configure_font(self, font_choice: str = "") -> tuple[bool, str]:
        if not font_choice:
            font_choice = input("\n🖊️  Use Google fonts? (y/N): ")
        font = input("\n-> Font name: ")

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
        primary = "#" + input("\nPrimary colour (hex): #")
        secondary = "#" + input("\nSecondary colour (hex): #")

        if not re.fullmatch(HEX_REGEX, primary) or re.fullmatch(HEX_REGEX, secondary):
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
        domain: str = utils.encase(
            "https://" + input("\nDomain: https://").replace("www.", "")
        )
        if not domain:
            domain = "https://example.com"

        use_subdomain_api_base = input(
            f"\nUse https://api.{domain[8:]} as API base URL? (Y/n): "
        )
        if use_subdomain_api_base:
            api_base_url = utils.encase(f"https://api.{domain[8:]}")
        else:
            api_base_url = utils.encase(f"{domain}/api")

        def prompt_api_keys() -> None:
            while True:
                env_var_name = input("\nEnvironment variable name: ")
                env_var_value = utils.encase(input(f"Value for '{env_var_name}': "))

                api_integrations[env_var_name] = env_var_value
                utils.prln(f"✅ API key '{env_var_name}' added")

                add_another = input("Add another API key? (y/N): ")
                if not utils.cli_string_to_bool(add_another):
                    break

        add_api = input("\nAdd API integration? (y/N): ")
        if utils.cli_string_to_bool(add_api):
            prompt_api_keys()

        env["domain"] = domain
        env["api_base_url"] = api_base_url
        env["api_integrations"] = api_integrations

        return env

    # <================ Set Methods ================>

    def write_font(self, use_google_fonts: bool, font: str) -> None:
        if use_google_fonts:
            utils.write_config(
                file_path=path.TW_CONFIG_PATH,
                example="<font>",
                new_setting=font.replace(" ", "+").capitalize(),
            )
        else:
            utils.write_config(
                file_path=path.TW_CONFIG_PATH,
                example="<font>",
                new_setting=font.replace(" ", "-").lower(),
            )

        utils.write_config(
            file_path=path.INDEX_CSS_PATH, example="<font>", new_setting=font
        )

    def write_colours(self, colours: types.Colours) -> None:
        utils.write_config(
            file_path=path.TW_CONFIG_PATH,
            example="<colors>",
            new_setting=utils.to_tailwind_js(colours),
        )

    def write_env(self, env: types.Env) -> None:
        if not path.ENV_PATH.exists():
            path.ENV_PATH.touch()

        with open(path.ENV_PATH, "w") as f:
            f.seek(0)
            lines = ['ENV="DEV"']
            lines.append(
                f'DOMAIN={env.get("domain", utils.encase("https://example.com"))}'
            )
            lines.append(
                f'API_BASE_URL={env.get("api_base_url", utils.encase("https://api.example.com"))}'
            )
            for key, value in env.get("api_integrations", {}).items():
                lines.append(f"{key}={utils.encase(value)}")

            f.write("\n".join(lines))
