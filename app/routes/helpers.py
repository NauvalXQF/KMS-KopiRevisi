"""Helper auth, upload, notifikasi."""
import os
import uuid
from functools import wraps

from flask import current_app, flash, redirect, session, url_for
from werkzeug.utils import secure_filename

from app import db
from app.models import Notifikasi, Pengguna

ALLOWED_EXT = {"png", "jpg", "jpeg", "gif", "mp4", "mov", "pdf"}


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Silakan login dulu.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper


def pemilik_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            return redirect(url_for("auth.login"))
        if user.peran != "pemilik":
            flash("Hanya pemilik yang boleh mengakses halaman itu.", "danger")
            return redirect(url_for("dashboard.index"))
        return f(*args, **kwargs)
    return wrapper


def get_current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return Pengguna.query.get(uid)


def kirim_notifikasi(pengguna_id, judul, pesan="", terkait_tipe=None, terkait_id=None):
    n = Notifikasi(pengguna_id=pengguna_id, judul=judul, pesan=pesan,
                   terkait_tipe=terkait_tipe, terkait_id=terkait_id)
    db.session.add(n)
    db.session.commit()


def notify_pemilik(judul, pesan="", terkait_tipe=None, terkait_id=None):
    for p in Pengguna.query.filter_by(peran="pemilik", aktif=True).all():
        kirim_notifikasi(p.id, judul, pesan, terkait_tipe, terkait_id)


def save_upload(file_storage):
    if not file_storage or not file_storage.filename:
        return None
    ext = file_storage.filename.rsplit(".", 1)[-1].lower() if "." in file_storage.filename else ""
    if ext not in ALLOWED_EXT:
        return None
    fname = f"{uuid.uuid4().hex}_{secure_filename(file_storage.filename)}"
    dest = os.path.join(current_app.config["UPLOAD_FOLDER"], fname)
    file_storage.save(dest)
    return f"uploads/{fname}"
