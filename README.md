# Renovate
[![pipeline status](https://git.sk5.io/skale-5/renovate/badges/main/pipeline.svg?ignore_skipped=true)](https://git.sk5.io/skale-5/renovate/-/commits/main)
[![Latest Release](https://git.sk5.io/skale-5/renovate/-/badges/release.svg)](https://git.sk5.io/skale-5/renovate/-/releases)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

## Exemples

Des templates de configuration sont présents dans `/configs`.

Selon le type de repo, les configurations ont des différences car Renovate ne cherche pas à update le même type de dépendances.

Pour utiliser renovate sur un repo présent dans https://git.sk5.io/skale-5, il faut ajouter un fichier `.renovaterc` à la racine de celui-ci (c'est tout ce qu'il y a à faire).

```json
{
    "$schema": "https://docs.renovatebot.com/renovate-schema.json",
    "extends": [
        "skale-5/renovate//configs/<workflow>"
    ]
}
```

Pour utiliser les conf sur des repos externes à git.sk5.io, on peut procéder de la manière suivante :
```json
{
    "$schema": "https://docs.renovatebot.com/renovate-schema.json",
    "extends": [
        "github>skale-5/renovate//configs/<workflow>"
    ]
}
```

👨🏼‍🔧 veillez à bien adapter le workflow en fonction de votre cas. La liste des workflows disponnible est [ici](https://git.sk5.io/skale-5/renovate/-/tree/main/configs).

<br />

## Maintenir à jour une version dans...
Utilisez un commentaire sur la ligne qui précède la version à maintenir à jour.

Vous spécifierez au moins la datasource et la depName, ainsi que la registryUrl si cela est nécessaire.

Vous pourez également spécifier le versionning.

📝 Sous réserve de l'activation du regexManager approprié.

<br />

### cookiecutter.json
Valable pour maintenir la version de tout type de programme.

Dans ce fichier, les commentaires prendront la forme suivante :
```json
{
    "_renovate": "datasource=helm depName=redis registryUrl=https://charts.bitnami.com/bitnami versioning=helm",
    "a_maintenir": "16.13.0",
}
```
*Dans ce cas illustré, Renovate proposera ou fera toujours des changements de version pour "a_maintenir", en utilisant la dernière version disponnible de la chart Helm de Redis dans la registry Bitnami.*

💡 Notez que la version de TF dispose d'un regexManager dédié, inutile d'ajouter un commentaire pour la maintenir.

<br />

### chart.sh
Uniquement valable pour maintenir "CHART_VERSION".

Dans ce fichier, les commentaires prendront la forme suivante :
```bash
# renovate: datasource=helm depName=redis registryUrl=https://charts.bitnami.com/bitnami
CHART_VERSION="16.13.0"
```
*Dans ce cas illustré, Renovate proposera ou fera toujours des changements de version pour "CHART_VERSION", en utilisant la dernière version disponnible de la chart Helm de Redis dans la registry Bitnami.*

<br />

### Chart.yaml
Uniquement valable pour maintenir "version" (du chart) ou "appVersion".

⚠️ La version des dépendances est maintenue automatiquement ; n'y ajoutez pas de commentaire !

Dans ce fichier, les commentaires prendront la forme suivante (même forme que pour chart.sh) :
```yaml
apiVersion: v2
name: redis
description: A Helm chart for Kubernetes

type: application
# renovate: datasource=helm depName=redis registryUrl=https://charts.bitnami.com/bitnami
version: 16.13.0

# renovate: datasource=docker depName=redis
appVersion: "6.2.7"

# LA VERSION DES DÉPENDANCES EST MAINTENUE AUTOMATIQUEMENT PAR RENOVATE
# N'ajoutez pas de commentaires pour leur maintenance !
dependencies:
- name: redis
  version: "16.13.0"
  repository: "https://charts.bitnami.com/bitnami"
```
*Dans ce cas illustré, Renovate proposera ou fera toujours des changements de version pour "version" (du Chart), en utilisant la dernière version disponnible de la chart Helm de Redis dans la registry Bitnami.*

*Il proposera ou fera également des changements de version pour "appVersion", en utilisant la dernière version disponnible du container Docker, dans la registry Docker Hub.*
