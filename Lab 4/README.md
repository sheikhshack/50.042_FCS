# Lab 4 

## The PRESENT algo

Generally my approach for this part was to just follow the algo closely in PDF and try to do it on paper first (for one cycle) to see what is going on. The algo is pretty much given in the handout

For the decryption phase, it is simply an invert of the encryption process. We can resuse the `addRoundKey` function as it is just a `XOR`, hence fully invertible.

Flow for decryption:
1. `pLayerDecrypt`
2. `sBoxLayerDecrypt`
3. `addRoundKey`

## The ECB

Original image given by: 
![](https://i.imgur.com/LnmQhmH.png)

### The Padding
![](https://i.imgur.com/G5TEete.png)
*Adapted from https://www.di-mgt.com.au/cryptopad.html*

For this case, I have selected option 1, also known as **PKCS7**. To support this padding, we would also need to create a 'padding remover' function. Here i have made thr `remove_padding` function to achieve this. 

The function will check the last bit to determine the number of padding bytes, and will then move from LSB to MSB to see if this is truly a padding, or just a coincidence. If verified, we remove

*More here: https://en.wikipedia.org/wiki/Padding_(cryptography)#Byte_padding*

### Result

To check the integrity of the encryption and make sure that our padding is working properly, we will have to check for binaric difference between files. In this case, we utilise the `diff` function available in linux terminal

Result: **No difference**
![](https://i.imgur.com/h9wQj7T.png)

Just to be sure, here are the (last few lines) hexdumps of the encrypted and decrypted


**Original**: `hexdump Tex.ppm`
```
...
00df0e0 3220 3535 3220 3535 3220 3535 3220 3535
*
00df110 3220 3535 3220 3535 3220 3535 0a20 3532
00df120 2035 3532 2035 3532 2035 3532 2035 3532
*
00df160 2035 3532 2035 000a                    
00df167
```
**Decryption Result**:  `hexdump Texdec.ppm`
```
....
00df0e0 3220 3535 3220 3535 3220 3535 3220 3535
*
00df110 3220 3535 3220 3535 3220 3535 0a20 3532
00df120 2035 3532 2035 3532 2035 3532 2035 3532
*
00df160 2035 3532 2035 000a                    
00df167

```

## Section 5 - Decrypting `letter.e`

The first step taken is to hexdump the file and do some eye power analysis. From a quick look at the hexes, we can see a recurring 8-byte pattern occuring. 


![](https://i.imgur.com/ZXatDlb.png)

Very quickly, even at a glance, we can see the common 8-byte `0x7aa10bff92fd4179`. Given that we know this image is monotone, we assume this is true black, and hence let the rest map over to white without having to analyse them. 

After a quick and simple replacement for all `0x7aa10bff92fd4179` to `00000000`, and the rest of the bytes to `11111111` we should get some idea of the original

Now the task is to make this code more dynamic, and let the program analyse it instead of having to work with hexdumps. To make this work
1. Run through the entire `infile` and count the byte frequency using a dict
2. Run through a second time to start writing out the most common byte to be equal to black value
3. Profit
![](https://i.imgur.com/cky555P.png)



