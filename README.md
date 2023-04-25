# Renovate

[![pipeline status](https://git.sk5.io/skale-5/renovate/badges/main/pipeline.svg?ignore_skipped=true)](https://git.sk5.io/skale-5/renovate/-/commits/main)
[![Latest Release](https://git.sk5.io/skale-5/renovate/-/badges/release.svg)](https://git.sk5.io/skale-5/renovate/-/releases)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
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

Pour utiliser les conf sur des repos externes à git.sk5.io, on peut procéder de la manière suivante :
```json
{
    "$schema": "https://docs.renovatebot.com/renovate-schema.json",
    "extends": [
        "github>skale-5/renovate//configs/basic"
    ]
}
```
