import pikepdf
import os

# pdf_loc = input("PDF location: ")
# pdf_pass = input("PDF password: ")
pdf_loc = os.path.join("data","test.pdf")
pdf_pass = "abc1234"

pdf = pikepdf.open(pdf_loc, password=pdf_pass)

print("\nProcessing...\n")

# pdf_save = input("Save file as: ")
# pdf_loc2 = input("Save location: ")

pdf_loc2 = os.path.join("data", "test-no-pass.pdf")


pdf.save(pdf_loc2)

print("The password successfully removed from the PDF")
print("\aLocation: " + pdf_loc2)