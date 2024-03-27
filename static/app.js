// app.js
document.addEventListener('DOMContentLoaded', function() {
    laadGebruikersData();
});

function laadGebruikersData() {
    // AJAX-request om gebruikersdata op te halen
    
    fetch('/api/gebruikers')
        .then(response => response.json())
        .then(gebruikers => toonGebruikersData(gebruikers));
};

function toonGebruikersData(gebruikers) {
    // Dynamisch vullen van de tabel in de SPA
    const tabelBody = document.querySelector('#gebruikerstabel tbody');
    tabelBody.innerHTML = '';


    gebruikers.forEach(gebruiker => {
        const rij = document.createElement('tr');
        rij.innerHTML = `
            <td>${gebruiker.id}</td>
            <td>${gebruiker.gebruikersnaam}</td>
            <td>${gebruiker.naam}</td>
            <td>${gebruiker.adres}</td>
            <td>${gebruiker.postcode}</td>
            <td>${gebruiker.geboortedatum}</td>
            <td>
                <button onclick="wijzigGebruikersData(${gebruiker.id})">Wijzigen</button>
                <button onclick="verwijderGebruiker(${gebruiker.id})">Verwijderen</button>
            </td>
        `;
        tabelBody.appendChild(rij);
    });

    console.log(document.getElementById("newUser"));
};


function verwijderGebruiker(gebruikerId) {
  // Implementeer logica voor het verwijderen van een gebruiker via AJAX
  fetch(`/api/delete/${gebruikerId}`)
    .then((response) => response.json())
    .then((return_resp) =>
      alert("Succesvol gebruiker " + return_resp.id + " verwijderd.")
    );
    laadGebruikersData();
};


function wijzigGebruikersData(gebruikerId) {
  // AJAX-request om gebruikersdata op te halen
  fetch("/api/gebruikers")
    .then((response) => response.json())
    .then((gebruikers) => wijzigGebruikerSetup(gebruikers, gebruikerId));
};

var wijzigCheck = 0

function wijzigGebruikerSetup(gebruikers, gebruikerId) {
  // Implementeer logica voor het wijzigen van een gebruiker via AJAX

  var gebruiker = gebruikers[gebruikerId - 1];

  var data;

  console.log(gebruiker);

  const tabelBody = document.querySelector("#gebruikerstabel tbody");
  const rij = document.createElement("tr");
  rij.innerHTML = `
            <td id="checkId">${gebruiker.id}*</td>
            <td><div id="checkGebr" contenteditable>${gebruiker.gebruikersnaam}</div></td>
            <td><div id="checkNaam" contenteditable>${gebruiker.naam}</div></td>
            <td><div id="checkAdre" contenteditable>${gebruiker.adres}</div></td>
            <td><div id="checkPost" contenteditable>${gebruiker.postcode}</div></td>
            <td><div id="checkGebo" contenteditable>${gebruiker.geboortedatum}</div></td>
            <td>
                <button onclick="wijzigGebruiker(${gebruiker.id}, '${gebruiker.wachtwoord}')">Wijziging doorvoeren</button>
            </td>
        `;

  if (wijzigCheck === 0) {
    // maak nieuwe rij aan
    tabelBody.innerHTML = tabelBody.innerHTML + rij.innerHTML;
    wijzigCheck = 1;
  } else {
    // vervang laatste lijn ipv toevoegen
    var table = document.querySelector("#gebruikerstabel tbody");
    var rowCount = table.rows.length;
    table.deleteRow(rowCount - 1);
    tabelBody.innerHTML = tabelBody.innerHTML + rij.innerHTML;
  };


  console.log("wijzigen geclickt");

};

function wijzigGebruiker(gebrId, gebrWach) {
  console.log("Wijziging doorvoeren geclickt")
  console.log("id: " + gebrId);

  data = {
    id: gebrId,
    gebruikersnaam: document.getElementById("checkGebr").innerText,
    wachtwoord: gebrWach,
    naam: document.getElementById("checkNaam").innerText,
    adres: document.getElementById("checkAdre").innerText,
    postcode: document.getElementById("checkPost").innerText,
    geboortedatum: document.getElementById("checkGebo").innerText,
  };

  console.log(data);

  fetch("/api/update", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ data: data }),
  })
    .then((response) => response.text())
    .then((result) => {
      console.log(result);
      console.log("success")
    });
};

document.addEventListener("submit", function () {
  console.log("submitted")
  fetch("/api/read", {
    method: "POST",
  }).then(alert("Succesvol gebruiker aangemaakt."));
});
