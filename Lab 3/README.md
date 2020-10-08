# FCS Lab 3

Name: Sheikh
StudentID: 1003367


## Part 3: Break Hash - Bruteforcing
As given, we select the following constraints as the potential choice of chars for the 5 character plaintext:
- `string.ascii_lowercase`
- `string.digits`

Using our brute force method, time taken to reverse all fifteen hashes is `28.535s`. 

## Part 5: The Writeup
In this segment, we will discuss the differences between salted and non-salted `rcrack` strategies, as well as understanding the performance differences better.

### The no-salt situation

In the no-salt scenario, we generate 600,000 rainbow chains as discussed in the handout. Plaintext length is kept at 5. The following metric was achieved.

```
Command used : `./rtgen md5 loweralpha-numeric 5 5 0 3800 600000 0`
Command: `./rtsort .`
Command: ` ./rcrack . -l hash5.txt `
```
**Performance metric**
```
statistics
----------------------------------------------------------------
plaintext found:                             15 of 15
total time:                                  5.27 s
**time of chain traverse:                      3.42 s**
time of alarm check:                         1.78 s
time of disk read:                           0.04 s
hash & reduce calculation of chain traverse: 108271500
hash & reduce calculation of alarm check:    41963252
number of alarm:                             144646
performance of chain traverse:               31.61 million/s
performance of alarm check:                  23.59 million/s


```
Table generation time: `69.4s` for 600000 rainbow chains of length 3800

Evidently, we can see that much of the time was spent in the generation of the rainbow table using `rtgen`. This is particularly so as we know that the runtime of hash lookup is much lower than that of the hashing operation itself. Given that `rtgen` is responsible for hashing, we would expect the time taken to be much larger

Evidently we can also see, `rtcrack`, which does the lookup, spent most of the time in chain traversal

### With salt

In this scenario, the handout mentions that we will only be salting a singular, lower chase character at random into the plaintext. Hence, it is evidently clear that the plaintext range would be only of length 6. 

Hence, the strategy here would be to regenrate a rainbow table to meet the new plaintext length requirements. We will first keep every other argument constant, so that we have a basis of comparison

Command used: `./rtgen md5 loweralpha-numeric 6 6 0 3800 600000 0`


**Performance Metric**

Result:
```
statistics
----------------------------------------------------------------
plaintext found:                             8 of 15
total time:                                  5.48 s
time of chain traverse:                      4.24 s
time of alarm check:                         1.20 s
time of disk read:                           0.02 s
hash & reduce calculation of chain traverse: 108243000
hash & reduce calculation of alarm check:    26568002
number of alarm:                             24240
performance of chain traverse:               25.50 million/s
performance of alarm check:                  22.20 million/s
```
Table generation time: `72.4s` for 600000 rainbow chains of length 3800

We noted very quickly that the number of plaintexts were drastically lower than that of an unsalted example. We will now proceed to explain the discrepancies and address the method to solve this


### Why the difference

It is crucial to first understand the point of salting. Salting itself is a good deterrent to rainbow attacks, given its ability at modifying the potential plaintext/possible input lengths. As a result, the attacker would have to come up with a larger table to accomodate this increase in plaintext lengths. Hence, given the increase in plaintext space by 1 character, the attacker would have to potentially scale up the table significantly.

Even if the attacker were to know that only 1 salt character was added (and it being a lowercase letter), the attacker would have to deal with a 26 fold increase in the space of possible plaintexts. We can picture each salt having require its own rainbow table. In our lab practice, we can imagine 26 different tables, each of the size equal to that of our original 5-character unsalted table 

In a real-life scenario, salts can be of much longer lengths, and can take a much larger variety of possible characters, hence rendering rainbow attacks useless, since the attacker would have to essentially store an extremely huge rainbow table(s). This may not be feasible, hence the tradeoff between storage-space vs computational effort becomes nullified. It would hence be better off for the attacker to attempt other alternatives. 

### The approach

