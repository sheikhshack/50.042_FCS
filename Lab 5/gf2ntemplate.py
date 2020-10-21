# Sheikh Salim 1003367
# 50.042 FCS Lab 5 Modular Arithmetics
# Year 2020

import copy
class Polynomial2:

    def __init__(self, coeffs):
        self.coeffs = coeffs

    def add(self, p2):
        # setting both to same length first
        first_poly = copy.deepcopy(self.coeffs)
        second_poly = copy.deepcopy(p2.coeffs)

        # print('First poly ', first_poly)
        # print('Second Poly ', second_poly)


        if len(first_poly) != len(second_poly):
            diff = abs(len(first_poly) - len(second_poly))
            if len(second_poly) < len(first_poly):
                for i in range(diff):
                    second_poly.append(0)
            else:
                for i in range(diff):
                    first_poly.append(0)

        res = []
        for i, j in zip(first_poly, second_poly):
            res.append(i ^ j)
        return Polynomial2(res)

    def sub(self, p2):
        first_poly = copy.deepcopy(self.coeffs)
        second_poly = copy.deepcopy(p2.coeffs)

        if len(first_poly) != len(second_poly):
            diff = abs(len(first_poly) - len(second_poly))
            if len(second_poly) < len(first_poly):
                for i in range(diff):
                    second_poly.append(0)
            else:
                for i in range(diff):
                    first_poly.append(0)
        res = []
        for i, j in zip(first_poly, second_poly):
            res.append(i ^ j)
        return Polynomial2(res)

    def mul(self, p2, modp=None):
        num_of_iters = self.deg()
        multiplier = copy.deepcopy(p2.coeffs)
        source = copy.deepcopy(self.coeffs)
        # print('Entered Multiplication Mode')

        if modp:
            modp_array = copy.deepcopy(modp.coeffs)
            length_difference = len(modp_array) - len(multiplier)
            multiplier.extend([0] * (length_difference -1))
            partial_results = []

            for i in range(num_of_iters + 1):
                # this does the multiplication (bitshift to the right)
                if i ==0:
                    multiplier = multiplier

                elif multiplier[-1] == 0 and i == num_of_iters -1:
                    multiplier.insert(0, 0)
                    multiplier.pop()

                elif multiplier[-1] == 0:
                    # shift the result one bit to the right...
                    multiplier.insert(0, 0)
                    multiplier.pop()

                elif multiplier[-1] == 1:
                    # shift one bit to the right
                    multiplier.insert(0, 0)
                    # ptoceed to do XOR
                    partial_XOR = []
                    for x_i, y_j in zip(multiplier, modp_array):
                        partial_XOR.append(x_i ^ y_j)
                    # ignore the last bit
                    # print('Partial XOR with reduction given by ', partial_XOR)
                    partial_XOR.pop()
                    multiplier = partial_XOR
                # print('Iteration ', i, ' gives value of ', multiplier)
                if source[i] == 1:
                    partial_results.append(copy.deepcopy(multiplier))
        else:
            # No mod p
            partial_results = []
            multiplier.extend([0] * num_of_iters)
            for i in range(num_of_iters + 1):

                if i != 0:
                    # cos we do nothing on first iter
                    multiplier.insert(0, 0)
                    multiplier.pop()
                if source[i] == 1:
                    partial_results.append(copy.deepcopy(multiplier))


        finalResult = []
        for aligned_bits in zip(*partial_results):
            res = 0
            for bits in aligned_bits:
                res = bits ^ res
            finalResult.append(res)
        return Polynomial2(finalResult)



    def deg(self):
        coefficients = copy.deepcopy(self.coeffs)
        if len(coefficients) == 0:
            return 0
        index = len(coefficients) - 1
        for i in range(index + 1):
            highest_coeff = coefficients.pop()
            if highest_coeff == 1:
                return index
            index += -1
        return 0

    def lc(self):
        coefficients = copy.deepcopy(self.coeffs)
        # TODO: added this for aes
        if len(coefficients) == 0:
            return 0
        for i in range(len(coefficients)):
            highest_coeff = coefficients.pop()
            if highest_coeff == 1:
                return highest_coeff
        return 0


    def div(self, p2):
        # Code is verbatim from the handout
        # I had previously did the longdiv without looking at the handout's wikipedia page proper. Code for old longdiv
        # is commented at the top under mul function. Its the same thing actually

        q = Polynomial2([])

        r = Polynomial2(copy.deepcopy(self.coeffs))
        d = p2.deg()
        c = p2.lc()

        while r.deg() >= d:

            if r.deg() == 0 and r.lc() == 0:
                break
            s_content = int((r.lc()/c))
            s_index = r.deg() - d
            temp_array = [0] * s_index
            temp_array.append(s_content)
            s = Polynomial2(temp_array)
            q = s.add(q)
            r = r.sub(s.mul(p2))

        return q, r

    def __str__(self):
        coefficients = self.coeffs
        coeff_len = len(coefficients)
        if coeff_len == 0 or sum(coefficients) == 0:
            return '0'
        last_one = coefficients.index(1)
        coeff_string = ''
        for i in range(coeff_len):
            if coefficients[coeff_len - i - 1] == 1 and i != coeff_len-1 and coeff_len - i - 1 == last_one:
                coeff_string += 'x^' + str(coeff_len - i - 1)

            elif coefficients[coeff_len - i - 1] == 1 and i != coeff_len-1:
                coeff_string += 'x^' + str(coeff_len - i - 1) + '+'
            elif coefficients[coeff_len - i - 1] == 1 and i == coeff_len-1:
                coeff_string += 'x^' + str(coeff_len - i - 1)
        return coeff_string

    def getInt(p):
        index = 0
        sum = 0
        coefficients = p.coeffs
        for coeff in coefficients:
            if coeff == 1:
                sum += coeff * (2**index)
            index += 1
        return sum




