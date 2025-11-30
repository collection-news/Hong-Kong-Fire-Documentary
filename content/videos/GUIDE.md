# 影片收集指南

本指南說明如何為本專案提交影片片段及其資料。

## 影片命名規則 (Video Naming Convention)

### 影片檔案命名

建議使用以下命名格式：

- **格式**: `YYYY-MM-DD_platform_post-id_video-number.mp4`
- **範例**: `2025-11-26_threads_DRgr4zOgdp7_01.mp4`

### 資料檔命名

每個影片應有對應的中文和英文資料檔，使用 `-zh` 和 `-en` 後綴：

- **中文資料檔格式**: `YYYY-MM-DD_platform_post-id_video-number-zh.md`
- **英文資料檔格式**: `YYYY-MM-DD_platform_post-id_video-number-en.md`
- **範例**:
  - `2025-11-26_threads_DRgr4zOgdp7_01-zh.md` (中文)
  - `2025-11-26_threads_DRgr4zOgdp7_01-en.md` (English)

## 資料檔結構 (Metadata File Structure)

每個影片都有獨立的中文和英文資料檔，包含以下章節：

### 基本資料 (Basic Information)

- 檔案名稱 (File Name)
- 標題 (Title)

### 來源資料 (Source Information)

- 原始網址 (Original URL)
- 來源平台 (Source Platform)
- 發布者 (Publisher)
- 貼文日期 (Post Date)

### 收集資料 (Collection Information)

- **收集時間 (Collection Time)**: 見首次提交時間 (見 git commit) - 自動從 git commit 記錄取得
- **收集方法 (Collection Method)**: 請參閱[主 README 的收集方法選項](../index.md#4-收集方法-collection-method)
- **收集者 (Collector)**: 見首次提交者 (見 git commit) - 自動從 git commit 記錄取得

### 影片描述 (Video Description)

- 簡短描述影片內容、拍攝角度、時間點或關鍵畫面
- 如為 AI 生成，會標註「*由 AI 生成，待補充*」

### 技術資料 (Technical Information)

- 檔案雜湊值 (SHA-256)
- 影片時長 (Duration)
- 解析度 (Resolution)
- 檔案大小 (File Size)

### 備註 (Notes)

- 其他相關資訊，如該影片在貼文中的位置等

## 提交影片時的資料要求

為確保影片可作為有效證據，**每個影片**都應提供以下完整資料：

### 必需資料 (Required Information)

**1. 原始網址 (Original URL)**

- 影片的原始來源網址（如 Threads、Instagram、YouTube 等）
- 如果多個影片來自同一貼文，每個影片都應包含該貼文的完整 URL
- 如來源已失效，請註明並提供備份來源（如 Wayback Machine）

**2. 收集時間 (Collection Time)**

- 將自動從首次提交該檔案的 git commit 時間取得
- 格式：`見首次提交時間 (見 git commit)`

**3. 收集方法 (Collection Method)**

- 請參閱[主 README 的收集方法選項](../index.md#4-收集方法-collection-method)

**4. 影片描述 (Video Description)**

- **必需**：簡短描述影片內容、拍攝角度、時間點或關鍵畫面
- 例如：「從地面拍攝，可見火勢從低層向上蔓延」、「近距離拍攝建築物外牆燃燒情況」
- 如為 AI 生成，請標註「*由 AI 生成，待補充*」

### 可選資料 (Optional Information)

**5. 檔案雜湊值 (File Hash)** [建議]

- 如果下載了影片檔案，建議提供 SHA-256 雜湊值
- Mac/Linux 指令：`shasum -a 256 filename.mp4`
- Windows 指令：`certutil -hashfile filename.mp4 SHA256`

**6. 收集者 (Collector)**

- 將自動從首次提交該檔案的 git commit 作者取得
- 格式：`見首次提交者 (見 git commit)`

**7. 技術資料 (Technical Information)**

- 影片時長、解析度、檔案大小等（如已知）

**8. 備註 (Notes)**

- 其他相關資訊，如該影片在貼文中的位置、是否為轉發等

## 資料檔範例 (Metadata File Example)

### 中文資料檔範例

請參閱：[`2025-11-26_threads_DRgr4zOgdp7_01-zh.md`](./2025-11-26_threads_DRgr4zOgdp7_01-zh.md)

### 英文資料檔範例

請參閱：[`2025-11-26_threads_DRgr4zOgdp7_01-en.md`](./2025-11-26_threads_DRgr4zOgdp7_01-en.md)

## 影片分類方式 (Video Categorization)

影片採用多層級分類方式：

### 第一層：按內容類型分類 (Primary: By Content Type)

- **現場片段 (On-site Footage)**: 市民拍攝的現場影片
- **新聞報道 (News Reports)**: 媒體報道及新聞片段
- **官方聲明 (Official Statements)**: 政府、消防處等官方發布的影片
- **訪問 (Interviews)**: 目擊者、官員、專家訪問
- **分析影片 (Analysis Videos)**: 技術分析、專家解說影片
- **後續紀錄 (Aftermath Documentation)**: 火災後續的紀錄影片

### 第二層：按來源平台分類 (Secondary: By Source Platform)

在每個內容類型下，再按來源平台分類：

- Threads、Instagram、YouTube、Facebook 等社交媒體
- 新聞媒體網站（HK01、Now 新聞、RTHK 等）
- 官方網站（政府新聞網、消防處等）

### 第三層：按日期排序 (Tertiary: By Date)

最後按日期排序，方便按時序查找。

### 範例結構 (Example Structure)

```
## 現場片段 (On-site Footage)
  ### Threads 來源
    - 2025-11-26 - Threads (@striking_biking)
  ### Instagram 來源
    - (待補充)
## 新聞報道 (News Reports)
  ### HK01
    - (待補充)
```
