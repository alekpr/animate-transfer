const fs = require('fs');
const orig = '/Users/direkprama/comfy-ui-projects/animate-transfer/original-files/Wan2.2+Animate.json';
const modi = '/Users/direkprama/comfy-ui-projects/animate-transfer/modify-files/Wan2.2+Animate.json';

const origData = JSON.parse(fs.readFileSync(orig, 'utf8'));
const modiData = JSON.parse(fs.readFileSync(modi, 'utf8'));

const origNodes = {};
const modiNodes = {};
origData.nodes.forEach(n => origNodes[n.id] = n);
modiData.nodes.forEach(n => modiNodes[n.id] = n);

console.log('=== QUALITY COMPARISON (excluding upscale) ===\n');

// 1. Sampling settings (WanVideoSampler - node 1001)
console.log('1. SAMPLING (WanVideoSampler - Node 1001):');
const origSampler = origNodes[1001].widgets_values;
const modiSampler = modiNodes[1001].widgets_values;
console.log('  Steps:');
console.log('    Original:', origSampler[0]);
console.log('    Modified:', modiSampler[0]);
console.log('  CFG Scale:');
console.log('    Original:', origSampler[1]);
console.log('    Modified:', modiSampler[1]);
console.log('  Scheduler:');
console.log('    Original:', origSampler[7]);
console.log('    Modified:', modiSampler[7]);
console.log('  Denoise:');
console.log('    Original:', origSampler[8]);
console.log('    Modified:', modiSampler[8]);

// 2. Context settings (WanVideoContextOptions - node 985)
console.log('\n2. CONTEXT (WanVideoContextOptions - Node 985):');
const origContext = origNodes[985].widgets_values;
const modiContext = modiNodes[985].widgets_values;
console.log('  Context Frames:');
console.log('    Original:', origContext[1]);
console.log('    Modified:', modiContext[1]);
console.log('  Context Stride:');
console.log('    Original:', origContext[2]);
console.log('    Modified:', modiContext[2]);
console.log('  Context Overlap:');
console.log('    Original:', origContext[3]);
console.log('    Modified:', modiContext[3]);

// 3. Resolution settings (WanVideoAnimateEmbeds - node 62)
console.log('\n3. RESOLUTION (WanVideoAnimateEmbeds - Node 62):');
const origEmbeds = origNodes[62].widgets_values;
const modiEmbeds = modiNodes[62].widgets_values;
console.log('  Dimensions:');
console.log('    Original:', origEmbeds[0] + 'x' + origEmbeds[1]);
console.log('    Modified:', modiEmbeds[0] + 'x' + modiEmbeds[1]);
console.log('  Frame Count:');
console.log('    Original:', origEmbeds[2]);
console.log('    Modified:', modiEmbeds[2]);
console.log('  Total Frames:');
console.log('    Original:', origEmbeds[4]);
console.log('    Modified:', modiEmbeds[4]);

// 4. Pose/Face strength
console.log('\n4. POSE/FACE STRENGTH (WanVideoAnimateEmbeds - Node 62):');
console.log('  Pose Strength:');
console.log('    Original:', origEmbeds[6]);
console.log('    Modified:', modiEmbeds[6]);
console.log('  Face Strength:');
console.log('    Original:', origEmbeds[7]);
console.log('    Modified:', modiEmbeds[7]);

// 5. Model precision (WanVideoModelLoader - node 970)
console.log('\n5. MODEL PRECISION (WanVideoModelLoader - Node 970):');
const origModel = origNodes[970].widgets_values;
const modiModel = modiNodes[970].widgets_values;
console.log('  Precision:');
console.log('    Original:', origModel[1]);
console.log('    Modified:', modiModel[1]);

// 6. Video output settings (VHS_VideoCombine - node 867)
console.log('\n6. VIDEO OUTPUT (VHS_VideoCombine - Node 867):');
const origOutput = origNodes[867].widgets_values;
const modiOutput = modiNodes[867].widgets_values;
console.log('  Frame Rate:');
console.log('    Original:', origOutput.frame_rate);
console.log('    Modified:', modiOutput.frame_rate);
console.log('  CRF (quality):');
console.log('    Original:', origOutput.crf, '(lower = better quality)');
console.log('    Modified:', modiOutput.crf, '(lower = better quality)');
console.log('  Format:');
console.log('    Original:', origOutput.format);
console.log('    Modified:', modiOutput.format);

// 7. Image preprocessing (ImageResizeKJv2 - node 64)
console.log('\n7. PREPROCESSING (ImageResizeKJv2 - Node 64):');
const origResize = origNodes[64].widgets_values;
const modiResize = modiNodes[64].widgets_values;
console.log('  Resize Target:');
console.log('    Original:', origResize[0] + 'x' + origResize[1]);
console.log('    Modified:', modiResize[0] + 'x' + modiResize[1]);
console.log('  Interpolation:');
console.log('    Original:', origResize[2]);
console.log('    Modified:', modiResize[2]);

console.log('\n=== SUMMARY ===');
console.log('\nQuality Impact Summary:');
console.log('  Steps increased:', origSampler[0], '→', modiSampler[0], '(+' + (modiSampler[0] - origSampler[0]) + ')');
console.log('  CFG increased:', origSampler[1], '→', modiSampler[1], '(+' + (modiSampler[1] - origSampler[1]) + ')');
console.log('  Context frames reduced:', origContext[1], '→', modiContext[1], '(' + (modiContext[1] - origContext[1]) + ')');
console.log('  Context overlap reduced:', origContext[3], '→', modiContext[3], '(' + (modiContext[3] - origContext[3]) + ')');
console.log('  Orientation changed:', origEmbeds[0] + 'x' + origEmbeds[1], '→', modiEmbeds[0] + 'x' + modiEmbeds[1], '(landscape → portrait)');
console.log('  Total frames reduced:', origEmbeds[4], '→', modiEmbeds[4], '(' + (modiEmbeds[4] - origEmbeds[4]) + ')');
console.log('  Pose/Face strength reduced:', origEmbeds[6], '→', modiEmbeds[6], '(-' + (origEmbeds[6] - modiEmbeds[6]) + ')');
