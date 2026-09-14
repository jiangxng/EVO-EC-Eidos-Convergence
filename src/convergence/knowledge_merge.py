from __future__ import annotations
from .util import uid, now

def key(r): return (r.get('subject'),r.get('predicate'),r.get('scope'),r.get('validFrom'))
def semantic_key(r): return (r.get('subject'),r.get('predicate'))

def merge_exports(a:dict,b:dict,mode='NEW_BRAIN_MERGE'):
    if mode not in {'COPY_MERGE','NEW_BRAIN_MERGE'}: raise ValueError('unsupported merge mode')
    merged=[];conflicts=[];audit=[]
    by_exact={}
    for src,doc in [('A',a),('B',b)]:
        for r in doc.get('records',[]):
            k=key(r); sk=semantic_key(r)
            exact=(k,repr(r.get('value')))
            if exact in by_exact:
                existing=by_exact[exact]
                existing.setdefault('mergedProvenance',[]).append(r.get('provenance',{}))
                audit.append({'class':'DUPLICATE','source':src,'recordId':r.get('recordId')})
                continue
            same_sem=[x for x in merged if semantic_key(x)==sk]
            if same_sem:
                # Different scope/time is preserved as parallel knowledge, not flattened.
                for x in same_sem:
                    if x.get('scope')==r.get('scope') and x.get('validFrom')==r.get('validFrom') and x.get('value')!=r.get('value'):
                        conflicts.append({'class':'CONFLICTING','subject':sk[0],'predicate':sk[1],'left':x,'right':r,'resolution':'UNRESOLVED'})
                        audit.append({'class':'CONFLICTING','source':src,'recordId':r.get('recordId')})
                    elif x.get('scope')!=r.get('scope'):
                        audit.append({'class':'SCOPE_DIFFERENT','source':src,'recordId':r.get('recordId')})
                    elif x.get('validFrom')!=r.get('validFrom'):
                        audit.append({'class':'TEMPORALLY_DIFFERENT','source':src,'recordId':r.get('recordId')})
            nr=dict(r);nr['originEc']=doc.get('ecId');nr['mergedProvenance']=[r.get('provenance',{})]
            merged.append(nr);by_exact[exact]=nr
    return {"contractVersion":"0.1.0","mergeId":uid('MERGE'),"mode":mode,"sourceA":a.get('ecId','EC-A'),"sourceB":b.get('ecId','EC-B'),"merged":merged,"conflicts":conflicts,"audit":{"createdAt":now(),"events":audit,"rule":"preserve provenance/scope/time/conflicts; never overwrite truth"}}
