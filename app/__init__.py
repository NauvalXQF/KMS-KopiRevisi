"""Flask app factory untuk KMS Kopi Revisi."""
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

BASE_DIR = Path(__file__).resolve().parent.parent


def _build_db_uri() -> str:
    load_dotenv(BASE_DIR / ".env")
    driver = os.getenv("DB_DRIVER", "auto").lower()
    sqlite_uri = f"sqlite:///{BASE_DIR / 'kms_kopi.db'}"

    if driver == "sqlite":
        print("[Kopi Revisi] Menggunakan database: SQLite (kms_kopi.db)")
        return sqlite_uri

    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    name = os.getenv("DB_NAME", "kms_kopi")
    mysql_uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset=utf8mb4"

    if driver == "mysql":
        print(f"[Kopi Revisi] Menggunakan database: MySQL ({host}:{port}/{name})")
        return mysql_uri

    # Driver 'auto': coba cek apakah MySQL sedang aktif
    import socket
    try:
        sock = socket.create_connection((host, port), timeout=0.5)
        sock.close()
        print(f"[Kopi Revisi] MySQL terdeteksi aktif pada {host}:{port}. Menggunakan MySQL.")
        return mysql_uri
    except OSError:
        print("[Kopi Revisi] Layanan MySQL tidak aktif. Otomatis beralih ke SQLite (kms_kopi.db) agar aplikasi tetap berjalan lancar.")
        return sqlite_uri


def create_app():
    app = Flask(__name__)
    load_dotenv(BASE_DIR / ".env")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-kms-kopi-revisi-2026")
    app.config["SQLALCHEMY_DATABASE_URI"] = _build_db_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = str(BASE_DIR / "app" / "static" / "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)

    # Import models agar terdaftar di SQLAlchemy
    from app import models  # noqa: F401

    # Blueprint routes
    from app.routes.auth import bp as auth_bp
    from app.routes.dashboard import bp as dashboard_bp
    from app.routes.komplain import bp as komplain_bp
    from app.routes.notifikasi import bp as notifikasi_bp
    from app.routes.pengetahuan import bp as pengetahuan_bp
    from app.routes.penjualan import bp as penjualan_bp
    from app.routes.stok import bp as stok_bp
    from app.routes.supplier import bp as supplier_bp
    from app.routes.validasi import bp as validasi_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(pengetahuan_bp)
    app.register_blueprint(validasi_bp)
    app.register_blueprint(stok_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(penjualan_bp)
    app.register_blueprint(komplain_bp)
    app.register_blueprint(notifikasi_bp)

    # Context processor: user login + jumlah notifikasi belum dibaca
    @app.context_processor
    def inject_user():
        from flask import session
        from app.models import Notifikasi, Pengguna

        user = None
        unread = 0
        if session.get("user_id"):
            user = Pengguna.query.get(session["user_id"])
            if user:
                unread = Notifikasi.query.filter_by(
                    pengguna_id=user.id, dibaca=False
                ).count()
        return {"current_user": user, "unread_count": unread}

    return app
