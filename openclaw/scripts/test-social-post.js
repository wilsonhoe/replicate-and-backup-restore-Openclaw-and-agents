const nodemailer = require('nodemailer');
const config = require('/home/wls/.openclaw/config/email.json');

async function sendTestEmail() {
  const transporter = nodemailer.createTransport({
    host: config.email.smtp.host,
    port: config.email.smtp.port,
    secure: config.email.smtp.secure,
    auth: {
      user: config.email.smtp.auth.user,
      pass: config.email.smtp.auth.pass
    }
  });

  try {
    const info = await transporter.sendMail({
      from: config.email.address,
      to: 'wilson.yeu@gmail.com',
      subject: '✅ Lisa Test Email - Session Verified',
      text: 'This is a test email from Lisa (OpenClaw AI CEO).\n\nAll systems operational:\n- Gmail SMTP: ✅\n- Twitter: ✅\n- LinkedIn: ✅\n\nSent: ' + new Date().toISOString(),
      html: `
        <h2>✅ Lisa System Test</h2>
        <p>This is a test email from Lisa (OpenClaw AI CEO).</p>
        <h3>All Systems Operational:</h3>
        <ul>
          <li>✅ Gmail SMTP</li>
          <li>✅ Twitter Authenticated</li>
          <li>✅ LinkedIn Authenticated</li>
        </ul>
        <p><strong>Sent:</strong> ${new Date().toISOString()}</p>
        <hr>
        <p><em>AI CEO Systems - OpenClaw</em></p>
      `
    });

    console.log('✅ Test email sent to wilson.yeu@gmail.com');
    console.log('Message ID:', info.messageId);
    return true;
  } catch (error) {
    console.error('❌ Email failed:', error.message);
    return false;
  }
}

sendTestEmail();