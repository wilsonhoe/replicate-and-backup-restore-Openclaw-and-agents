// Verification script for Gumroad activation status
// Run this after completing the activation guide to verify setup

const fs = require('fs');
const path = require('path');

console.log('🔍 GUMROAD ACTIVATION VERIFICATION SCRIPT');
console.log('=' .repeat(50));

// Check if product files exist
const productFiles = [
  'ai-business-assessment-quiz.pdf',
  'ai-automation-playbook.pdf', 
  'ai-ceo-technical-setup-guide.pdf',
  'ai-roi-calculator.pdf',
  'ai-ceo-complete-bundle.zip'
];

const productsPath = '/home/wls/.openclaw/workspace/products/';
let allFilesExist = true;

console.log('\n📁 CHECKING PRODUCT FILES:');
productFiles.forEach(file => {
  const filePath = path.join(productsPath, file);
  if (fs.existsSync(filePath)) {
    const stats = fs.statSync(filePath);
    const sizeMB = (stats.size / (1024 * 1024)).toFixed(2);
    console.log(`  ✅ ${file} (${sizeMB} MB)`);
  } else {
    console.log(`  ❌ ${file} - MISSING`);
    allFilesExist = false;
  }
});

// Check for activation guide
const activationGuidePath = '/home/wls/.openclaw/workspace/PAYMENT_INTEGRATION_ACTIVATION_GUIDE.md';
if (fs.existsSync(activationGuidePath)) {
  console.log(`\n📋 ACTIVATION GUIDE: ✅ Found`);
} else {
  console.log(`\n📋 ACTIVATION GUIDE: ❌ Missing`);
}

// Check revenue tracking file
const revenueTrackingPath = '/home/wls/.openclaw/workspace/revenue-tracking.json';
if (fs.existsSync(revenueTrackingPath)) {
  try {
    const revenueData = JSON.parse(fs.readFileSync(revenueTrackingPath, 'utf8'));
    console.log(`\n💰 REVENUE TRACKING:`);
    console.log(`  Current Revenue: $${revenueData.totalRevenue || 0}`);
    console.log(`  Monthly Target: $${revenueData.monthlyTarget || 0}`);
    console.log(`  Gumroad Status: ${revenueData.platforms?.gumroad?.status || 'unknown'}`);
    console.log(`  Products Listed: ${revenueData.platforms?.gumroad?.products || 0}`);
  } catch (e) {
    console.log(`\n💰 REVENUE TRACKING: ❌ Error reading file`);
  }
} else {
  console.log(`\n💰 REVENUE TRACKING: ❌ File not found`);
}

// Check immediate revenue plan
const immediatePlanPath = '/home/wls/.openclaw/workspace/immediate-revenue-action-plan.md';
if (fs.existsSync(immediatePlanPath)) {
  console.log(`\n🚀 LAUNCH PLAN: ✅ Found`);
} else {
  console.log(`\n🚀 LAUNCH PLAN: ❌ Missing`);
}

// Summary
console.log('\n' + '=' .repeat(50));
if (allFilesExist) {
  console.log('✅ PRODUCT FILES: READY FOR UPLOAD');
  console.log('📋 NEXT STEPS:');
  console.log('  1. Follow PAYMENT_INTEGRATION_ACTIVATION_GUIDE.md');
  console.log('  2. Create Gumroad account at gumroad.com');
  console.log('  3. Upload the 4 product files');
  console.log('  4. Configure payment processing');
  console.log('  2. Update revenue-tracking.json with active status');
  console.log('  3. Execute launch plan from immediate-revenue-action-plan.md');
} else {
  console.log('❌ SOME PRODUCT FILES MISSING - PLEASE CHECK');
}
console.log('=' .repeat(50));