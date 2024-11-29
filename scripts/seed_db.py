import os
import sys
import pandas as pd
from db_conn import get_session, get_engine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import Base, Ville, Equipement, Annonce, AnnonceEquipement


def create_tables():
    """Create the tables in the database."""
    engine = get_engine()
    Base.metadata.create_all(engine)


def seed_db(csv_file):
    """Seed the database using data from a CSV file."""
    session = get_session()

    create_tables()  # Ensure tables are created before seeding

    # Load the CSV data
    data = pd.read_csv(csv_file)

    # Define equipment columns (Boolean columns indicating equipment availability)
    equipement_columns = [
        'Ascenseur', 'Balcon', 'Chauffage', 'Climatisation', 'Concierge',
        'Cuisine equipee', 'Duplex', 'Meuble', 'Parking', 'Securite', 'Terrasse'
    ]

    # Insert Ville data
    for _, row in data.iterrows():
        ville = session.query(Ville).filter_by(nom=row['city']).first()
        if not ville:
            ville = Ville(nom=row['city'])
            session.add(ville)

    session.commit()  # Commit Ville data

    # Insert Annonce data
    for _, row in data.iterrows():
        ville = session.query(Ville).filter_by(nom=row['city']).first()
        if ville:
            annonce = session.query(Annonce).filter_by(
                prix=row['price'],
                surface=row['surface_area'],
                nb_pieces=row['nb_rooms'],
                nb_salles_bain=row['nb_baths'],
                ville_id=ville.id,
                titre=row['title']  # Include title in the uniqueness check
            ).first()

            if not annonce:
                annonce = Annonce(
                    titre=row['title'],  # Add the title field
                    prix=row['price'],
                    surface=row['surface_area'],
                    date_publication=row['Date'],
                    nb_pieces=row['nb_rooms'],
                    nb_salles_bain=row['nb_baths'],
                    ville_id=ville.id
                )
                session.add(annonce)

    session.commit()  # Commit Annonce data

    # Insert Equipement and AnnonceEquipement relationships
    for _, row in data.iterrows():
        annonce = session.query(Annonce).filter_by(
            prix=row['price'],
            surface=row['surface_area'],
            nb_pieces=row['nb_rooms'],
            nb_salles_bain=row['nb_baths'],
            titre=row['title']  # Include title in the lookup
        ).first()

        if annonce:
            for equipement_name in equipement_columns:
                if row[equipement_name]:  # Check if the equipment is available (True)
                    # Check if Equipement exists
                    equipement = session.query(Equipement).filter_by(nom=equipement_name).first()
                    if not equipement:
                        equipement = Equipement(nom=equipement_name)
                        session.add(equipement)
                        session.commit()  # Commit to get the Equipement ID

                    # Check if the relationship exists
                    existing_relation = session.query(AnnonceEquipement).filter_by(
                        annonce_id=annonce.id,
                        equipement_id=equipement.id
                    ).first()

                    if not existing_relation:  # Only add if it doesn't exist
                        annonce_equipement = AnnonceEquipement(
                            annonce_id=annonce.id,
                            equipement_id=equipement.id
                        )
                        session.add(annonce_equipement)

    print('data inserted successfuly')

    session.commit()  # Commit relationships after ensuring no duplicates

    session.close()  # Close the session


# Running the seeding function
if __name__ == "__main__":
    seed_db('scripts/data_final.csv')  # Ensure the correct file path if running from 'scripts' folder
