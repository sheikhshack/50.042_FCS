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
        print(res)
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
            partial_results = []

            for i in range(num_of_iters + 1):
                # this does the multiplication (bitshift to the right)
                if i ==0:
                    multiplier = multiplier

                elif multiplier[-1] == 0 and i == num_of_iters -1:
                    multiplier.insert(0, 0)
                    multiplier.pop()

                elif multiplier[-1] == 0:
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





    # def mul_out(self, p2, modp=None):
    #     # first step is to reverse so that we can basically do what prof teach
    #     multiplier = copy.deepcopy(p2.coeffs)
    #     source = copy.deepcopy(self.coeffs)
    #     source.reverse()
    #
    #     print('I am multiplying {0} and {1}'.format(source, multiplier))
    #
    #     # we need to do bitwise AND, followed by reduction due to beyond field status
    #     combined_and = []
    #     for i in range(len(multiplier)):
    #         # since ANDing with 0 yield nothing, we skip and go on to next iter
    #         if multiplier[i] == 0:
    #             continue
    #         positional_array = []
    #         # adds the padding first
    #         for leftpad in range(len(multiplier) - i -1):
    #             # print('trigger left pad, value of i is {0} and value of len(multiplier) is {1}'.format(i, len(multiplier)))
    #             positional_array.append(0)
    #         # does the xor-ing TODO: make this just copy the whole damn array rather than XOR specific
    #         for j in source:
    #             positional_array.append(j & multiplier[i])
    #         # adds the right padding
    #         for rightpad in range(i):
    #             positional_array.append(0)
    #         print('positional_array given by {0}'.format(positional_array))
    #         combined_and.append(positional_array)
    #
    #     # proceed to XOR them
    #     final_XOR = []
    #     for aligned_bits in zip(*combined_and):
    #         res = 0
    #         for bits in aligned_bits:
    #             res = bits ^ res
    #         final_XOR.append(res)
    #     print(final_XOR)
    #     if not modp:
    #         final_XOR.reverse()
    #         return Polynomial2(final_XOR)
    #     else:
    #         # for the case of modp
    #         modp_copy = copy.deepcopy(modp.coeffs)
    #         modp_copy.reverse()
    #         mod_p_len = len(modp_copy)
    #         number_of_iters = len(final_XOR) - mod_p_len + 1
    #         res = final_XOR[0:mod_p_len]
    #         print('init res has value: ', res)
    #
    #
    #         for i in range(number_of_iters):
    #             # In the case where the value of first bit = 0
    #             print('Iteration ', i)
    #             if res[0] == 0:
    #                 if mod_p_len + i >= len(final_XOR):
    #                     # in the scenario that there is a trailing zero and the damn thing wont stop seeking rotation
    #                     break
    #                 # we rotate Left
    #                 res.pop(0)
    #                 print('First equals zero detected, moving by 1 to  ', res, 'at iter', i , 'out of ', number_of_iters)
    #                 res.append(final_XOR[mod_p_len + i])
    #
    #                 continue
    #
    #             # Step 1: Do the XOR
    #             partial_XOR = []
    #             for v_i, d_i in zip(res, modp_copy):
    #                 partial_XOR.append(v_i ^ d_i)
    #             # Step 2: remove the first element, then proceed to add on to the next elem
    #             if mod_p_len + i < len(final_XOR) - 1:
    #                 partial_XOR.append(final_XOR[mod_p_len + i])
    #                 MSB = partial_XOR.pop(0)
    #
    #             res = partial_XOR
    #             print('Iteration {0} has partial of {1}'.format(i, res))
    #         res.reverse()
    #         Polynomial2(res)

    def deg(self):
        coefficients = copy.deepcopy(self.coeffs)
        index = len(coefficients) - 1
        while True:
            highest_coeff = coefficients.pop()
            if highest_coeff == 1:
                return index
            index += -1

    def lc(self):
        coefficients = copy.deepcopy(self.coeffs)
        while True:
            highest_coeff = coefficients.pop()
            if highest_coeff == 1:
                return highest_coeff


    def div(self, p2):
        # Code is verbatim from the handout
        q = Polynomial2([])
        r = Polynomial2(copy.deepcopy(self.coeffs))
        d = p2.deg()
        c = p2.lc()

        while r.deg() >= d:
            print('rdeg is ', r.deg(), 'and d is ', d)
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
        coeff_string = ''
        for i in range(coeff_len):
            if coefficients[coeff_len - i - 1] == 1 and i != coeff_len-1:
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
        pass


    def add(self,g2):
        pass
    def sub(self,g2):
        pass
    
    def mul(self,g2):
        pass

    def div(self,g2):
        pass

    def getPolynomial2(self):
        pass

    def __str__(self):
        pass

    def getInt(self):
        pass

    def mulInv(self):
        pass

    def affineMap(self):
        pass


############### My tests ###################3


# print('Multiply Test')
# p1 = Polynomial2([0,1,1,0,0,1])
# p2 = Polynomial2([1,0,1,0,1,1])
# print(p2.mul(p1).coeffs)

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

# ####
# print('\nTest 4')
# print('======')
# g1=GF2N(100)
# g2=GF2N(5)
# print('g1 = ', g1.getPolynomial2())
# print('g2 = ', g2.getPolynomial2())
# g3=g1.add(g2)
# print('g1+g2 = ', g3)
#
# print('\nTest 5')
# print('======')
# ip=Polynomial2([1,1,0,0,1])
# print('irreducible polynomial', ip)
# g4=GF2N(0b1101,4,ip)
# g5=GF2N(0b110,4,ip)
# print('g4 = ', g4.getPolynomial2())
# print('g5 = ', g5.getPolynomial2())
# g6=g4.mul(g5)
# print('g4 x g5 = ', g6.p)
#
# print('\nTest 6')
# print('======')
# g7=GF2N(0b1000010000100,13,None)
# g8=GF2N(0b100011011,13,None)
# print('g7 = ', g7.getPolynomial2())
# print('g8 = ', g8.getPolynomial2())
# q,r=g7.div(g8)
# print('g7/g8 =')
# print('q = ', q.getPolynomial2())
# print('r = ', r.getPolynomial2())
#
# print('\nTest 7')
# print('======')
# ip=Polynomial2([1,1,0,0,1])
# print('irreducible polynomial', ip)
# g9=GF2N(0b101,4,ip)
# print('g9 = ', g9.getPolynomial2())
# print('inverse of g9 =', g9.mulInv().getPolynomial2())
#
# print('\nTest 8')
# print('======')
# ip=Polynomial2([1,1,0,1,1,0,0,0,1])
# print('irreducible polynomial', ip)
# g10=GF2N(0xc2,8,ip)
# print('g10 = 0xc2')
# g11=g10.mulInv()
# print('inverse of g10 = g11 =', hex(g11.getInt()))
# g12=g11.affineMap()
# print('affine map of g11 =', hex(g12.getInt()))
