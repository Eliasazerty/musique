<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style_global.css">
    <title>Connexion</title>
</head>
<body>
    <form method="post" action="traitement.php">
        <h1>Connexion</h1>

        <div class="inputs">
            <input type="text" name="pseudo" id="pseudo" placeholder="Pseudonyme">
            <input type="password" name="password" id="password" placeholder="Mot de passe">
        </div>

        <div class="bouton">
            <input type="submit" value="Valider" id="bouton_valider" class="button">
        </div>

    </form>
</body>
</html>