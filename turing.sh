#!/usr/bin/env bash
#
# turing.sh
# Usage: ./turing.sh [encrypt|decrypt] [RECIPIENT]
#

set -eo pipefail

SCRIPT_NAME="$(basename "$0")"
KEY_ID="$2"

usage() {
  cat <<EOF
Usage: $SCRIPT_NAME <command>

Commands:
  encrypt   Chiffre tous les fichiers (créé .gpg pour chaque fichier non .gpg)
  decrypt   Déchiffre tous les fichiers *.gpg (restitue la version sans .gpg)
  help      Affiche ce message

Exemples:
  ./$SCRIPT_NAME encrypt
  ./$SCRIPT_NAME decrypt
EOF
  exit 1
}

# Exclure .git, ce script, et les fichiers .gpg (pour encrypt)
encrypt_all() {
  find . \
    -path "./.git" -prune -o \
    -path "./.idea" -prune -o \
    -name "$(printf '%s\n' "$SCRIPT_NAME")" -prune -o \
    -type f  \( \
        -iname '*.png' -o \
        -iname '*.jpg' -o \
        -iname '*.ico' -o \
        -iname '*.py'  -o \
        -iname '*.html' -o \
        -iname '*.spec' \
    \)   -print0 \
  | while IFS= read -r -d '' file; do
      echo "Chiffrement de $file..."
      echo "gpg --encrypt --recipient $2 $file"
      gpg --encrypt --recipient "$KEY_ID" "$file"
    done
}

# Déchiffrer tous les .gpg
decrypt_all() {
  find . \
    -path "./.git" -prune -o \
    -path "./.idea" -prune -o \
    -type f -name '*.gpg' -print0 \
  | while IFS= read -r -d '' file; do
      plaintext="${file%.gpg}"
      echo "Déchiffrement de $file -> $plaintext"
      gpg --decrypt --recipient "$KEY_ID" "$file" > "$plaintext"
    done
}

if [ $# -ne 2 ]; then
  usage
fi

case "$1" in
  encrypt) encrypt_all ;;
  decrypt) decrypt_all ;;
  help|--help|-h) usage ;;
  *)
    echo "Commande inconnue : $1" >&2
    usage
    ;;
esac