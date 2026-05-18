/**
 * Delivery — routes formatted digest to configured channel.
 * Supports: stdout (default), Telegram, Email, Feishu.
 */

async function deliver(formatted) {
  const channels = detectChannels();

  if (channels.length === 0) {
    // Default: stdout
    console.log(formatted);
    return;
  }

  for (const channel of channels) {
    switch (channel) {
      case 'telegram':
        await deliverTelegram(formatted);
        break;
      case 'email':
        await deliverEmail(formatted);
        break;
      case 'feishu':
        await deliverFeishu(formatted);
        break;
    }
  }

  // Always also print to stdout
  console.log(formatted);
}

function detectChannels() {
  const channels = [];
  if (process.env.TELEGRAM_BOT_TOKEN && process.env.TELEGRAM_CHAT_ID) {
    channels.push('telegram');
  }
  if (process.env.EMAIL_SMTP_HOST && process.env.EMAIL_TO) {
    channels.push('email');
  }
  if (process.env.FEISHU_WEBHOOK_URL) {
    channels.push('feishu');
  }
  return channels;
}

async function deliverTelegram(formatted) {
  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;
  const url = `https://api.telegram.org/bot${token}/sendMessage`;

  try {
    const resp = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: chatId,
        text: formatted,
        parse_mode: 'Markdown'
      })
    });
    if (resp.ok) {
      console.log('[DELIVERY] Telegram: sent successfully');
    } else {
      console.warn('[DELIVERY] Telegram: failed -', resp.status);
    }
  } catch (e) {
    console.warn('[DELIVERY] Telegram: error -', e.message);
  }
}

async function deliverEmail(formatted) {
  try {
    const nodemailer = require('nodemailer');
    const transporter = nodemailer.createTransport({
      host: process.env.EMAIL_SMTP_HOST,
      port: parseInt(process.env.EMAIL_SMTP_PORT || '587'),
      auth: {
        user: process.env.EMAIL_SMTP_USER,
        pass: process.env.EMAIL_SMTP_PASS
      }
    });

    await transporter.sendMail({
      from: process.env.EMAIL_SMTP_USER,
      to: process.env.EMAIL_TO,
      subject: `Amazon Seller Digest - ${new Date().toISOString().slice(0, 10)}`,
      text: formatted
    });
    console.log('[DELIVERY] Email: sent successfully');
  } catch (e) {
    console.warn('[DELIVERY] Email: error -', e.message);
  }
}

async function deliverFeishu(formatted) {
  const url = process.env.FEISHU_WEBHOOK_URL;
  try {
    const resp = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        msg_type: 'text',
        content: { text: formatted }
      })
    });
    if (resp.ok) {
      console.log('[DELIVERY] Feishu: sent successfully');
    } else {
      console.warn('[DELIVERY] Feishu: failed -', resp.status);
    }
  } catch (e) {
    console.warn('[DELIVERY] Feishu: error -', e.message);
  }
}

module.exports = { deliver };
