FROM nginx:1.21-alpine

# ヘルスチェックの設定
HEALTHCHECK --interval=30s --timeout=3s CMD curl --fail http://localhost || exit 1

EXPOSE 80
