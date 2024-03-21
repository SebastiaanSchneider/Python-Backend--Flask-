from pickle import TRUE
from flask import Flask, g, jsonify, render_template, request
import sqlite3


app = Flask(__name__, '/static')

# Configuratie van de database-locatie
DATABASE = 'mijn_database.db'

# Een tabel maken
conn = sqlite3.connect('mijn_database.db')

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
    if hasattr(g, 'database'):
        g.database.close()


# Route voor het ophalen van gegevens uit de database
@app.route('/', methods=['GET', 'POST'])
def index():
    return read()

# Route voor Create, pagina om een nieuwe gebruiken aan te maken
@app.route('/create', methods=['GET', 'POST'])
def create():
    db = krijg_database()
    
    if request.method == "POST":
        
        gebr2 = request.form.get("gebr")
        wach2 = request.form.get("wach")
        naam2 = request.form.get("naam")
        adre2 = request.form.get("adre")
        post2 = request.form.get("post")
        gebo2 = request.form.get("gebo")

        check = db.execute('SELECT EXISTS(SELECT 1 FROM gebruikers WHERE gebruikersnaam=?)', (gebr2, )).fetchone()

        if check == (1,):
            return render_template("create.html", error=gebr2)
        else:
            db.cursor().execute("""
                                INSERT INTO gebruikers(gebruikersnaam, wachtwoord, 
                                naam, adres, postcode, geboortedatum) 
                                VALUES(?, ?, ?, ?, ?, ?)""", 
                                ([gebr2, wach2, naam2, adre2, post2, gebo2]))
            db.commit()
            return render_template("create.html", gebruiker=gebr2)
    
    return render_template("create.html")

# Route voor Read, het overzicht van alle gebruiken en bewerkingsopties
@app.route('/"read"', methods=['GET', 'POST'])
def read():
    # Maak verbinding met de database
    db = krijg_database()

    # Voer een query uit
    resultaat = db.execute('SELECT * FROM gebruikers').fetchall()

    if request.method == "POST":
        
        gebr2 = request.form.get("gebr")
        wach2 = request.form.get("wach")
        naam2 = request.form.get("naam")
        adre2 = request.form.get("adre")
        post2 = request.form.get("post")
        gebo2 = request.form.get("gebo")

        check = db.execute('SELECT EXISTS(SELECT 1 FROM gebruikers WHERE gebruikersnaam=?)', (gebr2, )).fetchone()

        if check == (1,):
            return render_template("create.html", error=gebr2)
        else:
            db.cursor().execute("""INSERT INTO gebruikers(gebruikersnaam, wachtwoord, 
                                naam, adres, postcode, geboortedatum) 
                                VALUES(?, ?, ?, ?, ?, ?)""", 
                                ([gebr2, wach2, naam2, adre2, post2, gebo2]))
            db.commit()
            return render_template("create.html", gebruiker=gebr2)

    # Resultaten weergeven
    return render_template("read.html", gebruikers=resultaat)

# Route voor Update, pagina om een specifieke gebruiken aan te passen
@app.route('/update/<gebruiker_id>', methods=['GET', 'POST'])
def update(gebruiker_id):
    db = krijg_database()
    gebruiker = db.execute('SELECT * FROM gebruikers WHERE id=?', (gebruiker_id, )).fetchone()

    if request.method == "POST":
        
        wach2 = request.form.get("wach")
        naam2 = request.form.get("naam")
        adre2 = request.form.get("adre")
        post2 = request.form.get("post")
        gebo2 = request.form.get("gebo")

        db.cursor().execute("""
                            UPDATE gebruikers
                            SET wachtwoord=?, naam=?, adres=?, postcode=?, 
                            geboortedatum=?
                            WHERE id=?
                            """, ([wach2, naam2, adre2, post2, gebo2, gebruiker_id]))
        db.commit()
        check = TRUE
        return render_template("update.html", gebruiker=gebruiker, check=check)

    return render_template("update.html", gebruiker=gebruiker, gebruiker_id=gebruiker_id)

# Route voor Delete, een melding dat een gebruiker succesvol is verwijderd
@app.route('/delete/<gebruiker_id>')
def delete(gebruiker_id):
    db = krijg_database()
    gebruiker = db.execute('SELECT * FROM gebruikers WHERE id=?', (gebruiker_id, )).fetchone()

    db.cursor().execute('DELETE FROM gebruikers WHERE id=?', (gebruiker_id, ))
    db.commit()

    return render_template("delete.html", gebruiker=gebruiker)


