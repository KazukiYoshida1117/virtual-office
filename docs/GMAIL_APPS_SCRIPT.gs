/**
 * Gmail連携 — Google Apps Script に追加するコード
 * 既存の doPost(e) の switch/if 文の中に、以下の case を追加してください。
 *
 * 追加先: 既存の Apps Script プロジェクト（APPS_SCRIPT_URL と同じもの）
 */

// ─── 既存の doPost 内に追加 ───────────────────────────────────
// 例: if (action === 'gmail_inbox') { return gmailInbox(data); }
//     if (action === 'gmail_draft') { return gmailDraft(data); }

function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  const action = data.action;

  // --- 既存の処理はそのまま残す ---
  // if (action === 'export_research') { ... }
  // if (action === 'notion_sync')     { ... }
  // if (action === 'notion_fetch')    { ... }

  // ↓↓↓ ここから Gmail 用を追加 ↓↓↓
  if (action === 'gmail_inbox') return ContentService
    .createTextOutput(JSON.stringify(gmailInbox(data)))
    .setMimeType(ContentService.MimeType.JSON);

  if (action === 'gmail_draft') return ContentService
    .createTextOutput(JSON.stringify(gmailDraft(data)))
    .setMimeType(ContentService.MimeType.JSON);

  // フォールバック
  return ContentService
    .createTextOutput(JSON.stringify({ success: false, error: 'unknown action' }))
    .setMimeType(ContentService.MimeType.JSON);
}

// ─── Gmail: 受信箱スレッドを取得 ────────────────────────────────
function gmailInbox(data) {
  try {
    const maxThreads = data.maxThreads || 20;
    const threads = GmailApp.getInboxThreads(0, maxThreads);

    const result = threads.map(thread => {
      const msg = thread.getMessages()[thread.getMessageCount() - 1]; // 最新メッセージ
      const body = msg.getPlainBody();
      return {
        threadId: thread.getId(),
        subject:  thread.getFirstMessageSubject(),
        from:     msg.getFrom(),
        date:     Utilities.formatDate(msg.getDate(), Session.getScriptTimeZone(), 'yyyy/MM/dd HH:mm'),
        isUnread: thread.isUnread(),
        body:     body.length > 2000 ? body.substring(0, 2000) + '…' : body
      };
    });

    return { success: true, threads: result };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

// ─── Gmail: 下書き作成 ───────────────────────────────────────────
function gmailDraft(data) {
  try {
    const { to, subject, body, threadId } = data;
    if (!to || !body) return { success: false, error: 'to と body は必須です' };

    GmailApp.createDraft(to, subject || '返信', body);
    return { success: true };
  } catch (e) {
    return { success: false, error: e.message };
  }
}
