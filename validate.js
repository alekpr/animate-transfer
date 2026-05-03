const fs = require('fs');
const p = '/Users/direkprama/comfy-ui-projects/animate-transfer/modify-files/Wan2.2+Animate.json';
const data = JSON.parse(fs.readFileSync(p, 'utf8'));
const nodes = Object.fromEntries(data.nodes.map(n => [n.id, n]));
const gi = (id, name) => nodes[id].inputs.find(i => i.name === name);

console.log('Node 64 (resize):', nodes[64].widgets_values[0] + 'x' + nodes[64].widgets_values[1], 
    'links:', gi(64, 'width').link + ',' + gi(64, 'height').link);
console.log('Node 62 (embeds):', nodes[62].widgets_values[0] + 'x' + nodes[62].widgets_values[1], 
    'links:', gi(62, 'width').link + ',' + gi(62, 'height').link);
console.log('Node 508 (pose detect):', nodes[508].widgets_values[0] + 'x' + nodes[508].widgets_values[1], 
    'links:', gi(508, 'width').link + ',' + gi(508, 'height').link);
console.log('Node 516 (draw pose):', nodes[516].widgets_values[0] + 'x' + nodes[516].widgets_values[1], 
    'links:', gi(516, 'width').link + ',' + gi(516, 'height').link);
console.log('Dimension integers:', nodes[966].widgets_values[0] + 'x' + nodes[967].widgets_values[0]);
console.log('Leftover bad links:', data.links.filter(l => [265, 266, 1062, 1063, 1651, 1652, 1653, 1654].includes(l[0])).length);
