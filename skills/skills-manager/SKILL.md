---
name: skills-manager
description: 好創整合行銷的 Manus 技能管理工具。當使用者需要盤點所有技能、更新中文管理手冊、查詢技能觸發語意、或判斷技能是否可合併時使用。觸發關鍵語：「盤點技能」、「更新技能手冊」、「哪個技能可以合併」、「技能怎麼呼叫」。
---

# Skills Manager

好創整合行銷的 Manus 技能管理工具，供團隊任何成員使用，提供技能盤點、中文手冊更新與合併判斷的完整工作流。

## 核心資源

- **`scripts/audit_skills.py`**：自動偵測並掃描 skills 目錄（預設為本 repo 內的 `skills/`，亦可 `--skills-dir` 指定），提取 name / description / 檔案清單，輸出 JSON。
- **`references/handbook.md`**：最新版中文技能管理手冊，含判斷時機、關鍵語意觸發句、好創場景對應表。

## 工作流

### 任務 A：查詢某個技能怎麼呼叫

直接讀取 `references/handbook.md`，搜尋對應技能名稱或場景關鍵字。

### 任務 B：全面盤點所有技能（手冊已過期或新增技能後）

1. 執行掃描腳本，取得最新技能清單（腳本會自動偵測 repo 內的 skills 目錄）：
   ```bash
   python skills-manager/scripts/audit_skills.py --output /tmp/skills_audit.json
   ```
2. 讀取 `/tmp/skills_audit.json`，逐一比對各技能的 `description` 欄位。
3. 合併判斷標準（必須同時滿足）：
   - SKILL.md 核心工作流步驟完全相同
   - 觸發條件（description）完全重疊
   - 輸出格式與工具棧相同
4. 更新 `references/handbook.md`，補充新技能的判斷時機與關鍵語意觸發句。

### 任務 C：判斷某兩個技能是否可合併

1. 讀取兩個技能的 SKILL.md 全文。
2. 逐行比對：工作流步驟、觸發條件、輸出格式、使用工具。
3. 只有三項全部相同才建議合併，否則說明功能邊界差異。

## 合併鐵則

**不可因「功能相似」就合併。** 必須是「功能邊界完全重疊」才合併。
已確認唯一可合併的技能對：`web-artifacts-builder` → `artifacts-builder`（SKILL.md 內容 100% 相同）。

## 好創專屬鐵則

任何好創相關任務，開頭說「**這是好創的任務**」，系統自動載入 `haochuang-brand-context`。
詳細的好創業務場景對應表見 `references/handbook.md` 末段。
