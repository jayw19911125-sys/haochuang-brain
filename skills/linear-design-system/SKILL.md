---
name: linear-design-system
description: "將 React/Tailwind 前端頁面重構為 Linear 設計語言風格。使用時機：使用者說「用 Linear 風格更新這個頁面」、「把這個 Card 改成 Linear 樣式」、「統一設計語言」、「移除 brand-gradient」、「介面太花俏要改成工具感」、「設計語言不統一」。核心能力：掃描舊樣式關鍵字、依對照表逐一替換、確保 TypeScript 零錯誤與測試通過。適用於 shadcn/ui + Tailwind CSS 4 專案。"
---

# Linear 設計系統重構技能

## 核心哲學（5 條鐵則）

1. **密度優先**：用 `h-7`、`h-8` 的小按鈕取代 `h-10` 的大按鈕。
2. **邊框取代陰影**：用 `border border-border` 定義層次，不用 `shadow-*` 或 `backdrop-blur`。
3. **等寬字體作為資訊標籤**：`font-mono` + `uppercase` + `tracking-wider` 是 Linear 的 metadata 標準格式。
4. **Icon 容器標準化**：`w-7 h-7 rounded border border-border bg-muted/50`，不再用圓形漸層。
5. **顏色語義化**：accent 色只用於狀態指示（emerald=成功、amber=警告、red=錯誤），不用於裝飾。

## 工作流

### 步驟 1：掃描舊樣式

用以下關鍵字掃描目標檔案：

```bash
grep -n "brand-gradient\|rounded-xl\|backdrop-blur\|CardDescription\|rounded-full\|h-10\|shadow-sm\|shadow-md" <target-file>
```

### 步驟 2：依對照表替換

讀取 `references/style-mapping.md` 取得完整對照表，逐一替換所有命中項目。

**優先順序**（由高到低）：
1. `brand-gradient` → 最顯眼的舊樣式，必須全部清除
2. `CardDescription` → 改為 `<p>` 標籤
3. `backdrop-blur-sm` → 移除透明度
4. `rounded-xl` → 改為 `rounded`
5. 按鈕尺寸 → 統一 `h-7` / `h-8`
6. CardTitle 字體 → 改為 `font-mono uppercase tracking-wider`

### 步驟 3：驗證

```bash
pnpm tsc --noEmit   # TypeScript 零錯誤
pnpm test           # 所有測試通過
```

### 步驟 4：存 checkpoint

完成後存 checkpoint，描述涵蓋「移除 brand-gradient、統一 Linear 設計語言」。

## 快速參考

完整樣式對照表、標準組件模板、顏色語義化規則，見 `references/style-mapping.md`。

## 適用範圍

- shadcn/ui + Tailwind CSS 4 專案
- 深色主題（`defaultTheme="dark"`）
- 有 `DashboardLayout` 的內部工具型應用

## 不適用範圍

- 公開行銷頁面（需要視覺衝擊力，不適合 Linear 極簡風）
- 淺色主題專案（部分 `bg-muted/50` 在淺色下效果不同，需個別調整）