@app.route('/api/read', methods=['GET', 'POST'])
def api_read():
    # Maak verbinding met de database
    db = krijg_database()

    # Voer een query uit
    resultaat = db.execute('SELECT * FROM gebruikers').fetchall()

    print("aangeroepen")
    
    if request.method == "POST":
        print("is post")
        gebr2 = request.form.get("gebr")
        wach2 = request.form.get("wach")
        naam2 = request.form.get("naam")
        adre2 = request.form.get("adre")
        post2 = request.form.get("post")
        gebo2 = request.form.get("gebo")
        print(gebr2)
        
        check = db.execute('SELECT EXISTS(SELECT 1 FROM gebruikers WHERE gebruikersnaam=?)', (gebr2, )).fetchone()

        if check == (1,):
            print("check == 1")
            return render_template("api_read.html", error=gebr2)
        else:
            print("submit dingen")
            db.cursor().execute("""
                                INSERT INTO gebruikers(gebruikersnaam, wachtwoord, 
                                naam, adres, postcode, geboortedatum) 
                                VALUES(?, ?, ?, ?, ?, ?)""", 
                                ([gebr2, wach2, naam2, adre2, post2, gebo2]))
            db.commit()
            return render_template("api_read.html")
    print("anders")
    # Resultaten weergeven
    return render_template("api_read.html", gebruikers = resultaat)

@app.route('/api/delete/<gebruiker_id>')
def gebruiker_delete(gebruiker_id):
    db = krijg_database()
    gebruiker = db.execute('SELECT * FROM gebruikers WHERE id=?', (gebruiker_id, )).fetchone()

    db.cursor().execute('DELETE FROM gebruikers WHERE id=?', (gebruiker_id, ))
    db.commit()

    return '{"status" : "ok", "id" : ' + gebruiker_id + '}'

@app.route('/api/gebruikers')
def gebruikers():
    db = krijg_database()
    resultaat = db.execute('SELECT * FROM gebruikers').fetchall()
    users_list = [{'id': row[0], 'gebruikersnaam': row[1], 'wachtwoord': row[2], 'naam': row[3], 'adres': row[4], 'postcode': row[5], 'geboortedatum': row[6]} for row in resultaat]
    return jsonify(users_list)

@app.route('/api/update', methods=['POST'])
def api_update():

    if request.method == "POST":
        data = request.json['data']
        # print(data["naam"])
        db = krijg_database()
        gebruiker = db.execute('SELECT * FROM gebruikers WHERE id=?', (data["id"], )).fetchone()
        # print(data)
        db.cursor().execute("""
                            UPDATE gebruikers
                            SET naam=?, adres=?, postcode=?, 
                            geboortedatum=?
                            WHERE id=?
                            """, ([data["naam"], data["adres"], data["postcode"], data["geboortedatum"], data["id"]]))
        db.commit()
        check = TRUE
    return render_template("api_read.html", check=check)

@app.route('/api/create', methods=['GET', 'POST'])
def api_create():
    print("aangeroepen")
    db = krijg_database()
    
    if request.method == "POST":
        print("is post")
        gebr2 = request.form.get("gebr")
        wach2 = request.form.get("wach")
        naam2 = request.form.get("naam")
        adre2 = request.form.get("adre")
        post2 = request.form.get("post")
        gebo2 = request.form.get("gebo")
        print(gebr2)
        
        check = db.execute('SELECT EXISTS(SELECT 1 FROM gebruikers WHERE gebruikersnaam=?)', (gebr2, )).fetchone()

        if check == (1,):
            print("check == 1")
            return render_template("api_read.html", error=gebr2)
        else:
            print("submit dingen")
            db.cursor().execute("""
                                INSERT INTO gebruikers(gebruikersnaam, wachtwoord, 
                                naam, adres, postcode, geboortedatum) 
                                VALUES(?, ?, ?, ?, ?, ?)""", 
                                ([gebr2, wach2, naam2, adre2, post2, gebo2]))
            db.commit()
            return render_template("api_read.html")
    print("anders")
    return render_template("api_read.html")


if __name__ == '__main__':
    app.run(debug=True)
