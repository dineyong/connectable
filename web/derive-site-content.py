"""Generate a public UI projection without changing source data or CSP."""
from pathlib import Path
import json, hashlib, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.site_content_validation import validate_content
root = Path(__file__).resolve().parents[1]
source = root / 'data/site/content-v2.json'
x = validate_content(json.loads(source.read_text()))
def pick(item, keys):
    return {key:item[key] for key in keys if key in item}
def refs(item):
    return [pick(ref, ('url','title','checked_on','published_on','record_id')) for ref in item.get('source_refs',[]) if isinstance(ref,dict)]
y = pick(x, ('schema_version','generated_on','disclosures'))
y['monitors'] = []
for m in x['monitors']:
    out = pick(m, ('id','title','display_model','manufacturer','region','review_status','public_status','missing_fields','variant','capabilities'))
    out['source_refs'] = refs(m)
    out['features'] = [pick(f, ('fact_id','source_refs','property','summary','conditions','payload','review_status','basis')) for f in m.get('features',[])]
    y['monitors'].append(out)
y['reviews'] = []
for r in x['reviews']:
    out = pick(r, ('id','title','macbook_display_name','reported_monitor_models','monitor_ids','connection_summary','review_status','public_status','missing_fields','reported_outcome','configuration_conclusions','commercial_context','functional_observations','monitor_links'))
    out['source_refs'] = refs(r)
    for field in ('observations', 'configurations', 'nodes', 'ports', 'evidence', 'attempts'):
        out[field] = r[field]
    y['reviews'].append(out)
y['guides'] = []
for g in x['guides']:
    out = pick(g, ('id','title','body','related_monitor_ids','related_review_ids','review_status','public_status'))
    out['source_refs'] = refs(g)
    y['guides'].append(out)
validate_content(y)
encoded = json.dumps(y,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
(root/'web/site-content-v2.js').write_text('// Derived from data/site/content-v2.json; sha256: '+hashlib.sha256(source.read_bytes()).hexdigest()+'\nwindow.CONNECTABLE_SITE_V2 = '+encoded+';\n')
print('Derived',len(y['monitors']),'monitors,',len(y['reviews']),'reviews,',len(y['guides']),'guides')
