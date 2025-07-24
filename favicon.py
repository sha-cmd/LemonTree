from PIL import Image
import os
import sys
import subprocess


def create_favicons(source_image_path, output_dir='.'):
    """Crée tous les formats de favicon à partir d'une image source"""

    # Vérifier que l'image source existe
    if not os.path.exists(source_image_path):
        print(f"Erreur: L'image source {source_image_path} n'existe pas.")
        return False

    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Ouvrir l'image source
        img = Image.open(source_image_path)

        # Définir les tailles d'icônes
        sizes = [16, 32, 48, 64, 128, 192, 256]

        # Créer les PNG de différentes tailles
        for size in sizes:
            resized_img = img.resize((size, size), Image.LANCZOS)
            output_path = os.path.join(output_dir, f"favicon-{size}x{size}.png")
            resized_img.save(output_path)
            print(f"Créé: {output_path}")

        # Créer le fichier ICO (Windows)
        ico_path = os.path.join(output_dir, "favicon.ico")
        ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save(ico_path, sizes=ico_sizes, format="ICO")
        print(f"Créé: {ico_path}")

        # Si sur macOS, créer le fichier ICNS
        if sys.platform.startswith('darwin'):
            try:
                # Créer le dossier temporaire pour les icônes
                iconset_dir = os.path.join(output_dir, "favicon.iconset")
                if not os.path.exists(iconset_dir):
                    os.makedirs(iconset_dir)

                # Générer les fichiers pour l'iconset
                for size in [16, 32, 128, 256, 512]:
                    # Normal resolution
                    resized_img = img.resize((size, size), Image.LANCZOS)
                    resized_img.save(os.path.join(iconset_dir, f"icon_{size}x{size}.png"))

                    # High resolution (2x) if possible
                    if size * 2 <= max(img.size):
                        resized_img = img.resize((size * 2, size * 2), Image.LANCZOS)
                        resized_img.save(os.path.join(iconset_dir, f"icon_{size}x{size}@2x.png"))

                # Convertir l'iconset en icns
                icns_path = os.path.join(output_dir, "favicon.icns")
                subprocess.run(["iconutil", "-c", "icns", iconset_dir, "-o", icns_path])
                print(f"Créé: {icns_path}")

                # Supprimer le dossier temporaire
                for f in os.listdir(iconset_dir):
                    os.remove(os.path.join(iconset_dir, f))
                os.rmdir(iconset_dir)

            except Exception as e:
                print(f"Erreur lors de la création du fichier ICNS: {e}")
                print("Vous pouvez utiliser un outil en ligne pour créer le fichier .icns")

        return True

    except Exception as e:
        print(f"Erreur lors de la création des favicons: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_favicons.py chemin/vers/image_source.png [dossier_sortie]")
    else:
        source_path = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else '.'
        create_favicons(source_path, output_dir)