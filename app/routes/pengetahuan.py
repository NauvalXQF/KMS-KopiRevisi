from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app import db
from app.models import Kategori, Pengetahuan, PengetahuanVersi
from app.routes.helpers import get_current_user, login_required, notify_pemilik, save_upload

bp = Blueprint("pengetahuan", __name__)


@bp.route("/pengetahuan")
@login_required
def daftar():
    q = request.args.get("q", "").strip()
    kat_id = request.args.get("kategori", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 12
    query = Pengetahuan.query
    # Karyawan hanya lihat yang terbit + miliknya sendiri; pemilik lihat semua.
    user = get_current_user()
    if user.peran != "pemilik":
        query = query.filter(
            (Pengetahuan.status == "terbit") | (Pengetahuan.penulis_id == user.id)
        )
    if kat_id.isdigit():
        query = query.filter(Pengetahuan.kategori_id == int(kat_id))
    if q:
        like = f"%{q}%"
        query = query.filter(
            (Pengetahuan.judul.like(like)) | (Pengetahuan.deskripsi.like(like))
        )
    items = query.order_by(Pengetahuan.updated_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    kategoris = Kategori.query.order_by(Kategori.nama).all()
    return render_template("pengetahuan_list.html", items=items.items, pagination=items, kategoris=kategoris, q=q, kat_id=kat_id)


@bp.route("/pengetahuan/<int:pid>")
@login_required
def detail(pid):
    p = Pengetahuan.query.get_or_404(pid)
    user = get_current_user()
    if user.peran != "pemilik" and p.status != "terbit" and p.penulis_id != user.id:
        flash("Kamu tidak punya akses ke pengetahuan ini.", "danger")
        return redirect(url_for("pengetahuan.daftar"))
    riwayat = PengetahuanVersi.query.filter_by(pengetahuan_id=p.id).order_by(PengetahuanVersi.versi.desc()).all()
    return render_template("pengetahuan_detail.html", p=p, riwayat=riwayat)


@bp.route("/pengetahuan/baru", methods=["GET", "POST"])
@login_required
def baru():
    kategoris = Kategori.query.order_by(Kategori.nama).all()
    if request.method == "POST":
        judul = request.form.get("judul", "").strip()
        kategori_id = request.form.get("kategori_id") or None
        deskripsi = request.form.get("deskripsi", "").strip()
        if not judul or not deskripsi:
            flash("Judul dan deskripsi wajib diisi.", "danger")
            return render_template("pengetahuan_form.html", kategoris=kategoris)
        lampiran = save_upload(request.files.get("lampiran"))
        user = get_current_user()
        p = Pengetahuan(judul=judul, kategori_id=kategori_id, deskripsi=deskripsi,
                        lampiran=lampiran, status="menunggu_validasi", versi=1,
                        penulis_id=user.id)
        db.session.add(p)
        db.session.commit()
        db.session.add(PengetahuanVersi(pengetahuan_id=p.id, versi=1, judul=judul,
                                        deskripsi=deskripsi, diubah_oleh=user.id))
        db.session.commit()
        notify_pemilik("Pengetahuan baru menunggu validasi",
                       f"'{judul}' oleh {user.nama}.",
                       terkait_tipe="pengetahuan", terkait_id=p.id)
        flash("Pengetahuan dikirim, menunggu validasi pemilik.", "success")
        return redirect(url_for("pengetahuan.detail", pid=p.id))
    return render_template("pengetahuan_form.html", kategoris=kategoris)


@bp.route("/pengetahuan/<int:pid>/edit", methods=["GET", "POST"])
@login_required
def edit(pid):
    p = Pengetahuan.query.get_or_404(pid)
    user = get_current_user()
    if user.peran != "pemilik" and p.penulis_id != user.id:
        flash("Hanya penulis atau pemilik yang boleh mengubah.", "danger")
        return redirect(url_for("pengetahuan.detail", pid=pid))
    kategoris = Kategori.query.order_by(Kategori.nama).all()
    if request.method == "POST":
        p.judul = request.form.get("judul", "").strip() or p.judul
        p.deskripsi = request.form.get("deskripsi", "").strip() or p.deskripsi
        if request.form.get("kategori_id"):
            p.kategori_id = int(request.form["kategori_id"])
        f = save_upload(request.files.get("lampiran"))
        if f:
            p.lampiran = f
        p.versi += 1
        # Edit oleh karyawan mengembalikan ke antrean validasi.
        if user.peran != "pemilik":
            p.status = "menunggu_validasi"
            notify_pemilik("Revisi pengetahuan menunggu validasi",
                           f"'{p.judul}' direvisi oleh {user.nama}.",
                           terkait_tipe="pengetahuan", terkait_id=p.id)
        db.session.add(PengetahuanVersi(pengetahuan_id=p.id, versi=p.versi,
                                        judul=p.judul, deskripsi=p.deskripsi,
                                        diubah_oleh=user.id))
        db.session.commit()
        flash(f"Disimpan sebagai versi {p.versi}.", "success")
        return redirect(url_for("pengetahuan.detail", pid=pid))
    return render_template("pengetahuan_form.html", kategoris=kategoris, p=p)


@bp.route("/pengetahuan/<int:pid>/hapus", methods=["POST"])
@login_required
def hapus(pid):
    p = Pengetahuan.query.get_or_404(pid)
    user = get_current_user()
    if user.peran != "pemilik" and p.penulis_id != user.id:
        flash("Tidak boleh menghapus.", "danger")
        return redirect(url_for("pengetahuan.detail", pid=pid))
    PengetahuanVersi.query.filter_by(pengetahuan_id=p.id).delete()
    db.session.delete(p)
    db.session.commit()
    flash("Pengetahuan dihapus.", "info")
    return redirect(url_for("pengetahuan.daftar"))
