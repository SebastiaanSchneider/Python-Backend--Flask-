"""Flask app voor simpele gebruikers database"""
import sqlite3
from pickle import TRUE
from flask import Flask, flash, g, jsonify, render_template, request


app = Flask(__name__, '/static')

# Configuratie van de database-locatie
DATABASE = 'mijn_database.db'

# Maakt de verbinding als variabel bruikbaar
conn = sqlite3.connect('mijn_database.db')

# Maakt een tabel aan
conn.cursor().execute('''
    CREATE TABLE IF NOT EXISTS gebruikers (
        id INTEGER PRIMARY KEY,
        gebruikersnaam TEXT,
        wachtwoord TEXT,
        naam TEXT,
        adres TEXT,
        postcode TEXT,
        geboortedatum TEXT
    )
''')

# Functie om de databaseverbinding op te zetten
def verbind_database():
    return sqlite3.connect(DATABASE)

# Functie om de databaseverbinding op te halen
def krijg_database():
    if 'database' not in g:
        g.database = verbind_database()
    return g.database

# Applicatie teardown om de databaseverbinding te sluiten bij afsluiting
@app.teardown_appcontext
def sluit_database(error):
    if error:
        flash("Something went wrong")
    if hasattr(g, 'database'):
        g.database.close()


# Route voor de index pagina, refereert naar Read
@app.route('/', methods=['GET', 'POST'])
def index():
    return read()

# Route voor Create, pagina om een nieuwe gebruiker aan te maken
@app.route('/create', methods=['GET', 'POST'])
def create():
    db = krijg_database()

    # Verwerking van nieuwe gebruiker
    if request.method == "POST":

        # Opzet nieuwe gebruiker
        gebr2 = request.form.get("gebr")
        wach2 = request.form.get("wach")
        naam2 = request.form.get("naam")
        adre2 = request.form.get("adre")
        post2 = request.form.get("post")
        gebo2 = request.form.get("gebo")

        # Check of gebruikersnaam niet bestaat en voeg nieuwe gebruiker toe
        # met sqlite
        check = db.execute('''SELECT EXISTS(SELECT 1 FROM gebruikers
                           WHERE gebruikersnaam=?)''', (gebr2, )).fetchone()
        if check == (1,):
            # Weergave Create pagina met error
            return render_template("create.html", error=gebr2)
        else:
            db.cursor().execute("""
                                INSERT INTO gebruikers(gebruikersnaam, 
                                wachtwoord, naam, adres, postcode, 
                                geboortedatum) VALUES(?, ?, ?, ?, ?, ?)""",
                                ([gebr2, wach2, naam2, adre2, post2, gebo2]))
            db.commit()
            # Weergave Create pagina met melding
            return render_template("create.html", gebruiker=gebr2)
    # Weergave Create pagina zonder input
    return render_template("create.html")

# Route voor Read, het overzicht van alle gebruiker en bewerkingsopties
@app.route('/"read"', methods=['GET', 'POST'])
def read():
    # Maak verbinding met de database
    db = krijg_database()
    resultaat = db.execute('SELECT * FROM gebruikers').fetchall()

    # Verwerking van nieuwe gebruiker
    if request.method == "POST":

        # Opzet nieuwe gebruiker
        gebr2 = request.form.get("gebr")
        wach2 = request.form.get("wach")
        naam2 = request.form.get("naam")
        adre2 = request.form.get("adre")
        post2 = request.form.get("post")
        gebo2 = request.form.get("gebo")

        # Check of gebruikersnaam niet bestaat en voeg nieuwe gebruiker toe
        # met sqlite
        check = db.execute('''SELECT EXISTS(SELECT 1 FROM gebruikers
                           WHERE gebruikersnaam=?)''', (gebr2, )).fetchone()
        if check == (1,):
            # Weergave Create pagina met error
            return render_template("create.html", error=gebr2)
        else:
            db.cursor().execute("""INSERT INTO gebruikers(gebruikersnaam,
                                wachtwoord, naam, adres, postcode, 
                                geboortedatum) VALUES(?, ?, ?, ?, ?, ?)""",
                                ([gebr2, wach2, naam2, adre2, post2, gebo2]))
            db.commit()
            # Weergave Create pagina
            return render_template("create.html", gebruiker=gebr2)
    # Resultaten weergeven zonder input
    return render_template("read.html", gebruikers=resultaat)

# Route voor Update, pagina om een specifieke gebruiker aan te passen
@app.route('/update/<gebruiker_id>', methods=['GET', 'POST'])
def update(gebruiker_id):
    db = krijg_database()
    gebruiker = db.execute('SELECT * FROM gebruikers WHERE id=?',
                           (gebruiker_id, )).fetchone()

    # Verwerking van geüpdatete gebruiker
    if request.method == "POST":

        # Opzet nieuwe gebruiker
        wach2 = request.form.get("wach")
        naam2 = request.form.get("naam")
        adre2 = request.form.get("adre")
        post2 = request.form.get("post")
        gebo2 = request.form.get("gebo")

        # Update nieuwe gegevens gebruiker in database met sqlite
        db.cursor().execute("""
                            UPDATE gebruikers
                            SET wachtwoord=?, naam=?, adres=?, postcode=?, 
                            geboortedatum=?
                            WHERE id=?
                            """, ([wach2, naam2, adre2, post2, gebo2,
                                   gebruiker_id]))
        db.commit()
        check = TRUE
        # Weergave update pagina met melding
        return render_template("update.html", gebruiker=gebruiker, check=check)
    # Weergave update pagina zonder input
    return render_template("update.html", gebruiker=gebruiker,
                           gebruiker_id=gebruiker_id)