class GF2N:
    affinemat=[[1,0,0,0,1,1,1,1],
               [1,1,0,0,0,1,1,1],
               [1,1,1,0,0,0,1,1],
               [1,1,1,1,0,0,0,1],
               [1,1,1,1,1,0,0,0],
               [0,1,1,1,1,1,0,0],
               [0,0,1,1,1,1,1,0],
               [0,0,0,1,1,1,1,1]]

    def __init__(self,x,n=8,ip=Polynomial2([1,1,0,1,1,0,0,0,1])):
        # need to convert the integer to list first
        self.x = x
        self.n = n
        self.ip = ip
        self.p = self.getPolynomial2()

    def add(self,g2):
        # Add is straightforward
        copy_array = copy.deepcopy(self.p.coeffs)
        copy_poly = Polynomial2(copy_array)

        # adds the polynomials
        res_poly = copy_poly.add(g2.p)
        # gets the integer
        x = res_poly.getInt()
        # get the highest power + 1
        n = res_poly.deg() + 1
        final = GF2N(x, n, self.ip)
        return final


    def sub(self,g2):
        # same same
        return self.add(self, g2)
    
    def mul(self,g2):
        # Mul is straightforward
        copy_array = copy.deepcopy(self.p.coeffs)
        copy_poly = Polynomial2(copy_array)


        # adds the polynomials
        res_poly = copy_poly.mul(g2.p, self.ip)
        # gets the integer
        x = res_poly.getInt()
        # get the highest power + 1
        n = res_poly.deg() + 1
        final = GF2N(x, n, self.ip)
        return final

    def div(self,g2):
        # Div is straightforward
        copy_array = copy.deepcopy(self.p.coeffs)
        copy_poly = Polynomial2(copy_array)

        # adds the polynomials
        quotient, remainder = copy_poly.div(g2.p)

        # gets the integer
        x_r = remainder.getInt()
        x_q = quotient.getInt()

        # get the highest power + 1
        n_r = remainder.deg() + 1
        n_q = quotient.deg() + 1

        final_remainder = GF2N(x_r, n_r, self.ip)
        final_quotient = GF2N(x_q, n_q, self.ip)

        return final_quotient, final_remainder

    def getPolynomial2(self):
        x = self.x
        if x == 0:
            return Polynomial2([0])
        coeffs = [1 if bit == '1' else 0 for bit in bin(x)[2:]]
        coeffs.reverse()
        return Polynomial2(coeffs)

    def __str__(self):
        return str(self.x)

    def getInt(self):
        return self.getPolynomial2().getInt()


    def mulInv(self):
        # for this segment, I did EEA as discussed in classs and use that to understand the wiki EEA
        r1, r2 = self.ip, self.p
        t1, t2 = Polynomial2([0]), Polynomial2([1])
        while r2.getInt() > 0:

            quotient, remainder = r1.div(r2)
            # remainder_largest_idx = remainder.deg() + 1
            r = r1.sub(quotient.mul(r2))
            r1 = r2
            r2 = r
            # r2 = Polynomial2(remainder.coeffs[0:remainder_largest_idx])
            t = t1.sub(quotient.mul(t2))
            t1 = t2
            t2 = t
        if r1.getInt() == 1:
            return GF2N(t1.getInt(), self.n, self.ip)
        # this case for table generation
        if self.x == 0:
            return GF2N(0, self.n, self.ip)


    def affineMap(self):
        # first step is get array of b_primes
        rhs = [1,1,0,0,0,1,1,0]
        b_prime = self.mulInv().getPolynomial2().coeffs #TODO: Await prof reply
        result = []
        index = 0
        for bit_array in self.affinemat:
            new_array = []
            for x_i, y_i in zip(bit_array, b_prime):
                new_array.append(x_i & y_i )

            res = 0
            for bit in new_array:
                res = res ^ bit
            res = res ^ rhs[index]
            result.append(res)
            index += 1
        return GF2N(Polynomial2(result).getInt(), self.n, self.ip)




