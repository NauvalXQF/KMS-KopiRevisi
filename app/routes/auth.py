from time import time

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import Pengguna
from app.routes.helpers import login_required, pemilik_only

bp = Blueprint("auth", __name__)

MAX_FAIL = 5
BLOCK_SECONDS = 60


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        fails = session.get("login_fail", 0)
        blocked_until = session.get("login_blocked_until", 0)
        if fails >= MAX_FAIL and time() < blocked_until:
            flash("Terlalu banyak percobaan. Coba lagi sebentar.", "danger")
            return render_template("login.html")
        pin = request.form.get("pin", "").strip()
        nama = request.form.get("nama", "").strip()
        if not pin or len(pin) > 12:
            flash("Nama atau PIN salah.", "danger")
            return render_template("login.html")
        # Cari user aktif; bila nama diisi, cocokkan nama juga.
        query = Pengguna.query.filter_by(aktif=True)
        candidates = query.all()
        user = None
        for c in candidates:
            if check_password_hash(c.pin_hash, pin):
                nama_input = nama.lower()
                c_nama = c.nama.lower()
                if not nama or c_nama == nama_input or (nama_input in ("barista", "karyawan", "staf") and c_nama in ("barista", "karyawan", "staf")):
                    user = c
                    break
                if user is None:
                    user = c
        if user:
            session.pop("login_fail", None)
            session.pop("login_blocked_until", None)
            session["user_id"] = user.id
            session["peran"] = user.peran
            flash(f"Selamat datang, {user.nama}!", "success")
            return redirect(url_for("dashboard.index"))
        session["login_fail"] = session.get("login_fail", 0) + 1
        if session["login_fail"] >= MAX_FAIL:
            session["login_blocked_until"] = time() + BLOCK_SECONDS
        flash("Nama atau PIN salah.", "danger")
    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("Berhasil keluar.", "info")
    return redirect(url_for("auth.login"))


@bp.route("/pengguna")
@login_required
@pemilik_only
def daftar():
    users = Pengguna.query.order_by(Pengguna.id).all()
    return render_template("pengguna.html", users=users)


@bp.route("/pengguna/tambah", methods=["POST"])
@login_required
@pemilik_only
def tambah():
    nama = request.form.get("nama", "").strip()
    peran = request.form.get("peran", "karyawan")
    pin = request.form.get("pin", "").strip()
    if not nama or not pin or peran not in ("pemilik", "karyawan"):
        flash("Nama, peran, dan PIN wajib diisi.", "danger")
        return redirect(url_for("auth.daftar"))
    if not pin.isdigit() or not 4 <= len(pin) <= 6:
        flash("PIN harus 4–6 digit angka.", "danger")
        return redirect(url_for("auth.daftar"))
    db.session.add(Pengguna(nama=nama, peran=peran, pin_hash=generate_password_hash(pin)))
    db.session.commit()
    flash("Pengguna ditambahkan.", "success")
    return redirect(url_for("auth.daftar"))


@bp.route("/pengguna/<int:user_id>/toggle", methods=["POST"])
@login_required
@pemilik_only
def toggle(user_id):
    u = Pengguna.query.get_or_404(user_id)
    u.aktif = not u.aktif
    db.session.commit()
    flash(f"Pengguna {u.nama} {'diaktifkan' if u.aktif else 'dinonaktifkan'}.", "info")
    return redirect(url_for("auth.daftar"))
