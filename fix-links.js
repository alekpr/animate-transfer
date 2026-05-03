const fs = require('fs');
const p = '/Users/direkprama/comfy-ui-projects/animate-transfer/modify-files/Wan2.2+Animate.json';
const data = JSON.parse(fs.readFileSync(p, 'utf8'));
const toRemove = [1651, 1652, 1653, 1654];
const before = data.links.length;
data.links = data.links.filter(l => !toRemove.includes(l[0]));
console.log('Removed', before - data.links.length, 'links');
console.log('Links remaining:', data.links.length);
fs.writeFileSync(p, JSON.stringify(data, null, '\t'));
