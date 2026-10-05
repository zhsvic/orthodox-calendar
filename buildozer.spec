[app]

# (str) Название вашего приложения на экране телефона
title = Orthodox Calendar

# (str) Имя пакета
package.name = orthodox_calendar

# (str) Домен пакета
package.domain = org.orthodox

# (str) Директория с исходным кодом (main.py)
source.dir = .

# (list) Расширения файлов, которые будут включены в APK
source.include_exts = py,png,jpg,kv,atlas

# (str) Версия приложения
version = 1.0

# (list) Зависимости приложения (УДАЛЕН встроенный datetime)
requirements = python3, kivy, sqlite3, requests, urllib3, certifi, idna, charset-normalizer

# (str) Экран загрузки (presplash) приложения
presplash.filename = %(source.dir)s/nino.png

# (str) Иконка приложения
icon.filename = %(source.dir)s/cross.png

# (list) Поддерживаемая ориентация экрана
orientation = portrait

# ==========================================
# Настройки для Android
# ==========================================

# (bool) Полноэкранный режим (0 — показывать статус-бар сверху, 1 — скрыть)
fullscreen = 0

# (list) Разрешения Android (ДОБАВЛЕН ИНТЕРНЕТ для сетевых библиотек)
android.permissions = android.permission.INTERNET

# (int) Целевая версия Android API (соответствует требованиям Google Play)
android.api = 33

# (int) Минимальная поддерживаемая версия Android (Android 7.0)
android.minapi = 24

# (str) Версия Android NDK (25b рекомендована для стабильной сборки)
android.ndk = 25b

# Добавлено Найдите строку с архитектурами (если её нет, добавьте в секцию [app])
android.archs = arm64-v8a

# (bool) Автоматически принимать лицензии SDK при сборке в GitHub Actions
android.accept_sdk_license = True

# (str) Формат сборки (debug для тестирования)
android.release_artifact = apk

# ==========================================
# Настройки логов и архитектуры
# ==========================================

# (int) Уровень логирования Buildozer
log_level = 2

# (int) Предупреждать о сборке от имени root (в GitHub Actions это нормально)
warn_on_root = 1

#[buildozer]
# (str) Путь к глобальной директории buildozer
#buildozer_dir = ./.buildozer
