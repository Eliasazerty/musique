<?php
session_start();
if(isset($_SESSION['id']))
{   
    try
    {
        $bdd = new PDO('mysql:host=localhost;dbname=musique;charset=utf8', 'root', '');
    }
    catch (Exception $e)
    {
        die('Erreur: '. $e->getMessage());
    }
    ?>
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="style_index.css">
        <script src="controles.js"></script>
        <script src="https://kit.fontawesome.com/e197ce4684.js" crossorigin="anonymous"></script>
        <title>Document</title>
    </head>
    <body>
        <nav>
            <form method="post" action="">
                <div class="inputs">
                    <input type="text" name="musique_recherchee" id="musique_recherchee" placeholder="recherchez votre musique">
                    <input type="submit" value="Rechercher">
                </div>
            </form>
            <p class="link"><a href="ajouter_musique.php"><button>Ajouter une musique !</button></a></p>
        </nav>
        <div class="musique">
            <?php
            if(isset($_POST['musique_recherchee']))
            {
                $recherche = htmlspecialchars($_POST['musique_recherchee']);

                $req = $bdd->prepare("SELECT * FROM musiques WHERE titre LIKE ? OR artiste LIKE ?");
                $req->execute(array("%".$recherche."%", "%".$recherche."%"));
                $counter = 0;
                while($donnees = $req->fetch())
                {
                    $counter+=1;
                    $req_tmp_genre = $bdd->prepare("SELECT genre FROM genre_musicaux WHERE id=?");
                    $req_tmp_genre->execute(array($donnees['genre']));
                    $genre = $req_tmp_genre->fetch();
                    $genre = $genre['genre'];

                    $req_tmp_source = $bdd->prepare("SELECT source FROM sources WHERE id=?");
                    $req_tmp_source->execute(array($donnees['source']));
                    $source = $req_tmp_source->fetch();
                    $source = $source['source']; ?>

                    <div class="element" id="element<?php echo $counter;?>">
                        <div class="infos">
                            <p>
                                <strong><?php echo  $donnees['titre']; ?></strong>
                                <strong><?php echo $donnees['artiste']; ?></strong>
                                <strong><?php echo $donnees['album']; ?></strong>
                                <strong><?php echo $genre; ?></strong>
                                <strong><?php echo  $source; ?></strong>
                            </p>
                        </div>
                        <audio src="<?php echo $donnees['path']?>" id="lecteur_musique<?php echo $counter;?>">Affichage audio pas compatible avec votre version de navigateur...</audio>
                        <div class="controls" id="controls<?php echo $counter;?>">
                            <!-- Ajout par javascript des boutons de gestion-->
                        </div>
                        <div class="download">
                            <button><a href="/<?php echo $donnees['path']?>" target="_blank" download=""><i class="fa-solid fa-download"></i></a></button>
                        </div>
                    </div> <?php
                }
                $req->closeCursor();
            }?>
        </div>
    </body>
    </html>
<?php
}
else
{
    header('Location: connexion.php');
}

?>