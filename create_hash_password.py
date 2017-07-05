# -*- coding: utf-8 -*-
import sys
import string
import random
import crypt

password = sys.argv[1]
salt = ''.join(random.sample(string.ascii_letters, 2))
print crypt.crypt(password, salt)

