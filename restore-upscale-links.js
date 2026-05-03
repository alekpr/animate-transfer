const fs = require('fs');
const p = '/Users/direkprama/comfy-ui-projects/animate-transfer/modify-files/Wan2.2+Animate.json';
const data = JSON.parse(fs.readFileSync(p, 'utf8'));

// Links to restore from original workflow:
// [1678, 1008, 0, 1009, 0, "IMAGE"] - node 1008 output → node 1009 input
// [1679, 28, 0, 1008, 0, "IMAGE"] - node 28 output → node 1008 input
// [1680, 1010, 0, 1012, 1, "AUDIO"] - node 1010 output → node 1012 input
// [1681, 1011, 0, 1012, 4, "FLOAT"] - node 1011 output → node 1012 input
// [1682, 1009, 0, 1012, 0, "IMAGE"] - node 1009 output → node 1012 input

const linksToAdd = [
    [1678, 1008, 0, 1009, 0, "IMAGE"],
    [1679, 28, 0, 1008, 0, "IMAGE"],
    [1680, 1010, 0, 1012, 1, "AUDIO"],
    [1681, 1011, 0, 1012, 4, "FLOAT"],
    [1682, 1009, 0, 1012, 0, "IMAGE"]
];

// Add links to links array
console.log('Before:', data.links.length, 'links');
data.links.push(...linksToAdd);
console.log('After:', data.links.length, 'links');

// Find nodes
const nodes = {};
data.nodes.forEach(n => nodes[n.id] = n);

// Restore node 28 output link 1679
const node28 = nodes[28];
if (node28 && node28.outputs) {
    const output = node28.outputs.find(o => o.name === 'images'); // Note: "images" not "image"
    if (output && output.links) {
        if (!output.links.includes(1679)) {
            output.links.push(1679);
            console.log('Added link 1679 to node 28 output');
        }
    }
}

// Restore node 1008 input link 1679 and output link 1678
const node1008 = nodes[1008];
if (node1008) {
    const input = node1008.inputs ? node1008.inputs.find(i => i.name === 'image') : null; // Note: "image" not "images"
    if (input) {
        input.link = 1679;
        console.log('Set node 1008 input link to 1679');
    }
    const output = node1008.outputs ? node1008.outputs.find(o => o.name === 'image') : null;
    if (output) {
        if (!output.links) output.links = [];
        if (!output.links.includes(1678)) {
            output.links.push(1678);
            console.log('Added link 1678 to node 1008 output');
        }
    }
}

// Restore node 1009 input link 1678 and output link 1682
const node1009 = nodes[1009];
if (node1009) {
    const input = node1009.inputs ? node1009.inputs.find(i => i.name === 'frames') : null; // Note: "frames" not "images"
    if (input) {
        input.link = 1678;
        console.log('Set node 1009 input link to 1678');
    }
    const output = node1009.outputs ? node1009.outputs.find(o => o.name === 'image') : null;
    if (output) {
        if (!output.links) output.links = [];
        if (!output.links.includes(1682)) {
            output.links.push(1682);
            console.log('Added link 1682 to node 1009 output');
        }
    }
}

// Restore node 1012 input links
const node1012 = nodes[1012];
if (node1012) {
    const imageInput = node1012.inputs.find(i => i.name === 'images');
    if (imageInput) {
        imageInput.link = 1682;
        console.log('Set node 1012 images input link to 1682');
    }
    const audioInput = node1012.inputs.find(i => i.name === 'audio');
    if (audioInput) {
        audioInput.link = 1680;
        console.log('Set node 1012 audio input link to 1680');
    }
    const frameRateInput = node1012.inputs.find(i => i.name === 'frame_rate');
    if (frameRateInput) {
        frameRateInput.link = 1681;
        console.log('Set node 1012 frame_rate input link to 1681');
    }
}

// Verify all nodes are still in bypass mode (mode 2)
console.log('\nVerifying bypass mode:');
[1008, 1009, 1012].forEach(id => {
    console.log('Node', id, 'mode:', nodes[id].mode, '(should be 2)');
});

// Write back
fs.writeFileSync(p, JSON.stringify(data, null, '\t'));
console.log('\n✅ Upscale links restored! Nodes remain in bypass mode.');
console.log('You can now toggle them in ComfyUI UI with right-click → Bypass');