Theoretically, we could try increase our table size by 26 fold to tackle the salted hashes. However, this could possibly take a very long time and would take up much storage space, something that we may have lack of. It would be much better if we did it sequentially, since we will know exactly how many tables we need, hence cutting the time lost in the table generation phase. 

`rtgen` supports partitioning the tables by including a `part index`, and incrementing them as we go, to generate rainbow tables sequentially. Starting with just 1 table with 600000 chains, we noted only 8/15 were cracked. We proceed to generate a second part, with the same reduction function (by keeping `table_index` the same, changing `part_index`). We evaluate each addition of a part, and stop when we cracked all 15


We can also opt to play around with different reducer function by incrementing the `table_index` instead


Command used: `./rtgen md5 loweralpha-numeric 6 6 0 3800 6000000 <part number>`

**Results**
1 part: 8/15 cracked
2 part: 12/15 cracked
3 part: 14/15 cracked
...
6 parts: 15/15 cracked

In our scenario here, we evidently see that 6 parts (or table) were sufficent in cracking our salted hashes.

Lookup time: 5.42s, table generation time = `8mins 23s ++`

Again we see that generation time >>> lookup time. We also not that the generation time is much larger than for the equivalent unsalted plaintexts (`69.4s`) as discussed previously, since much more chains had to be generated

## The Challenge Writeup

For the challenge, we will be utilising a myriad of tools and discuss the approaches and rationale as to why the tools and methodologies were chosen

### Dictionary attacks

The easiest way around the challenge is to first attempt to target the simple ones. Given that we have not much information about the hashes, the least computationally intensive way is to make use of a *dictionary attack*, hoping that some of these are commonly used passwords/phrases.

For this aspect, dictionaries were utilised, the first being the infamous `rockyou.txt` available from [rockyou.txt](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt) . With just the dictionary alone and with the usage of `John The Ripper (JTR)`, I easily obtained **56 password matches** that took a mere 3 seconds.

`JTR` also supported word mangling with rules. Simply put, it will create logical permutations to the wordlists. Some examples were from `Hello` -> `H3LL0`. Due to lack of time, the prebuilt 'Jumbo' version ruleset was used. More info [here](https://www.openwall.com/john/doc/RULES.shtml). With that,the success count was brought up to **80 password matches**. However, the process never managed to end unless interrupted. It was stopped after a while, when no more results were yielding. Given that JTR has not much support for GPU utilisation, it was better to try a different tool

I then migrated over to `Hashcat`, which offers CUDA support. The plan was to use a GPU to do the computationally expensive work here. In this regard, a second larger dictionary was used (for mangling). Credits to the creator [here](https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm). To complement this amazing list, a ruleset was also used (same equivalent as `JTR` mangling discussed earlier). Credits to the creator of this fantastic ruleset, obtained from [OneRuleToRuleThemAll](https://notsosecure.com/one-rule-to-rule-them-all/). With all these additions, the count was brought up to **103 password matches** in just 20++ mins. I also ran some other rulesets to try (T0XIC, Hashcat's prebuilt etc) but those did not yield any additions to the 103.

### Tapping on the community

To reach that remaining 45 hashes, I had to google in to see if any of these hashes were already computed and published by someone else. Very quicky, I discovered that there are a myriad of websites that offer these services - completely free. 
Using the following lookup tool: https://hashes.com/en/decrypt/hash, the count was brought up to **145 password matches**, leaving with just 3 more hashes

In some cases, I also noticed that some of the hashes computed from these sites were not correct. It was hence important to sieve out and make sure the cracked results provided were indeed correct


**Total Success Rate: 145/148 hashes cracked!**

### Parting Comments

The following approaches discussed were primarily taken as a means to avoid blindly bruteforcing. For the remaining 3 hashes, not much could be done as a blind bruteforce session would be unlikely to yield any successes by the time this lab is due.

Hashcat estimated an approx 42 hr for running the mega-wordlist with an ultra-extensive ruleset, but this option was also too time consuming just for the sake of the 3 hashes, and the results are not guaranteed.  


