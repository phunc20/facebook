- [https://www.facebook.com/groups/pythontw/permalink/10161017917533438](https://www.facebook.com/groups/pythontw/permalink/10161017917533438)

網友 Yang Wang 問了一個關於 logistic regression using stochastic gradient descent 如何 debug 他自己寫的 code 的問題. 他沒有附上 source code, 只有截圖,
截圖我放在 `./figs/` 里.

主要因為我覺得這個東西我應該不能說不會, 所以決定一起來看看問題出在哪裡. 結果是我必須改用另一個 dataset, 因為他原本的 dataset 是 NLP 那邊來的問題 (Stanford
Mr. Jurafsky 的課程), 我不清楚也沒時間做該 dataset 的前處理. 所以我改用簡單的 iris dataset 跑跑看. 目前還沒有定論;  我做的實驗記錄在 `./*.ipynb` 里.
