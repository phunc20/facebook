import numpy as np

ps = range(1, 4)

# -------------------------------------
# 1st: Failed
# -------------------------------------
#norms = { p: (lambda x: np.linalg.norm(x, ord=p)) for p in ps }
#norms = { p: lambda x: np.linalg.norm(x, ord=p) for p in ps }
## The two above lines are equiv.
# -------------------------------------
# 2nd: Succeeded
# -------------------------------------
## This line works, thanks to the suggestion of some user from facebook.
norms = { p: lambda x, p=p: np.linalg.norm(x, ord=p) for p in ps }
# -------------------------------------
# 3rd: Explain -- Weirdly, it was p=3 which turns out to give the same result
#      as 1st (i.e. when not specifying p=what)
# -------------------------------------
#norms = { p: lambda x, p=None: np.linalg.norm(x, ord=p) for p in ps }
#norms = { p: lambda x, p=1: np.linalg.norm(x, ord=p) for p in ps }
#norms = { p: lambda x, p=3: np.linalg.norm(x, ord=p) for p in ps }

print(f"norms = {norms}")

a = np.array([3,4])
b = np.array([-3,7])
for p in ps:
    print(f"norms[{p}](a-b) = {norms[p](a-b)}")
