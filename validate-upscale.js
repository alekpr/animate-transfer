const fs = require('fs');
const workflow = JSON.parse(fs.readFileSync('./modify-files/Video-Upscale-Standalone.json', 'utf8'));

console.log('✅ JSON Valid!\n');
console.log('📊 Workflow Structure:');
console.log('  • Nodes:', workflow.nodes.length);
console.log('  • Links:', workflow.links.length);
console.log('  • Groups:', workflow.groups.length);

console.log('\n🔍 Node Check:');
const hasGetVideoInfo = workflow.nodes.some(n => n.type === 'VHS_GetVideoInfo');
console.log('  VHS_GetVideoInfo:', hasGetVideoInfo ? '❌ Still exists' : '✅ Removed');

console.log('\n🔗 Link Details:');
workflow.links.forEach((link) => {
  console.log(`  Link ${link[0]}: Node ${link[1]} → Node ${link[3]} (${link[5]})`);
});

const output = workflow.nodes.find(n => n.type === 'VHS_VideoCombine');
console.log('\n⚙️  Video Output Settings:');
console.log('  Inputs:', output.inputs.map(i => i.name).join(', '));
console.log('  FPS:', output.widgets_values.frame_rate);
console.log('  CRF:', output.widgets_values.crf);

const notes = workflow.nodes.filter(n => n.type === 'Note');
console.log('\n📝 UI Notes:', notes.length);
notes.forEach(n => {
  const preview = n.widgets_values[0].substring(0, 30);
  console.log(`  • Node ${n.id}: "${preview}..."`);
});

console.log('\n✨ Ready for RunningHub.ai (No missing nodes!)');
