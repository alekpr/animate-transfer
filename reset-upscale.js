const fs = require('fs');
const p = '/Users/direkprama/comfy-ui-projects/animate-transfer/modify-files/Wan2.2+Animate.json';
const data = JSON.parse(fs.readFileSync(p, 'utf8'));

// Remove links 1678-1682 if they exist
const before = data.links.length;
data.links = data.links.filter(l => ![1678, 1679, 1680, 1681, 1682].includes(l[0]));
console.log('Removed', before - data.links.length, 'links');

// Find nodes and reset their connections
const nodes = {};
data.nodes.forEach(n => nodes[n.id] = n);

// Reset node 28 output
if (nodes[28] && nodes[28].outputs) {
    const output = nodes[28].outputs.find(o => o.name === 'images');
    if (output && output.links) {
        output.links = output.links.filter(l => l !== 1679);
        console.log('Cleared link 1679 from node 28 output');
    }
}

// Reset node 1008
if (nodes[1008]) {
    if (nodes[1008].inputs) {
        const input = nodes[1008].inputs.find(i => i.name === 'image');
        if (input) {
            input.link = null;
            console.log('Cleared node 1008 input');
        }
    }
    if (nodes[1008].outputs) {
        const output = nodes[1008].outputs.find(o => o.name === 'image');
        if (output) {
            output.links = [];
            console.log('Cleared node 1008 output');
        }
    }
}

// Reset node 1009
if (nodes[1009]) {
    if (nodes[1009].inputs) {
        const input = nodes[1009].inputs.find(i => i.name === 'frames');
        if (input) {
            input.link = null;
            console.log('Cleared node 1009 input');
        }
    }
    if (nodes[1009].outputs) {
        const output = nodes[1009].outputs.find(o => o.name === 'image');
        if (output) {
            output.links = [];
            console.log('Cleared node 1009 output');
        }
    }
}

// Reset node 1012
if (nodes[1012] && nodes[1012].inputs) {
    const imgInput = nodes[1012].inputs.find(i => i.name === 'images');
    if (imgInput) {
        imgInput.link = null;
        console.log('Cleared node 1012 images input');
    }
    const audioInput = nodes[1012].inputs.find(i => i.name === 'audio');
    if (audioInput) {
        audioInput.link = null;
        console.log('Cleared node 1012 audio input');
    }
    const frameRateInput = nodes[1012].inputs.find(i => i.name === 'frame_rate');
    if (frameRateInput) {
        frameRateInput.link = null;
        console.log('Cleared node 1012 frame_rate input');
    }
}

fs.writeFileSync(p, JSON.stringify(data, null, '\t'));
console.log('\n✅ Reset complete. Ready to restore links properly.');
