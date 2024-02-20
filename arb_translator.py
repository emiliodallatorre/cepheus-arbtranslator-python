import re

from tqdm import tqdm
from translators import translate_text

line_regex: str = r'\s*\"(.*)\": \"(.*)\"'


def separate(
    source_language_code: str,
    source_country_code: str,
) -> dict:
    strings: dict = {}

    with open(f"intl_{source_language_code}_{source_country_code}.arb", "r") as f:
        lines = f.readlines()

        for line in lines:
            match = re.match(line_regex, line)
            if match:
                strings[match.group(1)] = match.group(2)

    with open("values.txt", "w") as f:
        for value in strings.values():
            f.write(f"{value}\n")

    return strings


def join(
        destination_language_code: str,
        destination_country_code: str,
        strings: dict,
) -> None:
    translated: list[str] = open("values_translated.txt", "r").readlines()
    with open(f"intl_{destination_language_code}_{destination_country_code}.arb", "w") as f:
        f.write("{\n")

        for index, (key, value) in enumerate(strings.items()):
            f.write(f'  "{key}": "{translated[index].strip()}",\n')

        f.write("}\n")


def translate_values(
        source_language_code: str,
        destination_language_code: str,
) -> None:
    try:
        # translate_text(query_text: str, translator: str = 'bing', from_language: str = 'auto', to_language: str = 'en', **kwargs) -> Union[str, dict]

        with open("values.txt", "r") as f:
            lines = f.readlines()
            with open("values_translated.txt", "w") as f:
                for line in tqdm(lines):
                    f.write(
                        translate_text(
                            lines,
                            from_language=source_language_code,
                            to_language=destination_language_code,
                            translator="google"
                        ) + "\n")
    except Exception as e:
        print("Error in automatic translation...")
        print(e)
        input("Manually translate the values in values.txt and press enter to continue")


def translate(
    source_language_code: str,
    source_country_code: str,
    destination_language_code: str,
    destination_country_code: str
) -> None:
    strings = separate(source_language_code, source_country_code)
    translate_values(source_language_code, destination_language_code)
    join(destination_language_code, destination_country_code, strings)


translate("en", "GB", "zh", "CN")
