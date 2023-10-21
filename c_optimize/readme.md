# C Code Optimization

## How to run

```bash
# Compile and profile optimized version
./tasks.sh profile test_j

# Compile and profile original version
./tasks.sh profile test_j.orig
```

# Observations

## Run Time

There's three nested loops of size n, so code is O(n^3). Inner loop is doing redundant calculations.

## Improvements

- Several constants and variables were moved out of the inner loop and precomputed.
- Function was broken up so that expressions could be calculated and used more optimally in nested loops.
- Changed the order or the loops to be `fptilde, f, fp` instead of `f, fp, fptilde`. This allows pulling calculations that need fptilde out of the inner loop and reduces the number of times the `pow()` function is called by factor of n^2.
- Expanded out the calls to `pow()` with integer exponents to use multiplication instead.

## Results

- Original: 314.86s
- Optimized: 28.89s (10.89x faster)