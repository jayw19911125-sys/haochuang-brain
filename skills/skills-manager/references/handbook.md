# 好創整合行銷 — Manus 技能管理手冊

> 本手冊基於 58 個 SKILL.md 原始碼逐行比對，將所有技能轉化為「判斷時機」與「關鍵語意觸發句」。

---

## 核心觀念

你不需要記住任何技能名稱，也不需要說出完整句子。**只要說出關鍵語意，系統自動判斷並調用對應技能。**

**好創專屬鐵則**：任何好創相關任務，開頭說「**這是好創的任務**」，系統自動載入品牌語氣、定價邏輯、組織架構與工具棧。

---

## 常見錯誤對照

| 錯誤說法 | 正確關鍵語意 |
|---|---|
| 「請使用 imagegen 技能幫我畫圖」 | 「幫我畫一張圖，**用途是...**」 |
| 「請用 excel-generator 處理」 | 「幫我做一份**給老闆看的** Excel 報表」 |
| 「請幫我 debug」 | 「找出**根本原因**，不要只修表面」 |
| 「幫我寫社群貼文」 | 「**這是好創的任務**，幫我寫貼文」 |

---

## 合併結論

58 個技能逐行比對後，**確認只有 1 對可完全合併**：

| 廢棄 | 合併至 | 依據 |
|---|---|---|
| `web-artifacts-builder` | `artifacts-builder` | SKILL.md 內容 100% 相同，僅標題不同 |

其他看似重疊的技能均有功能邊界差異，不可合併。

---

## 技能速查表

### 【好創專屬核心】

| 技能 | 什麼時候用 | 關鍵語意觸發句 |
|---|---|---|
| `haochuang-brand-context` | 任何好創任務 | **「這是好創的任務」** |
| `marketing-ai-workflow` | 需要大量內容產出並同步到 Monday.com / Slack | **「依照好創的 AI 內容工作流產出...」** |
| `reels-script-writer` | 要拍短影音，目標是賣東西或衝流量 | **「寫一支高轉換率的 Reels 腳本」** |

---

### 【視覺與影音設計】

| 技能 | 什麼時候用 | 關鍵語意觸發句 |
|---|---|---|
| `imagegen` | 不確定要用哪種方式做圖時，讓系統判斷 | **「幫我做一張圖，用途是...」** |
| `generate-image` | 明確要 AI 生成圖片（照片、插畫） | **「AI 生成一張...風格的圖片」** |
| `video-generator` | 從零產出一支完整 AI 影片 | **「製作一支 AI 廣告影片，主題是...」** |
| `canvas-design` | 需要有設計感的主視覺海報，不是隨機 AI 產圖 | **「設計一張主視覺海報，設計哲學是...」** |
| `algorithmic-art` | 需要用程式碼生成互動式網頁藝術 | **「用 p5.js 生成一個互動藝術特效」** |
| `manim-animator` | 需要解釋複雜邏輯，要 3Blue1Brown 風格動畫 | **「用 Manim 製作一支動畫解釋...」** |
| `music-prompter` | 需要 AI 生成音樂，但不知道怎麼下指令 | **「生成一段...情境的背景音樂」** |
| `brand-guidelines` | 需要確保產出符合特定品牌的色彩與字體規範 | **「依照品牌規範調整視覺」** |

---

### 【市場與商業研究】

| 技能 | 什麼時候用 | 關鍵語意觸發句 |
|---|---|---|
| `deep-research` | 需要有引用來源的深度調查報告 | **「深度研究...市場，附引用來源」** |
| `market-research-reports` | 需要給老闆或投資人看的頂級市場報告 | **「生成一份顧問等級的市場研究報告」** |
| `competitive-ads-extractor` | 想知道競品在 Facebook 下什麼廣告 | **「提取並分析...品牌的競品廣告」** |
| `lead-research-assistant` | 需要找潛在客戶名單與開發策略 | **「找出...產業的潛在客戶名單」** |
| `meta-ads-analyzer` | Meta 廣告數據看不懂，需要專家診斷 | **「診斷我的 Meta 廣告，找出根本問題」** |