print('\nTest 1')
print('======')
print('p1=x^5+x^2+x')
print('p2=x^3+x^2+1')
p1=Polynomial2([0,1,1,0,0,1])
p2=Polynomial2([1,0,1,1])
p3=p1.add(p2)
print('p3= p1+p2 = ', p3)

print('\nTest 2')
print('======')
print('p4=x^7+x^4+x^3+x^2+x')
print('modp=x^8+x^7+x^5+x^4+1')
p4=Polynomial2([0,1,1,1,1,0,0,1])
# modp=Polynomial2([1,1,0,1,1,0,0,0,1])
modp=Polynomial2([1,0,0,0,1,1,0,1,1])
p5=p1.mul(p4,modp)
print('p5=p1*p4 mod (modp)=', p5)
#
print('\nTest 3')
print('======')
print('p6=x^12+x^7+x^2')
print('p7=x^8+x^4+x^3+x+1')
p6=Polynomial2([0,0,1,0,0,0,0,1,0,0,0,0,1])
p7=Polynomial2([1,1,0,1,1,0,0,0,1])
p8q,p8r=p6.div(p7)
print('q for p6/p7=', p8q)
print('r for p6/p7=', p8r)

####
print('\nTest 4')
print('======')
g1=GF2N(100)
g2=GF2N(5)
print('g1 = ', g1.getPolynomial2())
print('g2 = ', g2.getPolynomial2())
g3=g1.add(g2)
print('g1+g2 = ', g3)

print('\nTest 5')
print('======')
ip=Polynomial2([1,1,0,0,1])
print('irreducible polynomial', ip)
g4=GF2N(0b1101,4,ip)
g5=GF2N(0b110,4,ip)
print('g4 = ', g4.getPolynomial2())
print('g5 = ', g5.getPolynomial2())
g6=g4.mul(g5)
print('g4 x g5 = ', g6.p)

print('\nTest 6')
print('======')
g7=GF2N(0b1000010000100,13,None)
g8=GF2N(0b100011011,13,None)
print('g7 = ', g7.getPolynomial2())
print('g8 = ', g8.getPolynomial2())
q,r=g7.div(g8)
print('g7/g8 =')
print('q = ', q.getPolynomial2())
print('r = ', r.getPolynomial2())
#
print('\nTest 7')
print('======')
ip=Polynomial2([1,1,0,0,1])
print('irreducible polynomial', ip)
g9=GF2N(0b101,4,ip)
print('g9 = ', g9.getPolynomial2())
print('inverse of g9 =', g9.mulInv().getPolynomial2())



print('\nTest 8')
print('======')
ip=Polynomial2([1,1,0,1,1,0,0,0,1])
print('irreducible polynomial', ip)
g10=GF2N(0xc2,8,ip)
print('g10 = 0xc2')
g11=g10.mulInv()
print('inverse of g10 = g11 =', hex(g11.getInt()))
g12=g11.affineMap()
print('affine map of g11 =', hex(g12.getInt()))


# this segment is for generation of the tables as required in the handout
# the numbers (int) for GF(2^4) is given by 0 - 15
add_matrix = []
mul_matrix = []
ip_4 = Polynomial2([1,0,0,1,1])

for i in range(16):
    current_poly_row = i
    row_candidate = GF2N(current_poly_row, 4, ip_4)
    add_list = []
    for j in range(16):
        current_poly_col = j
        col_candidate = GF2N(current_poly_col, 4, ip_4)
        # does the operations here - Add
        add_list.append(col_candidate.add(row_candidate).getInt())
    add_matrix.append(add_list)

for i in range(15):
    current_poly_row = i + 1
    row_candidate = GF2N(current_poly_row, 4, ip_4)
    add_list = []
    mul_list = []
    for j in range(15):
        current_poly_col = j+1
        col_candidate = GF2N(current_poly_col, 4, ip_4)
        # does the operations here - Mul
        mul_list.append(col_candidate.mul(row_candidate).getInt())
    mul_matrix.append(mul_list)

ip=Polynomial2([1,1,0,1,1,0,0,0,1])
s_box_matrix = []
for i in range(16):
    x_row = i
    row_list = []
    for j in range(16):
        y_col = j
        int_value = int(16*x_row + y_col)
        current_candidate = GF2N(int_value, 8, ip)
        affined_candidate = current_candidate.affineMap()
        row_list.append(hex(affined_candidate.getInt()))
    s_box_matrix.append(row_list)



print('\n ############ The following is submission for part 1 ############ \n ')

# this segment is for printing the tables nicely lol
print('The tables generated have no index. Please see pdf if thats needed')
print('----- The Addition Table --------')

for j in add_matrix:
    for i in j:
        print('{:2}'.format(str(i)), end=" ")
    print()

print('----- The Multiplication Table --------')
for j in mul_matrix:
    for i in j:
        print('{:2}'.format(str(i)), end=" ")
    print()


print('\n ############ The following is submission for part 2 ############ \n ')

print('----- The S-Box AES Table --------')
for j in s_box_matrix:
    for i in j:
        print('{:4}'.format(str(i)), end=" ")
    print()


