from app import app
from extensions import db
from models import Word

with app.app_context():

    with open("words.txt", "r") as file:

        for line in file:

            word = line.strip().upper()

            if len(word) != 5:
                print(f"Skipping {word}")
                continue

            existing = Word.query.filter_by(word=word).first()

            if existing:
                print(f"{word} already exists.")
                continue

            new_word = Word(word=word)

            db.session.add(new_word)

        db.session.commit()

print("Words inserted successfully!")
