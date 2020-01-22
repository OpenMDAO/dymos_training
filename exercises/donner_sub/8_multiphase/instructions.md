Exercise 8: Using Multiple Phases to Capture Extremal Values
============================================================

- What is the maximum value of `y`?
- Path constraints may not provide the exact result, due to discretization
- If we solve the problem using two phases, and have them joined where y is at a maximum value, we can accurately retrieve is maximum value
- Be careful to pose the intermediate boundary constraint, Dymos may try to alter the solution to artificially satisfy the constraint.