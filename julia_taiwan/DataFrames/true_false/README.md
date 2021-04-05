# Origin
The original question asked by user 黃逸華 was as follows.

> 請問一個 DataFrames 的問題（v1.6）
  using Pkg
  using DataFrames
  df = DataFrame(A=1:10, B=2:2:20)
  df[:,:Names] = ["A","A","A","B","C","B", "A","B","C","A"]
  //條件A
  df[(df[:, :Names] .== "A"), :]
  //條件B
  df[(df[:, :B] .>4), 🙂
  //兩個條件組合就報錯
  df[(df[:, :Names] .== "A") & (df[:, :B] .>4), 🙂
  ---
  julia> df[(df[:, :Names] .== "A") & (df[:, :B] .>4), 🙂
  ERROR: MethodError: no method matching &(::BitVector, ::BitVector)     
  Closest candidates are:
   &(::Any, ::Any, ::Any, ::Any...) at operators.jl:560
  Stacktrace:
   [1] top-level scope
     @ REPL[69]:1
  請問何解？
  另，
  我按照YouTube /stackoverflow 的範例更是錯
  df[df[:Names] .=="A",:]


And a solution by using **`.&`** was immediately proposed
by user 杜岳華.
```julia
julia> (df[:Names] .== "A") & (df[:B] .> 4)
ERROR: MethodError: no method matching &(::BitArray{1}, ::BitArray{1})
Closest candidates are:
  &(::Any, ::Any, ::Any, ::Any...) at operators.jl:538
Stacktrace:
 [1] top-level scope at REPL[34]:1

julia> (df[:Names] .== "A") .& (df[:B] .> 4)
10-element BitArray{1}:
 0
 0
 1
 0
 0
 0
 1
 0
 0
 1

julia> df[(df[:Names] .== "A") .& (df[:B] .> 4), :]
3×3 DataFrame
│ Row │ A     │ B     │ Names  │
│     │ Int64 │ Int64 │ String │
├─────┼───────┼───────┼────────┤
│ 1   │ 3     │ 6     │ A      │
│ 2   │ 7     │ 14    │ A      │
│ 3   │ 10    │ 20    │ A      │

```


## My Own Questions
01. Diff btw `BitArray{1}` and `Array{Bool,1}`
    ```julia
    julia> x = [true, false, false]
    3-element Array{Bool,1}:
     1
     0
     0
    
    julia> df[:, :Names] .== "A"
    10-element BitArray{1}:
     1
     1
     1
     0
     0
     0
     1
     0
     0
     1

     julia> eltype(x)
     Bool
     
     julia> eltype(df[:, :Names] .== "A")
     Bool
    ```
01. `&&` and `&`
    ```julia
    julia> df[(df[:Names] .== "A") .& (df[:B] .> 4), :]
    3×3 DataFrame
    │ Row │ A     │ B     │ Names  │
    │     │ Int64 │ Int64 │ String │
    ├─────┼───────┼───────┼────────┤
    │ 1   │ 3     │ 6     │ A      │
    │ 2   │ 7     │ 14    │ A      │
    │ 3   │ 10    │ 20    │ A      │
    
    julia> df[(df[:Names] .== "A") .&& (df[:B] .> 4), :]
    ERROR: syntax: invalid syntax &((df[:B] .> 4)) around REPL[37]:1
    Stacktrace:
     [1] top-level scope at REPL[37]:1
    
    julia> @which true & false
    &(x::Bool, y::Bool) in Base at bool.jl:40
    
    julia> @edit &&
    ERROR: syntax: invalid identifier name "&&"
    Stacktrace:
     [1] top-level scope at none:1
    
    julia> @which &&
    ERROR: syntax: invalid identifier name "&&"
    Stacktrace:
     [1] top-level scope at none:1
    
    julia> @which true && true
    ERROR: expression is not a function call, or is too complex for @which to analyze; break it down to simpler parts if possi
    ble. In some cases, you may want to use Meta.@lower.
    Stacktrace:
     [1] error(::String) at ./error.jl:33
     [2] top-level scope at REPL[12]:1
    
    julia> Meta.@lower true && false
    :($(Expr(:thunk, CodeInfo(
        @ none within `top-level scope'
    1 ─     goto #3 if not true
    2 ─     return false
    3 ─     return false
    ))))
    ```
    ```julia
    julia> function always_true()
             println("Always print true")
             return true
           end
    always_true (generic function with 1 method)
    
    julia> false && always_true()
    false
    
    julia> true && always_true()
    Always print true
    true
    
    julia> true & false
    false
    
    julia> true & true
    true
    
    julia> false & true
    false
    
    julia> false & false
    false
    
    julia> true | false
    true
    
    julia> true | true
    true
    
    julia> false & always_true()
    Always print true
    false
    
    julia> false || always_true()
    Always print true
    true
    
    julia> true || always_true()
    true
    
    ```
01. Unlike `pandas`, one seems to have to always specify the columns:
    ```julia
    julia> df[(df[:Names] .== "A") .& (df[:B] .> 4)]
    ERROR: BoundsError: attempt to access data frame with 3 columns
      at index [false, false, true, false, false, false, true, false, false, true]
    Stacktrace:
     [1] getindex at /home/phunc20/.julia/packages/DataFrames/GtZ1l/src/other/index.jl:234 [inlined]
     [2] #manipulate#299 at /home/phunc20/.julia/packages/DataFrames/GtZ1l/src/abstractdataframe/selection.jl:550 [inlined]
     [3] #select#296 at /home/phunc20/.julia/packages/DataFrames/GtZ1l/src/abstractdataframe/selection.jl:493 [inlined]
     [4] getindex at /home/phunc20/.julia/packages/DataFrames/GtZ1l/src/dataframe/dataframe.jl:468 [inlined]
     [5] getindex(::DataFrame, ::BitArray{1}) at ./deprecated.jl:72
     [6] top-level scope at REPL[38]:1
    
    julia> df[(df[:Names] .== "A") .& (df[:B] .> 4), 1]
    3-element Array{Int64,1}:
      3
      7
     10
    
    julia> df[(df[:Names] .== "A") .& (df[:B] .> 4), :]
    3×3 DataFrame
    │ Row │ A     │ B     │ Names  │
    │     │ Int64 │ Int64 │ String │
    ├─────┼───────┼───────┼────────┤
    │ 1   │ 3     │ 6     │ A      │
    │ 2   │ 7     │ 14    │ A      │
    │ 3   │ 10    │ 20    │ A      │
    
    ```


