# Ferheng+ Gizlilik Politikası

**Son güncelleme:** 21 Ağustos 2026  
**Yürürlük tarihi:** 21 Ağustos 2026  
**Uygulama:** Ferheng+  
**Geliştirici/yayıncı:** Zana Game Studios

> Bu metin, Ferheng+ uygulamasının mevcut teknik davranışına göre hazırlanmış bir çalışma taslağıdır. Resmî hukuk danışmanlığı değildir; uygulama yayımlanmadan veya önemli bir uyumluluk kararı verilmeden önce yetkin bir hukukçu tarafından incelenmelidir.

## 1. Kapsam

Bu Gizlilik Politikası, Ferheng+ Android uygulamasının arama, favoriler, arayüz tercihleri, uzaktan sözlük verisi güncellemeleri, isteğe bağlı reklamlar ve isteğe bağlı destek ödemeleri sırasında veri işleme biçimini açıklar.

Ferheng+ bir Kurmancî/Kuzey Kürtçesi merkezli sözlük uygulamasıdır. Uygulama hesabı oluşturmayı, kullanıcı profili açmayı veya kullanıcıların sözlük kaydı yüklemesini gerektirmez.

## 2. Sorumlu kuruluş ve iletişim

Ferheng+’ın geliştiricisi ve yayıncısı **Zana Game Studios**’dur. Bu politika hakkında soru, düzeltme talebi veya gizlilik bildirimi için [Ferheng+ data repository Issues sayfası][1] üzerinden iletişim kurulabilir. Hassas kişisel bilgileri GitHub issue’larına yazmayın.

## 3. Uygulama içinde yerel olarak tutulan veriler

Ferheng+, temel sözlük işlevlerini sağlamak için bazı verileri cihazda yerel olarak tutabilir:

| Veri türü | Kullanım amacı | Geliştiriciye gönderilir mi? |
|---|---|---|
| Arama geçmişi | Önceki aramaları ve arama deneyimini desteklemek | Hayır; uygulamanın kendi yerel veritabanında tutulur |
| Favoriler | Kullanıcının seçtiği kelimeleri saklamak | Hayır; cihazda tutulur |
| Arayüz dili | Seçilen arayüz dilini korumak | Hayır; cihazda tutulur |
| Görünüm tercihi | Sistem, Açık veya Koyu temayı korumak | Hayır; cihazda tutulur |
| Sözlük veritabanı | Çevrimdışı arama ve kelime detaylarını sağlamak | Uygulama tarafından GitHub’dan indirilir; kullanıcı aramaları gönderilmez |

Bu yerel bilgiler uygulama verileri temizlendiğinde veya uygulama kaldırıldığında Android tarafından silinebilir. Android’in uygulama verisi yedekleme davranışı cihaz, işletim sistemi ve kullanıcı ayarlarına bağlı olabilir.

## 4. Arama sorguları ve kelime kullanımı

Ferheng+ arama sorgularını, sözlük veritabanında yerel arama yapmak için cihaz üzerinde işler. Uygulamanın sözlük araması için kullanıcının yazdığı kelimeyi kendi sunucusuna gönderen bir hesap veya arama API’si yoktur.

Remote veri güncellemesi sırasında uygulama, GitHub üzerinde yayımlanan manifest ve sıkıştırılmış SQLite sözlük paketini HTTPS üzerinden indirir. Bu istekler sözlük paketinin güncel olup olmadığını ve bütünlüğünü doğrulamak içindir; kullanıcı arama sorgusu bu isteklere eklenmez.

## 5. Reklamlar ve rıza seçenekleri

Ferheng+ isteğe bağlı ödüllü reklam desteği için **Google Mobile Ads / AdMob** hizmetlerini kullanır. Reklam hizmeti, reklam sunumu ve ölçümü için Google’ın kendi gizlilik uygulamalarına tabi olabilir. Bu kapsamda cihaz tanımlayıcıları, IP adresi, yaklaşık konum, uygulama etkileşimi, tanılama verileri veya reklamla ilgili teknik bilgiler Google tarafından kendi politikalarına göre işlenebilir.

Kişiselleştirilmiş reklamlar için gerekli rıza ve bölgesel açıklamalar Google’ın User Messaging Platform akışı üzerinden gösterilebilir. Reklam tercihleri ve kişiselleştirme seçenekleri, Google’ın sağladığı kontroller ve Android cihaz ayarları üzerinden yönetilebilir.

Google’ın reklam verisi uygulamaları hakkında güncel bilgi için [Google Ads Data Safety ve gizlilik açıklamalarına][2] bakın.

## 6. Google Play destek ödemeleri

