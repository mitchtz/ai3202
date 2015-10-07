#Assignment 5
Mitch Zinser

CSCI 3202 - AI

Assignment 5 - Markov Decision Process
#Changing Epsilon
Epsilon will only change the path when it is very large, and it changes 
the path so that it never completes. The path never changes at lower 
epsilon values because small epsilon values do not allow for much error in
the evaluation of utility, as value iteration is only stopped when 
the difference in utility between a squares utility and its next utility 
is small. Large values of epsilon allow for a less efficient path to be chosen
because larger error is tolerated (value iteration stops when the 
difference between current and next state is larger). To prove this I created a second world that 
was identical to the one given to us, but with a group of snakes after 
the barn when travelling up. This makes the best path to the right. 
When using a large epsilon (all values greater than 16), the algorithm 
chooses the up direction and gets caught in the snake field. However, 
when choosing a small epsilon (less than 16 for world2.txt), the 
correct and most efficient path is chosen. My program chooses to go up instead of right because the direction up is evaluated first, so in 
the case of a tie when evaluating neighbor utility, up will be chosen 
as the firection to go.
#Testing Epsilon Values Effect on Value Iteration
Using different epsilon value makes the value iteration loop run different amounts of times.
Here is how changing epsilon changed the number of times the value iteration while loop ran before exiting

| Epsilon | Value Iteration Loops |
| ------- | --------------------- |
| 0.1     | 15                    |
| 0.5     | 13                    |
| 1.0     | 13                    |
| 5.0     | 12                    |
| 10.0    | 11                    |
| 20.0    | 10                    |
| 30.0    | 9                     |
| 35.0    | 9                     |
| 40.0    | 8                     |

This shows that as epsilon is increased and more error is tolerated (
difference between current and next state can be larger), less loops 
of value iteration are run.
#Testing Epsilon Values Effect on Path
Epsilon = 0-35 Path

7,0

6,0

5,0

4,0

4,1

3,1

2,1

2,2

2,3

2,4

1,4

0,4

0,5

0,6

0,7

0,8

0,9

Epsilon > 35 Path

7,0

6,0

5,0

4,0

4,1

3,1

2,1

3,1

2,1

Loops between 3,1 and 2,1 indefinitely

When epsilon is greater than 35 in the World1 map, the path is unlikely
to be found, as a loop is present between the barn and the space above it.