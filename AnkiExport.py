import genanki
import csv
import random

# anki: csv轉anki
# https://www.volcengine.com/theme/9746040-P-7-1
def Convert(csv_file, deck_name):
    # Create a Genanki model
    model_id = random.randint(1000000000, 9999999999)
    model = genanki.Model(
        model_id,
        "基本型",
        fields=[
            {"name": "正面"},
            {"name": "背面"},
        ],
        templates=[
            {
                "name": "卡片 1",
                "qfmt": "{{Question}}",
                "afmt": "{{FrontSide}}<br>{{Answer}}",
            },
        ],
    )
    # print(model_id)

    # Create an Anki deck
    deck_id = random.randint(1000000000, 9999999999)
    deck = genanki.Deck(
        deck_id,
        deck_name
    )
    # print(deck_id)

    # Read the CSV file and add cards to the deck
    with open(csv_file, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question = row["Question"]
            answer = row["Answer"]
            note = genanki.Note(
                model = model,
                fields = [question, answer]
            )
            deck.add_note(note)

    # Save the deck to an Anki deck file (.apkg)
    package = genanki.Package(deck)
    apkg_file = csv_file.split(".")
    apkg_file = apkg_file[0]+".apkg"
    package.write_to_file(apkg_file)
    return apkg_file