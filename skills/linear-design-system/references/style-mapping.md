# Linear 設計語言對照表

## 樣式替換速查表

| 舊樣式（廢棄） | 新樣式（Linear 標準） | 用途 |
|---|---|---|
| `brand-gradient` | `border border-border bg-muted/50` | Icon 容器背景 |
| `rounded-xl` | `rounded` | 卡片、容器圓角 |
| `rounded-full`（序號/badge） | `rounded` | 方形序號、標籤 |
| `text-base font-semibold`（CardTitle） | `text-xs font-semibold uppercase tracking-wider font-mono` | CardTitle 標籤 |
| `text-xl font-semibold`（頁面標題） | `text-sm font-semibold tracking-tight` | 頁面主標題 |
| `text-sm text-muted-foreground`（副標題） | `text-[11px] text-muted-foreground font-mono` | 副標題 / 說明文字 |
| `backdrop-blur-sm bg-card/50` | `bg-card border-border` | Card 背景 |
| `h-10 w-10 rounded-lg bg-primary/10`（icon 容器） | `w-7 h-7 rounded border border-border bg-muted/50` | Header icon 容器 |
| `h-10`（按鈕高度） | `h-7`（次要）/ `h-8`（主要 CTA） | 按鈕尺寸 |
| `shadow-sm` / `shadow-md` | `border border-border` | 層次分隔 |
| `<CardDescription>` | `<p className="text-[11px] font-mono text-muted-foreground">` | 卡片副說明 |
| `bg-primary/10`（sidebar active） | `border-l-2 border-primary bg-muted/50` | Sidebar active 狀態 |

## Section Header 標準格式

```tsx
// ✅ Linear 標準 section header
<p className="text-[11px] font-mono uppercase tracking-wider text-muted-foreground mb-3">
  SECTION TITLE
</p>
```

## Icon 容器標準格式

```tsx
// ✅ Linear 標準 icon 容器
<div className="w-7 h-7 rounded border border-border bg-muted/50 flex items-center justify-center">
  <IconName className="w-3.5 h-3.5 text-muted-foreground" />
</div>
```

## Card Header 標準格式

```tsx
// ✅ Linear 標準 CardHeader
<CardHeader className="pb-3">
  <div className="flex items-center gap-2">
    <div className="w-7 h-7 rounded border border-border bg-muted/50 flex items-center justify-center">
      <IconName className="w-3.5 h-3.5 text-muted-foreground" />
    </div>
    <div>
      <CardTitle className="text-xs font-semibold uppercase tracking-wider font-mono text-muted-foreground">
        CARD TITLE
      </CardTitle>
      <p className="text-[11px] text-muted-foreground font-mono">副說明文字</p>
    </div>
  </div>
</CardHeader>
```

## 顏色語義化規則

| 狀態 | 顏色 class | 用途 |
|---|---|---|
| 成功 / 完成 | `text-emerald-500` / `bg-emerald-500/10` | 完成狀態、正向指標 |
| 警告 / 待處理 | `text-amber-500` / `bg-amber-500/10` | 警告狀態、待辦項目 |
| 錯誤 / 危險 | `text-red-500` / `bg-red-500/10` | 錯誤狀態、刪除操作 |
| 資訊 / 中性 | `text-blue-500` / `bg-blue-500/10` | 資訊提示 |
| 主要操作 | `bg-primary text-primary-foreground` | CTA 按鈕 |

## 常見避坑

1. **`backdrop-blur-sm` 在深色主題下讓邊框消失** → 改為 `bg-card border-border`，不使用透明度。
2. **`CardDescription` 不是 Linear 標準組件** → 改用 `<p className="text-[11px] font-mono text-muted-foreground">`。
3. **按鈕尺寸混用** → 統一次要操作 `h-7 text-xs`，主要 CTA `h-8 text-xs`。
4. **數字/統計值** → 加上 `font-mono tabular-nums` 確保數字對齊。
5. **`rounded-full` 用於序號** → 改為 `rounded`，Linear 偏好方塊美學。
