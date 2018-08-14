import utils
import base64


s = '5b71afa39dc6d6799ceb58f3'
email = 'tttt@tttt.ru'
pas = 'paspaspaspas'

key = s + s[0:8]
print(len(key))

key1 = base64.b64encode(bytes(key, 'utf-8'))
print(type(key1))


em_enc = utils.encrypt_string(email, key1)
print(em_enc)


dec_em = utils.decrypt_string(em_enc, key1)
print(dec_em)
print(type(dec_em))
