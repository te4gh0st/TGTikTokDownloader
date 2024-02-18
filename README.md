<h1 align="center">TGTikTokDownloader</h1>

<p align="center">
    <img src="./documentation_images/tt.png" width="100" height="100" style="">
</p>

## Описание

Проект TikTok Video Downloader Bot 
представляет собой автоматизированного бота для мессенджера Telegram,
разработанного с целью загрузки видео из популярной платформы TikTok по предоставленным ссылкам.

### Основные возможности

- Простота использования: Для загрузки видео достаточно отправить боту ссылку на видео из TikTok,
после чего пользователь получает запрошенное видео в ответном сообщении.
- Автоматизированный процесс: Бот уведомляет пользователя обо всех этапах загрузки видео,
обеспечивая прозрачность и комфорт в использовании.
- Поддержка режимов Poling и Webhook: Бот может работать в двух режимах: 
Poling для простой установки на локальном сервере и Webhook для интеграции с облачными платформами,
обеспечивая гибкость и масштабируемость.
- Ограниченный доступ: Существует возможность настройки бота таким образом,
чтобы он был доступен только для администратора,
обеспечивая дополнительный уровень безопасности и контроля.

---

## Инструкции по установке
Для установки и запуска бота на собственном сервере, следуйте инструкциям:

1. Клонируйте репозиторий проекта на свой локальный компьютер `git clone https://github.com/te4gh0st/TGTikTokDownloader.git`
2. Установите необходимые зависимости, указанные в файле requirements.txt `python3 -m pip install -r requirements.txt`.
3. Создайте бота в Telegram через [BotFather](https://t.me/BotFather).
4. Получите токен бота и настройте переменные окружения.
5. Запустите бота `python3 main.py`.

---

## Настройка

### Переменные окружения

| ENV            | Обязателен | Значение по умолчанию | Описание                                                                                               |
|----------------|:----------:|:---------------------:|--------------------------------------------------------------------------------------------------------|
| TOKEN          |     +      |           -           | Токен Telegram Бота                                                                                    |
| WEBHOOK_ACTIVE |     -      |           0           | Режим работы<br/>0: Poling \| 1: Webhook                                                               |
| WEBHOOK_HOST   |     +-     |           -           | Домен - **https-only** (Пример: https://example.com)                                                   |
| WEBHOOK_PATH   |     +-     |           -           | Url path (Пример: )                                                                                    |
| WEBHOOK_PATH   |     +-     |           -           | Url path (Пример: <i>/webhook</i>)                                                                     |
| WEBAPP_HOST    |     -      |       localhost       | Хост на котором запущено приложение                                                                    |
| WEBAPP_PORT    |     +-     |           -           | Порт на котором запущено приложение                                                                    |
| ADMIN_ID       |     -      |           0           | Telegram ID пользователя, для которого бот будет работать. Если не указано, то будет работать для всех |

### Пример пути Webhook для NGINX

```nginx
location = /webhook {
    proxy_pass http://127.0.0.1:3001;
}
```

### Пример Systemd сервиса
```shell
# Copy to /etc/systemd/systemd/system
#sudo systemctl enable <filename>.service

[Unit]
Description=Telegram TikTok Downloader
Requires=network.target
After=multi-user.target


[Service]
Type=simple
ExecStart=sudo python3 /<PATH>/TGTikTokDownloader/main.py # Need edit
WorkingDirectory=<PATH>/TGTikTokDownloader # Need edit
Restart=always

[Install]
WantedBy=multi-user.target
```

---
<h4>
Copyright &copy; 2024 te4gh0st (Vitaliy Timtsurak). All rights reserved.
<br>
Licensed under the Apache License, Version 2.0
</h4>