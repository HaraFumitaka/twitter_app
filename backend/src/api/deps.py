from fastapi import Depends
from ..auth.utils import require_authenticated_user
from ..auth.schemas import SessionData
# 認証済みユーザーの依存関係をエクスポート
get_current_user = require_authenticated_user
