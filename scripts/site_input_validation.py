"""Validate consumed input objects before deriving site content; no network."""
from scripts.validate_connection_model_pilot import validate as validate_pilot
from scripts.validate_official_products import validate_catalog
from scripts import validate_public_usage_review as usage
from scripts import validate_question_corpus_v2 as corpus


def require_valid(errors, path):
    if errors:
        raise ValueError(f'{path}: original validation failed: {errors[:5]}')


def validate_inputs(pilot, official, raw, mapped, records, root, inputs):
    require_valid(validate_pilot(pilot), inputs[0])
    require_valid(validate_catalog(official), inputs[1])
    # The envelope checker includes raw metadata/line hashes. Also validate the
    # objects actually consumed, so a caller cannot bypass checks via read().
    require_valid(usage.validate_files(root/inputs[3], root/inputs[2]), inputs[3])
    raw_lines = usage.read_jsonl(root/inputs[2])
    if raw != [r for _, r, _ in raw_lines]:
        raise ValueError('raw source snapshot changed after validation')
    sources = {r['id']: (r, h) for _, r, h in raw_lines}
    if len(mapped) != len(sources) or {r.get('id') for r in mapped} != set(sources):
        raise ValueError('mapping input ID coverage mismatch')
    schema = usage.review_schema()
    for record in mapped:
        key = record.get('source_id')
        if key not in sources:
            raise ValueError('mapping source ID missing')
        source, digest = sources[key]
        require_valid(usage.validate_record(record, source, digest, schema), key)
    schema = corpus.load_schema()
    ids, urls = set(), set()
    for record in records:
        require_valid(corpus.validate_record(record, schema), inputs[4])
        ident, url = record['id'], corpus.url_key(record['source']['source_url'])
        if ident in ids or url in urls:
            raise ValueError('duplicate corpus ID/URL')
        ids.add(ident); urls.add(url)
    if not records:
        raise ValueError('empty corpus input')
