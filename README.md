# 🗒️ MyBlog — Flask 部落格系統

一個以 **Flask** 為核心、搭配 **MySQL** 資料庫的輕量化部落格平台，並整合 **GitHub Actions** 實現 CI/CD 自動化，將 Docker Image 發布至 **GitHub Container Registry (GHCR)**，再透過 **Self-hosted Runner** 自動完成部署。

---

## 📋 目錄

- [技術棧](#-技術棧)
- [專案架構](#-專案架構)
- [功能說明](#-功能說明)
- [資料庫模型](#-資料庫模型)
- [路由一覽](#-路由一覽)
- [CI/CD 流程](#-cicd-流程)
- [快速啟動（Docker Compose）](#-快速啟動docker-compose)
- [本機開發](#-本機開發)
- [環境變數說明](#-環境變數說明)
- [預設帳號](#-預設帳號)

---

## 🛠 技術棧

| 類別 | 技術 |
|------|------|
| Web 框架 | Flask 3.0.3 |
| ORM | Flask-SQLAlchemy 3.1.1 + SQLAlchemy 2.0 |
| 資料庫 | MySQL 8.0 |
| 認證 | Flask-Login 0.6.3 |
| 表單驗證 | Flask-WTF 1.2.1 + WTForms 3.1.2 |
| 密碼加密 | bcrypt 4.2.0 |
| 模板引擎 | Jinja2 3.1.4 |
| 容器化 | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| 映像檔倉庫 | GitHub Container Registry (GHCR) |

---

## 📁 專案架構

```
githib_action_test_blog/
│
├── .github/
│   └── workflows/
│       └── docker-ghcr.yml        # GitHub Actions CI/CD 工作流程
│
├── .gitignore
│
└── myblog/                        # 主應用程式目錄
    ├── main.py                    # 應用程式進入點，負責資料庫初始化
    ├── Dockerfile                 # 多階段 Docker 建構檔
    ├── docker-compose.yaml        # 服務編排設定
    ├── requirements.txt           # Python 相依套件
    │
    ├── routes/                    # 路由層（Controller）
    │   ├── __init__.py            # Flask App 建立、資料庫設定、Blueprint 初始化
    │   ├── user_routes.py         # 前台路由（首頁、登入/登出、文章瀏覽）
    │   └── admin_routes.py        # 後台路由（文章新增/編輯、圖片上傳）
    │
    ├── models/                    # 資料模型層（Model）
    │   ├── user.py                # 使用者模型（User）
    │   └── article.py             # 文章模型（Article），BLOB 儲存內容
    │
    ├── services/                  # 業務邏輯層（Service）
    │   ├── article_service.py     # 文章的 CRUD 操作
    │   ├── user_service.py        # 使用者登入驗證
    │   └── image_service.py       # 圖片清單查詢
    │
    ├── forms/                     # 表單驗證層（Form）
    │   ├── article_form.py        # 文章新增/編輯表單
    │   ├── delete_article_form.py # 刪除文章表單（含 CSRF）
    │   ├── image_upload_form.py   # 圖片上傳表單
    │   └── login_form.py          # 登入表單
    │
    ├── commom/                    # 通用工具模組
    │   ├── profile.py             # 圖片儲存路徑管理（Profile）
    │   └── utils.py               # 檔案命名工具（避免同名覆蓋）
    │
    ├── templates/                 # Jinja2 HTML 模板
    │   ├── base.html              # 基底模板（導覽列、Flash 訊息）
    │   ├── index.html             # 首頁（文章列表）
    │   ├── article.html           # 文章詳情頁
    │   ├── editarticle.html       # 新增/編輯文章頁
    │   ├── images.html            # 圖片管理頁
    │   ├── login.html             # 登入頁
    │   ├── about.html             # 關於頁面
    │   └── includes/              # 可重用模板片段
    │
    ├── assets/                    # 靜態資源
    │   ├── js/                    # JavaScript 檔案
    │   └── plugins/               # 第三方插件
    │
    └── data/
        └── images/                # 使用者上傳的圖片（Volume 掛載）
```

---

## ✨ 功能說明

### 前台功能（所有人可見）

| 功能 | 說明 |
|------|------|
| 📄 文章列表 | 首頁顯示全部文章列表 |
| 📖 文章詳情 | 點擊文章標題後進入單篇文章頁面 |
| ℹ️ 關於頁面 | 靜態關於介紹頁 |
| 🔑 登入 | 管理員帳號登入 |

### 後台功能（需登入）

| 功能 | 說明 |
|------|------|
| ✏️ 新增文章 | 透過表單新增部落格文章 |
| 📝 編輯文章 | 修改已存在的文章標題與內容 |
| 🗑️ 刪除文章 | 從首頁直接刪除指定文章 |
| 🖼️ 圖片上傳 | 上傳圖片至伺服器，並顯示已上傳清單 |
| 🚪 登出 | 安全登出目前使用者 |

---

## 🗄️ 資料庫模型

### `users` 資料表

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | INTEGER (PK) | 主鍵，自動遞增 |
| `username` | VARCHAR(255) | 唯一使用者名稱 |
| `password` | VARCHAR(255) | bcrypt 雜湊後的密碼 |
| `fullname` | VARCHAR(255) | 顯示名稱 |
| `description` | VARCHAR(255) | 個人描述（可為空）|

### `articles` 資料表

| 欄位 | 型別 | 說明 |
|------|------|------|
| `id` | INTEGER (PK) | 主鍵，自動遞增 |
| `title` | VARCHAR(255) | 文章標題（唯一）|
| `content` | BLOB | 文章內容（以 UTF-8 bytes 儲存）|
| `create_time` | TIMESTAMP | 建立時間（自動設定）|
| `update_time` | TIMESTAMP | 更新時間（自動設定）|

> **設計說明**：`Article.content` 欄位以 `BLOB` 儲存，透過 Python `@property` 自動完成 `str ↔ bytes` 的編解碼，對外介面仍為普通字串。

---

## 🌐 路由一覽

### 前台路由（`user_routes.py`）

| 方法 | 路徑 | 說明 |
|------|------|------|
| GET / POST | `/` 或 `/index.html` | 首頁；已登入時支援刪除文章 |
| GET | `/about.html` | 關於頁面 |
| GET / POST | `/login.html` | 登入頁面 |
| GET | `/logout` | 登出並導回首頁 |
| GET | `/article/<article_id>.html` | 單篇文章詳情 |
| GET | `/image/<image_filename>` | 提供已上傳的圖片 |

### 後台路由（`admin_routes.py`，需 `@login_required`）

| 方法 | 路徑 | 說明 |
|------|------|------|
| GET / POST | `/create_article.html` | 新增文章 |
| GET / POST | `/editarticle/<article_id>.html` | 編輯指定文章 |
| GET / POST | `/images.html` | 圖片上傳與管理 |

---

## ⚙️ CI/CD 流程

本專案使用 **GitHub Actions** 實現完整的 CI/CD 自動化，工作流程檔案位於 `.github/workflows/docker-ghcr.yml`。

### 觸發條件

- 推送至 `main` 分支，且變更涉及 `myblog/**` 或 `docker-ghcr.yml`
- 手動觸發（`workflow_dispatch`）

### 工作流程說明

```
Push to main
     │
     ▼
┌─────────────────────────────────┐
│  Job 1: docker (ubuntu-latest)  │
│                                 │
│  1. Checkout 原始碼              │
│  2. 設定 Docker Buildx           │
│  3. 登入 GHCR                   │
│  4. 擷取 Docker Metadata        │
│     - Tag: latest               │
│     - Tag: sha-<commit hash>    │
│  5. 建構並推送 Image 至 GHCR    │
│     （啟用 GitHub Actions Cache）│
└────────────┬────────────────────┘
             │ needs: docker
             ▼
┌─────────────────────────────────┐
│  Job 2: deploy (self-hosted)    │
│                                 │
│  1. Checkout 原始碼              │
│  2. 登入 GHCR                   │
│  3. docker compose pull         │
│     （拉取最新 Image）           │
│  4. docker compose up -d        │
│     （重啟容器）                 │
└─────────────────────────────────┘
```

> **Self-hosted Runner**：部署 Job 執行於自架的 Runner 上，可直接操作目標主機的 Docker 環境，實現零停機更新。

---

## 🚀 快速啟動（Docker Compose）

### 前置需求

- Docker >= 24.x
- Docker Compose >= 2.x

### 啟動步驟

```bash
# 1. Clone 專案
git clone https://github.com/allen900913/githib_action_test_blog.git
cd githib_action_test_blog/myblog

# 2. 啟動所有服務（背景模式）
docker compose up -d

# 3. 查看容器狀態
docker compose ps

# 4. 查看應用程式日誌
docker compose logs -f myblog_server
```

啟動後，在瀏覽器開啟 **http://localhost** 即可訪問部落格。

### 停止服務

```bash
docker compose down
```

### 停止並清除所有資料（Volume）

```bash
docker compose down -v
```

---

## 💻 本機開發

```bash
# 1. 進入應用程式目錄
cd myblog

# 2. 建立並啟動虛擬環境
python -m venv myenv
myenv\Scripts\activate        # Windows
# source myenv/bin/activate   # Linux / macOS

# 3. 安裝相依套件
pip install -r requirements.txt

# 4. 準備本機 MySQL 資料庫，並設定環境變數
set MYSQL_HOST=localhost
set MYSQL_DB=myblog_db
set MYSQL_USER=root
set MYSQL_PWD=your_password

# 5. 啟動應用程式
python main.py
```

---

## 🔧 環境變數說明

| 變數名稱 | 預設值 | 說明 |
|----------|--------|------|
| `MYSQL_HOST` | `localhost` | MySQL 主機位址 |
| `MYSQL_PORT` | `3306` | MySQL 連接埠 |
| `MYSQL_USER` | `root` | MySQL 使用者名稱 |
| `MYSQL_PWD` | `123456` | MySQL 密碼 |
| `MYSQL_DB` | `myblog_db` | MySQL 資料庫名稱 |
| `DB_INIT_MAX_ATTEMPTS` | `20` | 資料庫連線最大重試次數 |
| `DB_INIT_DELAY_SECONDS` | `2` | 每次重試間隔秒數 |

> **啟動邏輯**：應用程式啟動時會以輪詢方式等待 MySQL 就緒，若 `users` 資料表不存在，則自動建立所有資料表，並建立預設管理員帳號。

---

## 👤 預設帳號

| 使用者名稱 | 密碼 | 角色 |
|-----------|------|------|
| `root` | `123456` | 管理員 |

> ⚠️ **安全提醒**：正式環境部署前，請務必修改預設密碼及 `SECRET_KEY`（位於 `routes/__init__.py`）。

---

## 📦 Docker Image

本專案 Image 發布於 GitHub Container Registry：

```
ghcr.io/allen900913/githib_action_test_blog:latest
ghcr.io/allen900913/githib_action_test_blog:sha-<commit>
```

### Dockerfile 說明（多階段建構）

```
Stage 1: builder (python:3.12-alpine)
  └─ 安裝相依套件至獨立 venv
  └─ 複製應用程式原始碼

Stage 2: runtime (python:3.12-alpine)
  └─ 僅複製 venv 與應用程式
  └─ 最小化映像檔體積
  └─ 進入點：python main.py
```

---

## 🏗️ 架構層次說明

本專案採用清晰的 **分層架構（Layered Architecture）**：

```
┌─────────────────────────────────────┐
│           Templates（視圖層）        │  Jinja2 HTML 模板
├─────────────────────────────────────┤
│           Routes（控制層）           │  處理 HTTP 請求 / 回應
├─────────────────────────────────────┤
│           Services（業務層）         │  封裝商業邏輯
├─────────────────────────────────────┤
│           Models（資料層）           │  SQLAlchemy ORM 模型
├─────────────────────────────────────┤
│        MySQL（資料庫）               │  持久化儲存
└─────────────────────────────────────┘
```

| 層次 | 目錄 | 職責 |
|------|------|------|
| 視圖層 | `templates/` | 渲染 HTML 頁面 |
| 控制層 | `routes/` | 接收請求、呼叫 Service、回傳回應 |
| 表單層 | `forms/` | 輸入驗證與 CSRF 保護 |
| 業務層 | `services/` | 執行 CRUD 與業務規則 |
| 資料層 | `models/` | 定義資料表結構 |
| 工具層 | `commom/` | 共用輔助工具（路徑管理、檔名處理）|
