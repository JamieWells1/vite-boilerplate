import sys
import re
import json

from forge import utils
from forge import path


HEX_REGEX = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"


def configure():
    utils.prln("🔧 Configure your Vite project")
    config = ConfigFactory()
    args: dict = config.get()
    config.set(args)


def main():
    if len(sys.argv) < 2:
        print("Usage: forge <command>")
        return

    command = sys.argv[1]
    if command == "configure":
        configure()
    else:
        print(f"Unknown command: {command}")


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
        colours: dict = self.configure_colours()

        args["font"] = font
        args["use_google_fonts"] = use_google_fonts
        args["colours"] = colours

        return args

    def set(self, args):
        self.write_font(args["use_google_fonts"], args["font"])
        self.write_colours(args["colours"])

    # <================ Get Methods ================>

    def configure_font(self, font_choice: str = "") -> tuple[bool, str]:
        if not font_choice:
            font_choice = input("\n🖊️  Use Google fonts? (y/N): ")
        font = input("\n-> Font name: ")

        if font_choice == "y" or font_choice == "Y":
            use_google_fonts: bool = True
        else:
            use_google_fonts: bool = False

        if not font:
            utils.prln("Please enter a font.")
            self.configure_font(font_choice)

        return use_google_fonts, font

    def configure_colours(self) -> dict:
        colours = {}
        primary = "#" + input("\nPrimary colour (hex): #")
        secondary = "#" + input("\nSecondary colour (hex): #")

        if not re.fullmatch(HEX_REGEX, primary) or re.fullmatch(HEX_REGEX, secondary):
            utils.prln("Please enter valid hexademical colours.")
            self.configure_colours()

        colours["primary"] = self.generate_shades(primary)
        colours["secondary"] = self.generate_shades(secondary)

        return colours

    def generate_shades(self, hex_color, delta=0.15):
        h, l, s = utils.hex_to_hsl(hex_color)
        return {
            "DEFAULT": hex_color,
            "light": utils.hsl_to_hex(h, min(l + delta, 1), s),
            "dark": utils.hsl_to_hex(h, max(l - delta, 0), s),
        }

    # <================ Set Methods ================>

    def write_font(self, use_google_fonts: bool, font: str):
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

    def write_colours(self, colours: dict):
        utils.write_config(
            file_path=path.TW_CONFIG_PATH,
            example="<colors>",
            new_setting=utils.to_tailwind_js(colours),
        )
