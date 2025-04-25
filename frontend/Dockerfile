FROM node:20-alpine

WORKDIR /app

# Angular CLIをグローバルにインストール
RUN npm install -g @angular/cli

# 起動スクリプトを作成
RUN echo '#!/bin/sh' > /entrypoint.sh && \
    echo 'if [ ! -d "/app/node_modules" ] || [ ! -f "/app/package.json" ]; then' >> /entrypoint.sh && \
    echo '  echo "Angularプロジェクトをセットアップします..."' >> /entrypoint.sh && \
    echo '  # 一時ディレクトリにプロジェクトを作成' >> /entrypoint.sh && \
    echo '  mkdir -p /tmp/new-angular-app' >> /entrypoint.sh && \
    echo '  cd /tmp/new-angular-app' >> /entrypoint.sh && \
    echo '  ng new twitter-app --skip-git --routing=true --style=scss --skip-tests' >> /entrypoint.sh && \
    echo '' >> /entrypoint.sh && \
    echo '  # プロジェクトが存在しない場合、必要なファイルをコピー' >> /entrypoint.sh && \
    echo '  if [ ! -f "/app/package.json" ]; then' >> /entrypoint.sh && \
    echo '    cp -r /tmp/new-angular-app/twitter-app/. /app/' >> /entrypoint.sh && \
    echo '    cd /app' >> /entrypoint.sh && \
    echo '    npm install' >> /entrypoint.sh && \
    echo '  fi' >> /entrypoint.sh && \
    echo 'else' >> /entrypoint.sh && \
    echo '  cd /app' >> /entrypoint.sh && \
    echo '  # 依存関係のチェックと更新' >> /entrypoint.sh && \
    echo '  if [ -f "/app/package.json" ] && [ ! -d "/app/node_modules" ]; then' >> /entrypoint.sh && \
    echo '    npm install' >> /entrypoint.sh && \
    echo '  fi' >> /entrypoint.sh && \
    echo 'fi' >> /entrypoint.sh && \
    echo '' >> /entrypoint.sh && \
    echo '# Angularの開発サーバーを起動' >> /entrypoint.sh && \
    echo 'cd /app && exec ng serve --host 0.0.0.0 --poll=2000 --disable-host-check' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# ポート4200を公開
EXPOSE 4200

# 起動スクリプトを実行
ENTRYPOINT ["/entrypoint.sh"]
