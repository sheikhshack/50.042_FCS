# Lab 1 - Part 3
From encrypted file:
![](https://i.imgur.com/uxZM9rl.png)

What it should look like:
![](https://i.imgur.com/CYmJN3F.png)


Form the file header, we know that `FD=` should have been `PNG`. Using the `ord` function in python interpreter to convert the ascii char to integer, we can easily determine the shifts

```
P -> F : 80 -> 70
N -> D : 78 -> 68
G -> = : 71 -> 61
```

Hence, from this, we can deduce that the key has to be 256-10 = 246, since we see it going backwards by -10 shifts

With this in mind, we decrypt and the result is a swiss flag :)


Another option is to just bruteforce