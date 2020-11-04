# Lab 6

# Contents
1. `dhke_template.py` has the dhke implementation
2. `primes_template.py` has the primes implementation
3. `babygiant_template.py` has the baby-giant implementation
    - generates `baby.txt` and `giant.txt`
5. `demo.py` is for the key exchange + encryption demo with PRESENT from lab 4
    - uses `message_to_send.txt` for sender to send
    - will generate `encrypted.txt` and `message_recieved_deciphered.txt`
6. `cracker.py` is for cracking of keys using baby step giant step algo and logging to csv
    - generates `result.csv` which will log the time taken for varying keylengths

## Part 2

Advantage:
- Good against a passive eavesdropper, as it is hard to solve the discrete logarithmic algorithm that DHKE is designed around, hence making it a good solution to the problem of key establishment

Disadvantage:
- DHKE is susceptible to MITM (active eavesdropper) as it does not establish the identity of other parties involved in key exchange
- If primes and generator not chosen properly, then generator will only generate to a small subgroup, hence leading to a much smaller cyclic group. This will reduce the complexity of the discrete log problem, making it potentially vulnerable. 


## Part 6

The algorithm is both spacially and computationally expensive over a large number of bits. This is so as it requires a large amount of intensive calculations (in the 2 steps) and also requires storing and retrieving of values. Hence, in order to determine a safe number of bits, we need to confidentially determine the number of bits such that these two costs are large. 


Based on testing with an i5 8250U and 8GB of RAM, the following graph is derived

![](https://i.imgur.com/F4XyiRt.png)

Using the '*GROWTH*' function, we conclude that for the time taken (on my PC) to crack the key to be equal to the age of the universe, **140 bits** will be much more than sufficient at  `5.86899E+17s`. This is of course assuming no storage constraints and limitted to my laptop's performance

If we account for space for the 140 bits, we will have to store ~ 1.1E+21 values (for number generated `1217181223195972093803365019885348074447099`), which will completely exhaust my pc storage multi-fold even if we grossly assume each value is 1 bit in length (which is ofc not the case)

However, to account for the upperbound and high performance machines such as super computers, we would go for a higher number of bits. Additional research  suggests using **512 bits** as it would require an amount of memory that is >> amount of memory in the world, hence making it impossible to crack due to the ridiculous storage requirements