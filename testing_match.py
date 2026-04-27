"""
testing_match.py
----------------
Adds a test match to try the web-app before the official launch.

Match: PSG vs Bayern Munich
Date:  29 April 2026
Time:  00:30 IST

This is a TESTING FILE — delete it when the web-app goes official in May.
Also remove the import line from app.py when deleting this file.
"""

from extensions import db


def seed_testing_match():
    from models import Match

    # Only insert if this test match doesn't already exist
    exists = Match.query.filter_by(match_date="2026-04-29").first()
    if exists:
        return

    test_match = Match(
        home_team      = "PSG",
        away_team      = "Bayern Munich",
        competition    = "TEST MATCH — Pre-launch Trial",
        match_date     = "2026-04-29",
        match_time_ist = "00:30 IST",
        venue          = "Parc des Princes, Paris",
        home_logo_url  = "logos/psg.png",
        away_logo_url  = "logos/bayern.png",
        status         = "upcoming",
        scorer_options = (
            "No Goal, Harry Kane (FCB), Ousmane Dembélé (PSG), Khvicha Kvaratskhelia (PSG), Randal Kolo Muani (PSG), Gonçalo Ramos (PSG), Bradley Barcola (PSG), Luis Díaz (FCB), Serge Gnabry (FCB), Michael Olise (FCB), Nicolas Jackson (FCB), Désiré Doué (PSG), Armindo Sieb (FCB), Ibrahim Mbaye (PSG), Quentin Ndjantou (PSG), Wassim Slama (PSG), Jonah Kusi-Asare (FCB), Wisdom Mike (FCB), Jamal Musiala (FCB), Vitinha (PSG), Fabián Ruiz (PSG), Lee Kang-in (PSG), João Neves (PSG), Warren Zaïre-Emery (PSG), Renato Sanches (PSG), Gabriel Moscardo (PSG), Senny Mayulu (PSG), Pedro Fernandez (PSG), Yanis Khafi (PSG), Noah Nsoki (PSG), Mathis Jangeal (PSG), Joshua Kimmich (FCB), Leon Goretzka (FCB), João Palhinha (FCB), Konrad Laimer (FCB), Aleksandar Pavlović (FCB), Bryan Zaragoza (FCB), Lovro Zvonarek (FCB), Tom Bischof (FCB), Arijon Ibrahimović (FCB), Jonathan Asp Jensen (FCB), Maurice Krattenmacher (FCB), Javier Fernandez (FCB), David Daiber (FCB), Guido Della Rovere (FCB), Felipe Chavez (FCB), Lennart Karl (FCB), Maycon Cardozo (FCB), Bara Sapoko Ndiaye (FCB), Achraf Hakimi (PSG), Nuno Mendes (PSG), Marquinhos (PSG), Lucas Hernández (PSG), Willian Pacho (PSG), Beraldo (PSG), Illia Zabarnyi (PSG), Yoram Zague (PSG), Naoufel El Hannach (PSG), Noham Kamara (PSG), David Boly (PSG), Jonathan Tah (FCB), Alphonso Davies (FCB), Raphaël Guerreiro (FCB), Dayot Upamecano (FCB), Kim Min-jae (FCB), Hiroki Ito (FCB), Sacha Boey (FCB), Josip Stanišić (FCB), Tarek Buchmann (FCB), Vincent Manuba (FCB), Deniz Emre Ofli (FCB), Cassiano Kiala (FCB), Filip Pavic (FCB), Manuel Neuer (FCB), Gianluigi Donnarumma (PSG), Matvey Safonov (PSG), Lucas Chevalier (PSG), Renato Marin (PSG), Martin James (PSG), Arthur Vignaud (PSG), Sven Ulreich (FCB), Alexander Nübel (FCB), Daniel Peretz (FCB), Jonas Urbig (FCB), Max Schmitt (FCB), Leon Klanac (FCB), Jannis Bartl (FCB), Leonard Prescott (FCB)"
        ),
    )

    db.session.add(test_match)
    db.session.commit()
    print("[Seed] ✅  Test match (PSG vs Bayern) inserted.")
