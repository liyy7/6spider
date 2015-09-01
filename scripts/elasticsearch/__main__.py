from elasticsearch import Elasticsearch
from elasticsearch_dsl import analysis, char_filter, analyzer, tokenizer

def main():
    client = Elasticsearch('localhost')
    _analyzer = analyzer('im_default', tokenizer='standard', char_filter=[char_filter('kuromoji_iteration_mark', 'builtin')])
    _analyzer = analyzer('im_kanji_only', tokenizer='standard', char_filter=[char_filter('kanji_iteration_mark', char_filter('kuromoji_iteration_mark', 'builtin'), normalize_kanji=True, normalize_kana=False)])

if __name__ == '__main__':
    main()
