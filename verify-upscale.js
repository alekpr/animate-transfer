const fs = require('fs');
const p = '/Users/direkprama/comfy-ui-projects/animate-transfer/modify-files/Wan2.2+Animate.json';
const data = JSON.parse(fs.readFileSync(p, 'utf8'));
const nodes = {};
data.nodes.forEach(n => nodes[n.id] = n);

console.log('=== Upscale Branch Verification ===\n');

// Check node 28 output
const node28 = nodes[28];
console.log('Node 28 (WanVideoDecode):');
if (node28.outputs) {
    const n28out = node28.outputs.find(o => o.name === 'images'); // Note: "images" not "image"
    if (n28out) {
        console.log('  Output "images" links:', n28out.links);
        console.log('  Expected: should include 1679');
    } else {
        console.log('  Output "images" NOT FOUND');
    }
} else {
    console.log('  No outputs array');
}

// Check node 1008
const node1008 = nodes[1008];
console.log('\nNode 1008 (ImageScaleByAspectRatio):');
console.log('  Mode:', node1008.mode, '(2=bypass)');
if (node1008.inputs) {
    const inp = node1008.inputs.find(i => i.name === 'image'); // Note: "image" not "images"
    console.log('  Input "image" link:', inp ? inp.link : 'NOT FOUND');
}
if (node1008.outputs) {
    const out = node1008.outputs.find(o => o.name === 'image'); // Note: "image" not "IMAGE"
    console.log('  Output "image" links:', out ? out.links : 'NOT FOUND');
}

// Check node 1009
const node1009 = nodes[1009];
console.log('\nNode 1009 (FlashVSR):');
console.log('  Mode:', node1009.mode, '(2=bypass)');
if (node1009.inputs) {
    const inp = node1009.inputs.find(i => i.name === 'frames'); // Note: "frames" not "images"
    console.log('  Input "frames" link:', inp ? inp.link : 'NOT FOUND');
}
if (node1009.outputs) {
    const out = node1009.outputs.find(o => o.name === 'image');
    console.log('  Output "image" links:', out ? out.links : 'NOT FOUND');
}

// Check node 1012
const node1012 = nodes[1012];
console.log('\nNode 1012 (VHS_VideoCombine upscale):');
console.log('  Mode:', node1012.mode, '(2=bypass)');
if (node1012.inputs) {
    const imgInp = node1012.inputs.find(i => i.name === 'images');
    const audInp = node1012.inputs.find(i => i.name === 'audio');
    const fpsInp = node1012.inputs.find(i => i.name === 'frame_rate');
    console.log('  Input "images" link:', imgInp ? imgInp.link : 'NOT FOUND');
    console.log('  Input "audio" link:', audInp ? audInp.link : 'NOT FOUND');
    console.log('  Input "frame_rate" link:', fpsInp ? fpsInp.link : 'NOT FOUND');
}

// Check links in array
console.log('\n=== Links Array ===');
[1678, 1679, 1680, 1681, 1682].forEach(id => {
    const link = data.links.find(l => l[0] === id);
    if (link) {
        console.log('Link', id, 'exists:', link);
    } else {
        console.log('Link', id, 'NOT FOUND');
    }
});
