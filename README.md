# Renovate

## Exemple

Des templates de configuration sont présents dans `/configs`.

Selon le type de repo, les configurations ont des différences car Renovate ne cherche pas à update le même type de dépendances.

Pour utiliser renovate sur un repo présent dans https://git.sk5.io/skale-5, il faut ajouter un fichier `.releaserc` à la racine de celui-ci.

```json
{
    "$schema": "https://docs.renovatebot.com/renovate-schema.json",
    "extends": [
        "skale-5/renovate//configs/basic"
    ]
}
```
