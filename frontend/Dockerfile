FROM node:20-alpine

WORKDIR /app

# Chrome と必要な依存関係をインストール
RUN apk add --no-cache chromium

# 環境変数の設定
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Angular CLIをグローバルにインストール
RUN npm install -g @angular/cli

# 起動スクリプトを修正して、必ず必要なパッケージをインストールする
RUN echo '#!/bin/sh' > /entrypoint.sh && \
    echo 'cd /app' >> /entrypoint.sh && \
    echo '' >> /entrypoint.sh && \
    echo '# 既存プロジェクトかチェック' >> /entrypoint.sh && \
    echo 'if [ -f "/app/package.json" ]; then' >> /entrypoint.sh && \
    echo '  echo "既存のAngularプロジェクトを検出しました"' >> /entrypoint.sh && \
    echo '  echo "依存関係をインストールしています..."' >> /entrypoint.sh && \
    echo '  npm install --save-dev @angular-devkit/build-angular' >> /entrypoint.sh && \
    echo 'else' >> /entrypoint.sh && \
    echo '  echo "新規Angularプロジェクトを作成します..."' >> /entrypoint.sh && \
    echo '  ng new twitter-app --skip-git --routing=true --style=scss --skip-tests --directory=.' >> /entrypoint.sh && \
    echo 'fi' >> /entrypoint.sh && \
    echo '' >> /entrypoint.sh && \
    echo '# Angularの開発サーバーを起動' >> /entrypoint.sh && \
    echo 'exec ng serve --host 0.0.0.0 --poll=2000 --disable-host-check' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# ポート4200を公開
EXPOSE 4200

# 起動スクリプトを実行
ENTRYPOINT ["/entrypoint.sh"]
