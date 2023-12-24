from psycopg2 import connect,extensions
from prettytable import PrettyTable
from prettytable import from_db_cursor
auto_commit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
dbismi = "muzikprogrami"
def createDB():
        conn = connect(host = "localhost",
                        user = "postgres",
                        password = "1411", 
                        port = 5432)
        conn.set_isolation_level(auto_commit)
        cur = conn.cursor()
        create_db = f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbismi}'"
        cur.execute(create_db)
        exists = cur.fetchone()
        if not exists:
            cur.execute(f'CREATE DATABASE {dbismi}')
            conn.close
            conn = connect(host = "localhost",
                      user = "postgres",
                      password = "1411", 
                      port = 5432,
                      database = dbismi)
            conn.set_isolation_level(auto_commit)
            cur = conn.cursor() 
            """/* TABLOLAR */"""
            cur.execute("""CREATE TABLE IF NOT EXISTS sanatci (           
                        sanatciID SERIAL PRIMARY KEY,
                        sanatciAdi VARCHAR(255) NOT NULL,
                        ulke VARCHAR(255),
                        bio TEXT
                        );              
                        """)
            cur.execute("""CREATE TABLE IF NOT EXISTS konser(
                        konserID SERIAL PRIMARY KEY,
                        sanatciID INTEGER,
                        CONSTRAINT sanatciID FOREIGN KEY(sanatciID)
                        REFERENCES sanatci(sanatciID)ON DELETE CASCADE,
                        mekan TEXT,
                        tarih DATE,
                        biletSayisi INTEGER
                        );""")
            cur.execute("""CREATE TABLE IF NOT EXISTS podcast(
                        podcastID SERIAL PRIMARY KEY,
                        sanatciID INTEGER,
                        CONSTRAINT sanatciID FOREIGN KEY(sanatciID)
                        REFERENCES sanatci(sanatciID)ON DELETE CASCADE,
                        baslik VARCHAR(30) NOT NULL
                        );""")
            cur.execute("""CREATE TABLE IF NOT EXISTS tur(
                        turID SERIAL PRIMARY KEY,
                        turAdi VARCHAR(30) NOT NULL
                        );""")
            cur.execute("""CREATE TABLE IF NOT EXISTS album(
                        albumID SERIAL PRIMARY KEY,
                        sanatciID INTEGER,
                        CONSTRAINT sanatciID FOREIGN KEY(sanatciID)
                        REFERENCES sanatci(sanatciID)ON DELETE CASCADE,
                        turID INTEGER,
                        CONSTRAINT turID FOREIGN KEY(turID)
                        REFERENCES tur(turID),
                        yayinTarih DATE,
                        albumAdi VARCHAR(55) NOT NULL
                        );""")
            cur.execute("""CREATE TABLE IF NOT EXISTS sarki(
                        sarkiID SERIAL PRIMARY KEY,
                        albumID INTEGER,
                        CONSTRAINT albumID FOREIGN KEY(albumID)
                        REFERENCES album(albumID)ON DELETE CASCADE,
                        sarkiAdi VARCHAR(50) NOT NULL,
                        sure FLOAT 
                        );""")
            cur.execute("""CREATE TABLE IF NOT EXISTS muzik_video(
                        videoID SERIAL PRIMARY KEY,
                        sarkiID INTEGER,
                        CONSTRAINT sarkiID FOREIGN KEY(sarkiID)
                        REFERENCES sarki(sarkiID)ON DELETE CASCADE,
                        yonetmen VARCHAR(50) NOT NULL,
                        cekimTarihi DATE,
                        link TEXT NOT NULL
                        );""")
            cur.execute("""CREATE TABLE IF NOT EXISTS katkida_bulunan(
                        yazarID SERIAL PRIMARY KEY,
                        albumID INTEGER,
                        CONSTRAINT albumID FOREIGN KEY(albumID)
                        REFERENCES album(albumID)ON DELETE CASCADE,
                        ad VARCHAR(50) NOT NULL,
                        katkiTuru TEXT
                        );""")
            cur.execute("""CREATE TABLE IF NOT EXISTS soz_yazari( 
	                    yazarID INTEGER PRIMARY KEY,
	                    sarkiSozu TEXT NOT NULL,
                        sarkiAdi TEXT,
                        CONSTRAINT yazarID FOREIGN KEY(yazarID)
	                    REFERENCES katkida_bulunan(yazarID)
	                    ON DELETE CASCADE
	                    ON UPDATE CASCADE
                        );""")
            cur.execute("""CREATE TABLE IF NOT EXISTS ensturman( 
	                    yazarID INTEGER PRIMARY KEY,
	                    ensturmanAdi VARCHAR(255),
                        CONSTRAINT yazarID FOREIGN KEY (yazarID)
	                  REFERENCES ensturman(yazarID)
	                  ON DELETE CASCADE
	                  ON UPDATE CASCADE
                  );""")

            cur.execute("""CREATE TABLE IF NOT EXISTS produktor( 
	                    yazarID INTEGER PRIMARY KEY,
	                    calistigiSirket VARCHAR(50) NOT NULL,
                        CONSTRAINT yazarID FOREIGN KEY (yazarID)
	                    REFERENCES produktor(yazarID)
	                    ON DELETE CASCADE
	                    ON UPDATE CASCADE
                    );""")
            cur.execute("""CREATE TABLE IF NOT EXISTS kullanici( 
	                    kullaniciID SERIAL PRIMARY KEY,
	                    kullaniciAdi VARCHAR(50) NOT NULL,
                        sifre VARCHAR(50) NOT NULL ,
                        mail VARCHAR(200) NOT NULL,
                        uyelikTarihi DATE DEFAULT '2000-01-01',
                        hesapturu VARCHAR(1)
                    );""")
            cur.execute("""CREATE TABLE IF NOT EXISTS premium( 
	                    kullaniciID INTEGER PRIMARY KEY,
	                    fiyat INTEGER,
                        CONSTRAINT listeID FOREIGN KEY(kullaniciID)
	                    REFERENCES kullanici(kullaniciID)
	                    ON DELETE CASCADE
	                    ON UPDATE CASCADE
                    );""")
            cur.execute("""CREATE TABLE IF NOT EXISTS standart( 
	                        kullaniciID INTEGER PRIMARY KEY,
	                        gecilenReklam INTEGER,
                            CONSTRAINT listeID FOREIGN KEY(kullaniciID)
	                        REFERENCES kullanici(kullaniciID)
	                        ON DELETE CASCADE
	                        ON UPDATE CASCADE
                        );""")
            cur.execute("""CREATE TABLE IF NOT EXISTS calma_listesi(
                            listeID SERIAL PRIMARY KEY,
                            kullaniciID INTEGER,
                            CONSTRAINT kullaniciID FOREIGN KEY(kullaniciID)
                            REFERENCES kullanici(kullaniciID)ON DELETE CASCADE,
                            calmalistesiAdi VARCHAR(30) NOT NULL
                            );""")

            cur.execute("""CREATE TABLE IF NOT EXISTS degerlendirme(
                            degerlendirmeID SERIAL PRIMARY KEY,
                            sarkiID INTEGER,
                            kullaniciID INTEGER,
                            tarih DATE,
                            degerlendirmeTuru TEXT,
                            CONSTRAINT sarkiID FOREIGN KEY(sarkiID)
                            REFERENCES sarki(sarkiID) ON DELETE CASCADE,
                            CONSTRAINT kullaniciID FOREIGN KEY(kullaniciID)
                            REFERENCES kullanici(kullaniciID)ON DELETE CASCADE
                        );""")
            cur.execute("""CREATE TABLE IF NOT EXISTS oy( 
	                        degerlendirmeID INTEGER PRIMARY KEY,
                            oySayisi INTEGER,
                            CONSTRAINT degerlendirmeID FOREIGN KEY(degerlendirmeID)
	                        REFERENCES degerlendirme(degerlendirmeID)
	                        ON DELETE CASCADE
	                        ON UPDATE CASCADE
                        );""")
            cur.execute("""CREATE TABLE IF NOT EXISTS inceleme( 
	                        degerlendirmeID INTEGER PRIMARY KEY,
                            incelemeMetni TEXT,
                            CONSTRAINT degerlendirmeID FOREIGN KEY(degerlendirmeID)
	                        REFERENCES degerlendirme(degerlendirmeID)
	                        ON DELETE CASCADE
	                    ON UPDATE CASCADE
                    );""")
            """/* FONKSİYONLAR- PROSEDURLER */"""
            cur.execute("""CREATE OR REPLACE FUNCTION album_ara(aranan_kelime VARCHAR(255))
            RETURNS TABLE(album_adi VARCHAR)AS $$
BEGIN
    RETURN QUERY SELECT albumAdi
                 FROM album WHERE lower(albumAdi) LIKE '%' || lower(aranan_kelime) || '%';
END;
$$ LANGUAGE plpgsql;
""")

            cur.execute("""CREATE OR REPLACE FUNCTION premium_kullanici_ekle(
                        kullaniciAdi VARCHAR(255),
                        sifre VARCHAR(255),
                        mail VARCHAR(255),
                        uyelikTarihi DATE,
                        fiyat INT
                        )RETURNS VOID AS $$
                        DECLARE 
                            kullanici_id INTEGER;
                        BEGIN
                            INSERT INTO kullanici(kullaniciAdi,sifre,mail,uyelikTarihi,hesapturu) VALUES
                        (kullaniciAdi,sifre,mail,uyelikTarihi,'p')RETURNING "kullaniciid" INTO kullanici_id;
                            INSERT INTO premium(kullaniciid,fiyat) VALUES (kullanici_id,fiyat);
                        END;
                        $$ LANGUAGE plpgsql;
                        """)
            cur.execute("""CREATE OR REPLACE FUNCTION standart_kullanici_ekle(
                        kullaniciAdi VARCHAR(50),
                        sifre VARCHAR(50),
                        mail VARCHAR(200),
                        uyelikTarihi DATE,
                        gecilenReklam INT
                        )RETURNS VOID AS $$
                        DECLARE 
                            kullanici_id INTEGER;
                        BEGIN
                            INSERT INTO kullanici(kullaniciAdi,sifre,mail,uyelikTarihi,hesapturu) VALUES
                        (kullaniciAdi,sifre,mail,uyelikTarihi,'s')RETURNING "kullaniciid" INTO kullanici_id;
                            INSERT INTO standart(kullaniciid,gecilenReklam) VALUES (kullanici_id,gecilenReklam);
                        END;
                        $$ LANGUAGE plpgsql;
                        """)

            cur.execute("""CREATE OR REPLACE FUNCTION oy_ile_degerlendirme(
                        sarkiID INTEGER,
                        kullaniciID INTEGER,
                        tarih DATE,
                        oySayisi INT
                        )RETURNS VOID AS $$
                        DECLARE 
                            degerlendirme_id INTEGER;
                        BEGIN
                            INSERT INTO degerlendirme(sarkiID,kullaniciID,tarih,degerlendirmeTuru) VALUES
                        (sarkiID,kullaniciID,tarih,'oy')RETURNING "degerlendirmeid" INTO degerlendirme_id;
                            INSERT INTO oy(degerlendirmeid,oySayisi) VALUES (degerlendirme_id,oySayisi);
                        END;
                        $$ LANGUAGE plpgsql;
                        """)
            cur.execute("""CREATE OR REPLACE FUNCTION inceleme_ile_degerlendirme(
                        sarkiID INTEGER,
                        kullaniciID INTEGER,
                        tarih DATE,
                        incelemeMetni TEXT
                        )RETURNS VOID AS $$
                        DECLARE 
                            degerlendirme_id INTEGER;
                        BEGIN
                            INSERT INTO degerlendirme(sarkiID,kullaniciID,tarih,degerlendirmeTuru) VALUES
                        (sarkiID,kullaniciID,tarih,'inceleme')RETURNING "degerlendirmeid" INTO degerlendirme_id;
                            INSERT INTO inceleme(degerlendirmeid,incelemeMetni) VALUES (degerlendirme_id,incelemeMetni);
                        END;
                        $$ LANGUAGE plpgsql;
                        """)
            cur.execute("""CREATE OR REPLACE FUNCTION degerlendirme_goruntule(degerlendirme_id INTEGER)
RETURNS TEXT AS $$
DECLARE
    deger TEXT;
BEGIN
    SELECT INTO deger CASE
        WHEN d.degerlendirmeTuru = 'oy' THEN
            (SELECT o.oySayisi::TEXT FROM oy o WHERE o.degerlendirmeid = degerlendirme_id)
        WHEN d.degerlendirmeTuru = 'inceleme' THEN
            (SELECT i.incelemeMetni FROM inceleme i WHERE i.degerlendirmeid = degerlendirme_id)
    END
    FROM degerlendirme d WHERE d.degerlendirmeid = degerlendirme_id;

    RETURN deger;
END;
$$ LANGUAGE plpgsql;

""")
            cur.execute("""CREATE OR REPLACE FUNCTION kullanici_goruntule(kullanici_id INTEGER)
RETURNS TEXT AS $$
DECLARE
    deger TEXT;
BEGIN
    SELECT INTO deger CASE
        WHEN k.hesapTuru = 'p' THEN
            (SELECT p.fiyat FROM premium p WHERE p.kullaniciid = kullanici_id)
        WHEN k.hesapTuru = 's' THEN
            (SELECT s.gecilenReklam as GecilenReklam FROM standart s WHERE s.kullaniciid= kullanici_id)
    END
    FROM kullanici k WHERE k.kullaniciid = kullanici_id;

    RETURN deger;
END;
$$ LANGUAGE plpgsql;

""")
            
            

            cur.execute("""CREATE OR REPLACE FUNCTION katkida_bulunan_ekle_soz(
                        albumid INTEGER,
                        ad VARCHAR,
                        sarkiSozu TEXT,
                        sarkiAdi TEXT
                        )RETURNS VOID AS $$
                        DECLARE 
                            yazar_id INTEGER;
                        BEGIN
                            INSERT INTO katkida_bulunan(albumid,ad,katkiTuru) VALUES
                        (albumid,ad,'Söz Yazarı')RETURNING "yazarid" INTO yazar_id;
                            INSERT INTO soz_yazari(yazarid,sarkiAdi,sarkiSozu) VALUES (yazar_id,sarkiAdi,sarkiSozu);
                        END;
                        $$ LANGUAGE plpgsql;
                        """)
            cur.execute("""CREATE OR REPLACE FUNCTION katkida_bulunan_ekle_produktor(
                        albumid INTEGER,
                        ad VARCHAR,
                        calistigiSirket TEXT
                        )RETURNS VOID AS $$
                        DECLARE 
                            yazar_id INTEGER;
                        BEGIN
                            INSERT INTO katkida_bulunan(albumid,ad,katkiTuru) VALUES
                        (albumid,ad,'Prodüktör')RETURNING "yazarid" INTO yazar_id;
                            INSERT INTO produktor(yazarid,calistigiSirket) VALUES (yazar_id,calistigiSirket);
                        END;
                        $$ LANGUAGE plpgsql;
                        """)
            cur.execute("""CREATE OR REPLACE FUNCTION katkida_bulunan_ekle_ensturman(
                        albumid INTEGER,
                        ad VARCHAR,
                        ensturmanAdi TEXT
                        )RETURNS VOID AS $$
                        DECLARE 
                            yazar_id INTEGER;
                        BEGIN
                            INSERT INTO katkida_bulunan(albumid,ad,katkiTuru) VALUES
                        (albumid,ad,'Enstürman')RETURNING "yazarid" INTO yazar_id;
                            INSERT INTO ensturman(yazarid,ensturmanAdi) VALUES (yazar_id,ensturmanAdi);
                        END;
                        $$ LANGUAGE plpgsql;
                        """)
            cur.execute("""CREATE OR REPLACE PROCEDURE sarki_ekle(albumid int,sarkiAdi VARCHAR(55),sure FLOAT) 
                        LANGUAGE SQL
                        AS $$
                        INSERT INTO sarki(albumid,sarkiAdi,sure) values 
                        (albumid,sarkiAdi,sure);
                        $$;
                    """)
            
            cur.execute("""CREATE OR REPLACE FUNCTION upgrade_to_premium(kullanici_id INTEGER, fiyat INTEGER)
RETURNS VOID AS $$
BEGIN
    DELETE FROM standart WHERE kullaniciID = kullanici_id;
    INSERT INTO premium (kullaniciID, fiyat) VALUES (kullanici_id, fiyat);
    UPDATE kullanici set hesapturu = 'p' where kullaniciid = kullanici_id;
END;
$$ LANGUAGE plpgsql;
 """)
            cur.execute("""CREATE OR REPLACE FUNCTION upgrade_to_standart(kullanici_id INTEGER, gecilenReklam INTEGER)
RETURNS VOID AS $$
BEGIN
    DELETE FROM premium WHERE kullaniciID = kullanici_id;
    INSERT INTO standart (kullaniciID, gecilenReklam) VALUES (kullanici_id, gecilenReklam);
    UPDATE kullanici set hesapturu = 's' where kullaniciid = kullanici_id;
END;
$$ LANGUAGE plpgsql;
 """)
            cur.execute("""CREATE OR REPLACE FUNCTION upgrade_account(kullanici_id INTEGER,detay int) RETURNS VOID AS $$
DECLARE
    hesap_turu CHAR(1);
BEGIN
    SELECT hesapturu INTO hesap_turu
    FROM kullanici
    WHERE kullaniciid = kullanici_id;

    IF hesap_turu = 'p' THEN
        PERFORM upgrade_to_standart(kullanici_id,detay);
    ELSIF hesap_turu = 's' THEN
        PERFORM upgrade_to_premium(kullanici_id,detay);
    END IF;
END;
$$ LANGUAGE plpgsql;
""")


            cur.execute("""CREATE FUNCTION fn_katkida_bulunan_goster (album_id INTEGER)
RETURNS TABLE (
    ad VARCHAR(50),
    katkituru TEXT,
    detay TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT k.ad, k.katkituru, 
    CASE 
        WHEN k.katkituru = 'Söz Yazarı' THEN s.sarkisozu
        WHEN k.katkituru = 'Enstürman' THEN e.ensturmanadi
        WHEN k.katkituru = 'Prodüktör' THEN p.calistigisirket
        ELSE 'Bilinmiyor'
    END AS detay
    FROM katkida_bulunan k
    LEFT JOIN soz_yazari s ON k.yazarid = s.yazarid
    LEFT JOIN ensturman e ON k.yazarid = e.yazarid
    LEFT JOIN produktor p ON k.yazarid = p.yazarid
    WHERE k.albumid = album_id;
END;
$$ LANGUAGE plpgsql;







 """)
            cur.execute("""CREATE OR REPLACE FUNCTION album_sure_hesapla(album_id INTEGER)
RETURNS INTERVAL AS $$
DECLARE
    total_duration INTERVAL := '00:00:00';
    song_duration INTERVAL;
BEGIN
    FOR song_duration IN (SELECT sure FROM sarki WHERE albumid = album_id) LOOP
        total_duration := total_duration + song_duration;
    END LOOP;

    RETURN total_duration;
END;
$$ LANGUAGE plpgsql;
""")
            """TRIGER"""    
            cur.execute(""" 
ALTER TABLE sanatci ADD COLUMN album_sayisi INT;

UPDATE sanatci SET album_sayisi = (SELECT COUNT(*) FROM album WHERE sanatci.sanatciID = album.sanatciID);

CREATE OR REPLACE FUNCTION update_album_sayisi() RETURNS TRIGGER AS $$
BEGIN
  
    UPDATE sanatci SET album_sayisi = (SELECT COUNT(*) FROM album WHERE sanatci.sanatciID = album.sanatciID) WHERE sanatciID = NEW.sanatciID;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER album_after_insert
AFTER INSERT ON album
FOR EACH ROW EXECUTE FUNCTION update_album_sayisi();
""")
            

            cur.execute("""
CREATE OR REPLACE FUNCTION bilet_satis(konser_id INTEGER, satilan_bilet_sayisi INTEGER) RETURNS VOID AS $$
BEGIN
    UPDATE konser
    SET biletSayisi = biletSayisi - satilan_bilet_sayisi
    WHERE konserID = konser_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION bilet_sayisi_azalt() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.biletSayisi < 0 THEN
        RAISE EXCEPTION 'Yetersiz bilet';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER bilet_satildi
AFTER UPDATE OF biletSayisi ON konser
FOR EACH ROW EXECUTE FUNCTION bilet_sayisi_azalt();
""")
            
            cur.execute("""ALTER TABLE album ADD COLUMN sarki_sayisi INT;

UPDATE album SET sarki_sayisi = (SELECT COUNT(*) FROM sarki WHERE album.albumID = sarki.albumID);
""")
            cur.execute("""CREATE OR REPLACE FUNCTION yeni_sarki_eklendi() RETURNS TRIGGER AS $$
BEGIN
    UPDATE album SET sarki_sayisi = (SELECT COUNT(*) FROM sarki WHERE album.albumID = sarki.albumID);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER yeni_sarki_eklendi_trigger
AFTER INSERT ON sarki
FOR EACH ROW EXECUTE FUNCTION yeni_sarki_eklendi();
""")
            cur.execute("""CREATE OR REPLACE FUNCTION konser_tarihi_kontrol()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.tarih < CURRENT_DATE THEN
        RAISE EXCEPTION 'Konser Tarihi ileri bir tarihte olmalı';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER konser_tarihi_kontrol_trigger
BEFORE INSERT ON konser
FOR EACH ROW EXECUTE FUNCTION konser_tarihi_kontrol();
""")
            cur.execute("""CREATE OR REPLACE FUNCTION oy_kontrol()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.oySayisi < 0 OR NEW.oySayisi > 10 THEN
        RAISE EXCEPTION 'Oy sayısı 0 ile 10 arasında olmalıdır';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER oy_kontrol_trigger
BEFORE INSERT OR UPDATE ON oy
FOR EACH ROW EXECUTE FUNCTION oy_kontrol();
""")
            
            
        

            """VERİ EKLEME"""
        
            cur.execute("""
                    INSERT INTO sanatci(sanatciAdi,ulke,bio) values 
                    ('Tarkan', 'Türkiye', 'Tarkan Tevetoglu, Türk şarkıcı, söz yazarı ve prodüktördür.'),
                    ('Sezen Aksu', 'Türkiye', 'Fatma Sezen Yıldırım, Türk şarkıcı ve söz yazarıdır.'),
                    ('George Michael', 'İngiltere', 'Georgios Kyriacos Panayiotou, İngiliz şarkıcı, söz yazarı ve yapımcıdır.'),
                    ('Amy Winehouse','İngiltere', 'Amy Jade Winehouse, İngiliz şarkıcı ve söz yazarıdır.'),
                    ('Elton John', 'İngiltere', 'Reginald Kenneth Dwight, İngiliz şarkıcı, söz yazarı ve piyanisttir.'),
                    ('Janis Joplin', 'ABD', 'Janis Lyn Joplin, Amerikalı şarkıcı ve söz yazarıdır.'),
                    ('Frank Ocean', 'ABD', 'Christopher Edwin Breaux, Amerikalı şarkıcı, söz yazarı ve yapımcıdır.'),
                    ('Haluk Levent', 'Türkiye', 'Haluk Levent, Türk rock müzik şarkıcısı ve söz yazarıdır.'),
                    ('Zeki Müren', 'Türkiye', 'Zeki Müren, Türk sanat müziği sanatçısıdır.'),
                    ('Fikret Kızılok', 'Türkiye', 'Fikret Kızılok, Türk rock müziği sanatçısı ve müzik öğretmenidir.'),
                    ('Barış Manço', 'Türkiye', 'Barış Manço, Türk rock müzik sanatçısı, şarkıcı, besteci, yazar ve televizyon programcısıdır.'),
                    ('Emre Aydın',  'Türkiye', 'Emre Aydın, Türk rock müzik şarkıcısı ve söz yazarıdır.'),
                    ('Kenan Doğulu',  'Türkiye', 'Kenan Doğulu, Türk pop müziği sanatçısıdır.'),
                    ('Sertab Erener', 'Türkiye', 'Sertab Erener, Türk pop müziği sanatçısı ve söz yazarıdır.'),
                    ('Cem Karaca', 'Türkiye', 'Cem Karaca, Türk rock müziği sanatçısı ve siyasi aktivisttir.'),
                    ('Prince',  'ABD', 'Prince Rogers Nelson, Amerikalı müzisyen, şarkıcı, söz yazarı ve aktördür.'),
                    ('Severe Torture', 'Hollanda', 'Severe Torture, Hollandalı bir death metal grubudur.'),
                    ('Ludwig van Beethoven', 'Almanya', 'Ludwig van Beethoven, ünlü bir Alman besteci ve piyanisttir.'),
                    ( 'Miles Davis', 'ABD', 'Miles Davis, Amerikalı bir caz trompetçisi, besteci ve bandleaderdır.'),
                    ( 'John Coltrane', 'ABD', 'John Coltrane, Amerikalı bir caz saksofonisti ve bestecisidir.'),
                    ( 'Beyoncé', 'ABD', 'Beyoncé, Amerikalı R&B şarkıcısı, söz yazarı ve oyuncusudur.'),
                    ( 'Usher', 'ABD', 'Usher, Amerikalı R&B şarkıcısı, dansçı ve aktördür.'),
                    ( 'Alicia Keys', 'ABD', 'Alicia Keys, Amerikalı R&B şarkıcısı, söz yazarı ve yapımcısıdır.'),
                    ( 'Kendrick Lamar', 'ABD', 'Kendrick Lamar, Amerikalı bir hip hop sanatçısı ve söz yazarıdır.'),
                    ( 'Nicki Minaj', 'ABD', 'Nicki Minaj, Trinidad doğumlu Amerikalı bir rapçi, şarkıcı ve söz yazarıdır.'),
                    ( 'J. Cole', 'ABD', 'J. Cole, Amerikalı bir rapçi, söz yazarı ve yapımcıdır.'),
                    ( 'Drake', 'Kanada', 'Drake, Kanadalı bir rapçi, şarkıcı ve söz yazarıdır.'),
                    ( 'Cardi B', 'ABD', 'Cardi B, Amerikalı bir rapçi, şarkıcı ve televizyon kişiliğidir.'),
                    ( 'Eminem', 'ABD', 'Eminem, Amerikalı rapçi, şarkıcı, söz yazarı ve yapımcıdır.'),
                    ( 'Sagopa K', 'Türkiye', 'Sagopa K, Türk rap müziği sanatçısı ve söz yazarıdır.'),
                    ( 'Nas', 'ABD', 'Nas, Amerikalı rapçi ve söz yazarıdır.'),
                    ( 'Kanye West', 'ABD', 'Kanye West, Amerikalı rapçi, yapımcı ve modacıdır.')
                    ; 
                    """)     
            cur.execute("""
                    INSERT INTO tur(turAdi) values
                    ('Pop'),
                    ('Jazz'),
                    ('Rock'),
                    ('R&B'),
                    ('Sanat müziği'),
                    ('Blues'),
                    ('Hip Hop'),
                    ('Klasik'),
                    ('Rap'),
                    ('Metal');
                    """)
            cur.execute("""
                    INSERT INTO album(sanatciid,turid,yayinTarih,albumAdi) values
(1, 1, '1997-12-05', 'Ölürüm Sana'),
(2, 1, '2001-01-01', 'Düş Bahçeleri'),
(3, 1, '1996-05-13', 'Older'),
(4, 1, '2003-10-20', 'Frank'),
(5, 1, '1983-04-30', 'Too Low for Zero'),
(6, 3, '1968-08-12', 'Big Brother and the Holding Company'),
(7, 1, '2012-07-10', 'Channel Orange'),
(7, 6, '2011-02-18', 'Nostalgia, Ultra'),
(8, 3, '1993-01-01', 'Bu Ateş Sönmez'),
( 9, 5, '1989-01-01', 'Sev Beni'),
( 10, 3, '1985-01-01', 'Yana yana'),
( 11, 3, '1969-01-01', 'Mançoloji V1'),
( 12, 3, '2013-01-01', 'Afili Yalnızlık'),
( 13, 1, '1993-10-25', 'Yaparım Bilirsin'),
( 18, 8, '1803-04-05', 'Symphony No. 3 in E-flat major, Op. 55 "Eroica"'),
( 14, 1, '2003-05-06', 'Turuncu'),
( 15, 3, '1987-01-01', 'Nerde Kalmıştık'),
( 16, 1, '1979-04-07', 'Prince'),
( 17, 10, '2000-01-01', 'Feasting on Blood'),
( 19, 2, '1957-12-04', 'Round About Midnight'),
( 20, 2, '1957-11-26', 'Blue Train'),
( 21, 4, '2008-11-14', 'I Am... Sasha Fierce'),
( 21, 4, '2013-12-13', 'Beyoncé'),
( 22, 4, '1994-08-30', 'Usher'),
( 23, 4, '2003-12-02', 'The Diary of Alicia Keys'),
( 24, 7, '2012-10-22', 'good kid, m.A.A.d city'),
( 25, 7, '2010-11-22', 'Pink Friday'),
( 26, 7, '2018-04-20', 'KOD'),
( 27, 7, '2013-09-24', 'Nothing Was the Same'),
( 28, 7, '2018-04-06', 'Invasion of Privacy'),
( 29, 9, '2002-05-26', 'The Eminem Show'),
( 30, 9, '2000-10-27', 'Bir Pesimistin Gözyaşları'),
( 31, 9, '2001-04-17', 'Stillmatic')

                    ;                                                                                       
                    """)
            cur.execute(""" 
                    CALL sarki_ekle( 1, 'İnci Tanem', 5.28);
                    CALL sarki_ekle(1, 'Unut Beni', 3.43);
                    CALL sarki_ekle(2,'Kaçın Kurası',3.45);
                    CALL sarki_ekle(2,'Zalim',3.48);
                    CALL sarki_ekle(3,'Move on',4.45);
                    CALL sarki_ekle(4,'Know you know',3.03);
                    CALL sarki_ekle(4,'Take the box',3.20);
                    CALL sarki_ekle(5,'Kiss the bride',4.22);
                    CALL sarki_ekle(5,'Dreamboat',3.13);
                    CALL sarki_ekle(6,'Call on me',4.24);
                    CALL sarki_ekle(7,'Sierra Leone',5.13);
                    CALL sarki_ekle(8,'Swim good',4.17);
                    CALL sarki_ekle(9,'Ankara',4.51);
                    CALL sarki_ekle(9,' Bu Ateş Sönmez',4.02);
                    CALL sarki_ekle(10,' Seni nasıl sevdim',3.16);
                    CALL sarki_ekle(10,' Akşam olur gizli gizli',4.56);
                    CALL sarki_ekle(11,'Bir Harmanım Bu akşam',2.32);
                    CALL sarki_ekle(12,'Gül Pembe',2.36);
                    CALL sarki_ekle(12,'Unutamadım',4.01);
                    CALL sarki_ekle(13,'Afili Yalnızlık',5.01);
                    CALL sarki_ekle(13,'Dayan Yalnızlığım',3.45);
                    CALL sarki_ekle(14,'Yaparım Bilirsin',3.45);
                    CALL sarki_ekle(15,'Symphony No. 3 in E-flat major, Op. 55 "Eroica"',14.12);
                    CALL sarki_ekle(16,'Söz bitti',2.12);
                    CALL sarki_ekle(16,'Başa Döneceksin',3.51);
                    CALL sarki_ekle(17,'Sen de Başını Alıp Gitme',4.36);
                    CALL sarki_ekle(17,'Herkes Gibisin',4.01);
                    CALL sarki_ekle(18,'Purple Rain',6.13);
                    CALL sarki_ekle(19,'Twist the cross',2.59);
                    CALL sarki_ekle(19,'Feces for Jesus',4.04);
                    CALL sarki_ekle(20,'All of You',3.16);
                    CALL sarki_ekle(32,'Maskeli Balo',4.12);
                               """)    
            cur.execute(""" INSERT INTO muzik_video(sarkiid,yonetmen,cekimTarihi,link) values 
                        (8,'UNKNOW','2002-03-08','https://youtu.be/7JJH5GZPJNw?si=2-gtQbsVOBnANaRZ'),
                        (5,'UNKNOW','2001-02-01','https://youtu.be/oCXfMJnGWaA?si=aJb72dj9BCXp3hRf'),
                        (6,'UNKNOW','1980-04-02','https://youtu.be/TvnYmWpD_T8?si=IJHJJv_gGe9rLUAo')
                        ;""")
            cur.execute("""INSERT INTO konser(sanatciid,mekan,tarih,biletSayisi) values
                        (12,'İstanbul','2024-01-05',589),
                        (30,'Ankara','2024-04-10',432),
                        (17,'İstanbul','2024-01-05',235)
                        ;""")
            cur.execute("""INSERT INTO podcast(sanatciid,baslik) values
                        (8,'Sanatçılarla Söyleşi'),
                        (21,'POP 2023'),
                        (14,'Dönsün Dünya')
                        ;""")
            cur.execute("""
                    SELECT premium_kullanici_ekle('mkayik45','mehmet12122413','mehmet@hotmail.com','2016-01-03',130);
                    SELECT premium_kullanici_ekle('christinwe','sophie12','sophiechristine@hotmail.com','2022-03-03',45);
                    SELECT standart_kullanici_ekle('fonkkow','17858qw-1','fonkkow@hotmail.com','2023-09-01',15);
                    SELECT standart_kullanici_ekle('flash','flashing1213','flashh@hotmail.com','2018-01-03',20);""")
            cur.execute(""" INSERT INTO calma_listesi(kullaniciid,calmalistesiAdi) values
                        (1,'Yerli şarkılar'),
                        (1,'Yabancı şarkılar'),
                        (2, 'Dance'),
                        (3,'Fear on row'),
                        (4,'matlover'),
                        (4,'flashtvseriessongs')
                        ;""")
            cur.execute("""SELECT oy_ile_degerlendirme(5,2,'2023-01-01',9);
                        SELECT oy_ile_degerlendirme(16,3,'2023-11-11',1);
                        SELECT oy_ile_degerlendirme(30,4,'2023-07-01',2);
                        """)
            cur.execute("""SELECT inceleme_ile_degerlendirme(
                        21,1,'2012-02-06','Şarkıyı çok beğendim'
                         );
                        SELECT inceleme_ile_degerlendirme(
                        23,4,'2018-11-12','Şarkının her anı çok duygusal'
                         );
                        SELECT inceleme_ile_degerlendirme(
                        12,1,'2012-02-06','Şarkıyı hiç beğenmedim, vokal çok kötü'
                         );
                        """)
            cur.execute("""SELECT katkida_bulunan_ekle_soz(16,'Sezen Aksu','Yarından haber yok, dün bitti
                            Saatler son günü çalıp gitti
                            Yeminler yaşlandı dudaklarda
                            Düğümlendi derken söz bitti
                            Vagonlar bi dolup, bi boşaldı
                            Kuruyan gözlerim yine yaşardı
                            Sarardı sırayla fotoğraflar
                            Ne hayatlar içimde kaldı
                            Unutursun için yana yana
                            Unutursun, ölüm sana, bana
                            Zaman basıp kanayan yarana
                            Unutursun, unutursun','Söz bitti');
                        
                        SELECT katkida_bulunan_ekle_soz(17,'Cem Karaca','Sende başını alıp gitme ne olur. ne olur tut ellerimi
                        Hayatta hiçbir şeyim az olmadı senin kadar
                        Hiçbir şeyi istemedim seni istediğim kadar
                        Sende başını alıp gitme ne olur. ne olur tut ellerimi
                        Hayatta hiçbir şeyim az olmadı senin kadar
                        Hiçbir şeyi istemedim seni istediğim kadar
                        Sende başını alıp gitme ne olur. ne olur tut ellerimi
                        Ne olur, ne olur','Sen de Başını Alıp Gitme');                       
                        """)
            cur.execute("""SELECT katkida_bulunan_ekle_produktor(32,'Sagopa Kajmer','SK');
                            SELECT katkida_bulunan_ekle_produktor(18,'Prince and the Revolution','Warner Bros.');
                        """)
            cur.execute("""SELECT katkida_bulunan_ekle_ensturman(19,'Thijs van Laarhoven','Gitar');
                            SELECT katkida_bulunan_ekle_ensturman(9,'Fahir Atakoğlu','Piyano');
""")
            
            
        
