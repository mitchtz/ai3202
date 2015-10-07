#Assignment 5
Mitch Zinser

CSCI 3202 - AI

Assignment 5 - Markov Decision Process
#Changing Epsilon
Epsilon will only change the path when it is very large, and it changes 
the path so that it never completes. The path never changes at lower 
epsilon values because when it evaluates the maximum utility, my 
program considers the direction north first. Up just so happens to be 
the correct path, so when the first loop in value iteration is run, 
both up and right are equal. Since up is considered first, it will be 
chosen in case of a tie. To prove this I created a second world that 
was identical to the one given to us, but with a group of snakes after 
the barn when travelling up. This makes the best path to the right. 
When using a large epsilon (all values greater than 16), the algorithm 
chooses the up direction and gets caught in the snake field. However, 
when choosing a small epsilon (less than 16 for world2.txt), the 
correct and most efficient path is chosen.
#Testing Epsilon Values
" " = Blank Space

"X" = Path

"@" = Wall

"^" = Mountain

"%" = Snake

"B" = Barn
Epsilon = 0-35

|----------|

|    XXXXXE|

|@@^^X%@ @ |

| XXXX%@   |

|@X@@ % B@ |

|XX@  @^%^ |

|X%@  @  @ |

|X%@ ^@ ^@@|

|S         |

|----------|

Epsilon > 35

|----------|

|         E|

|@@^^ %@ @ |

| X   %@   |

|@X@@ % B@ |

|XX@  @^%^ |

|X%@  @  @ |

|X%@ ^@ ^@@|

|S         |

|----------|

When epsilon is greater than 35 in the World1 map, the path is unlikely
to be found, as a loop is present between the barn and the 