# {%= name %}

{%= description %} Per [Wikipedia](http://en.wikipedia.org/wiki/Stop_words):

> Stop words are words which are filtered out prior to, or after, processing of natural language data [...] these are some of the most common, short function words, such as *the*, *is*, *at*, *which*, and *on*.

You can use all stopwords with [stopwords-all.json](stopwords-all.json) (keyed by language ISO 639-1 code), or see the below table for individual language stopword files.

## Languages
{%= _.doc("supported-languages.md") %}

## Sources

- [Apache Lucene](http://lucene.apache.org/) - [Apache 2.0 License](http://www.apache.org/licenses/LICENSE-2.0)
- [Carrot2](https://github.com/carrot2/carrot2) - [License](http://project.carrot2.org/license.html)
- [cue.language](https://github.com/vcl/cue.language) - [Apache 2.0 License](https://github.com/vcl/cue.language/blob/master/license.txt)
- [Jacques Savoy](http://members.unine.ch/jacques.savoy/clef/index.html) - BSD License
- SMART Information Retrieval System: ftp://ftp.cs.cornell.edu/pub/smart/

## License and Copyright
{%= copyright %}
{%= license %}
