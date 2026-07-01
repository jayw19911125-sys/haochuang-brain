---
name: inline-edit-ux-pattern
description: React + tRPC 的 Inline 編輯 UX 標準模板。當使用者說「inline 編輯」、「點擊編輯」、「原地修改」、「點鉛筆圖示編輯」、「hover 顯示編輯按鈕」、「點擊文字直接編輯」、「Enter 確認 Escape 取消」、「失焦自動儲存」時，必須使用此 skill。涵蓋 cancelledRef 防止 Escape 觸發 onBlur 儲存、isEditing state 管理、Enter/Escape/onBlur 三種觸發儲存的完整實作模板。適用於任何需要「不跳頁、不開 Dialog、直接在原位編輯文字」的 React 組件。
---

# Inline 編輯 UX 模板（React + tRPC）

## 什麼是 Inline 編輯？

Inline 編輯是指「不跳頁、不開 Modal，直接點擊文字就能在原位編輯」的 UX 模式。常見場景：

- 卡片標題旁有鉛筆圖示，點擊後文字變成 input
- 表格 cell 點擊後直接可以輸入
- 備註區域點擊後展開 Textarea

**核心交互規則（業界標準）：**
- **Enter** → 確認儲存，關閉編輯模式
- **Escape** → 取消，恢復原值，關閉編輯模式（**不觸發儲存**）
- **失焦（onBlur）** → 自動儲存（等同 Enter）
- **Shift+Enter**（Textarea 專用）→ 換行，不儲存

---

## 核心問題：Escape 後 onBlur 仍觸發儲存

這是 Inline 編輯最常見的 Bug。

**問題根因：** 按下 Escape 時，React 會先觸發 `onKeyDown`，然後因為 input 失去焦點，立即觸發 `onBlur`。如果 `onBlur` 裡有儲存邏輯，就會在 Escape 取消後立即執行儲存，把空字串或修改中的值存進 DB。

**解法：`cancelledRef` flag 模式**

用 `useRef` 建立一個 flag，在 Escape 的 `onKeyDown` 裡**先設 flag**，再關閉編輯模式。`onBlur` 裡檢查 flag，若為 true 則跳過儲存。

**關鍵順序：** `cancelledRef.current = true` 必須在 `setIsEditing(false)` 之前，否則 `onBlur` 在 flag 設定前就已執行。

---

## 完整實作模板

### 單行文字（Input）

```tsx
import { useRef, useState } from "react";
import { Pencil, Check, Loader2 } from "lucide-react";
import { trpc } from "@/lib/trpc";

interface InlineEditTitleProps {
  scriptId: number;
  initialTitle: string | null;
}

export function InlineEditTitle({ scriptId, initialTitle }: InlineEditTitleProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [titleValue, setTitleValue] = useState(initialTitle ?? "");
  const cancelledRef = useRef(false);
  const utils = trpc.useUtils();

  const updateTitle = trpc.script.updateTitle.useMutation({
    onSuccess: () => {
      // 成功後讓相關 query 重新拉取，確保 UI 同步
      utils.script.list.invalidate();
      utils.script.recent.invalidate();
    },
  });

  const handleSave = async () => {
    if (titleValue.trim() === (initialTitle ?? "")) {
      setIsEditing(false);
      return; // 沒有變更，不呼叫 API
    }
    await updateTitle.mutateAsync({ id: scriptId, title: titleValue.trim() });
    setIsEditing(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSave();
    }
    if (e.key === "Escape") {
      cancelledRef.current = true;   // ← 必須先設 flag
      setTitleValue(initialTitle ?? ""); // 恢復原值
      setIsEditing(false);           // ← 再關閉（會觸發 onBlur）
    }
  };

  const handleBlur = () => {
    if (cancelledRef.current) {
      cancelledRef.current = false;  // 重置 flag
      return;                        // 不儲存
    }
    handleSave();
  };

  if (isEditing) {
    return (
      <div className="flex items-center gap-1">
        <input
          autoFocus
          value={titleValue}
          onChange={(e) => setTitleValue(e.target.value)}
          onKeyDown={handleKeyDown}
          onBlur={handleBlur}
          className="border rounded px-2 py-0.5 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
          placeholder="輸入自訂標題..."
          maxLength={255}
        />
        {updateTitle.isPending && (
          <Loader2 className="h-3 w-3 animate-spin text-muted-foreground" />
        )}
      </div>
    );
  }

  return (
    <div
      className="group flex items-center gap-1 cursor-pointer"
      onClick={() => setIsEditing(true)}
    >
      <span className="text-sm text-amber-400/80">
        {initialTitle || "點擊新增標題"}
      </span>
      <Pencil className="h-3 w-3 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
    </div>
  );
}
```

