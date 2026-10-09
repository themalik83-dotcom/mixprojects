# 1. Membaca dan menampilkan isi file saat ini
try:
    with open('quotes.txt', "r", encoding="UTF-8") as file:
        print("--- Fill of the current file ---")
        for line in file:
            print(line.strip())  # Menggunakan strip() agar tidak ada double newline saat print
        print("-------------------------\n")
except FileNotFound:
    print("File 'quotes.txt' belum ada. File baru akan dibuat jika kamu menambah quote.\n")




# 2. Loop konfirmasi terlebih dahulu sebelum meminta data
while True:
    answer = input("do u want add a quote? (yes/no): ").strip().lower()
   
    if answer == "yes":
        # Jika belum beres (mau nambah), baru minta input quote dan author
        quote = input("Entered quote: ")
        author = input("Entered Author name: ")
       
        # Tulis ke file menggunakan 'with open' agar otomatis close dan lebih aman
        with open("quotes.txt", "a", encoding="UTF-8") as file:
            file.write(quote + "\n" + "(" + author + ")" + "\n")
        print("Quote has added!\n")
    else:
        # Jika memilih 'no' atau sudah beres, keluar dari loop
        print("\nProgram selesai mengisi.")
        break




# 3. Menampilkan isi file final setelah di-update
print("\n--- Isi File Terbaru ---")
try:
    with open('quotes.txt', "r", encoding="UTF-8") as file:
        for line in file:
            print(line.strip())
    print("------------------------")
except FileNotFound:
    print("File kosong.")

