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
