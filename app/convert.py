from pdf2image import convert_from_path

# Spécifiez le chemin du fichier PDF
pdf_path ="Documents\Audacity\mongomarket.pdf"

# Convertissez le PDF en une liste d'images
images = convert_from_path(pdf_path)
print(images)
# Enregistrez chaque image individuellement
for i, image in enumerate(images):
    image.save(f"image_{i}.png", "PNG")