---

### 多行文字（Textarea）

```tsx
import { useRef, useState } from "react";
import { Loader2 } from "lucide-react";
import { Textarea } from "@/components/ui/textarea";
import { trpc } from "@/lib/trpc";

interface InlineEditMemoProps {
  scriptId: number;
  initialMemo: string | null;
}

export function InlineEditMemo({ scriptId, initialMemo }: InlineEditMemoProps) {
  const [memoValue, setMemoValue] = useState(initialMemo ?? "");
  const cancelledRef = useRef(false);
  const utils = trpc.useUtils();

  const updateMemo = trpc.script.updateMemo.useMutation({
    onSuccess: () => {
      utils.script.list.invalidate();
    },
  });

  const handleSave = async () => {
    if (memoValue === (initialMemo ?? "")) return; // 無變更
    await updateMemo.mutateAsync({ id: scriptId, memo: memoValue });
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Escape") {
      cancelledRef.current = true;   // ← 先設 flag
      setMemoValue(initialMemo ?? "");
      e.currentTarget.blur();        // ← 手動觸發 blur（會被 cancelledRef 攔截）
    }
    // Shift+Enter = 換行（預設行為，不攔截）
    // Enter 不儲存（Textarea 中 Enter = 換行）
  };

  const handleBlur = () => {
    if (cancelledRef.current) {
      cancelledRef.current = false;
      return;
    }
    handleSave();
  };

  return (
    <div className="relative">
      <Textarea
        value={memoValue}
        onChange={(e) => setMemoValue(e.target.value)}
        onKeyDown={handleKeyDown}
        onBlur={handleBlur}
        placeholder="新增備註（失焦自動儲存，Escape 取消）..."
        className="min-h-[80px] resize-none text-sm"
      />
      {updateMemo.isPending && (
        <Loader2 className="absolute bottom-2 right-2 h-3 w-3 animate-spin text-muted-foreground" />
      )}
    </div>
  );
}
```

---

## 四件套模式總結

任何 Inline 編輯組件都由這四個部分組成：

| 部分 | 用途 | 關鍵點 |
|------|------|--------|
| `cancelledRef` | 防止 Escape 觸發 onBlur 儲存 | 必須在 `setIsEditing(false)` 之前設為 true |
| `isEditing` state | 控制顯示模式（文字 or input） | 單行用 state，多行 Textarea 通常常駐顯示 |
| `onKeyDown` handler | Enter 確認、Escape 取消 | Textarea 中 Enter 不儲存（Shift+Enter 換行） |
| `onBlur` handler | 失焦自動儲存 | 先檢查 cancelledRef，再執行儲存 |

---

## 常見變體

### 變體一：Hover 顯示鉛筆圖示（最常見）

```tsx
// 顯示模式：文字 + hover 才顯示鉛筆
<div className="group flex items-center gap-1">
  <span>{title || "未設定"}</span>
  <Pencil
    className="h-3 w-3 opacity-0 group-hover:opacity-100 cursor-pointer"
    onClick={() => setIsEditing(true)}
  />
</div>
```

### 變體二：點擊文字直接進入編輯

```tsx
// 顯示模式：整個文字區域可點擊
<span
  className="cursor-text hover:bg-muted/50 rounded px-1"
  onClick={() => setIsEditing(true)}
>
  {title || "點擊編輯"}
</span>
```

### 變體三：儲存中禁用 input

```tsx
<input
  disabled={updateTitle.isPending}
  // ...其他 props
/>
```

---

## 注意事項

- **`autoFocus`**：input 進入編輯模式時加 `autoFocus`，讓使用者不需要再點一次
- **`invalidate` 時機**：mutation 成功後，呼叫 `utils.xxx.invalidate()` 讓相關 query 重新拉取，確保列表頁也同步更新
- **空值處理**：儲存前用 `.trim()` 去除首尾空白；若結果為空字串，視業務需求決定是否允許
- **最大長度**：input 加 `maxLength` 屬性，與 DB schema 的 varchar 長度一致
- **Textarea 的 Enter**：Textarea 中 Enter 是換行，不是確認儲存。若要 Enter 儲存，必須攔截並排除 Shift+Enter
