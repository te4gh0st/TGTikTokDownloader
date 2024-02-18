<h1 align="center">TGTikTokDownloader</h1>

<p align="center">
     <img src="./documentation_images/tt.png" width="100" height="100" style="">
</p>

<div align="center" markdown>

🌏 English | [**Русский**](./README.ru.md) |

</div>

## Description

TikTok Video Downloader Bot Project
is an automated bot for the Telegram messenger,
designed to download videos from the popular TikTok platform using the links provided.

### Key Features

- Ease of use: To download a video, just send the bot a link to the video from TikTok,
after which the user receives the requested video in a response message.
- Automated process: The bot notifies the user about all stages of video downloading,
providing transparency and ease of use.
- Support for Poling and Webhook modes: The bot can work in two modes:
Poling for easy installation on a local server and Webhook for integration with cloud platforms,
providing flexibility and scalability.
- Limited access: It is possible to configure the bot in such a way
so that it is accessible only to the administrator,
providing an additional level of security and control.

---

## Installation Instructions
To install and run the bot on your own server, follow the instructions:

1. Clone the project repository to your local computer `git clone https://github.com/te4gh0st/TGTikTokDownloader.git`
2. Install the required dependencies specified in the requirements.txt file `python3 -m pip install -r requirements.txt`.
3. Create a bot in Telegram via [BotFather](https://t.me/BotFather).
4. Get the bot token and configure the environment variables.
5. Run the bot `python3 main.py`.

---

## Settings

### Environment Variables

| ENV | Required | Default | Description |
|----------------|:----------:|:------------------ ---:|-------------------------------------------- -------------------------------------------------- ---------|
| TOKEN | + | - | Telegram Bot Token |
| WEBHOOK_ACTIVE | - | 0 | Operating mode<br/>0: Poling \| 1: Webhook |
| WEBHOOK_HOST | +- | - | Domain - **https-only** (Example: https://example.com) |
| WEBHOOK_PATH | +- | - | Url path (Example: ) |
| WEBHOOK_PATH | +- | - | Url path (Example: <i>/webhook</i>) |
| WEBAPP_HOST | - | localhost | Host on which the application is running |
| WEBAPP_PORT | +- | - | Port on which the application is running |
| ADMIN_ID | - | 0 | Telegram ID of the user for whom the bot will work. If not specified, will work for everyone |

### Example Webhook path for NGINX

```nginx
location = /webhook {
     proxy_pass http://127.0.0.1:3001;
}
```

### Example Systemd service
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