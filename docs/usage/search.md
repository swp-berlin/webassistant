# Search

The search interface uses the ElasticSearch index to search through all publications.

[Elastic Search Query Syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax) applies.

The following fields are indexed:

| Field             | Type            |
|-------------------|-----------------|
| id                | Integer         |
| thinktank_id      | Integer         |
| title             | String          |
| subtitle          | String          |
| ris_type          | String          |
| authors           | List[String]    |
| abstract          | String          |
| publication_date  | String          |
| last_access       | String/Datetime |
| url               | String          |
| pdf_url           | String          |
| pdf_pages         | Integer         |
| doi               | String          |
| isbn              | String          |
| tags              | List[String]    |
| created           | String/Datetime |
| thinktank.name    | String          |

Any word without a field qualifier is searched in all fields.

Phrases can be searched by enclosing them in double quotes.

    "This is a phrase"

The index contains embeddings for full text content and documents. To "search" for content similar to a given phrase, enclose the phrase in angle brackets.

    <This is a phrase>

