想上來請教 gitlab cicd 相關的問題: https://gitlab.com/phunc20/vina2vi/-/blob/main/.gitlab-ci.yml?ref_type=heads#L65

我自己本身 cicd 的知識不是很深, 第一次在自己的 (python) side project 裡加 cicd, 目前主要的想法是 unit tests 以後, 如果 developer 有改過 version number 且該 version number 新於 PyPi 上現有 package 的 version number, cicd 就會 進行 publish 的步驟.

我有 1 個主要問題和 1 個次要問題:
- 主要: 根據 version numbers 的大小比較, 我需要 script 有不同的 control flow, 如  但是如果一個 control flow 裡頭放太多指令, gitlab-ci visualization 綠色黑色字就不太清楚. 有經驗的各位都是怎麼處理?
    - 在 47 行我有做另一個嚐試，也有試著使用 rules 但失敗收場
- 次要: 我想請教一些一般的建議. 我知道自己 cicd 經驗不足，所以一定寫得不夠好，如果有人有想到增減什麼，還請指教
