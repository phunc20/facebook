### 這個資料夾是源自於下面兩個連接
- [https://www.facebook.com/groups/pythontw/permalink/10160992441463438/](https://www.facebook.com/groups/pythontw/permalink/10160992441463438/)
- [https://github.com/TritonHo/slides/blob/master/introToAlgorithm.pdf?fbclid=IwAR3W54V7n_bsfiQuWTTqskj7KyrTAYFSPoAUthXKjV5CxlsZUq9LerIILzI](https://github.com/TritonHo/slides/blob/master/introToAlgorithm.pdf?fbclid=IwAR3W54V7n_bsfiQuWTTqskj7KyrTAYFSPoAUthXKjV5CxlsZUq9LerIILzI)
大抵上是網友 TritonHo 寫了一篇講義, 解釋說如果是他來做 10k 個經緯度座標的 nearest neighbor 的話, 他會選擇用兩個 for loop 簡單地解決, 取代任何複雜的演算法或資料結構.
他的論點是 10k 太少了, 不足以造成威脅, 大概 1 秒就能跑完.

出於好奇是否真的 10k 太少, 我作了個實驗在 `./01_timeit.ipynb` 里.

**Rmk.** 我有把講義下載下來在本資料夾里, 就是 `./introToAlgorithm.pdf`.
