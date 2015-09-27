# -*- coding: utf-8 -*-

import ConfigParser

import os
from elasticsearch_dsl import Index, DocType, MetaField
from elasticsearch_dsl.connections import connections

__hosts = []


def get_hosts():
    global __hosts
    if not __hosts:
        config_file = os.path.join(os.path.dirname(__file__), '../setup.cfg')
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        host = config.get('elasticsearch', 'host') if config.has_option('elasticsearch', 'host') else '127.0.0.1'
        port = config.get('elasticsearch', 'port') if config.has_option('elasticsearch', 'port') else '9200'
        __hosts = ['{}:{}'.format(host, port)]
    return __hosts


def create_index(index_name, force=False):
    connections.create_connection(hosts=get_hosts())

    index = Index(index_name)

    index.settings(
        number_of_shards=1,
        number_of_replicas=0,
        analysis={'filter': {'pos_filter': {'type': 'kuromoji_part_of_speech',
                                            'stoptags': ['助詞-格助詞-一般',
                                                         '助詞-終助詞']},
                             'greek_lowercase_filter': {'type': 'lowercase',
                                                        'language': 'greek'}},
                  'analyzer': {'kuromoji_analyzer': {'type': 'custom',
                                                     'tokenizer': 'kuromoji_tokenizer',
                                                     'filter': ['kuromoji_baseform',
                                                                'pos_filter',
                                                                'greek_lowercase_filter',
                                                                'cjk_width']}}}
    )

    index.doc_type(JobPosting)

    if force:
        index.delete(ignore=404)

    index.create()


class JobPosting(DocType):
    class Meta:
        source = MetaField(enabled=True)
        all = MetaField(enabled=True, analyzer='kuromoji_analyzer')


__all__ = [
    'get_hosts',
    'create_index',
    'JobPosting'
]
