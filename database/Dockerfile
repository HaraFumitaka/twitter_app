FROM mysql:8.0
# タイムゾーンの設定
ENV TZ=Asia/Tokyo
# ログディレクトリを作成
RUN mkdir -p /var/log/mysql
RUN touch /var/log/mysql/mysqld.log


# ヘルスチェックの設定
HEALTHCHECK --interval=5s --timeout=5s --retries=3 CMD mysqladmin ping -h localhost -u root -p${MYSQL_ROOT_PASSWORD} || exit 1

EXPOSE 3306
