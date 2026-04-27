"""
seed_data.py
------------
Inserts the 4 competition matches into the database on first run.
Skipped automatically if matches already exist.

LOGOS — download team badges and save them here:
  static/images/logos/arsenal.png
  static/images/logos/atletico.png
  static/images/logos/bayern.png
  static/images/logos/psg.png
  static/images/logos/barcelona.png
  static/images/logos/realmadrid.png
  static/images/logos/ucl.png
"""

from extensions import db


def seed_matches():
    from models import Match

    if Match.query.count() > 0:
        return  # already seeded, skip

    matches = [
        # ── Match 1 ──────────────────────────────────────────────
        Match(
            home_team      = "Arsenal",
            away_team      = "Atletico Madrid",
            competition    = "UEFA Champions League – Semi Final 2nd Leg",
            match_date     = "2026-05-06",
            match_time_ist = "00:30 IST",
            venue          = "Emirates Stadium, London",
            home_logo_url  = "logos/arsenal.png",
            away_logo_url  = "logos/atletico.png",
            status         = "upcoming",
            scorer_options = (
                "No Goal, Bukayo Saka (ARS), Antoine Griezmann (ATM), Julián Álvarez (ATM), Gabriel Jesus (ARS), Gabriel Martinelli (ARS), Alexander Sørloth (ATM), Kai Havertz (ARS), Ademola Lookman (ATM), Viktor Gyökeres (ARS), Nicolas Gonzalez (ATM), Eberechi Eze (ARS), Noni Madueke (ARS), Reiss Nelson (ARS), Giuliano Simeone (ATM), Carlos Martin (ATM), Diego Bri (ATM), Ethan Nwaneri (ARS), Charles Sagoe Jr (ARS), Brando Bailey-Joseph (ARS), Iker Luque Sierra (ATM), Sergio Esteban (ATM), Martin Ødegaard (ARS), Marcos Llorente (ATM), Alex Baena (ATM), Thiago Almada (ATM), Declan Rice (ARS), Mikel Merino (ARS), Leandro Trossard (ARS), Christian Norgaard (ARS), Fabio Vieira (ARS), Johnny Cardoso (ATM), Pablo Barrios (ATM), Obed Vargas (ATM), Javi Serrano (ATM), Aitor Gismera (ATM), Rodrigo Mendoza (ATM), Julio Diaz (ATM), Alejandro Monserrate (ATM), Javier Morcillo (ATM), Taufik Zanzi (ATM), Myles Lewis-Skelly (ARS), Max Dowman (ARS), Andre Harriman-Annous (ARS), Ife Ibrahim (ARS), Koke (ATM), Thomas Lemar (ATM), Ben White (ARS), William Saliba (ARS), Gabriel Magalhães (ARS), Riccardo Calafiori (ARS), Jurriën Timber (ARS), Jakub Kiwior (ARS), Piero Hincapié (ARS), Cristhian Mosquera (ARS), Joshua Nichols (ARS), Jaden Dixon (ARS), Marli Salmon (ARS), José María Giménez (ATM), Robin Le Normand (ATM), Clément Lenglet (ATM), Dávid Hancko (ATM), Nahuel Molina (ATM), Matteo Ruggeri (ATM), Ilias Kostis (ATM), Pablo Perez (ATM), Javier Bonar (ATM), Rayane Belaid (ATM), Daniel Martinez (ATM), Aleksa Puric (ATM), Geronimo Spina (ATM), Marc Pubill (ATM), David Raya (ARS), Jan Oblak (ATM), Kepa Arrizabalaga (ARS), Juan Musso (ATM), Karl Hein (ARS), Tommy Setford (ARS), Alexei Rojas (ARS), Jack Porter (ARS), Khari Ranson (ARS), Horatiu Moldovan (ATM), Mario De Luis (ATM), Salvador Esquivel Gamez (ATM), Alvaro Moreno (ATM)"
            ),
        ),
        # ── Match 2 ──────────────────────────────────────────────
        Match(
            home_team      = "Bayern Munich",
            away_team      = "PSG",
            competition    = "UEFA Champions League – Semi Final 2nd Leg",
            match_date     = "2026-05-07",
            match_time_ist = "00:30 IST",
            venue          = "Allianz Arena, Munich",
            home_logo_url  = "logos/bayern.png",
            away_logo_url  = "logos/psg.png",
            status         = "upcoming",
            scorer_options = (
                "No Goal, Harry Kane (FCB), Ousmane Dembélé (PSG), Khvicha Kvaratskhelia (PSG), Randal Kolo Muani (PSG), Gonçalo Ramos (PSG), Bradley Barcola (PSG), Luis Díaz (FCB), Serge Gnabry (FCB), Michael Olise (FCB), Nicolas Jackson (FCB), Désiré Doué (PSG), Armindo Sieb (FCB), Ibrahim Mbaye (PSG), Quentin Ndjantou (PSG), Wassim Slama (PSG), Jonah Kusi-Asare (FCB), Wisdom Mike (FCB), Jamal Musiala (FCB), Vitinha (PSG), Fabián Ruiz (PSG), Lee Kang-in (PSG), João Neves (PSG), Warren Zaïre-Emery (PSG), Renato Sanches (PSG), Gabriel Moscardo (PSG), Senny Mayulu (PSG), Pedro Fernandez (PSG), Yanis Khafi (PSG), Noah Nsoki (PSG), Mathis Jangeal (PSG), Joshua Kimmich (FCB), Leon Goretzka (FCB), João Palhinha (FCB), Konrad Laimer (FCB), Aleksandar Pavlović (FCB), Bryan Zaragoza (FCB), Lovro Zvonarek (FCB), Tom Bischof (FCB), Arijon Ibrahimović (FCB), Jonathan Asp Jensen (FCB), Maurice Krattenmacher (FCB), Javier Fernandez (FCB), David Daiber (FCB), Guido Della Rovere (FCB), Felipe Chavez (FCB), Lennart Karl (FCB), Maycon Cardozo (FCB), Bara Sapoko Ndiaye (FCB), Achraf Hakimi (PSG), Nuno Mendes (PSG), Marquinhos (PSG), Lucas Hernández (PSG), Willian Pacho (PSG), Beraldo (PSG), Illia Zabarnyi (PSG), Yoram Zague (PSG), Naoufel El Hannach (PSG), Noham Kamara (PSG), David Boly (PSG), Jonathan Tah (FCB), Alphonso Davies (FCB), Raphaël Guerreiro (FCB), Dayot Upamecano (FCB), Kim Min-jae (FCB), Hiroki Ito (FCB), Sacha Boey (FCB), Josip Stanišić (FCB), Tarek Buchmann (FCB), Vincent Manuba (FCB), Deniz Emre Ofli (FCB), Cassiano Kiala (FCB), Filip Pavic (FCB), Manuel Neuer (FCB), Gianluigi Donnarumma (PSG), Matvey Safonov (PSG), Lucas Chevalier (PSG), Renato Marin (PSG), Martin James (PSG), Arthur Vignaud (PSG), Sven Ulreich (FCB), Alexander Nübel (FCB), Daniel Peretz (FCB), Jonas Urbig (FCB), Max Schmitt (FCB), Leon Klanac (FCB), Jannis Bartl (FCB), Leonard Prescott (FCB)"
            ),
        ),
        # ── Match 3 ──────────────────────────────────────────────
        Match(
            home_team      = "FC Barcelona",
            away_team      = "Real Madrid",
            competition    = "La Liga – El Clasico",
            match_date     = "2026-05-11",
            match_time_ist = "00:30 IST",
            venue          = "Estadi Olimpic Lluis Companys, Barcelona",
            home_logo_url  = "logos/barcelona.png",
            away_logo_url  = "logos/realmadrid.png",
            status         = "upcoming",
            scorer_options = (
                "Lamine Yamal, Raphinha, Robert Lewandowski, Pedri, Dani Olmo, "
                "Vinicius Jr, Jude Bellingham, Rodrygo, Kylian Mbappe, Federico Valverde"
            ),
        ),
        # ── Match 4 ──────────────────────────────────────────────
        Match(
            home_team      = "UCL Final – Team A",
            away_team      = "UCL Final – Team B",
            competition    = "UEFA Champions League – Final",
            match_date     = "2026-05-30",
            match_time_ist = "21:30 IST",
            venue          = "Puskas Arena, Budapest, Hungary",
            home_logo_url  = "logos/ucl.png",
            away_logo_url  = "logos/ucl.png",
            status         = "upcoming",
            scorer_options = (
                "Bukayo Saka, Kai Havertz, Martin Odegaard, Antoine Griezmann, "
                "Alvaro Morata, Harry Kane, Jamal Musiala, Kylian Mbappe, "
                "Ousmane Dembele, Leroy Sane, Rodrigo De Paul, Vitinha"
            ),
        ),
    ]

    db.session.add_all(matches)
    db.session.commit()
    print("[Seed] ✅  4 matches inserted.")
