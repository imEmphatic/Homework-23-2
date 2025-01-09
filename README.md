Задание 1
Продолжаем работать с проектом. Установите брокер для кеширования Redis. Внесите необходимые настройки и проверьте работоспособность проекта с новыми настройками.
Обратите внимание на то, что Redis не работает на Windows. Для запуска используйте WSL Linux (вы устанавливали его ранее). Инструкцию можно найти здесь.
После проведения настроек Redis будет доступен для использования по адресу 127.0.0.1:6379, если вы не меняли порт для запуска. Если порт был изменен, указывайте тот, на котором запущен процесс.

Задание 2
Настройте кеширование всего контроллера отображения данных относительно одного продукта.
Примечание
Помните, что кеширование можно подключать не только в файле views.py, но и в файле маршрутизации urls.py. Важно делать всё в одном месте, чтобы достичь единообразия в коде проекта и не запутаться впоследствии.

Задание 3
Создайте сервисную функцию, которая будет отвечать за выборку категорий и которую можно переиспользовать в любом месте системы. Добавьте низкоуровневое кеширование для списка категорий.
Также можно реализовать функцию для кеширования списка продуктов. Если вы не использовали категории в своей работе, реализуйте контроллер и шаблон для выдачи списка категорий и в качестве контекста передавайте результат работы этой функции. Также можно воспользоваться переопределением кверисета в CBV.

Задание 4
Вынесите необходимые настройки в переменные окружения и настройте проект для работы с ними.
К необходимым настройкам относятся все чувствительные данные, которые хранятся в настройках приложения: секретный ключ Django, настройки базы данных, настройки кеширования (адрес подключения к брокеру, включение кеширования), включение режима отладки и любые логины и пароли от сторонних сервисов, например данные учетной записи для отправки почты. Любые данные, которые могут при утечке навредить вашему приложению и являются чувствительными.

Дополнительное задание
Добавьте кеширование всего сайта целиком, при этом отключите от кеширования определенные контроллеры, которые отвечают за работу по заполнению продуктов и блога.