def menu():

        conn = connect(host = "localhost",
                      user = "postgres",
                      password = "1411", 
                      port = 5432,
                      database = "muzikprogrami")
        conn.set_isolation_level(auto_commit)
        cur = conn.cursor()
        secenek = -1
        menu = PrettyTable()
        menu.field_names = ["Seçenek", "Açıklama"]
        menu.add_row(["1", "Tüm sanatçıları görüntülemek"])
        menu.add_row(["2", "Sanatçı eklemek"])
        menu.add_row(["3", "Sanatçı çıkarmak"])
        menu.add_row(["4", "Bir albümdeki şarkılara göz atmak"])
        menu.add_row(["5", "İstediğiniz sanatçının albümlerini sıralamak"])
        menu.add_row(["6", "Albüm eklemek"])
        menu.add_row(["7", "Albüm çıkarmak"])
        menu.add_row(["8", "Tüm Albümleri Görüntülemek"])
        menu.add_row(["9", "İstediğiniz albüme şarkı eklemek"])
        menu.add_row(["10", "Görmek istediğiniz albume katkıda bulunanları sıralama"])
        menu.add_row(["11", "Albümleri türü ile sıralama"])
        menu.add_row(["12", "Albüm isminin içinde bulunan bir şeyi girerek albümü bulmak"])
        menu.add_row(["13", "Konser görüntüle"])
        menu.add_row(["14", "Konser ekle"])
        menu.add_row(["15", "Konser için bilet satın almak"])
        menu.add_row(["16", "Albümlerin süresini hesaplama"])
        menu.add_row(["17", "Değerlendirmeleri görmek"])
        menu.add_row(["18", "Değerlendirme eklemek"])
        menu.add_row(["19", "Şarkı silmek"])
        menu.add_row(["20", "Müzik videosu sıralamak"])
        menu.add_row(["21", "Müzik videosu eklemek"])
        menu.add_row(["22", "Kullanıcı eklemek"])
        menu.add_row(["23", "Kullanıcı görüntülemek"])
        menu.add_row(["24", "Kullanıcı silmek"])
        menu.add_row(["25", "Kullanıcı güncellemek"])
        menu.add_row(["26", "Podcast görüntüleme"])
        menu.add_row(["27", "Kullanıcı çalma listesi görüntüleme"])
        menu.add_row(["28", "Kullanıcı çalma listesi ekleme"])
        menu.add_row(["29", "Kullanıcı çalma listesi silme"])
        menu.add_row(["0", "Çıkış"])

    
        while secenek != 0:
            print(menu)
            print('Menüye hoşgeldiniz! Yapacağınız işlemi seçiniz')            
            secenek = input()
            if secenek == '1':
                """Tüm sanatçıları görüntülemek """
                cur.execute("SELECT * FROM sanatci order by sanatciid")
                print(from_db_cursor(cur))
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                    continue            
            if secenek == '2':
                """Sanatçı eklemek """
                sanatci_adi = input("Sanatçı Adı: ")
                ulke = input("Ülke: ")
                bio = input("Biyografi: ")               
                cur.execute(f"""INSERT INTO sanatci(sanatciAdi,ulke,bio) VALUES ('{sanatci_adi}','{ulke}','{bio}');""")
                print(from_db_cursor(cur))
                print("\nSANATÇI BAŞARI İLE EKLENDİ!\n")
                cur.execute("""SELECT * FROM sanatci order by sanatciid DESC LIMIT 1;
                             """)
                print(from_db_cursor(cur))
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '3':
                """Sanatçı çıkarmak """
                cur.execute("SELECT * FROM sanatci order by sanatciid")
                print(from_db_cursor(cur))
                sanatciid = input("Çıkarmak istediğiniz sanatçının idsini lütfen giriniz: ")
                cur.execute(f"""DELETE FROM sanatci WHERE sanatciid = {sanatciid};""")
                print(f"\n{sanatciid} nolu sanatçı silindi!\n")
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '4':
                """Bir albümdeki şarkılara göz atmak"""
                cur.execute("SELECT * FROM album order by albumid")
                print(from_db_cursor(cur))
                albumid = input("Görmek istediğiniz albümün idsini giriniz: ")
                cur.execute(f"""SELECT sarkiAdi,sure from sarki where albumid = {albumid}""")
                print(from_db_cursor(cur))
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '5':
                """İstediğiniz sanatçının albümlerini sıralamak """
                cur.execute("SELECT sanatciid,sanatciadi FROM sanatci order by sanatciid ")
                print(from_db_cursor(cur))
                sanatciid = input("Sanatçının idsini giriniz: ")
                cur.execute(f"SELECT album.albumadi,tur.turadi,album.yayintarih,album.sarki_sayisi FROM album INNER JOIN tur ON album.turid = tur.turid where sanatciid= {sanatciid} ")
                print(from_db_cursor(cur))
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '6':
                """Albüm eklemek  """
                cur.execute("SELECT sanatciid,sanatciadi FROM sanatci order by sanatciid   ")
                print(from_db_cursor(cur))
                sanatciid = input("Sanatçı idyi giriniz: ")
                albumadi = input("Albümün adını giriniz: ")
                cur.execute("SELECT * from tur")
                print(from_db_cursor(cur))
                turid = input("Albümün türünün idsini yazınız: ")
                yayinTarihi  = input("Albümün yayın tarihini yazınız: ")
                cur.execute(f"""INSERT INTO album(sanatciid,turid,yayinTarih,albumAdi) values ({sanatciid},{turid},'{yayinTarihi}','{albumadi}')""")
                print(from_db_cursor(cur))
                cur.execute("""SELECT * from album order by albumid DESC LIMIT 1""")
                print(from_db_cursor(cur))
                print("Album eklendi!")
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '7':
                """Albüm çıkarmak """
                cur.execute("SELECT albumid,albumAdi FROM album order by albumid")
                print(from_db_cursor(cur))
                albumid = input("Silmek istediğiniz albümün idyi giriniz: ")
                cur.execute(f"""DELETE FROM album WHERE albumid = {albumid}; """)
                print("\nBaşarıyla silindi!\n")
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '8':
                """Tüm Albümleri Görüntülemek  """
                cur.execute("SELECT album.albumid,album.albumadi,sanatci.sanatciAdi,tur.turadi,album.yayintarih,album.sarki_sayisi FROM album left join sanatci on sanatci.sanatciid = album.sanatciid left join tur on tur.turid = album.turid order by albumid")
                print(from_db_cursor(cur))
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '9':
                """İstediğiniz albüme şarkı eklemek """
                cur.execute("SELECT albumid,albumadi FROM album")
                print(from_db_cursor(cur))
                albumid = input("Hangi albüme şarkı eklemek istiyorsunuz id giriniz: ")
                cur.execute(f"""SELECT albumadi,sarki_sayisi from album where albumid = {albumid}""")
                print(from_db_cursor(cur))
                sarkiAdi = input("Şarkının adını giriniz: ")
                sure = input("Şarkının süresini giriniz: ")
                cur.execute(f"""CALL sarki_ekle({albumid},'{sarkiAdi}',{sure});""")
                cur.execute(f"""SELECT sarkiAdi,sure from sarki where albumid = {albumid}""")
                print(from_db_cursor(cur))
                print("\nŞarkınız başarı ile eklenmiştir!\n ")
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '10':
                """Görmek istediğiniz albume katkıda bulunanları sıralama"""
                cur.execute("SELECT albumid,albumadi FROM album order by albumid")
                print(from_db_cursor(cur))
                albumid = input("Görmek istediğiniz albümün idsini giriniz: ")
                cur.execute(f"""SELECT * FROM fn_katkida_bulunan_goster({albumid})""")
                print(from_db_cursor(cur))
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '11':
                """Albümleri türü ile sıralama """
                cur.execute("""SELECT album.albumAdi, tur.turAdi
                FROM album
                JOIN tur ON album.turID = tur.turID
                ORDER BY tur.turAdi;""")
                print(from_db_cursor(cur))
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '12':
                """Albüm isminin içinde bulunan bir şeyi girerek albümü bulmak """
                kelime = input("Aramak istediğiniz şeyi yazınız: ")
                cur.execute(f"SELECT album_ara('{kelime}')")
                print(from_db_cursor(cur))
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '13':
                 """konser görüntüle"""
                 cur.execute("SELECT konserid,sanatci.sanatciAdi,mekan,tarih,biletSayisi FROM konser left join sanatci on sanatci.sanatciid = konser.sanatciid order by konserid")
                 print(from_db_cursor(cur))
                 print("Geri menüye dönmek için 1'e basınız")
                 secenek == input()
                 if secenek == '1':
                     break
            if secenek == '14':
                """Konser eklemek"""
                
                cur.execute("SELECT * FROM sanatci order by sanatciid")
                print(from_db_cursor(cur))
                sanatciid = input("Sanatci id giriniz: ")
                mekan = input("Mekan adını giriniz: ")
                tarih = input("Tarihi giriniz: ")
                biletSayisi = input("Mevcut bilet sayısını girinz: ")
                cur.execute(f"INSERT INTO konser(sanatciid,mekan,tarih,biletSayisi) values ({sanatciid},'{mekan}','{tarih}',{biletSayisi})")
                print("Hatalı giriş tekrar deneyiniz")
                print("Başarıyla yüklenmiştir!\n")
                cur.execute("SELECT konserid,sanatci.sanatciAdi,mekan,tarih,biletSayisi FROM konser left join sanatci on sanatci.sanatciid = konser.sanatciid order by konserid desc limit 1")
                print(from_db_cursor(cur))
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '15':
                """ Konser için bilet satın almak """
                cur.execute("""SELECT konserid, sanatci.sanatciAdi,biletSayisi,mekan from konser inner join sanatci on sanatci.sanatciid = konser.sanatciid order by konserid""")
                print(from_db_cursor(cur))
                konserid = input("Satın almak istediğiniz konserin idsini giriniz: ")
                biletSayisi = input("Kaç adet bilet satın almak istiyorsunuz: ")
                cur.execute(f"""SELECT bilet_satis({konserid},{biletSayisi}) """)
                print("\nBilet satışınız gerçekleşti!\n ")
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '16':
                """Albümlerin süresini hesaplama"""
                cur.execute("SELECT albumid,albumadi FROM album order by albumid")
                print(from_db_cursor(cur))
                albumid = input("Hesaplamak istediğiniz albümün idsini giriniz: ")
                cur.execute(f"""SELECT album_sure_hesapla({albumid})""")
                print(from_db_cursor(cur))
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '17':
                """Değerlendirmeleri görmek"""
                cur.execute("SELECT degerlendirmeid,sarki.sarkiadi,kullanici.kullaniciAdi,tarih, degerlendirmeturu FROM degerlendirme JOIN sarki on sarki.sarkiid = degerlendirme.sarkiid JOIN kullanici on kullanici.kullaniciid = degerlendirme.kullaniciid")
                print(from_db_cursor(cur))
                dgtur = input("Görmek istediğiniz değerlendirmenin idsini giriniz: ")
                cur.execute(f"SELECT degerlendirmeturu from degerlendirme where degerlendirmeid = {dgtur}")
                dturu = cur.fetchone()[0]
                if dturu == 'oy':
                    cur.execute(f"""Select degerlendirme_goruntule({dgtur})""")
                    tb = from_db_cursor(cur)
                    tb.field_names = ('Oy',)
                    print(tb)
                elif dturu == 'inceleme':
                    cur.execute(f"""Select degerlendirme_goruntule({dgtur})""")
                    tb = from_db_cursor(cur)
                    tb.field_names = ('İnceleme Metni',)
                    print(tb)
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '18':
                """Değerlendirme eklemek """
                dtur = input("Ne tur değerlendirme eklemek istiyorsunuz:\n1-)Oy\n2-)İnceleme\n")
                if dtur == '1':
                     cur.execute("""SELECT sarkiid,sarkiadi from sarki order by sarkiid""")
                     print(from_db_cursor(cur))
                     sarkiid = input("Değerlendirmek istediğiniz şarkının idsini giriniz: ")
                     cur.execute("""SELECT * from kullanici order by kullaniciid""")
                     print(from_db_cursor(cur))
                     kullaniciid = input("Kullanici idnizi giriniz: ")
                     oySayisi = input("Vermek istediğiniz oyu 0-9 arasında yazınız ")
                     cur.execute(f"""SELECT oy_ile_degerlendirme({sarkiid},{kullaniciid},CURRENT_DATE,{oySayisi}) """)
                     print("\nDeğerlendirmeiniz başarıyla kaydedildi\n")
                     cur.execute("""select d.degerlendirmeid,d.sarkiid,d.kullaniciid,d.tarih,o.oySayisi from degerlendirme d LEFT JOIN oy o on d.degerlendirmeid = o.degerlendirmeid order by degerlendirmeid desc limit 1""")
                     print(from_db_cursor(cur))
                if dtur == '2':
                     cur.execute("""SELECT sarkiid,sarkiadi from sarki order by sarkiid""")
                     print(from_db_cursor(cur))
                     sarkiid = input("Değerlendirmek istediğiniz şarkının idsini giriniz: ")
                     cur.execute("""SELECT * from kullanici order by kullaniciid""")
                     print(from_db_cursor(cur))
                     kullaniciid = input("Kullanici idnizi giriniz: ")
                     text = input("İnceleme metninizi giriniz: ")
                     cur.execute(f"""SELECT inceleme_ile_degerlendirme({sarkiid},{kullaniciid},CURRENT_DATE,'{text}') """)
                     print("\nDeğerlendirmeiniz başarıyla kaydedildi\n")
                     cur.execute("""select d.degerlendirmeid,d.sarkiid,d.kullaniciid,d.tarih,i.incelemeMetni from degerlendirme d LEFT JOIN inceleme i on d.degerlendirmeid = i.degerlendirmeid order by degerlendirmeid desc limit 1""")
                     print(from_db_cursor(cur))
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '19':
                """Şarkı silmek"""
                cur.execute("SELECT sarkiid,album.albumadi,sarkiadi,sure FROM sarki left join album on album.albumid = sarki.albumid order by sarkiid")
                print(from_db_cursor(cur))
                sarkiid = input("Silmek istediğiniz şarkının idsini giriniz: ")
                cur.execute(f"DELETE from sarki where sarkiid = {sarkiid}")
                print("\nBaşarıyla silindi!\n")
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '20':
                """Müzik videosu sıralamak"""
                cur.execute("SELECT sarki.sarkiadi, yonetmen, cekimTarihi,link FROM muzik_video LEFT JOIN sarki on sarki.sarkiid = muzik_video.sarkiid")
                print(from_db_cursor(cur))
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '21':
                """Müzik videosu eklemek"""
                cur.execute("""SELECT sarkiid,sarkiadi from sarki order by sarkiid""")
                print(from_db_cursor(cur))
                sarkiid = input("Şarkı id giriniz: ")
                yonetmen = input("Yönetmenin ismini giriniz: ")
                cekimTarihi = input("Tarihi giriniz: ")
                link = input("Linki yazınız: ")
                cur.execute(f"""INSERT INTO muzik_video(sarkiid,yonetmen,cekimTarihi, link) values ({sarkiid},'{yonetmen}','{cekimTarihi}','{link}')""")
                cur.execute("""SELECT * from muzik_video order by videoid desc limit 1""")
                print(from_db_cursor(cur))
                print("\nBaşarıyla Eklendi\n")
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '22':
                """Kullanıcı eklemek"""
                secim = input("Hangi tür kullanıcı eklemek istiyorsunuz:\n1-)Premium\n2-)Standart\n")
                if secim == '1': 
                    kullaniciAdi = input("Kullanıcı adını giriniz: ")
                    sifre = input("Şifreyi girin: ")
                    mail = input("Maili giriniz: ")
                    fiyat = input("Üyelik fiyatını giriniz: ")
                    cur.execute(f"""SELECT premium_kullanici_ekle('{kullaniciAdi}','{sifre}','{mail}',CURRENT_DATE,{fiyat})""")
                    cur.execute("""SELECT * from kullanici order by kullaniciid desc limit 1""")
                    print(from_db_cursor(cur))
                    print("\nBaşarıyla Eklendi\n")
                    print("Geri menüye dönmek için 1'e basınız")
                if secim == '2':
                     kullaniciAdi = input("Kullanıcı adını giriniz: ")
                     sifre = input("Şifreyi girin: ")
                     mail = input("Maili giriniz: ")
                     geçilenReklam = input("Geçilen reklamı giriniz: ")
                     cur.execute(f"""SELECT standart_kullanici_ekle('{kullaniciAdi}','{sifre}','{mail}',CURRENT_DATE,{geçilenReklam})""")
                     cur.execute("""SELECT * from kullanici order by kullaniciid desc limit 1""")
                     print(from_db_cursor(cur))
                     print("\nBaşarıyla Eklendi\n")
                     print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '23':
                """Kullanıcıları görüntülemek"""
                cur.execute("SELECT * FROM kullanici order by kullaniciid")
                print(from_db_cursor(cur))
                secim = input("Detayını görmek istediğiniz kullanıcının idsini seçiniz: ")
                cur.execute(f"SELECT hesapturu from kullanici where kullaniciid = {secim}")
                hturu = cur.fetchone()[0]
                if hturu == 's':
                     print("\nHesap Standart\n")
                     cur.execute(f"""SELECT kullanici_goruntule({secim})""")
                     tb = from_db_cursor(cur)
                     tb.field_names = ('Geçilen Reklam',)
                     print(tb)
                elif hturu == 'p':
                    print("\nHesap Premium\n")
                    cur.execute(f"""SELECT kullanici_goruntule({secim})""")
                    tb = from_db_cursor(cur)
                    tb.field_names = ('Fiyat',)
                    print(tb)
                
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '24':
                """Kullanıcı silmek """
                cur.execute("SELECT * FROM kullanici order by kullaniciid")
                print(from_db_cursor(cur))
                kullaniciid = input("Silmek istediğiniz kullanıcının idsini girimiz: ")
                cur.execute(f"DELETE FROM kullanici where kullaniciid = {kullaniciid}")
                print("\nKullanıcı başarıyla silindi\n")
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '25':
                """Kullanıcı güncellemek"""
                cur.execute("SELECT * FROM kullanici order by kullaniciid")
                print(from_db_cursor(cur))
                kullaniciid = input("Hangi kullanıcıyı düzenlemek istiyorsunuz, idsini giriniz: ")
                sec = input("\nHangi işlemi yapmak istiyorsunuz:\n1-)Kullanıcı adı değiştirmek\n2-)şifre değiştirmek\n3-)mail değiştirmek\n4-)hesap turu değiştirmek\n")
                if sec == '1':
                     yenikullaniciadi = input("yeni kullanıcı adını giriniz: ")
                     cur.execute(f"UPDATE kullanici set kullaniciadi = '{yenikullaniciadi}' where kullaniciid = {kullaniciid}")
        
                     cur.execute(f"SELECT * FROM kullanici where kullaniciid={kullaniciid} order by kullaniciid")
                     print(from_db_cursor(cur))
                     print("\nGüncelleme gerçekleşti\n")
                if sec == '2':
                     yenisifre = input("yeni şifreyi giriniz: ")
                     cur.execute(f"UPDATE kullanici set sifre = '{yenisifre}' where kullaniciid = {kullaniciid} ")
                     cur.execute(f"SELECT * FROM kullanici where kullaniciid={kullaniciid} order by kullaniciid")
                     print(from_db_cursor(cur))
                     print("\nGüncelleme gerçekleşti\n")
                if sec == '3':
                     yenimail = input("yeni maili giriniz: ")
                     cur.execute(f"UPDATE kullanici set sifre = '{yenimail}' where kullaniciid = {kullaniciid}")
                     cur.execute(f"SELECT * FROM kullanici where kullaniciid={kullaniciid} order by kullaniciid")
                     print(from_db_cursor(cur))
                     print("\nGüncelleme gerçekleşti\n")
                if sec == '4':
                    cur.execute(f"SELECT hesapturu from kullanici where kullaniciid = {kullaniciid}")
                    hturu = cur.fetchone()[0]
                    if hturu == 'p':
                         gecilenReklam = input("Geçilen reklamı giriniz: ")
                         cur.execute(f"SELECT upgrade_account({kullaniciid},{gecilenReklam}) ")
                         print("\nGüncelleme gerçekleşti\n")
                         cur.execute(f"SELECT * from kullanici where kullaniciid = {kullaniciid} order by kullaniciid")
                         print(from_db_cursor(cur))
                    elif hturu == 's':
                         fiyat = input("Fiyatı giriniz: ")
                         cur.execute(f"SELECT upgrade_account({kullaniciid},{fiyat}) ")
                         print("\nGüncelleme gerçekleşti\n")
                         cur.execute(f"SELECT * from kullanici where kullaniciid = {kullaniciid} order by kullaniciid")
                         print(from_db_cursor(cur)) 
                    print("\nGüncelleme gerçekleşti\n")
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '26':
                """Podcast görüntüleme"""
                cur.execute("SELECT s.sanatciAdi,baslik FROM podcast left join sanatci as s on podcast.sanatciid = s.sanatciid")
                print(from_db_cursor(cur))
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '27':
                """ Kullanıcı çalma listesi görüntüleme """
                cur.execute("SELECT * FROM kullanici order by kullaniciid")
                print(from_db_cursor(cur))
                kullaniciid = input("Hangi kullanıcının çalma listesini görüntülemek istiyorsun id giriniz: ")
                cur.execute(f"SELECT listeid,calmalistesiAdi FROM calma_listesi where kullaniciid = {kullaniciid} ")
                print(from_db_cursor(cur))
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '28':
                """"Kullanıcı çalma listesi ekleme"""
                cur.execute("""SELECT * FROM kullanici order by kullaniciid""")
                print(from_db_cursor(cur))
                kullaniciid = input("Hangi kullanıcıya çalma listesi eklemek istiyorsunuz id giriniz: ")
                calmalistesiAdi = input("Çalma listesin adını giriniz: ")
                cur.execute(f"INSERT INTO calma_listesi(kullaniciid,calmalistesiAdi) values ({kullaniciid},'{calmalistesiAdi}') ")
                cur.execute("SELECT listeid,calmalistesiadi from calma_listesi order by listeID DESC limit 1")
                print(from_db_cursor(cur))
                print("\nKullanıcının çalma listeleri:\n")
                cur.execute(f"SELECT listeid,calmalistesiAdi FROM calma_listesi where kullaniciid = {kullaniciid} ")
                print(from_db_cursor(cur))
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            if secenek == '29':
                """ Kullanıcı çalma listesi silme"""
                cur.execute("""SELECT * FROM kullanici order by kullaniciid""")
                print(from_db_cursor(cur))
                kullaniciid = input("Hangi kullanıcının çalma listesini silmek istiyorsunuz : ")
                cur.execute(f"SELECT listeid,calmalistesiAdi FROM calma_listesi where kullaniciid = {kullaniciid} ")
                print(from_db_cursor(cur))
                listeid = input("Hangi çalma listesini silmek istiyorsunuz : ")
                cur.execute(f"DELETE from calma_listesi where listeid = {listeid}")
                print("\nBaşarıyla silindi!\n")
                print("Geri menüye dönmek için 1'e basınız")
                secenek == input()
                if secenek == '1':
                     break
            
            if secenek == '0':
                break
                 
            
              
createDB()
menu()


                        