// Offline unit test of the Fetch Origin-header reference oracle (same logic as the test page).
const A={origin:"https://a",site:"S1"}, Asub={origin:"https://asub",site:"S1"}, B={origin:"https://b",site:"S2"};
const O={origin:"https://a",site:"S1"};
const NODES={A,Asub,B};
const sameOrigin=(x,y)=>x.origin===y.origin, sameSite=(x,y)=>x.site===y.site;
function redirectTaint(reqOrigin,urlNodes){let last=null,t="same-origin";for(const u of urlNodes){if(last===null){last=u;continue;}if(!sameSite(u,last)&&!sameSite(reqOrigin,last))return"cross-site";if(!sameOrigin(u,last)&&!sameOrigin(reqOrigin,last))t="same-site";last=u;}return t;}
function serialize(reqOrigin,urlNodes){return redirectTaint(reqOrigin,urlNodes)==="same-origin"?reqOrigin.origin:"null";}
function finalMethod(m,st){for(const s of st){if((s===301||s===302)&&m==="POST")m="GET";else if(s===303&&m!=="GET"&&m!=="HEAD")m="GET";}return m;}
function expected(chain){const nodes=chain.hops.map(h=>NODES[h.host]).concat([NODES[chain.finalHost]]);const ser=serialize(O,nodes);const fm=finalMethod(chain.method,chain.hops.map(h=>h.status));if(chain.mode==="cors")return ser;if(fm!=="GET"&&fm!=="HEAD")return ser;return"<no-origin-header>";}

const cases=[
 [{hops:[{host:"B",status:307}],finalHost:"A",mode:"form",method:"POST"}, "null"],
 [{hops:[{host:"B",status:307}],finalHost:"A",mode:"cors",method:"POST"}, "null"],
 [{hops:[{host:"A",status:307}],finalHost:"A",mode:"cors",method:"POST"}, "https://a"],
 [{hops:[{host:"A",status:307}],finalHost:"A",mode:"form",method:"POST"}, "https://a"],
 [{hops:[{host:"B",status:307}],finalHost:"A",mode:"iframe",method:"GET"}, "<no-origin-header>"],
 [{hops:[{host:"B",status:302}],finalHost:"A",mode:"form",method:"POST"}, "<no-origin-header>"],
 [{hops:[{host:"B",status:302}],finalHost:"A",mode:"cors",method:"POST"}, "null"],
 [{hops:[{host:"Asub",status:307}],finalHost:"A",mode:"cors",method:"POST"}, "null"],
 [{hops:[],finalHost:"B",mode:"cors",method:"POST"}, "https://a"],
];
let ok=0,bad=0;
for(const [c,e] of cases){const g=expected(c);const p=g===e;console.log((p?"PASS":"FAIL"),JSON.stringify(c.hops.map(h=>h.host+":"+h.status)),c.mode,c.method,"=>",c.finalHost,"got",g,"want",e);p?ok++:bad++;}
console.log("ok="+ok+" bad="+bad);
