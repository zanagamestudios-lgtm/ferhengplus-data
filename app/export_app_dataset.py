import sqlite3,json
con=sqlite3.connect('ferheng_remote.db')
con.row_factory=sqlite3.Row
entries=con.execute('select id,headword,part_of_speech,gender,etymology,source_url from entries where language_code="ku"').fetchall()
trans={}
for row in con.execute('select entry_id,language_code,translation from translations'):
    trans.setdefault(row['entry_id'],{}).setdefault(row['language_code'],[]).append(row['translation'])
senses={}
for row in con.execute('select entry_id,definition from senses order by entry_id,ordinal'):
    senses.setdefault(row['entry_id'],[]).append(row['definition'])
exs={}
for row in con.execute('select entry_id,text from examples order by entry_id,id'):
    d=exs.setdefault(row['entry_id'],[])
    if len(d)<4: d.append(row['text'])
forms={}
for row in con.execute('select entry_id,kind,value from forms order by entry_id,id'):
    forms.setdefault(row['entry_id'],[]).append([row['kind'],row['value']])
rels={}
for row in con.execute('select entry_id,relation_type,target_title from relations order by entry_id,id'):
    rels.setdefault(row['entry_id'],[]).append([row['relation_type'],row['target_title']])
prons={}
for row in con.execute('select entry_id,system,value from pronunciations order by entry_id,id'):
    prons.setdefault(row['entry_id'],[]).append([row['system'],row['value']])
POS={'Navder':'noun','Rengder':'adjective','Leker':'verb','Hoker':'adverb','Cinav':'pronoun','Hejmar':'numeral','Hevok':'phrase','Gotin':'phrase','Dacek':'preposition','Giredek':'conjunction','Baneşan':'interjection'}
out=[]
for e in entries:
    terms={'ku':[e['headword']]}
    for lang in ('tr','en','de'):
        vals=trans.get(e['id'],{}).get(lang)
        if vals: terms[lang]=vals
    posraw=e['part_of_speech'] or ''
    pos=None
    for part in [p.strip() for p in posraw.split('·')]:
        if part in POS: pos=POS[part]; break
    item={'id':str(e['id']),'terms':terms,'pos':pos}
    g=e['gender']
    if g=='me': item['gender']='f'
    elif g=='ner': item['gender']='m'
    if senses.get(e['id']): item['definitions']=senses[e['id']][:6]
    if exs.get(e['id']): item['examples']=exs[e['id']]
    if prons.get(e['id']): item['pronunciations']=prons[e['id']][:2]
    if forms.get(e['id']): item['forms']=forms[e['id']][:12]
    if rels.get(e['id']): item['relations']=rels[e['id']][:8]
    eth=e['etymology']
    if eth: item['etymology']=eth[:1000]
    out.append(item)
json.dump({'schemaVersion':1,'meta':{'name':'Ferheng+','version':'2.5.0','updatedAt':'2026-09-16','dialect':'Kurmanji (Latin)','license':'CC BY-SA 4.0 — ku.wiktionary.org','languages':['ku','tr','en','de']},'entries':out},open('/tmp/dictionary-full.json','w'),ensure_ascii=False,separators=(',',':'))
