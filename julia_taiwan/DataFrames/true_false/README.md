# Origin
The original question asked by user 黃逸華 was as follows.
```
請問一個 DataFrames 的問題（v1.6）
using Pkg
using DataFrames
df = DataFrame(A=1:10, B=2:2:20)
df[:,:Names] = ["A","A","A","B","C","B", "A","B","C","A"]
//條件A
df[(df[:, :Names] .== "A"), :]
//條件B
df[(df[:, :B] .>4), :]
//兩個條件組合就報錯
df[(df[:, :Names] .== "A") & (df[:, :B] .>4), :]
julia> df[(df[:, :Names] .== "A") & (df[:, :B] .>4), :]
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
```


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


### R1 (on `BitArray` and `Array{Bool}`)
- [https://stackoverflow.com/questions/29623059/whats-the-difference-between-arraybool-and-bitarray-in-julia-and-how-are-they](https://stackoverflow.com/questions/29623059/whats-the-difference-between-arraybool-and-bitarray-in-julia-and-how-are-they)
- [https://docs.julialang.org/en/v1/base/arrays/#Base.BitArray](https://docs.julialang.org/en/v1/base/arrays/#Base.BitArray)
- [https://github.com/JuliaLang/julia/blob/master/base/bitarray.jl](https://github.com/JuliaLang/julia/blob/master/base/bitarray.jl)

Proof that `Bool` occupies `1` byte:
```julia
julia> sizeof(Bool)
1

julia> sizeof(UInt8)
1

julia> sizeof(UInt16)
2

julia> sizeof(UInt32)
4

julia> sizeof(UInt128)
16
```
Let's explore the meaning of 8x storage efficiency.
```julia
julia> a = BitArray(rand([0, 1], 3))
3-element BitArray{1}:
 0
 0
 1

julia> sizeof(a)
8

julia> b = rand([false, true], 3)
3-element Array{Bool,1}:
 1
 0
 1

julia> sizeof(b)
3
```
What? `BitArray` consumes more space? Wait and see more.
```julia
julia> a = BitArray(rand([0, 1], 64))
64-element BitArray{1}:
 0
 0
 1
 0
 1
 0
 0
 0
 1
 1
 0
 1
 1
 0
 ⋮
 0
 1
 0
 1
 0
 0
 1
 1
 0
 0
 0
 1
 0
 0

julia> sizeof(a)
8

julia> b = rand([false, true], 64)
64-element Array{Bool,1}:
 1
 1
 1
 1
 1
 1
 0
 1
 1
 1
 0
 0
 1
 0
 ⋮
 0
 0
 1
 1
 1
 0
 1
 1
 0
 0
 1
 0
 0
 1

julia> sizeof(b)
64
```


### R2 (on `&&` and `&`)
From the following
```julia
julia> Meta.@lower false && true
:($(Expr(:thunk, CodeInfo(
    @ none within `top-level scope'
1 ─     goto #3 if not false
2 ─     return true
3 ─     return false
))))

julia> Meta.@lower false && false
:($(Expr(:thunk, CodeInfo(
    @ none within `top-level scope'
1 ─     goto #3 if not false
2 ─     return false
3 ─     return false
))))

julia> Meta.@lower true && true
:($(Expr(:thunk, CodeInfo(
    @ none within `top-level scope'
1 ─     goto #3 if not true
2 ─     return true
3 ─     return false
))))

julia> Meta.@lower true && false
:($(Expr(:thunk, CodeInfo(
    @ none within `top-level scope'
1 ─     goto #3 if not true
2 ─     return false
3 ─     return false
))))

```
we can see that the code for `A && B`, where `A` and `B`
are boolean, will be translated to code
```
goto #3 if not A
return B
return false
```
That is, when `A` equals `true`, then `A && B` will be
equal to `B`; when `A` equals `false`, then `A && B` will
be equal to `false`.

Similarly, the code for `A || B` is
```
%1 = A
     goto #3 if not %1
     return %1
     return B
```
This can be deduced from the following.
```julia
julia> Meta.@lower true || true
:($(Expr(:thunk, CodeInfo(
    @ none within `top-level scope'
1 ─ %1 = true
└──      goto #3 if not %1
2 ─      return %1
3 ─      return true
))))

julia> Meta.@lower true || false
:($(Expr(:thunk, CodeInfo(
    @ none within `top-level scope'
1 ─ %1 = true
└──      goto #3 if not %1
2 ─      return %1
3 ─      return false
))))

julia> Meta.@lower false || true
:($(Expr(:thunk, CodeInfo(
    @ none within `top-level scope'
1 ─ %1 = false
└──      goto #3 if not %1
2 ─      return %1
3 ─      return true
))))

