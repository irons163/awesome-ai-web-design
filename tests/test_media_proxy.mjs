import assert from 'node:assert/strict';
import test from 'node:test';
import {createHash} from 'node:crypto';
import {createMediaHandler} from '../build/media-proxy.mjs';

const original=Buffer.from('original media bytes');
const sha256=createHash('sha256').update(original).digest('hex');
const base='https://raw.githubusercontent.com/owner/repository/'+'a'.repeat(40)+'/';
const groups=[{prefix:'/official-drafts/',base,assets:[{path:'example/photo.png',bytes:original.length,sha256}]}];
const request=(path='example/photo.png',options={})=>new Request('https://example.test/official-drafts/'+path,options);

test('streams exact original bytes from the pinned allowlist without visitor credentials',async()=>{
  let call;
  const handler=createMediaHandler(groups,async(url,options)=>{
    call={url,options};
    return new Response(original,{headers:{'Content-Length':String(original.length),'Set-Cookie':'upstream=value'}});
  });
  const response=await handler(request('example/photo.png?source=https://attacker.test',{headers:{Cookie:'private=value',Authorization:'Bearer private','OAI-Sites-Authorization':'private'}}));
  assert.deepEqual(Buffer.from(await response.arrayBuffer()),original);
  assert.equal(call.url,base+'example/photo.png');
  assert.deepEqual([...call.options.headers],[]);
  assert.equal(call.options.redirect,'manual');
  assert.equal(response.headers.get('Content-Type'),'image/png');
  assert.equal(response.headers.get('Set-Cookie'),null);
  assert.equal(response.headers.get('X-Source-SHA256'),sha256);
  assert.equal(response.headers.get('Access-Control-Allow-Origin'),'*');
  assert.equal(response.headers.get('Cross-Origin-Resource-Policy'),'cross-origin');
});

test('supports video-style byte ranges and preserves 206/416 response headers',async()=>{
  for(const status of [206,416]) {
    const handler=createMediaHandler(groups,async(_,options)=>{
      assert.equal(options.headers.get('Range'),'bytes=2-5');
      return new Response(status===206?original.subarray(2,6):null,{status,headers:{'Content-Range':status===206?'bytes 2-5/'+original.length:'bytes */'+original.length,'Content-Length':status===206?'4':'0'}});
    });
    const response=await handler(request(undefined,{headers:{Range:'bytes=2-5'}}));
    assert.equal(response.status,status);
    assert.equal(response.headers.get('Content-Length'),status===206?'4':'0');
    assert.equal(response.headers.get('Content-Range'),status===206?'bytes 2-5/'+original.length:'bytes */'+original.length);
  }
});

test('conditional requests return 304 without fetching and stale If-Range gets full content',async()=>{
  let calls=0;
  const handler=createMediaHandler(groups,async(_,options)=>{
    calls++;
    assert.equal(options.headers.get('Range'),null);
    return new Response(original);
  });
  const etag='"sha256-'+sha256+'"';
  assert.equal((await handler(request(undefined,{headers:{'If-None-Match':'W/'+etag}}))).status,304);
  assert.equal(calls,0);
  assert.equal((await handler(request(undefined,{headers:{Range:'bytes=2-5','If-Range':'"old"'}}))).status,200);
  assert.equal(calls,1);
});

test('HEAD is bodyless and unsupported methods never fetch',async()=>{
  let calls=0;
  const handler=createMediaHandler(groups,async(_,options)=>{
    calls++;
    assert.equal(options.method,'HEAD');
    return new Response(null,{headers:{'Content-Length':String(original.length)}});
  });
  const head=await handler(request(undefined,{method:'HEAD'}));
  assert.equal(head.body,null);
  assert.equal(head.headers.get('Content-Length'),String(original.length));
  const post=await handler(request(undefined,{method:'POST'}));
  assert.equal(post.status,405);
  assert.equal(post.headers.get('Allow'),'GET, HEAD');
  assert.equal(calls,1);
});

test('unknown, encoded traversal, and malformed paths cannot turn the route into an open proxy',async()=>{
  const handler=createMediaHandler(groups,async()=>assert.fail('Unexpected external fetch'));
  for(const path of ['https://attacker.test/file.png','example/%252e%252e/secret.png','example/%zz','example/missing.png']) {
    assert.equal(await handler(request(path)),null);
  }
  assert.throws(()=>createMediaHandler([{...groups[0],base:base.replace('a'.repeat(40),'main')}]),/immutable/);
  assert.throws(()=>createMediaHandler([{...groups[0],assets:[{...groups[0].assets[0],path:'../secret.png'}]}]),/allowlist/);
});

test('upstream failures remain explicit noncacheable errors',async()=>{
  for(const fetchMedia of [async()=>{throw new Error('offline');},async()=>new Response('missing',{status:404}),async()=>Response.redirect('https://attacker.test/',302)]) {
    const response=await createMediaHandler(groups,fetchMedia)(request());
    assert.equal(response.status,502);
    assert.equal(response.headers.get('Cache-Control'),'no-store');
  }
});

test('large bodies remain lazy streams instead of being buffered',async()=>{
  let reads=0;
  const body=new ReadableStream({pull(controller){reads++;controller.enqueue(original);controller.close();}},{highWaterMark:0});
  const handler=createMediaHandler(groups,async()=>new Response(body));
  const response=await handler(request());
  assert.equal(reads,0);
  assert.deepEqual(Buffer.from(await response.arrayBuffer()),original);
  assert.equal(reads,1);
});
