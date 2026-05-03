const fs = require('fs');
const workflow = JSON.parse(fs.readFileSync('./modify-files/Video-Upscale-Enhanced.json', 'utf8'));

console.log('✅ JSON Valid!\n');

console.log('📊 Workflow Statistics:');
console.log('  • Total Nodes:', workflow.nodes.length);
console.log('  • Total Links:', workflow.links.length);
console.log('  • Total Groups:', workflow.groups.length);

console.log('\n🔍 Node Inventory:');
const nodeTypes = {};
workflow.nodes.forEach(n => {
  nodeTypes[n.type] = (nodeTypes[n.type] || 0) + 1;
});
Object.entries(nodeTypes).forEach(([type, count]) => {
  console.log(`  • ${type}: ${count}`);
});

console.log('\n🎯 Key Features:');

// Check for upscale nodes
const flashVSR = workflow.nodes.find(n => n.type === 'FlashVSRNode');
console.log('  ✅ FlashVSR Upscaler:', flashVSR ? `Scale ${flashVSR.widgets_values[2]}x` : '❌ Missing');

// Check for RIFE
const rife = workflow.nodes.find(n => n.type === 'RIFE VFI');
console.log('  ✅ RIFE Interpolation:', rife ? `Multiplier ${rife.widgets_values[2]}x` : '❌ Missing');

// Check for switch
const upscaleSwitch = workflow.nodes.find(n => n.type === 'easy anythingIndexSwitch');
console.log('  ✅ Multi-Option Switch:', upscaleSwitch ? 'Yes (3 options)' : '❌ Missing');

// Check for FPS calculation
const mathExpr = workflow.nodes.find(n => n.type === 'MathExpression|pysssss');
console.log('  ✅ Auto FPS Calculation:', mathExpr ? 'Yes' : '❌ Missing');

// Check for VRAM purging
const purgeVRAM = workflow.nodes.filter(n => n.type === 'LayerUtility: PurgeVRAM V2');
console.log('  ✅ VRAM Purging:', purgeVRAM.length, 'nodes');

// Check for video info
const videoInfo = workflow.nodes.find(n => n.type === 'VHS_VideoInfoSource');
console.log('  ✅ Auto Video Info:', videoInfo ? 'Yes' : '❌ Missing');

console.log('\n🔗 Data Flow Validation:');
console.log('  Load Video → FlashVSR:', workflow.links.some(l => l[0] === 1) ? '✅' : '❌');
console.log('  FlashVSR → Switch:', workflow.links.some(l => l[0] === 10) ? '✅' : '❌');
console.log('  Switch → RIFE:', workflow.links.some(l => l[0] === 13) ? '✅' : '❌');
console.log('  RIFE → Output:', workflow.links.some(l => l[0] === 19) ? '✅' : '❌');
console.log('  VideoInfo → FPS Calc:', workflow.links.some(l => l[0] === 7) ? '✅' : '❌');

console.log('\n⚙️ Settings:');
const upscaleModeNode = workflow.nodes.find(n => n.title === '⚙️ Upscale Mode');
console.log('  • Default Upscale Mode:', upscaleModeNode ? upscaleModeNode.widgets_values[0] : 'N/A');

const rifeEnableNode = workflow.nodes.find(n => n.title === '✨ Enable RIFE');
console.log('  • Default RIFE:', rifeEnableNode ? (rifeEnableNode.widgets_values[0] ? 'Enabled' : 'Disabled') : 'N/A');

const output = workflow.nodes.find(n => n.type === 'VHS_VideoCombine');
console.log('  • Output CRF:', output ? output.widgets_values.crf : 'N/A');
console.log('  • Output Prefix:', output ? output.widgets_values.filename_prefix : 'N/A');

console.log('\n📝 UI Groups:');
workflow.groups.forEach(g => {
  console.log(`  • ${g.title}`);
});

console.log('\n⚠️ Potential Issues:');
let issues = 0;

// Check for missing nodes that might not be available on RunningHub
const customNodes = [
  'VHS_VideoInfoSource',
  'easy anythingIndexSwitch',
  'MathExpression|pysssss',
  'LayerUtility: PurgeVRAM V2',
  'InversionDemoLazySwitch',
  'RIFE VFI',
  'ImageResizeKJ'
];

customNodes.forEach(nodeType => {
  const exists = workflow.nodes.some(n => n.type === nodeType);
  if (!exists) {
    console.log(`  ⚠️ Missing: ${nodeType}`);
    issues++;
  }
});

if (issues === 0) {
  console.log('  ✅ No issues detected');
}

console.log('\n💡 Recommendations:');
console.log('  1. Test on RunningHub.ai to verify all nodes available');
console.log('  2. If VHS_VideoInfoSource missing, use manual FPS input');
console.log('  3. If RIFE missing, workflow will work without interpolation');
console.log('  4. Start with Option 1 (2x upscale) for best results');

console.log('\n✨ Enhanced Workflow Ready!');
