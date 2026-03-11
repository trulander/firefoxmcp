# FoxMCP: Автоматизация Firefox через протокол MCP (Model Context Protocol)
[![English](https://img.shields.io/badge/lang-English-blue)](README.md)

Полноценный Docker-стек для управления реальным браузером Firefox через протокол MCP. Проект предоставляет GUI доступ через noVNC и мощный HTTP-эндпоинт для ИИ-агентов.

## Возможности
- **Реальный браузер Firefox**: Firefox ESR работает в режиме с графическим интерфейсом внутри Xvfb.
- **Доступ через noVNC**: Визуальный доступ к браузеру через веб (без пароля).
- **Расширение FoxMCP**: Предустановленное и настроенное расширение для браузера.
- **MCP HTTP Сервер**: Сервер на базе FastMCP, предоставляющий 35 инструментов для автоматизации.
- **Интеграционные тесты**: Встроенный набор тестов с использованием Pytest и UV для проверки всего стека.

## Архитектура
- **Сервис: `firefox`**: Запускает X11, Firefox и noVNC.
- **Сервис: `foxmcp`**: Python-сервер, который транслирует MCP-запросы в расширение Firefox через WebSockets.
- **Сервис: `tester`**: Эфемерный контейнер для запуска интеграционных тестов. Все файлы, относящиеся к тестам (`pyproject.toml`, `uv.lock`, тесты), находятся в директории `tests/`.

## Порты и назначение
| Порт | Сервис | Назначение |
|------|---------|---------|
| `6080` | `firefox` | Веб-интерфейс noVNC (http://localhost:6080/vnc_lite.html) |
| `3000` | `foxmcp` | MCP HTTP эндпоинт (http://localhost:3000/mcp) |
| `8765` | `foxmcp` | Внутренний порт WebSocket для связи с расширением |

## Развертывание

1. **Запуск стека**:
   ```bash
   docker compose up --build -d
   ```

2. **Запуск тестов**:
   ```bash
   docker compose up --build tester
   ```

## Полный список MCP инструментов (35 инструментов)

### Управление окнами
- `list_windows`: Список всех окон браузера и вкладок.
- `get_window`: Информация о конкретном окне.
- `get_current_window`: Получить текущее активное окно.
- `get_last_focused_window`: Получить последнее окно в фокусе.
- `create_window`: Создать новое окно (поддержка размера, позиции, инкогнито).
- `close_window`: Закрыть конкретное окно.
- `focus_window`: Вывести окно на передний план и сфокусировать.
- `update_window`: Обновить свойства окна (состояние, размер, позиция).

### Управление вкладками
- `tabs_list`: Список всех открытых вкладок с индикаторами статуса.
- `tabs_create`: Создать новую вкладку с URL.
- `tabs_close`: Закрыть конкретную вкладку.
- `tabs_switch`: Переключиться на конкретную вкладку.
- `tabs_capture_screenshot`: Сделать скриншот видимой вкладки (base64 или файл).

### Навигация
- `navigation_go_to_url`: Перейти по URL в вкладке.
- `navigation_back`: Перейти назад по истории.
- `navigation_forward`: Перейти вперед по истории.
- `navigation_reload`: Перезагрузить страницу (поддержка сброса кэша).

### Взаимодействие с контентом
- `content_get_text`: Извлечь весь текст со страницы вкладки.
- `content_get_html`: Получить полный HTML-код страницы.
- `content_execute_script`: Выполнить произвольный JavaScript в вкладке.
- `content_execute_predefined`: Выполнить предустановленный внешний скрипт.

### История и Закладки
- `history_query`: Поиск по истории браузера с фильтрами по времени.
- `history_get_recent`: Получить последние элементы истории.
- `history_delete_item`: Удалить конкретный элемент истории по URL.
- `bookmarks_list`: Список всех закладок (папки и элементы).
- `bookmarks_search`: Поиск конкретных закладок.
- `bookmarks_create`: Создать новую закладку.
- `bookmarks_create_folder`: Создать новую папку закладок.
- `bookmarks_update`: Обновить заголовок или URL закладки.
- `bookmarks_delete`: Удалить закладку.

### Мониторинг сети
- `requests_start_monitoring`: Начать мониторинг сетевых запросов (JSON/Text) по паттернам URL.
- `requests_stop_monitoring`: Остановить мониторинг с завершением текущих запросов.
- `requests_list_captured`: Список сводок перехваченных запросов.
- `requests_get_content`: Получить полное тело запроса/ответа по ID.

### Отладка
- `debug_websocket_status`: Получить информацию о статусе соединения с расширением.

## Внешние ресурсы
- **FoxMCP Расширение и Сервер**: [ThinkerYzu/foxmcp](https://github.com/ThinkerYzu/foxmcp)
- **noVNC**: [novnc/noVNC](https://github.com/novnc/noVNC)
- **websockify**: [novnc/websockify](https://github.com/novnc/websockify)

## Использование в Claude/Cursor
Добавьте следующее в настройки MCP серверов:
```json
{
  "mcpServers": {
    "firefox": {
      "type": "http",
      "url": "http://localhost:3000/mcp"
    }
  }
}
```
