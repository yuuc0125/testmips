# 模擬器專案 README

## 專案概述
本專案旨在開發一個簡單的 MIPS 模擬器，支援流水線執行並處理 Hazard 問題。我們的模擬器包含以下主要功能：
- 支援 R-Type、I-Type 和 Branch 類型指令的執行。
- 提供 Forwarding 和 Stalling 機制以解決資料依賴問題。
- 具備檔案輸入與輸出功能，方便進行測試與結果保存。

---

## 環境需求
- **Python** 版本：3.8 或以上

---

## 專案結構
```
project_directory/
├── inputs/             # 輸入檔案資料夾
│   ├── test1.txt       # 測試用輸入檔案
│   ├── test2.txt
│   ├── test3.txt
│   └── test4.txt
├── outputs/            # 輸出檔案資料夾
│   ├── test1.txt       # 測試用輸出檔案
│   ├── test2.txt
│   ├── test3.txt
│   └── test4.txt
├── src/                # 原始碼資料夾
│   ├── mips_simulator.py # 模擬器的主程式
│   └── ...             # 其他相關程式碼
├── pyproject.toml      # Python 專案配置檔案
└── README.md           # 本說明文件
```

---

## 安裝與執行

### 安裝依賴
本專案不需要額外的外部依賴，確認系統已安裝 Python 3.8 或以上版本即可。

### 執行模擬器
1. 將組合語言指令程式放入 `inputs/` 資料夾。
2. 執行模擬器：
   ```bash
   python src/mips_simulator.py inputs/test1.txt outputs/test1.txt
   ```
3. 結果會被輸出到 `outputs/` 資料夾對應的檔案中。

---

## 測試

1. 測試資料位於 `inputs/` 和 `outputs/` 資料夾。
2. 使用以下指令執行測試：
   ```bash
   python src/tests/run_tests.py
   ```
3. 測試腳本會自動驗證 Forwarding、Hazard 和 Branch 處理的正確性。

---

輸入格式(Input Example 1):

lw $2, 8($0)
lw $3, 16($0)
add $6, $4, $5
sw $6, 24($0)

------------------------------------------------------------------------------------------------------------------------------
輸出格式(Example 1)
# Example 1 Case
## Each clocks
Clock Cycle 1:
lw IF
Clock Cycle 2:
lw ID
lw IF
Clock Cycle 3:
lw EX RegDst=X ALUSrc=X Branch=X MemRead=X MemWrite=X RegWrite=X MemToReg=X
lw ID
add IF
Clock Cycle 4:
lw MEM Branch=X MemRead=X MemWrite=X RegWrite=X MemToReg=X
lw EX RegDst=X ALUSrc=X Branch=X MemRead=X MemWrite=X RegWrite=X MemToReg=X
add ID
sw IF
Clock Cycle 5:
lw WB RegWrite=X MemToReg=X
lw MEM Branch=X MemRead=X MemWrite=X RegWrite=X MemToReg=X
add EX RegDst=X ALUSrc=X Branch=X MemRead=X MemWrite=X RegWrite=X MemToReg=X
sw ID
Clock Cycle 6:
lw WB RegWrite=X MemToReg=X
add MEM Branch=X MemRead=X MemWrite=X RegWrite=X MemToReg=X
sw EX RegDst=X ALUSrc=X Branch=X MemRead=X MemWrite=X RegWrite=X MemToReg=X
Clock Cycle 7:
add WB RegWrite=X MemToReg=X
sw MEM Branch=X MemRead=X MemWrite=X RegWrite=X MemToReg=X
Clock Cycle 8:
sw WB RegWrite=X MemToReg=X

## Final Result:
Total Cycles: 8
Final Register Values:
0 1 1 1 1 1 2 ...
Final Memory Values:
1 1 1 1 1 1 2 ...
```

------------------------------------------------------------------------------------------------------------------------------

## 專案驗收
- 測試部分：
  - 提供 5 組指令檔案，其中 4 組為開放測資，1 組為隱藏測資（驗收時使用）。
- 專案繳交：
  - 繳交期限為 **2025/01/05**。
  - 繳交內容包括：
    - 原始碼
    - 執行檔
    - 專案報告
- 注意事項：
  - 原始碼需可成功編譯，否則不給予分數。
  - 執行檔需可正常執行，否則不給予分數。
  - 成績取決於執行結果數據的正確性以及報告內容。
- 專案報告需包含：
  - 組員間的工作分配。
  - 製作過程中所遇問題及解決方法。
  - 與專案相關的個人心得。

## 測試正確性驗收標準
1. 總 Cycles 數是否正確。
2. 每個 Cycle 中的各指令所在 Stage 與該 Stage 的 Signal 是否正確。
3. 暫存器與記憶體中的值是否正確。

## 輸出要求
1. 各個 Clock Cycle 中，在 CPU 中執行的指令狀態：
   - 顯示各指令在 ID、EX、MEM、WB 階段即將使用的 Signal 值。
   - 包括 Don't Care 的情況。
2. 最後輸出：
   - 執行該段指令所需的總 Cycles 數。
   - 記憶體與暫存器執行後的最終結果。

## 聯絡方式
如有任何問題，請聯繫助教：
- Email: a1105534@mail.nuk.edu.tw