---

### 【辦公室與文件處理】

| 技能 | 什麼時候用 | 關鍵語意觸發句 |
|---|---|---|
| `excel-generator` | 需要排版精美、有洞察結論的 Excel 報表 | **「做一份給老闆看的專業 Excel 報表」** |
| `xlsx` | 需要修復公式、轉換格式、處理大量數據 | **「修復/轉換/計算這個 Excel 檔案」** |
| `pptx` | 需要建立或修改 PowerPoint 簡報 | **「把這份內容做成 PPT 簡報」** |
| `scientific-slides` | 需要學術發表或論文答辯用的嚴謹簡報 | **「製作學術研討會用的簡報」** |
| `pptx-posters` | 需要一張可以後續修改的活動大海報 | **「設計一張可匯出成 PPTX 的海報」** |
| `latex-posters` | 需要學術會議用的 A0 精準排版海報 | **「用 LaTeX 製作學術會議海報」** |
| `docx` | 需要精確控制 Word 文件格式或批量取代 | **「編輯/修改這份 Word 文件」** |
| `pdf` | 需要合併、分割、OCR、加浮水印 PDF | **「對這個 PDF 進行...操作」** |
| `markitdown` | 需要把任何格式（PDF/影片/音頻）轉成純文字 | **「把這個...格式轉成 Markdown 文字」** |
| `file-organizer` | 資料夾太亂，需要自動分類整理 | **「幫我整理這個資料夾，自動分類」** |
| `invoice-organizer` | 有一堆發票收據需要辨識、命名、做報表 | **「整理這些發票，自動辨識並做成報表」** |
| `raffle-winner-picker` | 需要公平抽獎且能證明過程透明 | **「從這份名單公平抽出...名得獎者」** |

---

### 【系統自動化與整合】

| 技能 | 什麼時候用 | 關鍵語意觸發句 |
|---|---|---|
| `automation-and-scheduling` | 想做自動化系統，但不知道用哪種架構 | **「評估這個自動化需求的最佳架構」** |
| `persistent-computing` | 需要 24 小時不關的服務，不知道租哪種主機 | **「評估這個服務應該部署在哪種環境」** |
| `manus-config` | 需要設定 Manus 連接器或排程任務 | **「設定一個每天...點自動執行的排程」** |
| `manus-api` | 需要寫程式控制 Manus 平台 | **「透過 Manus API 程式化建立...」** |
| `connect` | 需要直接在外部 App 執行動作（不是給草稿） | **「直接幫我在...App 執行...操作」** |

---

### 【開發與除錯】

| 技能 | 什麼時候用 | 關鍵語意觸發句 |
|---|---|---|
| `brainstorming` | 有模糊想法，需要討論出具體設計規格 | **「先陪我腦力激盪，再開始開發」** |
| `scientific-brainstorming` | 需要生成研究假設或跨學科創新觀點 | **「針對...研究領域進行科學腦力激盪」** |
| `writing-plans` | 寫程式前需要極度詳細的原子化實作計畫 | **「先寫一份詳細的實作計畫，再動手」** |
| `doc-coauthoring` | 需要寫重要文件，且要通過讀者測試 | **「陪我協作撰寫這份文件，並做讀者測試」** |
| `executing-plans` | 已有實作計畫，需要逐步確實執行 | **「載入並執行這份實作計畫」** |
| `systematic-debugging` | 程式一直報錯，需要找根本原因 | **「系統化找出根本原因，不要只修表面」** |
| `receiving-code-review` | 收到 Code Review，需要評估建議是否合理 | **「評估這份 Code Review 是否正確」** |
| `finishing-a-development-branch` | 開發完成，需要跑測試並合併分支 | **「跑完測試，推上 GitHub 並建立 PR」** |
| `verification-before-completion` | （系統防呆機制，自動觸發，無需呼叫） | — |
| `plugin-authoring` | 需要開發或修改 Claude Code Plugin | **「開發一個 Claude Code Plugin，功能是...」** |
| `vercel-react-best-practices` | 需要優化 React/Next.js 效能 | **「依照 Vercel 最佳實踐優化這段程式碼」** |
| `artifacts-builder` | 需要複雜互動式網頁工具，打包成單一 HTML | **「用 React + Tailwind 開發一個互動工具」** |
| `d3-viz` | 需要高度客製化、可互動的複雜網頁圖表 | **「用 D3.js 製作一個互動式...圖表」** |
| `matplotlib` | 需要精確的科學統計圖表，輸出高解析度圖片 | **「用 matplotlib 畫一張...圖，輸出高畫質 PNG」** |
| `postgres` | 需要安全唯讀查詢 PostgreSQL 資料庫 | **「安全查詢這個 PostgreSQL 資料庫」** |
| `langsmith-fetch` | AI Agent 出錯，需要抓底層執行記錄 | **「從 LangSmith 抓執行追蹤記錄來分析錯誤」** |
| `developer-growth-analysis` | 想知道自己的開發盲點並獲得學習建議 | **「分析我的開發記錄，找出常犯的錯誤模式」** |

