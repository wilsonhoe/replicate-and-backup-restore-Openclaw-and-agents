const { ImapFlow } = require('imapflow');
const config = require('../config/email-config.json');

async function scanInbox() {
  console.log('📬 Scanning Inbox...\n');

  const client = new ImapFlow({
    host: config.email.imap.host,
    port: config.email.imap.port,
    secure: config.email.imap.secure,
    auth: {
      user: config.email.imap.auth.user,
      pass: config.email.imap.auth.pass
    }
  });

  try {
    await client.connect();
    console.log('✅ IMAP connected\n');

    const mailbox = await client.mailboxOpen('INBOX');
    console.log(`📁 Inbox: ${mailbox.exists} messages\n`);

    if (mailbox.exists === 0) {
      console.log('📭 Inbox is empty');
      await client.logout();
      return [];
    }

    // Get last 10 messages
    const messages = [];
    const limit = Math.min(mailbox.exists, 10);
    
    for await (const msg of client.fetch(`${mailbox.exists - limit + 1}:*`, { 
      envelope: true, 
      source: true 
    })) {
      const envelope = msg.envelope;
      messages.push({
        from: envelope.from[0]?.address || 'unknown',
        fromName: envelope.from[0]?.name || '',
        subject: envelope.subject || '(no subject)',
        date: envelope.date,
        id: msg.seq
      });
    }

    console.log('📧 Recent Messages:\n');
    console.log('=' .repeat(80));
    
    for (const msg of messages.reverse()) {
      console.log(`\n[${msg.date}]`);
      console.log(`From: ${msg.fromName} <${msg.from}>`);
      console.log(`Subject: ${msg.subject}`);
      console.log('-'.repeat(80));
    }

    await client.logout();
    return messages;

  } catch (error) {
    console.error('❌ IMAP error:', error.message);
    try { await client.logout(); } catch {}
    return [];
  }
}

// Run if called directly
if (require.main === module) {
  scanInbox();
}

module.exports = { scanInbox };