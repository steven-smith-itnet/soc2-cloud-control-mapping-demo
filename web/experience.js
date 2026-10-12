// Shared dependency-free view for GitHub Pages and the Bright Ridge React route.
// All incoming content is escaped; event handlers are delegated and cleaned up.
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))
const tabs = [
  ['overview','01','Start here'],['foundations','02','SOC 2 foundations'],['scope','03','System & AWS scope'],
  ['lifecycle','04','The full process'],['controls','05','Control explorer'],['lab','06','Engineering lab'],
  ['evidence','07','Evidence & testing'],['findings','08','Findings & audit'],['practice','09','Review & practice'],
]
const icons = {
  arrow:'<path d="M5 12h14m-6-6 6 6-6 6"/>', shield:'<path d="M12 3 3 7v5c0 5 9 9 9 9s9-4 9-9V7l-9-4Z"/><path d="m8 12 3 3 5-6"/>',
  download:'<path d="M12 3v12m-5-5 5 5 5-5M4 17v4h16v-4"/>', book:'<path d="M12 5v16M12 5C9 2 3 3 3 3v16s6-1 9 2c3-3 9-2 9-2V3s-6-1-9 2Z"/>',
}
const icon = name => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">${icons[name] || icons.arrow}</svg>`
const tag = (text, state='') => `<span class="s2-tag ${state ? 's2-'+state.toLowerCase() : ''}">${esc(text.replaceAll('_',' '))}</span>`
const card = (title, text, label='') => `<article class="s2-card">${label ? `<span class="s2-kicker">${esc(label)}</span>` : ''}<h3>${esc(title)}</h3><p>${esc(text)}</p></article>`
const intro = (kicker,title,text) => `<header class="s2-section-head"><span class="s2-kicker">${esc(kicker)}</span><h2 tabindex="-1">${esc(title)}</h2><p>${esc(text)}</p></header>`
const list = rows => `<ul class="s2-list">${rows.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`
const code = text => `<pre class="s2-code"><code>${esc(text)}</code></pre>`
const note = (title,text) => `<aside class="s2-note"><strong>${esc(title)}</strong><p>${esc(text)}</p></aside>`
const table = (headers,rows) => `<div class="s2-table-scroll" tabindex="0" role="region" aria-label="Scrollable data table"><table><thead><tr>${headers.map(x=>`<th scope="col">${esc(x)}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${r.map(x=>`<td>${x}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`

function inlineMarkdown(text, guideBase) {
  let value=esc(text)
  value=value.replace(/\[([^\]]+)\]\(([^)]+)\)/g,(_,label,href)=>{
    const decoded=href.replaceAll('&amp;','&')
    let url
    try { url = new URL(decoded,guideBase) } catch { return label }
    if (!['https:','http:'].includes(url.protocol)) return label
    return `<a href="${esc(url.href)}" target="_blank" rel="noopener noreferrer">${label}</a>`
  })
  return value.replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>').replace(/`([^`]+)`/g,'<code>$1</code>')
}
// A small safe reader for checked-in Markdown guides; no arbitrary HTML is accepted.
function markdown(text,base) {
  const lines=text.split('\n');const output=[];let i=0
  const format=x=>inlineMarkdown(x,base)
  while(i<lines.length){
    const line=lines[i]
    if(!line.trim()){i++;continue}
    if(line.startsWith('```')){const block=[];i++;while(i<lines.length&&!lines[i].startsWith('```'))block.push(lines[i++]);i++;output.push(code(block.join('\n')));continue}
    if(/^#{1,6} /.test(line)){const level=Math.min(5,line.match(/^#+/)[0].length+1);output.push(`<h${level}>${format(line.replace(/^#+ /,''))}</h${level}>`);i++;continue}
    if(line.startsWith('|')){const rows=[];while(i<lines.length&&lines[i].startsWith('|'))rows.push(lines[i++].split('|').slice(1,-1).map(x=>x.trim()));if(rows.length>1){output.push(table(rows[0],rows.slice(2).map(r=>r.map(format))));continue}}
    if(/^([-*] |\d+\. )/.test(line)){const ordered=/^\d/.test(line),items=[];while(i<lines.length&&/^([-*] |\d+\. )/.test(lines[i]))items.push(format(lines[i++].replace(/^([-*] |\d+\. )/,'')));output.push(`<${ordered?'ol':'ul'} class="s2-list">${items.map(x=>`<li>${x}</li>`).join('')}</${ordered?'ol':'ul'}>`);continue}
    const paragraph=[];while(i<lines.length&&lines[i].trim()&&!/^(#|```|\||[-*] |\d+\. )/.test(lines[i]))paragraph.push(lines[i++]);
    if(paragraph.length)output.push(`<p>${format(paragraph.join(' '))}</p>`);else i++
  }
  return output.join('')
}

export function mountProgram(root, program, baseline, options={}) {
  const resourceBase = (options.resourceBase || './').replace(/\/?$/,'/')
  const repo=program.repo
  const resource = path => resourceBase+path
  const source = id => program.sources.find(s=>s.id===id)
  const sourceLink = id => {const s=source(id);return `<a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.title)} ↗</a>`}
  const guides = ids => `<div class="s2-guides"><h3>Go deeper</h3>${ids.map(id=>{
    const g=program.guides.find(g=>g.id===id)
    return g ? `<details class="s2-guide"><summary>${icon('book')}<span>${esc(g.title)}</span><span class="s2-plus">+</span></summary><div class="s2-reading">${markdown(g.content,repo+'/blob/main/docs/')}</div></details>` : ''
  }).join('')}</div>`
  let active = tabs.some(t=>'#soc2-'+t[0]===window.location.hash) ? window.location.hash.slice(6) : 'overview'
  let query='',domain='all',criterion='all',labState='all'

  function stats() {
    return `<div class="s2-stats">${[['36','Documented controls'],['34','Plain-language definitions'],['4','Executable assertions'],['3','Selected categories']].map(([n,l])=>`<div><strong>${n}</strong><span>${l}</span></div>`).join('')}</div>`
  }
  function overview() {
    return intro('A service, an objective, a proof','Learn the whole assurance process.','Follow a fictional AWS SaaS service from its customer promises through control design, tested operation, findings and independent examination support.')+
      `<div class="s2-grid three">${card('Start with the basics','Understand report types, criteria, risks, controls and the language used by management and auditors.','Learn')}${card('Follow the AWS boundary','Explore a six-account design, data paths, shared responsibility, tenant isolation and cloud-native evidence.','Understand')}${card('Inspect the actual work','Run narrow tests, examine mixed results, check provenance and write a corrective action with an independent retest.','Practice')}</div>`+
      `<div class="s2-feature"><div><span class="s2-kicker">Northstar Workspace · fictional SaaS</span><h3>A document service built around customer trust.</h3><p>${esc(program.scope.service)}</p><div class="s2-tags">${program.scope.categories.map(x=>tag(x)).join('')}</div></div><div>${list(program.scope.commitments)}</div></div>`+
      `<h3>From promise to evidence</h3><div class="s2-chain">${['Commitment','Risk','Control','Test','Evidence','Remediation'].map((x,i)=>`<div><small>0${i+1}</small><strong>${x}</strong>${i<5?icon('arrow'):''}</div>`).join('')}</div>`+
      note('A transparent work sample',program.disclosure)+
      `<div class="s2-grid two">${card('Documented does not mean deployed','The 36-control catalog provides proposed implementations and detailed test procedures. Four assertion types are executable; one Config adapter supports live read-only collection.')}${card('A snapshot does not cover a period','The synthetic baseline is an end-of-period observation. Human review, full population reconciliation and dated operation evidence are still needed for a Type II examination.')}</div>`+
      `<div class="s2-actions"><button data-view="foundations" class="s2-button primary">Start learning ${icon('arrow')}</button><button data-view="lab" class="s2-button">Inspect the engineering lab</button><a class="s2-button" href="${esc(resource('downloads/soc2-learning-kit.zip'))}" download>${icon('download')} Download learning kit</a></div>`+guides(['01','02'])
  }
  function foundations() {
    return intro('Words before tools','Understand SOC 2 precisely.','Use these original definitions to interpret the case study. Open the full guide for report boundaries, management responsibilities and practical examples.')+
      `<div class="s2-grid two">${card('Type I','Description and suitability of control design at a specified date. Useful for understanding what is in place at that date.','At a date')}${card('Type II','Adds operating effectiveness throughout a specified period, with tests and results. A recent configuration screenshot cannot establish that history.','Across a period')}</div>`+
      `<h3>Five categories. Nine Common Criteria groupings.</h3><div class="s2-grid three">${[['Security','Selected','Protection against unauthorized access and use.'],['Availability','Selected','Service availability consistent with commitments.'],['Confidentiality','Selected','Handling of designated confidential information.'],['Processing Integrity','Learning extension','Complete, valid, accurate, timely and authorized processing.'],['Privacy','Learning extension','Personal-information obligations through the lifecycle.']].map(([t,l,p])=>card(t,p,l)).join('')}</div>`+
      note('Avoid false precision','Points of focus help interpret criteria; they are not a universal cloud configuration checklist. Control count and group coverage do not establish satisfaction of every criterion.')+
      `<label class="s2-search">Search 34 definitions<input type="search" data-filter="glossary" placeholder="Try CUEC, RPO, evidence or Identity Center" value="${esc(query)}"></label><div class="s2-glossary-results"></div>`+guides(['01','10'])
  }
  function scope() {
    const s=program.scope
    return intro('A bounded system','Make the AWS scope explicit.','The architecture below is a proposed design for learning. It includes cloud resources, supporting people, release processes and critical external suppliers.')+
      `<div class="s2-feature"><div><span class="s2-kicker">${esc(s.name)}</span><h3>${esc(s.service)}</h3><div class="s2-tags">${s.categories.map(x=>tag(x)).join('')}</div></div><div><strong>Illustrative examination period</strong><p>${esc(s.period)}</p><strong>Regions</strong><p>${s.regions.map(esc).join(' + ')}</p></div></div>`+
      `<h3>Six account boundaries</h3><div class="s2-accounts">${s.accounts.map(a=>`<article class="s2-card"><span class="s2-kicker">${esc(a.id)} · fictional</span><h3>${esc(a.name)}</h3><p>${esc(a.purpose)}</p></article>`).join('')}</div>`+
      `<h3>Follow the data and the evidence</h3><div class="s2-flow">${s.dataflow.map((x,i)=>`<div><span>${String(i+1).padStart(2,'0')}</span><p>${esc(x)}</p></div>`).join('')}</div>`+
      note('Tenant isolation is an application control','Private subnets, KMS encryption and IAM policies add protection. They cannot prove that a valid user is blocked from another tenant’s records. Trace authorization through the API, processing jobs, storage and export paths.')+
      `<div class="s2-grid two">${card('AWS as a subservice organization',s.provider)}${card('Responsibilities expected at customers',s.customer)}${card('Included in the boundary',s.boundary)}${card('Documented exclusions',s.exclusions)}</div>`+
      `<h3>Scoping decisions</h3>${table(['Decision','Rationale'],s.decisions.map(([d,r])=>[esc(d),esc(r)]))}`+guides(['02','09'])
  }
  function lifecycle() {
    return intro('Seven connected stages','Move from readiness to sustained assurance.','Each stage has an accountable owner, a concrete deliverable and a review gate. The examination is independently performed by the CPA practitioner.')+
      `<div class="s2-timeline">${program.phases.map(p=>`<article><span class="s2-step">${p.number}</span><div><span class="s2-kicker">${esc(p.owner)}</span><h3>${esc(p.title)}</h3><p class="s2-lead">${esc(p.purpose)}</p><p>${esc(p.activities)}</p><dl><dt>Deliverables</dt><dd>${esc(p.deliverables)}</dd><dt>Review gate</dt><dd>${esc(p.gate)}</dd></dl></div></article>`).join('')}</div>`+
      `<h3>The risk register drives the design</h3><div class="s2-grid two">${program.risks.map(r=>`<article class="s2-card"><span class="s2-kicker">${esc(r.id)} · ${esc(r.owner)}</span><h3>${esc(r.scenario)}</h3><p>${esc(r.impact)}</p><dl><dt>Inherent risk</dt><dd>${esc(r.inherent)}</dd><dt>Residual assessment</dt><dd>${esc(r.residual)}</dd><dt>Treatment</dt><dd>${esc(r.treatment)}</dd></dl><div class="s2-tags">${r.controls.map(x=>tag(x)).join('')}</div></article>`).join('')}</div>`+guides(['03','07','08'])
  }
  const controlMatches = c => (domain==='all'||c.domain===domain) && (criterion==='all'||c.criteria.some(x=>x.startsWith(criterion))) && JSON.stringify(c).toLowerCase().includes(query.toLowerCase())
  function controlCards() {
    const filtered=program.controls.filter(controlMatches)
    return `<p class="s2-result-count" role="status">${filtered.length} of ${program.controls.length} documented controls · mappings support criteria; they do not establish compliance.</p>${filtered.length ? filtered.map(c=>`<details class="s2-control" id="soc2-control-${esc(c.id)}"><summary><span class="s2-control-id">${esc(c.id)}</span><span class="s2-control-name"><strong>${esc(c.title)}</strong><small>${esc(c.domain)} · ${esc(c.frequency)}</small></span><span class="s2-control-tags">${c.criteria.slice(0,3).map(x=>tag(x)).join('')}${c.criteria.length>3?tag('+'+(c.criteria.length-3)):''}</span><span class="s2-plus">+</span></summary><div class="s2-control-detail"><div class="s2-tags">${c.criteria.map(x=>tag(x)).join('')}${tag(c.automation)}</div><div class="s2-grid two">${card('Risk addressed',c.risk)}${card('Population and accountability',c.population+' Accountable owner: '+c.owner+'.')}${card('Proposed AWS / process implementation',c.implementation)}${card('Test the design',c.designTest)}${card('Test operating effectiveness',c.operatingTest)}<article class="s2-card"><h3>Evidence to retain</h3>${list(c.evidence)}</article></div>${note('What this does not prove',c.limits)}<p class="s2-muted">${esc(c.mapping)}</p><p>${sourceLink(c.source)}</p></div></details>`).join('') : note('No matching controls','Try a broader search or clear the domain and criteria filters.')}`
  }
  function controlsView() {
    const domains=[...new Set(program.controls.map(c=>c.domain))]
    return intro('36 detailed control designs','Explore the controls and their proof.','Expand a control to inspect its population, owner, AWS or process implementation, design test, operating test, evidence and limits. All 36 are documented; four narrow assertions are executable.')+
      `<div class="s2-filters"><label class="s2-search">Search controls<input type="search" data-filter="controls" placeholder="Try access, backup, CC6.3 or root cause" value="${esc(query)}"></label><label>Domain<select data-filter="domain"><option value="all">All domains</option>${domains.map(d=>`<option ${domain===d?'selected':''}>${esc(d)}</option>`).join('')}</select></label><label>Criteria grouping<select data-filter="criterion">${['all',...Array.from({length:9},(_,i)=>'CC'+(i+1)),'A1','C1','PI1','P'].map(c=>`<option value="${c}" ${criterion===c?'selected':''}>${c==='all'?'All references':c}</option>`).join('')}</select></label></div>`+
      `<div class="s2-control-results">${controlCards()}</div><div class="s2-actions"><a class="s2-button" href="${esc(resource('data/controls.csv'))}" download>${icon('download')} Control workbook CSV</a></div>`+guides(['04','10'])
  }
  function resultRows() {
    const rows=baseline.results.filter(r=>labState==='all'||r.state===labState)
    return `<p class="s2-result-count" role="status">${rows.length} of ${baseline.expected_count} expected items shown.</p>`+table(['Control / item','State','Reason'],rows.map(r=>[`<strong>${esc(r.control_id)}</strong><small class="s2-block">${esc(r.resource_id)}</small>`,tag(r.state,r.state),esc(r.reason)]))
  }
  function lab() {
    const counts=baseline.counts
    return intro('Executable evidence','Run four narrow assertions. Inspect every result.','The synthetic baseline intentionally includes errors and evidence gaps. It is evaluated at a fixed end-of-period time for reproducibility and does not claim full-period effectiveness.')+
      `<div class="s2-result-stats">${Object.entries(counts).map(([state,n])=>`<div class="s2-card">${tag(state,state)}<strong>${n}</strong><span>${state==='NOT_APPLICABLE'?'Approved exclusion':state==='UNKNOWN'?'Needs reliable evidence':state==='FAIL'?'Observed deviations':'Assertions satisfied'}</span></div>`).join('')}</div>`+
      `<div class="s2-metric-bar"><div><strong>${baseline.pass_rate}%</strong><span>Narrow-assertion pass rate</span></div><p>5 / (5 + 8 + 7) = 25%. ${baseline.expected_count} expected; ${baseline.observed_count} observed; one approved exclusion. UNKNOWN stays in the denominator. This is not a SOC 2 compliance or readiness score.</p></div>`+
      `<div class="s2-grid two">${card('DAT-01 · S3 public read','Fresh native Config evaluation for every expected bucket. One optional live read-only AWS adapter. Public write, access points and tenant access still need separate tests.')}${card('IAM-04 · Leaver removal','Verified final effective-access removal across reconciled paths within one hour. The lab evaluates exports; it does not query HR/IdP or revoke access.')}${card('CHG-01 · Exact-commit approval','Independent authorized approval at the deployed SHA before deployment, with required checks passed. Export completeness and bypass paths still need review.')}${card('RES-02 · Recovery objectives','Validated recovery within four hours and recovered data within one-hour lag. The lab evaluates measurements; it does not restore AWS resources.')}</div>`+
      `<h3>Run locally · Python standard library</h3>${code('python3 -m unittest discover -s tests -v\npython3 scripts/evaluate.py --as-of 2026-09-30T15:00:00Z --out evidence/local-run\npython3 scripts/verify_evidence.py evidence/local-run')}`+
      `<p>Use a new output directory for every run. Current-time runs deliberately treat old fixture evidence as stale. The source guides explain optional live collection, input contracts and seeded-fault tests.</p><label class="s2-result-filter">Filter results<select data-filter="labState">${['all','PASS','FAIL','UNKNOWN','NOT_APPLICABLE'].map(x=>`<option value="${x}" ${labState===x?'selected':''}>${x==='all'?'All result states':x.replaceAll('_',' ')}</option>`).join('')}</select></label><div class="s2-lab-results">${resultRows()}</div>`+
      `<div class="s2-actions"><a class="s2-button" href="${esc(resource('evidence/examples/baseline/results.json'))}" download>${icon('download')} Result JSON</a><a class="s2-button" href="${esc(resource('evidence/examples/baseline/results.csv'))}" download>Result CSV</a><a class="s2-button primary" href="${esc(resource('downloads/soc2-learning-kit.zip'))}" download>Download runnable lab ${icon('arrow')}</a></div>`+guides(['05','09'])
  }
  function evidence() {
    return intro('Assurance depends on the inputs','Make every conclusion traceable.','A good result preserves source identity, scope, timestamps, logic version, population context and custody. Validate the report before relying on its conclusions.')+
      `<div class="s2-chain">${['Scope','Collect','Normalize','Evaluate','Review','Retain'].map((t,i)=>`<div><small>0${i+1}</small><strong>${t}</strong>${icon('arrow')}</div>`).join('')}</div>`+
      `<div class="s2-grid two">${card('Observation ≠ collection','A fresh API call can return an old evaluation. Preserve native observation, collection and evaluation times, and test freshness against the assertion’s approved requirement.')}${card('A population needs reconciliation','Start from the complete eligible inventory or event source. HR terminations, all production deployments and scheduled restore exercises are populations; successful tickets are not.')}${card('Validate generated reports','Inspect scope/date filters, account/region identity, pagination, joins, types, duplicates and source totals. An empty response or dropped page must not become a passing result.')}${card('Preserve the original record','Keep immutable source pointers, normalized input, code/parameter versions and separate retests. A later fix does not erase the original examination-period exception.')}</div>`+
      `<h3>Baseline provenance</h3>${table(['Field','Value'],[['Evaluation time',esc(baseline.as_of)],['Test version',esc(baseline.test_version)],['Scope SHA-256',`<code class="s2-hash">${esc(baseline.scope_sha256)}</code>`],['Logic SHA-256',`<code class="s2-hash">${esc(baseline.logic_sha256)}</code>`],['Input SHA-256',`<code class="s2-hash">${esc(baseline.input_sha256)}</code>`]])}`+
      note('A hash is not source authentication','The verifier catches changes relative to a supplied trusted manifest. It cannot prove the export came from AWS or protect a manifest that an operator can also replace. Restricted custody, provenance and appropriate retention remain required.')+
      `<h3>Full-period evidence requires more than this snapshot</h3>${list(['Reconcile expected runs to actual collections by account, region, control and cadence.','Review every event-based population, including items with no completion ticket.','Validate selected manual evidence and reviewer decisions across the period.','Retain effective code, parameter, policy and configuration versions.','Let the CPA determine sampling and reliance; there is no universal SOC 2 sample count.'])}`+
      `<div class="s2-actions"><a class="s2-button" href="${esc(resource('data/pbc-requests.csv'))}" download>${icon('download')} PBC request workbook</a><a class="s2-button" href="${esc(resource('evidence/examples/baseline/manifest.json'))}" download>Evidence manifest</a></div>`+guides(['06','08'])
  }
  function findingsView() {
    return intro('Deficiency to verified correction','Own the findings. Support the examination.','These five illustrative findings connect observable conditions to root-cause hypotheses, business impact, accountable owners and independent retests. All remain open in the baseline.')+
      `<div class="s2-findings">${program.findings.map(f=>`<details class="s2-control"><summary><span class="s2-control-id">${esc(f.id)}</span><span class="s2-control-name"><strong>${esc(f.condition)}</strong><small>${esc(f.control)} · ${esc(f.owner)}</small></span>${tag(f.severity,'FAIL')}<span class="s2-plus">+</span></summary><div class="s2-control-detail"><dl><dt>Root-cause hypothesis</dt><dd>${esc(f.cause)}</dd><dt>Business impact</dt><dd>${esc(f.impact)}</dd><dt>Corrective action</dt><dd>${esc(f.action)}</dd><dt>Target date</dt><dd>${esc(f.due)}</dd><dt>Independent retest</dt><dd>${esc(f.retest)}</dd><dt>Status</dt><dd>${esc(f.closure)}</dd></dl></div></details>`).join('')}</div>`+
      `<h3>Management-side examination deliverables</h3><div class="s2-grid two">${card('System description','Describe the actual system, commitments, boundary, people, procedures, data, relevant incidents and changes, providers and complementary responsibilities.')}${card('Management assertion','Support management’s claims about the description, control design and, for Type II, period operation. Use practitioner-reviewed wording for an actual signed assertion.')}${card('PBC and walkthrough support','Supply validated native exports and complete populations. Track requests, submitted versions and questions. Demonstrate normal and failure paths without overstating evidence.')}${card('Independent report','The CPA owns the examination procedures and opinion. Individual deviations do not mechanically determine the opinion; nature, cause, extent and evidence matter.')}</div>`+
      note('Provider report review is a control','Review the relevant AWS service/region/period, scope, opinion, exceptions and complementary controls using restricted reports from Artifact. A bridge letter is management context; it does not extend the CPA’s audited period.')+
      `<div class="s2-actions"><a class="s2-button" href="${esc(resource('data/findings.csv'))}" download>${icon('download')} Findings & actions CSV</a><a class="s2-button" href="${esc(resource('data/risk-register.csv'))}" download>Risk register CSV</a></div>`+guides(['07','08'])
  }
  function practice() {
    return intro('Explain it. Test it. Defend it.','Build your own assurance reasoning.','Try each question before opening the answer. Then use the learner workshop to introduce faults, interpret results and design a meaningful retest.')+
      `<div class="s2-grid three">${card('Beginner','Read the definitions, trace an upload through the AWS boundary, choose a control and explain the risk-to-evidence chain.','Track 1')}${card('Assurance engineer','Seed a wrong SHA, missed resource, stale observation and recovery-data gap. Check the exact state and reason, then verify artifact custody.','Track 2')}${card('Authorized AWS sandbox','Review explicit scope and a read-only profile, collect existing Config evaluations, retain raw pages and prove denied reads remain unknown.','Track 3')}</div>`+
      `<div class="s2-questions">${program.questions.map((q,i)=>`<details class="s2-guide"><summary><span class="s2-control-id">${String(i+1).padStart(2,'0')}</span><strong>${esc(q.question)}</strong><span class="s2-plus">+</span></summary><p>${esc(q.answer)}</p></details>`).join('')}</div>`+guides(['11','10'])+
      `<h3>Authoritative references</h3><p>Reviewed ${esc(program.reviewedAt)}. Original teaching summaries and internal control designs are linked to AICPA and official AWS resources. Live service behavior should be checked for your implementation.</p><div class="s2-sources">${program.sources.map(s=>`<article><a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.title)} ↗</a><p>${esc(s.use)}</p></article>`).join('')}</div>`
  }
  const views={overview,foundations,scope,lifecycle,controls:controlsView,lab,evidence,findings:findingsView,practice}
  function updateFilters() {
    if(active==='controls')root.querySelector('.s2-control-results').innerHTML=controlCards()
    if(active==='lab')root.querySelector('.s2-lab-results').innerHTML=resultRows()
    if(active==='foundations'){
      const items=program.glossary.filter(x=>(x.term+' '+x.definition).toLowerCase().includes(query.toLowerCase()))
      root.querySelector('.s2-glossary-results').innerHTML=`<p class="s2-result-count" role="status">${items.length} definitions shown</p><div class="s2-grid two">${items.map(x=>card(x.term,x.definition)).join('')}</div>`
    }
  }
  function render() {
    const idx=tabs.findIndex(t=>t[0]===active)
    root.innerHTML=`<div class="s2-experience"><header class="s2-hero"><div class="s2-hero-top"><span class="s2-kicker">${icon('shield')} ${esc(program.label)}</span><a href="${esc(repo)}" target="_blank" rel="noopener noreferrer" class="s2-repo">Source repository ↗</a></div><h1>${esc(program.title)}<span>Scope. Operate. Test. Prove.</span></h1><p>${esc(program.subtitle)}</p><div class="s2-tags">${tag('AWS SaaS')}${tag('Security + Availability + Confidentiality')}${tag('Synthetic case study')}</div>${stats()}</header><div class="s2-workspace"><nav class="s2-nav" aria-label="SOC 2 learning chapters"><span class="s2-kicker">Inside the project</span>${tabs.map(([id,n,title])=>`<button data-view="${id}" class="${active===id?'active':''}" ${active===id?'aria-current="page"':''}><span>${n}</span>${title}${icon('arrow')}</button>`).join('')}<div class="s2-nav-note">Version ${esc(program.version)}<br>Reviewed ${esc(program.reviewedAt)}<br>Fictional data. Real methods.</div></nav><div class="s2-main"><section class="s2-panel" aria-label="${esc(tabs[idx][2])}">${views[active]()}</section><div class="s2-next">${idx>0?`<button data-view="${tabs[idx-1][0]}" class="s2-button">← ${esc(tabs[idx-1][2])}</button>`:'<span></span>'}${idx<tabs.length-1?`<button data-view="${tabs[idx+1][0]}" class="s2-button primary">${esc(tabs[idx+1][2])} ${icon('arrow')}</button>`:''}</div></div></div><footer class="s2-footer"><p>${esc(program.disclosure)}</p><p>Criteria mappings are illustrative contributions. An independent CPA practitioner determines examination conclusions.</p></footer></div>`
    updateFilters()
  }
  function click(event) {
    const button=event.target.closest('[data-view]')
    if(!button||!root.contains(button))return
    active=button.dataset.view;query='';domain='all';criterion='all';labState='all';render()
    window.history.replaceState(window.history.state,'','#soc2-'+active)
    const heading=root.querySelector('.s2-section-head h2');heading.focus({preventScroll:true});heading.scrollIntoView({block:'start',behavior:'instant'})
  }
  function filter(event) {
    const type=event.target.dataset.filter
    if(!type)return
    if(type==='glossary'||type==='controls')query=event.target.value
    if(type==='domain')domain=event.target.value
    if(type==='criterion')criterion=event.target.value
    if(type==='labState')labState=event.target.value
    updateFilters()
  }
  render();root.addEventListener('click',click);root.addEventListener('input',filter)
  return ()=>{root.removeEventListener('click',click);root.removeEventListener('input',filter);root.replaceChildren()}
}
