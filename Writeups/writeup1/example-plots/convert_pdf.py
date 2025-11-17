from pdf2image import convert_from_path

pdf_path = "Rplots.pdf"
images = convert_from_path(pdf_path)

# Save first page as PNG
images[0].save("Rplots.png", "PNG")

