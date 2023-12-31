# Day3

## Possible approaches:

 - Find digit, search adjacent cells for symbols
 - Find set of digits, search adjacent cells for symbols
 - Find symbols, search adjacent cells for digits

 I think the second approach will be easiest to implement because it allows for (what I think) is a simpler solution. 

 This solution is to traverse the input and construct and intermediate representation that handles numbers (sets of digits) and symbols separately. The intermediate representation of the problem can then define algorithms to solve the problem.

 This solution is poor from a memory perspective. The most memory efficient solution would hold information for only 3 lines at a time.

## Notes on solution

