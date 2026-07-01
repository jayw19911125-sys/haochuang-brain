---
name: db-schema-iteration-sop
description: Drizzle ORM + tRPC 全端專案的 DB 欄位迭代標準作業流程。當使用者說「新增欄位」、「加一個欄位」、「DB 要加」、「schema 要改」、「加個 memo 欄位」、「加個 title 欄位」、「資料庫要新增」時，必須使用此 skill。涵蓋從 schema.ts 修改、migration 執行、db.ts helper 新增、routers.ts 路由更新、前端 select 物件同步，到 TypeScript 零錯誤驗證的完整六步驟 Checklist。適用於任何使用 Drizzle ORM + MySQL/TiDB + tRPC + React 架構的 Manus WebDev 專案。
---

# DB 欄位迭代 SOP（Drizzle + tRPC 全端）

## 為什麼需要這個 SOP？

在 Drizzle ORM + tRPC 架構中，新增一個 DB 欄位不只是「改 schema」這麼簡單。它牽動四個層次：

1. **DB 層**：schema.ts 定義欄位 → migration 推送到資料庫
2. **後端 helper 層**：db.ts 新增對應的 CRUD helper
3. **API 層**：routers.ts 新增路由，並更新 `db.select({...})` 物件
4. **前端型別層**：tRPC 的型別推斷依賴 `select` 物件，漏加欄位 = 前端 TypeScript 報錯

任何一層漏掉，都會導致「DB 有資料但前端讀不到」或「TypeScript 編譯失敗」。

---

## 六步驟 Checklist

### Step 1：編輯 `drizzle/schema.ts`

在對應的 table 定義中加入新欄位：

```ts
// 常見欄位型別範例
title: varchar("title", { length: 255 }),           // 短文字，有長度限制
memo: text("memo"),                                   // 長文字，無長度限制
isPublished: boolean("isPublished").default(false),  // 布林值
sortOrder: int("sortOrder").default(0),              // 整數
```

**欄位型別選擇原則：**
- 標題、名稱、標籤 → `varchar(255)` 或 `varchar(512)`
- 備註、描述、內容 → `text`（長度不可預測時一律用 text）
- 狀態、旗標 → `boolean` 或 `mysqlEnum`
- 數字、排序 → `int` 或 `decimal`

**Nullable vs Not Null：**
- 新欄位加入現有表格時，若表格已有資料，**必須設為 nullable 或提供 default**，否則 migration 會失敗
- 語法：`.default(null)` 或直接不加 `.notNull()`

---

### Step 2：執行 `pnpm db:push`

```bash
pnpm db:push
```

這個指令等同於 `drizzle-kit generate && drizzle-kit migrate`，會：
1. 根據 schema.ts 的變更生成 migration SQL
2. 將 migration 推送到遠端資料庫（MySQL/TiDB）

**常見錯誤排查：**
- `Column cannot be null` → 新欄位未設 default，且表格已有資料 → 加 `.default(null)` 或 `.default('')`
- `Connection refused` → DATABASE_URL 環境變數未設定 → 確認 `.env` 或 Manus secrets

---

### Step 3：在 `server/db.ts` 新增 helper

每個新欄位通常需要對應的 update helper：

```ts
// 範例：updateScriptTitle
export async function updateScriptTitle(
  id: number,
  userId: number,
  title: string
): Promise<void> {
  const db = await getDb();
  if (!db) return;

  await db
    .update(scripts)
    .set({ title })
    .where(and(eq(scripts.id, id), eq(scripts.userId, userId)));
}
```

**安全原則：**
- update helper 必須同時驗證 `id` 和 `userId`（或 `openId`），防止越權修改
- 不要只用 `id` 做 WHERE 條件

---

### Step 4：在 `server/routers.ts` 新增路由

```ts
// 在對應的 router 中加入
updateTitle: protectedProcedure
  .input(z.object({
    id: z.number(),
    title: z.string().max(255),
  }))
  .mutation(async ({ ctx, input }) => {
    await updateScriptTitle(input.id, ctx.user.id, input.title);
    return { success: true };
  }),
```

**同時更新 import：**
```ts
// 在 routers.ts 頂部的 import 中加入新 helper
import { updateScriptTitle, updateScriptMemo } from "./db";
```

---

### Step 5：更新所有相關路由的 `db.select({...})` 物件

**這是最容易遺漏的步驟。**

tRPC 的型別推斷完全依賴 `db.select({...})` 的物件定義。如果 `list` 或 `get` 路由的 select 物件沒有加入新欄位，前端 TypeScript 型別不會包含該欄位，即使 DB 已有資料也無法讀取。

```ts
// ❌ 錯誤：新欄位沒有加入 select 物件
const scripts = await db.select({
  id: scripts.id,
  clientName: scripts.clientName,
  // title 和 memo 沒有加 → 前端型別不包含這兩個欄位
}).from(scripts)

// ✅ 正確：明確列出所有需要的欄位
const scripts = await db.select({
  id: scripts.id,
  clientName: scripts.clientName,
  title: scripts.title,   // ← 必須明確加入
  memo: scripts.memo,     // ← 必須明確加入
}).from(scripts)
```

**搜尋需要更新的路由：**
```bash
# 找出所有使用 db.select 的路由
grep -n "db.select" server/routers.ts
```

---

### Step 6：TypeScript 零錯誤驗證

```bash
npx tsc --noEmit
```

確認輸出為空（零錯誤）才算完成。常見錯誤：

| 錯誤訊息 | 原因 | 修正 |
|----------|------|------|
| `Property 'title' does not exist` | select 物件未加入 title | Step 5 補加 |
| `Cannot find name 'updateScriptTitle'` | import 未更新 | Step 4 補 import |
| `Type 'string \| null' is not assignable to type 'string'` | nullable 欄位未做 null 處理 | 前端加 `?? ''` |

---

## 完整流程圖

```
schema.ts 加欄位
       ↓
pnpm db:push（推送 migration）
       ↓
db.ts 加 helper（含 userId 驗證）
       ↓
routers.ts 加路由 + 更新 import
       ↓
所有相關路由的 select 物件同步更新
       ↓
npx tsc --noEmit（零錯誤）✅
```

---

## 快速參考：欄位型別對照表

| 用途 | Drizzle 型別 | 範例 |
|------|-------------|------|
| 短標題/名稱 | `varchar("col", { length: 255 })` | `title`, `name`, `tag` |
| 長文字/備註 | `text("col")` | `memo`, `description`, `content` |
| 布林旗標 | `boolean("col").default(false)` | `isPublished`, `isDeleted` |
| 整數/排序 | `int("col").default(0)` | `sortOrder`, `count` |
| 時間戳記 | `timestamp("col").defaultNow()` | `createdAt`, `updatedAt` |
| 枚舉狀態 | `mysqlEnum("col", ["a","b","c"])` | `status`, `role` |
| 外鍵 ID | `int("col")` + relation | `userId`, `scriptId` |

---

## 注意事項

- **不要用 `db.select()` 不帶參數**：雖然會回傳所有欄位，但 TypeScript 型別推斷不精確，且效能較差（多傳不必要的資料）
- **migration 是不可逆的**：刪除欄位前確認沒有程式碼依賴，且已備份資料
- **pnpm test 驗證**：每次 schema 變更後執行 `pnpm test`，確認現有測試仍通過
