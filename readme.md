ວິທີການຕິດຕັ້ງ ແລະ Run
============================

ຕິດຕັ້ງ Python version 3 ຂື້ນໄປ
------------
ດາວໂຫຼດ Python
ຕິດຕັ້ງ Library Python
ຕິດຕັ້ງ Flask
ຕິດຕັ້ງ OpenCV
ຕິດຕັ້ງ Bootstrap 4
ຕິດຕັ້ງ Flask WTF
ຕິດຕັ້ງ Flask WTForms
ຕິດຕັ້ງ Matplotlib
ຕິດຕັ້ງ Numpy
Run Project
ດາວໂຫຼດ Source Code
ໃຊ້ commandline(CMD) ເຂົ້າຫາ path ທີເອົາ Source code ເກັບໄວ້ ແລ້ວ run ຄໍາສັ່ງ python app.py
ອ່ານເອກະສານເພີ່ມ >>>

INSTALLATION
------------

### Install
1. Download XAMPP OR APSERV  https://www.apachefriends.org/download.html
2. After downloaded and install XAPP
3. Download Zip file and unzip than copy project to www or html folder
4. Run  access the application through the following URL:

~~~
http://localhost/pos/web/index.php?r=site/install
~~~


CONFIGURATION
-------------

### Database

Edit the file `config/db.php` with real data, for example:

```php
return [
    'class' => 'yii\db\Connection',
    'dsn' => 'mysql:host=localhost;dbname=mk_db',
    'username' => 'root',
    'password' => '1234',
    'charset' => 'utf8',
];
```
