import random


def get_ticket():
    a = '1234567890qwertyuiopasdfghjklzxcvbnm'
    ticket = ''
    for i in range(30):
        ticket += random.choice(a)
    return ticket
