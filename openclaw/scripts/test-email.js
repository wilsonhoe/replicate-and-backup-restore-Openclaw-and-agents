const nodemailer = require('nodemailer');
const config = require('../config/email-config.json');

async function testEmail() {
  console.log('🧪 Testing Email Functionality\n');

  const transporter = nodemailer.createTransport(config.email.smtp);

  try {
    // Verify connection
    console.log('📧 Verifying SMTP connection...');
    await transporter.verify();
    console.log('✅ SMTP connection successful\n');

    // Send test email
    console.log('📤 Sending test email...');
    const info = await transporter.sendMail({
      from: config.email.address,
      to: config.email.address,
      subject: 'Lisa Email Test - ' + new Date().toLocaleString(),
      text: 'If you receive this, Lisa email is working!',
      html: '<h3>Lisa Email Setup Successful!</h3><p>OpenClaw email infrastructure is ready.</p>'
    });

    console.log('✅ Email sent:', info.messageId);
    console.log('📨 Check inbox for test email\n');
    return true;
  } catch (error) {
    console.error('❌ Email test failed:', error.message);
    if (error.message.includes('Invalid login')) {
      console.log('\n💡 Hint: Update email-config.json with your Gmail App Password');
    }
    return false;
  }
}

// Run if called directly
if (require.main === module) {
  testEmail();
}

module.exports = { testEmail };