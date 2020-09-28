# FCS Lab 2 
## Part 1

Given that the message is sufficiently long, we should first attempt a frequency analysis attack. I used an online tool to calculate the counts and frequencies for me from [here](https://crypto.interactive-maths.com/frequency-analysis-breaking-the-code.html). It would have also been insane to do a brute-force attack, as there are possibly 52! mappings

Standard english frequency
![](https://i.imgur.com/jMkqBYU.png)

Our ciphertext frequency ( + count)
![](https://i.imgur.com/jerdwTa.png)


In this case, the first approach is to try remapping the values accordingly to the standard english frequency ie:

    C -> E
    E -> T
    ...
    Q -> Z

Results achieved is then:
> it cah wlear tsat tsere cah alreadm ao foderhtaodioy betceeo tseu aod tsat tsem sad uet bm avvniotueot. tsem cere calkioy hlnclm alnoy io deev wnoperhatino, aod i hac ser uakioy xfiwk little unpeueoth ng ser saodh ah ig hse cere perm earoeht io csat hse cah hamioy, csile se lihteoed ioteotlm, aod nowe nr tciwe hsnnk sih sead io htrnoy dihheot. i htnnd aunoy tse rnwkh catwsioy tseu, perm ufws vfjjled ah tn csat i hsnfld dn oeqt. tn gnllnc tseu aod break iotn tseir iotiuate wnoperhatino heeued tn be ao nftraye, aod met um wlear dftm cah oeper gnr ao iohtaot tn let siu nft ng um hiyst. tn awt tse hvm fvno a grieod cah a sategfl tahk. htill, i wnfld hee on better wnfrhe tsao tn nbherpe siu grnu tse sill, aod tn wlear um wnohwieowe bm wnogehhioy tn siu agtercardh csat i sad dnoe. it ih trfe tsat ig aom hfddeo daoyer sad tsreateoed siu i cah tnn gar acam tn be ng fhe, aod met i au hfre tsat mnf cill ayree cits ue tsat tse vnhitino cah perm diggiwflt, aod tsat tsere cah ontsioy unre csiws i wnfld dn.

We can see some familiar words from here. Hence we can continue adjusting the mappings accordingly (such as `wlear` -> `clear`). We do this for a few times, particularly paying attention to character frequencies that are very close to each. Heres the character mapping and final result
![](https://i.imgur.com/aFsdDDC.png)


> it was clear that there was already an understanding between them and that they had met by appointment. they were walking slowly along in deep conversation, and i saw her making quick little movements of her hands as if she were very earnest in what she was saying, while he listened intently, and once or twice shook his head in strong dissent. i stood among the rocks watching them, very much puzzled as to what i should do next. to follow them and break into their intimate conversation seemed to be an outrage, and yet my clear duty was never for an instant to let him out of my sight. to act the spy upon a friend was a hateful task. still, i could see no better course than to observe him from the hill, and to clear my conscience by confessing to him afterwards what i had done. it is true that if any sudden danger had threatened him i was too far away to be of use, and yet i am sure that you will agree with me that the position was very difficult, and that there was nothing more which i could do.

Took me quite a bit to realise the `N -> Z` lol

## Part 2

> b'161d0c56130b17493e2145625800514555596b52140116457942115d2c0b071b'

The handout mentions already that this is a plaintext encrypted with an OTP. We know that OTP cannot be beruteforced effectively. Hence, we can actually try our luck here by simply assuming that the implementer is recycling and reusing the same key over and over.

The objective here is to hence generate a mask such that i can get the points instead

This makes the OTP utterly useless. Heres the gameplan:
1. Send the challenge (c1) back to server to achieve the plaintext (m1)
2. We achieve `Student ID 1000000 gets 0 points`
3. We now create a malicious plaintext (m2)`Student ID 1003367 gets 4 points`
4. Now we will XOR the m1 and m2. The reason for this is that for a given reused key, we know that `c1 XOR c2 = m1 XOR m2`. Hence, to achieve c2, all we have to do is `c2 = (m1 XOR m2) XOR c1`
5. Boom profit!