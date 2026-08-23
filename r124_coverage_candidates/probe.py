#!/usr/bin/env python3
from __future__ import annotations
import csv, json, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT='https://data.binance.vision/data/futures/um/monthly/klines'
CANDIDATES=['DOTUSDT','HBARUSDT','TRXUSDT','WIFUSDT','1000BONKUSDT','ZORAUSDT']
INTERVALS=['1d','4h','1h','15m','5m','1m']
MONTHS=['2026-04','2026-05','2026-06','2026-07']

def now(): return datetime.now(timezone.utc).isoformat()
def get(url, timeout=30):
    req=Request(url,headers={'User-Agent':'Photon-R124-Coverage-Probe/1.0'})
    with urlopen(req,timeout=timeout) as r:
        return int(getattr(r,'status',r.getcode())),r.read()

def probe(item):
    s,tf,m=item
    name=f'{s}-{tf}-{m}.zip'
    url=f'{ROOT}/{s}/{tf}/{name}'
    checksum=url+'.CHECKSUM'
    last=None
    for attempt in range(1,5):
        try:
            status,body=get(checksum)
            text=body.decode('utf-8','replace').strip()
            return {'symbol':s,'interval':tf,'month':m,'status':'AVAILABLE','checksum_http_status':status,'checksum':text.split()[0] if text else None,'url':url,'checked_at_utc':now(),'attempt':attempt,'error':None}
        except HTTPError as e:
            if e.code==404:
                return {'symbol':s,'interval':tf,'month':m,'status':'UNAVAILABLE_OFFICIAL_404','checksum_http_status':404,'checksum':None,'url':url,'checked_at_utc':now(),'attempt':attempt,'error':str(e)}
            last=f'HTTP {e.code}: {e}'
        except (URLError,OSError) as e:
            last=f'{type(e).__name__}: {e}'
        if attempt<4: time.sleep(min(2**(attempt-1),8))
    return {'symbol':s,'interval':tf,'month':m,'status':'PROBE_FAILED_RETRYABLE','checksum_http_status':None,'checksum':None,'url':url,'checked_at_utc':now(),'attempt':4,'error':last}

def main():
    out=Path('r124_candidate_probe_output'); out.mkdir(parents=True,exist_ok=True)
    items=[(s,tf,m) for s in CANDIDATES for tf in INTERVALS for m in MONTHS]
    rows=[]
    with ThreadPoolExecutor(max_workers=24) as ex:
        futs={ex.submit(probe,x):x for x in items}
        for fut in as_completed(futs): rows.append(fut.result())
    rows.sort(key=lambda r:(CANDIDATES.index(r['symbol']),INTERVALS.index(r['interval']),MONTHS.index(r['month'])))
    by={}
    for s in CANDIDATES:
        sr=[r for r in rows if r['symbol']==s]
        available=sum(r['status']=='AVAILABLE' for r in sr)
        by[s]={'available_units':available,'total_units':len(sr),'full_24_available':available==24,'status_counts':{st:sum(r['status']==st for r in sr) for st in sorted({r['status'] for r in sr})}}
    qualified=[s for s in CANDIDATES if by[s]['full_24_available']]
    summary={'schema':'photon.r124.coverage_candidates.v1','created_at_utc':now(),'candidates_rank_order':CANDIDATES,'intervals':INTERVALS,'months':MONTHS,'unit_count':len(rows),'by_symbol':by,'coverage_qualified_rank_order':qualified,'first_two_qualified':qualified[:2],'all_candidate_units_available':all(r['status']=='AVAILABLE' for r in rows),'strategy_core_changed':False,'thomas_executed':False}
    (out/'R124_CANDIDATE_COVERAGE_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    with (out/'R124_CANDIDATE_COVERAGE_LEDGER.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    md=['# R124 Coverage Candidate Probe','',f"- Generated: **{summary['created_at_utc']}**",f"- Units: **{len(rows)}**",'- Thomas executed: **NO**','- Strategy core changed: **NO**','', '| Rank | Symbol | Available | Full 24 |','|---:|---|---:|---|']
    for i,s in enumerate(CANDIDATES,51): md.append(f"| {i} | {s} | {by[s]['available_units']}/24 | {'PASS' if by[s]['full_24_available'] else 'FAIL'} |")
    md += ['',f"First two coverage-qualified replacements: **{', '.join(qualified[:2]) if len(qualified)>=2 else 'NOT ENOUGH'}**"]
    (out/'R124_CANDIDATE_COVERAGE_SUMMARY.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))
    if len(qualified)<2: raise SystemExit(2)
if __name__=='__main__': main()
