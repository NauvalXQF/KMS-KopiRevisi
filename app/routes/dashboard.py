from flask import Blueprint, render_template
from sqlalchemy import func

from app import db
from app.models import Bahan, Komplain, Pengetahuan, Penjualan, Stok
from app.routes.helpers import login_required

bp = Blueprint("dashboard", __name__)


def _sisa_stok():
    rows = (
        db.session.query(
            Bahan.id, Bahan.nama, Bahan.satuan, Bahan.stok_minimum,
            func.coalesce(func.sum(
                db.case((Stok.tipe == "masuk", Stok.jumlah),
                        (Stok.tipe == "keluar", -Stok.jumlah), else_=0)), 0).label("sisa"),
        ).outerjoin(Stok, Stok.bahan_id == Bahan.id)
        .group_by(Bahan.id, Bahan.nama, Bahan.satuan, Bahan.stok_minimum)
        .all()
    )
    return rows


@bp.route("/")
@login_required
def index():
    menu_laris = (
        db.session.query(Penjualan.nama_menu,
                         func.sum(Penjualan.jumlah).label("total"),
                         func.sum(Penjualan.jumlah * Penjualan.harga_satuan).label("omzet"))
        .group_by(Penjualan.nama_menu).order_by(db.text("total DESC")).limit(5).all()
    )
    jam_ramai = (
        db.session.query(func.hour(Penjualan.waktu).label("jam") if db.engine.dialect.name == "mysql"
                         else func.strftime("%H", Penjualan.waktu).label("jam"),
                         func.sum(Penjualan.jumlah).label("total"))
        .group_by("jam").order_by(db.text("total DESC")).limit(5).all()
    )
    stok_rows = _sisa_stok()
    menipis = [r for r in stok_rows if (r.sisa or 0) <= (r.stok_minimum or 0)]
    antrean = Pengetahuan.query.filter_by(status="menunggu_validasi").count()
    total_pengetahuan = Pengetahuan.query.filter_by(status="terbit").count()
    komplain_baru = Komplain.query.filter_by(status="baru").count()
    return render_template("dashboard.html", menu_laris=menu_laris, jam_ramai=jam_ramai,
                           menipis=menipis, antrean=antrean,
                           total_pengetahuan=total_pengetahuan, komplain_baru=komplain_baru)