---

### 【工具管理】

| 技能 | 什麼時候用 | 關鍵語意觸發句 |
|---|---|---|
| `github-gem-seeker` | 想先找 GitHub 現成開源工具再動手 | **「先去 GitHub 找有沒有現成工具解決...」** |
| `internet-skill-finder` | 想找 Manus 有沒有現成擴充技能可安裝 | **「找找看有沒有適合...的 Manus 技能」** |
| `skill-creator` | 想自己建立一個新的 Manus 技能 | **「建立一個新的 Manus 技能，功能是...」** |
| `writing-skills` | 寫技能文件，確保 AI 看得懂會照做 | **「用 TDD 方法論優化這個技能文件」** |
| `article-extractor` | 只要網頁文章內容，不要廣告和選單 | **「提取這個網址的乾淨文章內容」** |
| `gws-best-practices` | 要用指令操作 Google Workspace，怕出錯 | **「操作 Google Drive/Docs/Sheets，先確認最佳實踐」** |

---

## 好創業務場景對應表

| 場景 | 執行順序 |
|---|---|
| 撰寫客戶提案/報價單 | `haochuang-brand-context` → `doc-coauthoring` |
| 製作 Reels 腳本 | `haochuang-brand-context` → `reels-script-writer` |
| SEO 文章批量產出 | `haochuang-brand-context` → `deep-research` → `marketing-ai-workflow` |
| 社群內容日曆規劃 | `haochuang-brand-context` → `marketing-ai-workflow` → `excel-generator` |
| 競品廣告分析 | `competitive-ads-extractor` → `excel-generator` |
| Meta 廣告成效診斷 | `meta-ads-analyzer` → `excel-generator` |
| 潛在客戶名單開發 | `lead-research-assistant` → `excel-generator` |
| 市場趨勢報告（給老闆/投資人） | `deep-research` → `market-research-reports` |
| 社群貼文配圖 | `imagegen` → `generate-image` |
| 品牌主視覺海報 | `brand-guidelines` → `canvas-design` |
| 全套 AI 廣告影片 | `video-generator` → `music-prompter` |
| 商業模式/漏斗動畫 | `manim-animator` |
| 企劃書轉簡報 | `docx` → `pptx` |
| 學術/嚴謹型簡報 | `scientific-slides` |
| 可修改的活動大海報 | `pptx-posters` |
| 整理發票收據 | `invoice-organizer` → `xlsx` |
| 整理電腦資料夾 | `file-organizer` |
| 公平線上抽獎 | `xlsx` → `raffle-winner-picker` |
| 規劃自動化機器人 | `automation-and-scheduling` → `manus-config` |
| 架設 24 小時內部工具 | `persistent-computing` → `artifacts-builder` |
| 找不出程式 Bug 根本原因 | `systematic-debugging` → `langsmith-fetch` |
| 想用現成開源工具省時間 | `github-gem-seeker` → `executing-plans` |
