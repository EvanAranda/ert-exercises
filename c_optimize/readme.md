# C Code Optimization

## Notes

- Aside from XCode / Instruments, I did not have any success finding a profiling tool that is compatible with Macos. I tried gperftools (google-perftools) but encountered problems with it not being able to locate some of it's dependencies because of changes to where they're located in newer Macos versions. I do not have storage space for XCode, so I was unable to use Instruments. I ultimately used the `time` command to measure the execution time of the program.

## How to run

```bash
# Compile and profile optimized version
./tasks.sh profile test_j

# Compile and profile original version
./tasks.sh profile test_j.orig
```

# Observations

There's three nested loops of size n, so code is O(n^3). Inner loop is doing redundant calculations, which are all happening in `function_j()`. The function `function_j()` accepts 3 parameters, each of which are involved in a chain of calculations. The computational time is dominated by the `math` functions such as `pow()`, `exp()`, `log()`. Reducing the number of times these functions are called is my goal to reduce the computational time.

## Improvements

- Several constants and variables were moved out of the inner loop and precomputed.
- Function was broken up so that expressions could be calculated and used more optimally in nested loops, i.e. only expressions needed for the innermost loop are calculated in the innermost loop, only expressions needed for the middle loop are calculated in the middle loop, etc.
- Changed the order of the loops to be `fptilde, f, fp` instead of `f, fp, fptilde`. This allows pulling calculations that need fptilde out of the inner loop and reduces the number of times the `pow()` function is called by factor of n^2. The expressions involving `pow()` in the fptilde loop can not be reduced to multiplication.
- Expanded out the calls to `pow()` with integer exponents to use multiplication instead.

## Results

- Original: 314.86s
- Optimized: 28.89s (10.89x faster)