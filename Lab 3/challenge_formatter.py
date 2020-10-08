## Sheikh Salim 1003367
## FCS Lab 3
## The following script is a simple formatter to csv format. Please refer to ChallengeWriteUp.md for more info :)


import hashlib
import csv

def hash_it(message):
    return hashlib.md5(message.encode()).hexdigest()


def save_and_format(input_target, output_target, cracked):
    results = []
    with open(input_target, 'r') as csvinput:
        csv_reader = csv.reader(csvinput, delimiter=',')
        for row in csv_reader:
            # Does the lookup
            detected = False
            with open(cracked, 'r') as f:

                for lines in f:
                    data = lines.split(':')
                    plaintext = data[1].strip()
                    if hash_it(plaintext) != data[0]:
                        print('ANOMALY!!!! for ', plaintext, ' and hash ', data[0], 'Hash by right shud be ', hash_it(plaintext))
                    if data[0] == row[0] and len(row) == 1 and hash_it(plaintext) == data[0]:
                        print('HIT + 1')
                        row.append(plaintext)
                        detected = True
                        results.append(row)
                        break
            if detected == False:
                results.append(row)

    csvinput.close()
    with open(output_target, 'w', newline='') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n', quoting=csv.QUOTE_NONE, escapechar='\\')
        writer.writerows(results)
    csvoutput.close()

if __name__ == "__main__":

    save_and_format('output.csv', 'outputv1.csv', 'cracked_lmao.txt')
