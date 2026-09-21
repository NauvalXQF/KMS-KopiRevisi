// Kopi Revisi — shared UI helpers (konsolidasi dari inline <script> per halaman)
document.addEventListener("DOMContentLoaded", () => {
  // Stok: hitung badge Menipis/Aman saat halaman dimuat
  const rows = document.querySelectorAll(".stok-row");
  if (rows.length) {
    let menipisCount = 0;
    let amanCount = 0;
    rows.forEach((r) => {
      if (r.dataset.status === "menipis") menipisCount++;
      else amanCount++;
    });
    const elM = document.getElementById("cntMenipis");
    const elA = document.getElementById("cntAman");
    if (elM) elM.textContent = menipisCount;
    if (elA) elA.textContent = amanCount;
  }

  // Penjualan: samakan visibilitas input tanggal/bulan + harga awal
  if (document.getElementById("filterMode")) togglePeriodeInputs();
  if (document.getElementById("selectMenu")) syncHargaPenjualan();
});

// Stok: filter client-side Semua/Menipis/Aman
function filterStok(type, btn) {
  document
    .querySelectorAll("#stokFilterTabs .filter-chip")
    .forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");
  document.querySelectorAll(".stok-row").forEach((r) => {
    r.style.display = type === "all" || r.dataset.status === type ? "" : "none";
  });
}

// Login: isi otomatis akun demo (khusus prototipe/demo)
function demoLogin(nama, pin) {
  const inputNama = document.getElementById("inputNama");
  const inputPin = document.getElementById("inputPin");
  const form = document.getElementById("loginForm");
  if (inputNama) inputNama.value = nama;
  if (inputPin) inputPin.value = pin;
  if (form) form.submit();
}

// Penjualan: tampilkan input tanggal/bulan sesuai mode filter
function togglePeriodeInputs() {
  const modeEl = document.getElementById("filterMode");
  if (!modeEl) return;
  const mode = modeEl.value;
  const wrapT = document.getElementById("wrapTanggal");
  const wrapB = document.getElementById("wrapBulan");
  if (wrapT) wrapT.style.display = mode === "harian" ? "" : "none";
  if (wrapB) wrapB.style.display = mode === "bulanan" ? "" : "none";
}

// Penjualan: isi harga otomatis dari master menu yang dipilih
function syncHargaPenjualan() {
  const sel = document.getElementById("selectMenu");
  const out = document.getElementById("inputHarga");
  if (!sel || !out) return;
  const opt = sel.options[sel.selectedIndex];
  const harga = opt ? opt.getAttribute("data-harga") : null;
  if (harga) {
    const num = Number(harga);
    out.value = "Rp " + num.toLocaleString("id-ID");
  } else {
    out.value = "";
  }
}
