## Soal 1

> Knight's Tour (Perjalanan Kuda).
> Masalah ini meminta kita untuk menemukan urutan langkah kuda catur pada papan 8 X 8 sedemikian rupa sehingga kuda mengunjungi setiap kotak tepat satu kali.

**Answer:**

- Screenshot

Hasil Visualisasi

<img width="532" height="551" alt="Image" src="https://github.com/user-attachments/assets/24cce699-07a8-4e71-9a44-fa16c3582dc0" />

- Explanation

Menginisiasi Papan catur & gerakan kuda ( x, y )

```
 def __init__(self, size=8):
        self.n = size

        self.board = [[-1 for _ in range(size)] for _ in range(size)]

        self.moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
```

Mengecek apakah langkah berada di dalam papan dan belum dikunjungi

```
 def is_valid(self, x, y):
        return 0 <= x < self.n and 0 <= y < self.n and self.board[y][x] == -1
```

Menghitung berapa banyak langkah valid berikutnya dari posisi (x, y)

```
def get_degree(self, x, y):
        count = 0
        for dx, dy in self.moves:
            if self.is_valid(x + dx, y + dy):
                count += 1
        return count
```

Fungsi untuk mencari solusi dengan

1. Membuat langkah pertama
2. Loop untuk mencari 63 langkah berikutnya
3. Warnsdorff's heuristic dengan memilih langkah yang memiliki tetangga valid paling sedikit
4. Pilih langkah terbaik

```
  def solve(self, start_x, start_y):
        self.board[start_y][start_x] = 0
        pos = 1
        curr_x, curr_y = start_x, start_y

        path = [(curr_x, curr_y)]


        for i in range(self.n * self.n - 1):
            next_moves = []

            for dx, dy in self.moves:
                nx, ny = curr_x + dx, curr_y + dy
                if self.is_valid(nx, ny):

                    degree = self.get_degree(nx, ny)
                    next_moves.append((degree, nx, ny))

            if not next_moves:
                return False, path

            next_moves.sort(key=lambda x: x[0])

            _, best_x, best_y = next_moves[0]

            self.board[best_y][best_x] = pos
            curr_x, curr_y = best_x, best_y
            path.append((curr_x, curr_y))
            pos += 1

        return True, path
```

Fungsi untuk membuat plot visualisasi langkah

```
   def visualize(self, path):

        fig, ax = plt.subplots(figsize=(8, 8))

        for x in range(self.n):
            for y in range(self.n):
                if (x + y) % 2 == 0:
                    ax.add_patch(plt.Rectangle((x, y), 1, 1, color='#f0d9b5'))
                else:
                    ax.add_patch(plt.Rectangle((x, y), 1, 1, color='#b58863'))

        x_coords = [p[0] + 0.5 for p in path]
        y_coords = [p[1] + 0.5 for p in path]


        ax.plot(x_coords, y_coords, color='black', linewidth=1.5, marker='o', markersize=4)

        ax.plot(x_coords[0], y_coords[0], marker='o', markersize=10, color='green', label='Start')
        ax.plot(x_coords[-1], y_coords[-1], marker='X', markersize=10, color='red', label='End')


        start_x, start_y = path[0]
        end_x, end_y = path[-1]
        diff_x = abs(start_x - end_x)
        diff_y = abs(start_y - end_y)
        is_closed = (diff_x == 1 and diff_y == 2) or (diff_x == 2 and diff_y == 1)

        title = "Knight's Tour Visualization "

        if is_closed:
            ax.plot([x_coords[-1], x_coords[0]], [y_coords[-1], y_coords[0]],
                    color='blue', linestyle='--', label='Closing Move')

        ax.set_xlim(0, self.n)
        ax.set_ylim(0, self.n)
        ax.set_xticks(range(self.n + 1))
        ax.set_yticks(range(self.n + 1))
        ax.set_aspect('equal')
        ax.grid(True, color='black', linewidth=0.5)
        ax.legend(loc='upper right')
        plt.title(title)
        plt.show()
```

Inisiasi posisis awal knight dan jalankan fungsi utama

```
start_x = 0
start_y = 0

tour = KnightsTour(8)
success, path = tour.solve(start_x, start_y)

if success:
    print(f"Solusi ditemukan! Total langkah adalah {len(path)}")
    tour.visualize(path)
else:
    print("Solusi tidak ditemukan dengan titik awal tersebut.")
```

<br>

## Soal 2


# Largest Monotonically Increasing Subsequence (LIS) — Tree Expansion Method

Program ini menyelesaikan permasalahan **Largest Monotonically Increasing Subsequence (LIS)** menggunakan pendekatan *tree expansion*.  
Setiap node pada tree merepresentasikan satu subsekuensi meningkat, dan tree bertumbuh seiring proses eksplorasi semua kemungkinan subsekuensi.  
Pendekatan ini memungkinkan program menemukan **seluruh subsekuensi meningkat** serta **seluruh LIS** yang mungkin, bukan hanya satu.

Dokumentasi ini menjelaskan secara detail fungsi dan alur logika dalam program.

---

## Tujuan Program
Program ini bertujuan untuk:

- Mengeksplorasi semua subsekuensi monotonik meningkat dari suatu urutan bilangan.
- Menghilangkan duplikasi subsekuensi menggunakan struktur set.
- Menentukan panjang LIS.
- Menampilkan **semua subsekuensi LIS** yang memiliki panjang maksimum.

Pendekatan tree dipilih untuk memperlihatkan bagaimana sebuah subsekuensi bisa berkembang menjadi banyak jalur cabang.

---

## Penjelasan Detail Setiap Bagian Kode

### **1. Class `Node`**
Class ini adalah struktur dasar tree.

Setiap node menyimpan:
- `value` → nilai terakhir subsekuensi
- `seq` → seluruh elemen subsekuensi sampai node tersebut
- `children` → daftar node turunan yang memperpanjang subsekuensi ini

**Perannya:**  
Menjadi representasi satu *state subsequence* dalam pohon yang bertumbuh.

---

### **2. Fungsi `build_tree(arr)`**
Fungsi ini membangun pohon dari awal menggunakan array input.

Prosesnya:
1. Menyimpan semua root dalam list `roots`.
2. Untuk setiap angka `num` pada array:
   - Mencoba menambahkan `num` ke subsekuensi yang sudah ada sebelumnya.
   - Membuat subsekuensi baru yang dimulai dari angka itu sendiri `[num]`.
3. Semua subsekuensi baru ditambahkan sebagai node baru.

**Tujuan:**  
Mengekspansi seluruh kemungkinan subsekuensi meningkat secara sistematis.

---

### **3. Fungsi `explore_add(node, num, new_nodes)`**
Fungsi rekursif yang menentukan apakah sebuah angka bisa ditambahkan ke subsekuensi tertentu.

Aturan yang digunakan:
- Jika `num > node.value`, berarti `num` dapat memperpanjang subsekuensi tersebut.
- Sebuah node baru dibentuk yang mewakili subsekuensi baru.
- Node baru tersebut ditambahkan sebagai anak (`children`) dari node current.

Setelah pengembangan node utama:
- Fungsi memanggil dirinya sendiri ke semua anak node untuk melanjutkan eksplorasi.

**Inti logika:**  
Menelusuri seluruh jalur subsekuensi tanpa melewatkan peluang pertumbuhan.

---

### **4. Fungsi `collect_all_sequences(roots)`**
Setelah tree selesai dibangun, fungsi ini mengumpulkan seluruh subsekuensi meningkat.

Langkah-langkah:
- Mengambil `seq` dari tiap root node.
- Mengubah `seq` menjadi tuple agar bisa disimpan dalam set.
- Set digunakan untuk menghapus duplikasi subsekuensi.
- Setelah itu, tuple dikembalikan dalam bentuk list.

**Mengapa perlu set?**  
Karena tree dapat menghasilkan subsekuensi yang sama melalui jalur berbeda.

---

### **5. Fungsi `get_all_LIS(sequences)`**
Fungsi ini mencari subsekuensi dengan panjang maksimum.

Alur kerja:
1. Menentukan panjang terpanjang di antara semua subsekuensi meningkat.
2. Mengembalikan semua subsekuensi yang memiliki panjang tersebut.

**Keuntungan:**  
Jika ada beberapa LIS, semuanya terdeteksi.

---

### **6. Bagian Utama Program**
Bagian utama program melakukan tahapan sebagai berikut:

1. Mendefinisikan urutan bilangan sebagai input.
2. Membangun tree subsekuensi menggunakan `build_tree`.
3. Mengambil semua subsekuensi meningkat melalui `collect_all_sequences`.
4. Menentukan LIS menggunakan `get_all_LIS`.
5. Menampilkan:
   - Semua subsekuensi meningkat
   - Semua LIS beserta panjangnya

Output memberikan gambaran lengkap mengenai seluruh perkembangan subsekuensi.

---

## Input Program
Program menerima list bilangan, contoh: `[4, 1, 13, 7, 0, 2, 8, 11, 3]`


---

## Output Program
Program menghasilkan dua bagian utama output:

### 🔹 Semua subsekuensi meningkat (tanpa duplikasi)
Disajikan dalam bentuk list, satu subsekuensi per baris.

### 🔹 Largest Monotonically Increasing Subsequences
Menampilkan:
- Panjang LIS
- Seluruh LIS (bisa lebih dari satu)

Output: 
```
=== Semua subsekuensi meningkat ===
[0]
[0, 2]
[0, 2, 3]
[0, 2, 8]
[0, 2, 8, 11]
[0, 2, 11]
...
=== Largest Monotonically Increasing Subsequence ===
Length : 4
[1, 2, 8, 11]
[1, 7, 8, 11]
[4, 7, 8, 11]
[0, 2, 8, 11]
```

---

## Ringkasan Logika Program
1. Tree dibangun untuk mengeksplorasi semua subsekuensi meningkat.
2. Node pada tree menyimpan subsekuensi hingga tahap tersebut.
3. Tree diekspansi menggunakan aturan `num > node.value`.
4. Semua subsekuensi dikumpulkan dan duplikasi dihilangkan.
5. LIS diambil berdasarkan panjang maksimum.
6. Hasil ditampilkan sepenuhnya.

Pendekatan ini cocok digunakan sebagai demonstrasi konsep tree, eksplorasi brute-force terstruktur, dan analisis subsekuensi.