# Route voor Delete, een melding dat een gebruiker succesvol is verwijderd
@app.route('/delete/<gebruiker_id>')
def delete(gebruiker_id):
    db = krijg_database()
    gebruiker = db.execute('SELECT * FROM gebruikers WHERE id=?',
                           (gebruiker_id, )).fetchone()

    # Verwijder de gebruiker met sqlite
    db.cursor().execute('DELETE FROM gebruikers WHERE id=?', (gebruiker_id, ))
    db.commit()

    # Weergave nieuwe pagina met melding
    return render_template("delete.html", gebruiker=gebruiker)

# Functie om de database als json te kunnen gebruiken
@app.route('/api/gebruikers')
def gebruikers():
    db = krijg_database()
    resultaat = db.execute('SELECT * FROM gebruikers').fetchall()
    users_list = [{'id': row[0], 'gebruikersnaam': row[1], 'wachtwoord': row[2],
                   'naam': row[3], 'adres': row[4], 'postcode': row[5],
                   'geboortedatum': row[6]} for row in resultaat]
    return jsonify(users_list)

# SPA versie van Create, om nieuwe gebruikers aan te maken
@app.route('/api/create', methods=['GET', 'POST'])
def api_create():
    db = krijg_database()

    if request.method == "POST":
        # Opzet nieuwe gebruiker
        gebr2 = request.form.get("gebr")
        wach2 = request.form.get("wach")
        naam2 = request.form.get("naam")
        adre2 = request.form.get("adre")
        post2 = request.form.get("post")
        gebo2 = request.form.get("gebo")

        # Check of gebruikersnaam niet bestaat en voeg nieuwe gebruiker toe
        # met sqlite
        check = db.execute('''SELECT EXISTS(SELECT 1 FROM gebruikers
                           WHERE gebruikersnaam=?)''', (gebr2, )).fetchone()
        if check == (1,):
            # Ververs pagina met error
            return render_template("api_read.html", error=gebr2)
        else:
            db.cursor().execute("""
                                INSERT INTO gebruikers(gebruikersnaam, 
                                wachtwoord, naam, adres, postcode, 
                                geboortedatum) VALUES(?, ?, ?, ?, ?, ?)""",
                                ([gebr2, wach2, naam2, adre2, post2, gebo2]))
            db.commit()
            # Ververs de pagina
            return render_template("api_read.html")
    # Ververs de pagina
    return render_template("api_read.html")

# SPA versie van Read, het overzicht van alle gebruikers
@app.route('/api/read', methods=['GET', 'POST'])
def api_read():
    # Maak verbinding met de database
    db = krijg_database()

    # Voer een query uit
    resultaat = db.execute('SELECT * FROM gebruikers').fetchall()

    if request.method == "POST":
        # Opzet nieuwe gebruiker
        gebr2 = request.form.get("gebr")
        wach2 = request.form.get("wach")
        naam2 = request.form.get("naam")
        adre2 = request.form.get("adre")
        post2 = request.form.get("post")
        gebo2 = request.form.get("gebo")

        # Check of gebruikersnaam niet bestaat en voeg nieuwe gebruiker toe
        # met sqlite
        check = db.execute('''SELECT EXISTS(SELECT 1 FROM gebruikers
                           WHERE gebruikersnaam=?)''', (gebr2, )).fetchone()
        if check == (1,):
            # Ververs pagina met error
            return render_template("api_read.html", error=gebr2)
        else:
            db.cursor().execute("""
                                INSERT INTO gebruikers(gebruikersnaam, 
                                wachtwoord, naam, adres, postcode, 
                                geboortedatum) VALUES(?, ?, ?, ?, ?, ?)""",
                                ([gebr2, wach2, naam2, adre2, post2, gebo2]))
            db.commit()
            # Ververs de pagina
            return render_template("api_read.html")
    # Ververs de pagina
    return render_template("api_read.html", gebruikers=resultaat)

# SPA versie van Update, om een specifieke gebruiker aan te passen
@app.route('/api/update', methods=['POST'])
def api_update():
    # Update nieuwe gegevens gebruiker in database met sqlite
    if request.method == "POST":
        data = request.json['data']
        db = krijg_database()
        db.cursor().execute("""
                            UPDATE gebruikers
                            SET naam=?, adres=?, postcode=?, 
                            geboortedatum=?
                            WHERE id=?
                            """, ([data["naam"], data["adres"],
                                   data["postcode"], data["geboortedatum"],
                                   data["id"]]))
        db.commit()
        check = TRUE
    # Ververs de pagina
    return render_template("api_read.html", check=check)

# SPA versie van delete, om gebruikers te verwijderen
@app.route('/api/delete/<gebruiker_id>')
def gebruiker_delete(gebruiker_id):
    # Verwijder de gebruiker met sqlite
    db = krijg_database()
    db.cursor().execute('DELETE FROM gebruikers WHERE id=?',
                        (gebruiker_id, ))
    db.commit()
    flash('Gebruiker ' + gebruiker_id + 'succesvol verwijderd')
    return '{"status" : "ok", "id" : ' + gebruiker_id + '}'


if __name__ == '__main__':
    app.run(debug=True)
