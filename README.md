# Data Penduduk Pesisir Barat Public static API

Unofficial API statis berdasarkan data publik milik pemerintah, dibuat dengan python Flask.

sumber data: https://disdukcapil.pesisirbaratkab.go.id/


### Dokumentasi
#### Endpoints
| HTTP Method | Route | Deskripsi |
|--------|----------------|------------|
| `GET`  | `/2019-semester-1` | data penduduk per-Desa tahun 2019 semester 1|
| `GET`  | `/2019-semester-2` | data penduduk per-Desa tahun 2019 semester 2|
| `GET`  | `/2020-semester-1` | data penduduk per-Desa tahun 2020 semester 1|
| `GET`  | `/2020-semester-2` | data penduduk per-Desa tahun 2020 semester 2|
| `GET`  | `/2021-semester-1` | data penduduk per-Desa tahun 2021 semester 1|

#### Query Parameter
| HTTP Method | Route | Parameter | Deskripsi | Contoh |
|--------|----------|------------|-----|-------|
| `GET`  | `/2019-semester-1?desa=` | `desa`:`string` | tampilkan data berdasarkan nama Desa | `/2019-semester-1?desa=rawas` |

parameter query di atas bisa digunakan untuk semua endpoints.

