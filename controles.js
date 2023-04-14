var dict = new Object();

function reagir(e)
{
    if(e.currentTarget.est_en_lecture == 0)
    {
        e.currentTarget.lecteur.play();
        e.currentTarget.est_en_lecture = 1;
        e.currentTarget.innerHTML = '<i class="fa-solid fa-circle-pause"></i>';
        //console.log(e.currentTarget);
    }
    else
    {
        e.currentTarget.lecteur.pause();
        e.currentTarget.est_en_lecture = 0;
        e.currentTarget.innerHTML = '<i class="fa-solid fa-circle-play"></i>';
    }
}

function telecharger(e)
{

}

function creerBoutons() {
    // on recupere les id des balises <audio> et des <div class="controls">
    const array_id_audios = Array.from(document.querySelectorAll("audio[id]")).map((audio) => audio.id);
    const array_id_divs_control = Array.from(document.querySelectorAll("div.controls")).map((div) => div.id);

    //console.log(array_id_audios);
    //console.log(array_id_divs_control);

    for(var i= 0; i < array_id_audios.length; i++) // il y a forcément autant de div <audio> que de <div class="controls">
    {
        var lecteur;
        var PlayPauseBTN = document.createElement("button");

        var controlesBox = document.getElementById(array_id_divs_control[i]);
        lecteur = document.getElementById(array_id_audios[i]);

        // Dictionnaire pour l'instant inutile, mais peut-être utile après, pour arrêter un lecteur lorsqu'un autre sera demarré...
        dict[i] = Array(lecteur, 0); // array: [lecteur, est_en_lecture]

        PlayPauseBTN.innerHTML= '<i class="fa-solid fa-circle-play"></i>';

        controlesBox.appendChild(PlayPauseBTN);

        // On ajoute les paramètres requis pour la fonction reagir
        PlayPauseBTN.addEventListener("click", reagir, false);
        PlayPauseBTN.lecteur = dict[i][0];
        PlayPauseBTN.est_en_lecture = dict[i][1];

        // Affiche les nouveaux boutons et supprime l'interface originale
        controlesBox.removeAttribute("hidden");
        lecteur.removeAttribute("controls");
    }
}

document.addEventListener('DOMContentLoaded', creerBoutons, false);