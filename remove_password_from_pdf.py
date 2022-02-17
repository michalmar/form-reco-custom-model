import pikepdf

# pdf_loc = input("PDF location: ")
# pdf_pass = input("PDF password: ")
pdf_loc = "test.pdf"
pdf_pass = "abc1234"

pdf = pikepdf.open(pdf_loc, password=pdf_pass)

print("\nProcessing...\n")

# pdf_save = input("Save file as: ")
# pdf_loc2 = input("Save location: ")

pdf_save = "test-no-pass.pdf"
pdf_loc2 = "."


pdf.save(pdf_loc2 + '\\' + pdf_save)

print("The password successfully removed from the PDF")
print("\aLocation: " + pdf_loc + '\\' + pdf_save)