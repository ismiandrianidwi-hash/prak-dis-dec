from sqlmodel import Field, Session, SQLModel, create_engine

class Produk(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    kode: str
    nama: str
    stok: int
    harga: float
    tersedia: bool

engine = create_engine("sqlite:///inventaris.db")

def isi_data():
    daftar_produk = [
        Produk(kode="PRD001", nama="Laptop Kerja", stok=15, harga=12500000.0, tersedia=True),
        Produk(kode="PRD002", nama="Mouse Wireless", stok=50, harga=175000.5, tersedia=True),
        Produk(kode="PRD003", nama="Keyboard Mechanical", stok=20, harga=650000.0, tersedia=True),
        Produk(kode="PRD004", nama="Monitor 24 Inch", stok=0, harga=1850000.0, tersedia=False),
        Produk(kode="PRD005", nama="Webcam HD", stok=12, harga=425000.75, tersedia=True),
    ]

    with Session(engine) as session:
        for item in daftar_produk:
            session.add(item)
        session.commit()
    print("Berhasil memasukkan 5 data produk!")

if __name__ == "__main__":
    isi_data()