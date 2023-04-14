<?php
session_start();
try
{
    $bdd = new PDO('mysql:host=localhost;dbname=musique;charset=utf8', 'root', '');
}
catch (Exception $e)
{
    die('Erreur: '. $e->getMessage());
}

if(isset($_POST['pseudo']) AND isset($_POST['password'])){
    $pseudo = htmlspecialchars($_POST['pseudo']);
    $pass = htmlspecialchars($_POST['password']);
    //echo 'tu t\'appelles '. $pseudo. ' et ton mdp est ' . $pass;
    $requete = $bdd->prepare('SELECT * FROM users WHERE pseudo=? AND motdepasse=?');
    $requete->execute(array($pseudo, $pass));
    $info_utilisateur = $requete->fetch();
    if(!empty($info_utilisateur['id']))
    {
        //echo 'vous etes connecté !';
        $_SESSION['id'] = $info_utilisateur['id'];
        $_SESSION['pseudo'] = $info_utilisateur['pseudo'];
        $_SESSION['prenom'] = $info_utilisateur['prenom'];
        $_SESSION['statut'] = $info_utilisateur['statut'];
        // fonctionne pas: $_SESSION['bdd'] = $bdd;
        //echo 'a = '. gettype($bdd);
        header('Location: index.php');

    }
    else{
        //echo 'pas co...'; 
        ?> <a href="connexion.php">connexion</a> <?php
        header('Location: connexion.php');
    }
}
else{
    //echo "il manque l'un ou l'autre...";
    header('Location: connexion.php');
}

?>