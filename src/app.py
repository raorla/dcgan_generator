import torch
import torch.nn as nn
import torchvision.utils as vutils
import os
import json
import sys

# Définir la classe du générateur DCGAN
class Generator(nn.Module):
    def __init__(self, nz=100, ngf=64, nc=3):
        super(Generator, self).__init__()
        self.tconv1 = nn.ConvTranspose2d(nz, ngf * 8, 4, 1, 0, bias=False)
        self.bn1 = nn.BatchNorm2d(ngf * 8)
        self.relu1 = nn.ReLU(True)
        self.tconv2 = nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(ngf * 4)
        self.relu2 = nn.ReLU(True)
        self.tconv3 = nn.ConvTranspose2d(ngf * 4, ngf * 2, 4, 2, 1, bias=False)
        self.bn3 = nn.BatchNorm2d(ngf * 2)
        self.relu3 = nn.ReLU(True)
        self.tconv4 = nn.ConvTranspose2d(ngf * 2, ngf, 4, 2, 1, bias=False)
        self.bn4 = nn.BatchNorm2d(ngf)
        self.relu4 = nn.ReLU(True)
        self.tconv5 = nn.ConvTranspose2d(ngf, nc, 4, 2, 1, bias=False)
        self.tanh = nn.Tanh()

    def forward(self, input):
        x = self.relu1(self.bn1(self.tconv1(input)))
        x = self.relu2(self.bn2(self.tconv2(x)))
        x = self.relu3(self.bn3(self.tconv3(x)))
        x = self.relu4(self.bn4(self.tconv4(x)))
        x = self.tanh(self.tconv5(x))
        return x

# Paramètres du modèle
nz = 100  # Taille du vecteur de bruit
ngf = 64  # Taille des filtres du générateur
nc = 3    # Nombre de canaux (RGB)

# Définir le chemin du modèle dans /app/src
model_path = "/app/src/dcgan_generator.pth"

# Vérifier que le fichier du modèle existe
if not os.path.exists(model_path):
    print(f"Erreur : Fichier modèle non trouvé : {model_path}", flush=True)
    sys.exit(1)

# Charger le modèle pré-entraîné
generator = Generator(nz, ngf, nc)
try:
    # Charger le fichier avec map_location pour CPU
    checkpoint = torch.load(model_path, map_location=torch.device('cpu'))
    # Vérifier si c'est un checkpoint ou un state_dict direct
    if isinstance(checkpoint, dict) and "generator" in checkpoint:
        generator.load_state_dict(checkpoint["generator"])
    else:
        generator.load_state_dict(checkpoint)
    generator.eval()
    print("Modèle chargé avec succès", flush=True)
except Exception as e:
    print(f"Erreur lors du chargement du modèle : {e}", flush=True)
    sys.exit(1)

# Déplacer le modèle vers le CPU (forcer CPU pour Scone)
device = torch.device("cpu")
generator = generator.to(device)

# Générer un vecteur de bruit aléatoire
noise = torch.randn(1, nz, 1, 1, device=device)

# Générer l'image
try:
    with torch.no_grad():
        generated_image = generator(noise)
    print("Image générée avec succès", flush=True)
except Exception as e:
    print(f"Erreur lors de la génération de l'image : {e}", flush=True)
    sys.exit(1)

# Sauvegarder l'image dans IEXEC_OUT
output_dir = os.environ["IEXEC_OUT"]
output_path = os.path.join(output_dir, "generated_image.png")
try:
    vutils.save_image(generated_image, output_path, normalize=True)
    print(f"Image enregistrée : {output_path}", flush=True)
except Exception as e:
    print(f"Erreur lors de l'enregistrement de l'image : {e}", flush=True)
    sys.exit(1)

# Écrire les résultats dans computed.json
try:
    with open(os.path.join(output_dir, 'computed.json'), 'w') as f:
        json.dump({"deterministic-output-path": output_path}, f)
    print("Résultats enregistrés dans computed.json", flush=True)
except Exception as e:
    print(f"Erreur lors de l'écriture des résultats : {e}", flush=True)
    sys.exit(1)

print("Génération d'image terminée avec succès", flush=True)