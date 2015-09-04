# coding: utf8
from __future__ import print_function

from elasticsearch_dsl import Index
from elasticsearch_dsl.connections import connections


def analyze(index, analyzer, text):
    print(index, analyzer)
    es_client = connections.get_connection()
    res = es_client.indices.analyze(index=index, analyzer=analyzer, text=text)
    print(text)
    print(''.join(map(lambda token: token['token'], res['tokens'])))
    print()


def main():
    connections.create_connection(hosts=['52.68.192.193:9200'])

    index_name = 'jobpostings'
    jobpostings = Index('jobpostings')

    # https://medium.com/hello-elasticsearch/elasticsearch-833a0704e44b
    analysis_settings = {'analyzer': {'im_default': {'char_filter': ['kuromoji_iteration_mark'],
                                                     'tokenizer': 'standard'},
                                      'im_kana_only': {'char_filter': ['kana_iteration_mark'],
                                                       'tokenizer': 'standard'},
                                      'im_kanji_only': {'char_filter': ['kanji_iteration_mark'],
                                                        'tokenizer': 'standard'}},
                         'char_filter': {'kana_iteration_mark': {'normalize_kana': True,
                                                                 'normalize_kanji': False,
                                                                 'type': 'kuromoji_iteration_mark'},
                                         'kanji_iteration_mark': {'normalize_kana': False,
                                                                  'normalize_kanji': True,
                                                                  'type': 'kuromoji_iteration_mark'}}}

    # define custom settings
    jobpostings.settings(
        number_of_shards=1,
        number_of_replicas=0,
        analysis=analysis_settings
    )

    # define aliases
    jobpostings.aliases(
        old_jobpostings={}
    )

    # # register a doc_type with the index
    # jobpostings.doc_type(Post)
    #
    # # can also be used as class decorator when defining the DocType
    # @jobpostings.doc_type
    # class Post(DocType):
    #     title = String()

    # delete the index, ignore if it doesn't exist
    jobpostings.delete(ignore=404)

    # create the index in elasticsearch
    jobpostings.create()

    for analyzer in 'im_default im_kana_only im_kanji_only'.split(' '):
        analyze(index_name, analyzer, u'ところゞゝゝ、ジヾが、時々、馬鹿々々しい')


if __name__ == '__main__':
    main()
