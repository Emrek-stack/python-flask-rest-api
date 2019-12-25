Db'yi create etmek icin, cli'dan "flask resetdb" komutunu calistirabilirsiniz

projede flask kullandim, flask kullanmamin amaci diger frameworklere gore (django v.s) daha lightweight ve atomic olmasindandir
Database olarak postgres, orm olarak SQLAlchmey kullandim
Bir Api beklenildigi icin, login islemlerinde session yerine JWT ile bir tokenize yapisi kurdum.

Projenin Customer kisimlari, Orm ve JWT tarafi biraz vaktigimi aldigi icin yetistiremeidim fakat jwt kullanimina ornek olmasi icin
Customer Create functionunda bir @jwt_required decorator'u ekledim.

Projeyi dockerize ettim, compose file icerisinde, docker islemleri ve postgres birlikte up oluyorlar.


Proje docker ortamında asagidaki sekilde ayaga kaldirilabilir

$ docker-compose build
$ docker-compose up