julia> Meta.@lower false || false
:($(Expr(:thunk, CodeInfo(
    @ none within `top-level scope'
1 ─ %1 = false
└──      goto #3 if not %1
2 ─      return %1
3 ─      return false
))))
```

If we examine the types, we don't get much information.
```julia
julia> typeof(&)
typeof(&)

julia> typeof(&&)
ERROR: syntax: invalid identifier name "&&"
Stacktrace:
 [1] top-level scope at none:1
```

We can still find a workaround using `&&`:
```julia
julia> [a && b for (a, b) in zip(df[:B] .> 4, df[:Names] .== "A")]
10-element Array{Bool,1}:
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
```

As for `&`, we won't go through an as lengthy discussion.
```julia
julia> @code_lowered true & false
CodeInfo(
1 ─ %1 = Base.and_int(x, y)
└──      return %1
)

julia> Meta.@lower true & false
:($(Expr(:thunk, CodeInfo(
    @ none within `top-level scope'
1 ─ %1 = true & false
└──      return %1
))))

julia> Meta.@lower 0 & 1
:($(Expr(:thunk, CodeInfo(
    @ none within `top-level scope'
1 ─ %1 = 0 & 1
└──      return %1
))))

julia> true & false
false

julia> true & true
true

julia> false & true
false

julia> false & false
false

julia> @edit Base.and_int(0, 1)
ERROR: ArgumentError: argument is not a generic function
Stacktrace:
 [1] which(::Any, ::Any) at ./reflection.jl:1152
 [2] functionloc at ./methodshow.jl:163 [inlined]
 [3] edit(::Function, ::Any) at /buildworker/worker/package_linux64/build/usr/share/julia/stdlib/v1.5/InteractiveUtils/src
/editless.jl:223
 [4] top-level scope at REPL[38]:1

julia> @which Base.and_int(0, 1)
ERROR: ArgumentError: argument is not a generic function
Stacktrace:
 [1] which(::Any, ::Any) at ./reflection.jl:1152
 [2] top-level scope at REPL[39]:1
```
**(?)** Where to find the definition of `Base.and_int()`?

```julia
julia> @code_llvm true & false

;  @ bool.jl:40 within `&'
define i8 @"julia_&_1144"(i8, i8) {
top:
  %2 = and i8 %0, 1
  %3 = and i8 %2, %1
  ret i8 %3
}

julia> @code_llvm 23 & 11

;  @ int.jl:308 within `&'
define i64 @"julia_&_1145"(i64, i64) {
top:
  %2 = and i64 %1, %0
  ret i64 %2
}

julia> @code_llvm 0 & 1

;  @ int.jl:308 within `&'
define i64 @"julia_&_1146"(i64, i64) {
top:
  %2 = and i64 %1, %0
  ret i64 %2
}

julia> @code_llvm 1 & 1

;  @ int.jl:308 within `&'
define i64 @"julia_&_1147"(i64, i64) {
top:
  %2 = and i64 %1, %0
  ret i64 %2
}
```



## A Few Other Observations
01. Parentheses are not omittable.
    ```julia
    julia> typeof((df[:Names] .== "A") .& (df[:B] .> 4))
    BitArray{1}
    
    julia> eltype((df[:Names] .== "A") .& (df[:B] .> 4))
    Bool
    
    julia> (df[:Names] .== "A") .& df[:B] .> 4
    10-element BitArray{1}:
     0
     0
     0
     0
     0
     0
     0
     0
     0
     0
    
    julia> df[:Names] .== "A" .& df[:B] .> 4
    ERROR: MethodError: no method matching &(::String, ::Int64)
    Closest candidates are:
      &(::Any, ::Any, ::Any, ::Any...) at operators.jl:538
      &(::Missing, ::Integer) at missing.jl:161
      &(::T, ::T) where T<:Union{Int128, Int16, Int32, Int64, Int8, UInt128, UInt16, UInt32, UInt64, UInt8} at int.jl:308
      ...
    Stacktrace:
     [1] _broadcast_getindex_evalf at ./broadcast.jl:648 [inlined]
     [2] _broadcast_getindex at ./broadcast.jl:621 [inlined]
     [3] getindex at ./broadcast.jl:575 [inlined]
     [4] copy at ./broadcast.jl:876 [inlined]
     [5] materialize(::Base.Broadcast.Broadcasted{Base.Broadcast.DefaultArrayStyle{1},Nothing,typeof(&),Tuple{Base.RefValue{String},Array{Int64,1}}}) at ./broadcast.jl:837
     [6] top-level scope at REPL[45]:1
    ```
02. Unlike `pandas`, one seems to have to always specify the columns:
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
