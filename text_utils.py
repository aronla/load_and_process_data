import re

class TextUtils:
    EN_WHITELIST = '0123456789abcdefghijklmnopqrstuvwxyz ' # space is included in whitelist
    EN_BLACKLIST = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\''
    UNK = '<UNK>'
    NUM = '<NUM>'
    MIXED_NUM = '<MIXED_NUM>'
    VOCAB_SIZE = 6000

    @staticmethod
    def split_line(line):
        return line.split('.')

    @staticmethod
    def filter_line(line, whitelist = EN_WHITELIST):
        return ''.join([ ch for ch in line if ch in whitelist])

    @staticmethod
    def filter_token(token):
        return TextUtils.filter_line(token)

    @staticmethod
    def remove_single_letter_tokens(tokenized_line):
        return [token for token in tokenized_line if len(token) > 1]

    @staticmethod
    def remove_single_letter_token(token):
        if len(token) <= 1:
            return ''
        else:
            return token

    @staticmethod
    def lower_case(line):
        return line.lower()

    @staticmethod
    def tokenize(line):
        return line.split(' ')

    @staticmethod
    def token_to_numeric(token):
            if bool(re.search(r'^\d*$', token)):
                return TextUtils.NUM
            else:
                return token

    @staticmethod
    def token_to_mixed_numeric(token):
            if bool(re.search(r'.*[0-9].*[a-zA-Z].*|.*[a-zA-Z].*[0-9].*', token)):
                return TextUtils.MIXED_NUM
            else:
                return token


    @staticmethod
    def convert_to_numeric_token(tokenized_line):
        return [TextUtils.token_to_mixed_numeric(TextUtils.token_to_numeric(token)) for token in tokenized_line if len(token) > 1]

    @staticmethod
    def text_to_sentences(text):
        return text.split('.')