Ferheng+ içinde 20 TL, 50 TL ve 100 TL tutarında isteğe bağlı destek ürünleri **Google Play Billing** üzerinden sunulabilir. Ödeme bilgileri, kart bilgileri ve fatura işlemleri Ferheng+ tarafından toplanmaz veya saklanmaz; ödeme işlemi Google Play’in kendi hizmetleri ve politikaları üzerinden yürütülür.

Uygulama, satın alma akışının tamamlanıp tamamlanmadığını ve destek işlemini sonuçlandırmak için Google Play Billing’dan dönen teknik satın alma durumunu işleyebilir. Google Play’in veri işleme uygulamaları için [Google Play Hizmet Şartları ve gizlilik bilgilerine][3] bakın.

## 7. Üçüncü taraf hizmetler

Ferheng+ aşağıdaki üçüncü taraf hizmetlerine bağlantı kurabilir:

| Hizmet | Amaç | Veri akışı |
|---|---|---|
| GitHub | Manifest ve sözlük verisi güncellemesi; bu politika metninin barındırılması | HTTPS üzerinden public dosya indirme |
| Google Mobile Ads / AdMob | İsteğe bağlı ödüllü reklam | Google’ın reklam SDK’sı ve politikaları geçerlidir |
| Google Play Billing | İsteğe bağlı destek ödemeleri | Ödeme Google Play üzerinden yürütülür |

Ferheng+ bu üçüncü tarafların kendi veri işleme faaliyetlerinden sorumlu değildir. Her hizmetin güncel politika ve şartları ayrıca incelenmelidir.

## 8. Veri paylaşımı ve satış

Zana Game Studios, Ferheng+ arama geçmişini, favorileri, arayüz tercihlerini veya sözlük sorgularını reklam amacıyla satmaz. Uygulamanın yerel sözlük verileri geliştiriciye kullanıcı bazında gönderilmez.

Bununla birlikte reklam ve ödeme hizmetleri, kendi SDK ve hizmet operasyonları için teknik verileri kendi politikalarına göre işleyebilir. Yasal zorunluluk, güvenlik olayı veya hakların korunması gerektiğinde ilgili bilgiler yetkili mercilerle paylaşılabilir.

## 9. Veri güvenliği

Uygulama remote sözlük paketini HTTPS üzerinden indirir ve paketi kurmadan önce manifestteki sıkıştırılmış SHA-256, açılmış SQLite SHA-256, boyut, entry sayısı ve Room şema bütünlüğünü doğrular. Bu kontroller veri paketinin değiştirilmesi veya eksik indirilmesi riskini azaltmak içindir; hiçbir internet veya yazılım sistemi mutlak güvenlik garantisi vermez.

## 10. Saklama süreleri ve silme

Yerel arama geçmişi, favoriler ve tercihler cihazda uygulama verileri temizlenene veya uygulama kaldırılana kadar tutulabilir. Kullanıcı Android ayarlarından Ferheng+ uygulamasının verilerini temizleyerek yerel verileri silebilir. Kullanıcı, üçüncü taraf reklam veya ödeme hizmetleri tarafından tutulan verilerin silinmesi için ilgili hizmetin kendi başvuru ve hesap kontrollerini kullanmalıdır.

## 11. Çocukların gizliliği

Ferheng+ bilerek çocuklardan kişisel veri toplamak amacıyla tasarlanmamıştır. Bir çocuğun uygulama üzerinden kişisel bilgi paylaştığını düşünüyorsanız, bu bilgiyi GitHub üzerinden göndermeden [Issues sayfası][1] aracılığıyla genel olmayan uygun bir iletişim yöntemi talep edin.

## 12. Uluslararası veri aktarımı

Google ve GitHub gibi hizmet sağlayıcılar teknik verileri kullanıcının bulunduğu ülke dışındaki sunucularda işleyebilir. Bu aktarımın kapsamı ve hukuki dayanağı ilgili sağlayıcının güncel gizlilik politikalarına ve kullanıcının bölgesindeki mevzuata göre değişebilir.

## 13. Politika değişiklikleri

Bu politika, uygulamanın teknik özellikleri, üçüncü taraf hizmetleri veya yürürlükteki gereklilikler değiştiğinde güncellenebilir. Güncel sürüm bu public GitHub sayfasında yayımlanır. Önemli değişikliklerde, mümkün olduğu ölçüde uygulama içi bildirim veya mağaza açıklaması kullanılabilir.

## 14. İletişim

Gizlilikle ilgili sorularınız için [Ferheng+ data repository Issues sayfasını][1] kullanın. GitHub issue’sunda arama geçmişi, ödeme bilgisi, cihaz kimliği veya başka hassas kişisel bilgi paylaşmayın.

## Referanslar

[1]: https://github.com/zanagamestudios-lgtm/ferhengplus-data/issues "Ferheng+ data repository Issues"
[2]: https://policies.google.com/technologies/partner-sites "Google partner and advertising technologies"
[3]: https://policies.google.com/privacy "Google Privacy Policy"
