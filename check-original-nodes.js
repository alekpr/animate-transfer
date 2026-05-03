const fs = require('fs');
const orig = '/Users/direkprama/comfy-ui-projects/animate-transfer/original-files/Wan2.2+Animate.json';
const data = JSON.parse(fs.readFileSync(orig, 'utf8'));
const nodes = {};
data.nodes.forEach(n => nodes[n.id] = n);

console.log('=== Node 28 (WanVideoDecode) ===');
console.log('Type:', nodes[28].type);
if (nodes[28].outputs) {
    console.log('Outputs:', nodes[28].outputs.length);
    nodes[28].outputs.forEach((o, i) => {
        console.log(`  [${i}] name: "${o.name}", links: ${JSON.stringify(o.links)}`);
    });
}

console.log('\n=== Node 1008 (FlashVSR) ===');
console.log('Type:', nodes[1008].type);
console.log('Mode:', nodes[1008].mode);
if (nodes[1008].inputs) {
    console.log('Inputs:', nodes[1008].inputs.length);
    nodes[1008].inputs.forEach((inp, i) => {
        console.log(`  [${i}] name: "${inp.name}", link: ${inp.link}`);
    });
}
if (nodes[1008].outputs) {
    console.log('Outputs:', nodes[1008].outputs.length);
    nodes[1008].outputs.forEach((o, i) => {
        console.log(`  [${i}] name: "${o.name}", links: ${JSON.stringify(o.links)}`);
    });
}

console.log('\n=== Node 1009 (FlashVSR) ===');
console.log('Type:', nodes[1009].type);
console.log('Mode:', nodes[1009].mode);
if (nodes[1009].inputs) {
    console.log('Inputs:', nodes[1009].inputs.length);
    nodes[1009].inputs.forEach((inp, i) => {
        console.log(`  [${i}] name: "${inp.name}", link: ${inp.link}`);
    });
}
if (nodes[1009].outputs) {
    console.log('Outputs:', nodes[1009].outputs.length);
    nodes[1009].outputs.forEach((o, i) => {
        console.log(`  [${i}] name: "${o.name}", links: ${JSON.stringify(o.links)}`);
    });
}
