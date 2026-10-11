/* Local drafts only. Nothing here publishes comments or supplies product evidence. */
(() => {
  'use strict';
  const KEY = 'connectable-v3-comment-drafts';
  const LIMIT = 300;
  const MAX_PRODUCTS = 30;
  const validId = id => typeof id === 'string' && /^monitor:[a-z0-9-]{1,100}$/.test(id);
  const length = text => [...text].length;
  function read() {
    const raw = localStorage.getItem(KEY);
    if (raw === null) return [];
    if (raw.length > 60000) throw new Error('oversized storage');
    const state = JSON.parse(raw);
    if (!state || state.version !== 1 || Object.keys(state).sort().join(',') !== 'drafts,version' ||
        !Array.isArray(state.drafts) || state.drafts.length > MAX_PRODUCTS) throw new Error('invalid storage');
    const ids = new Set();
    for (const item of state.drafts) {
      if (!item || Object.keys(item).sort().join(',') !== 'productId,text' || !validId(item.productId) ||
          typeof item.text !== 'string' || !item.text.trim() || length(item.text) > LIMIT || ids.has(item.productId)) {
        throw new Error('invalid draft');
      }
      ids.add(item.productId);
    }
    return state.drafts;
  }
  const el = (tag, text, className) => {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (className) node.className = className;
    return node;
  };
  function mount(container, productId) {
    if (!(container instanceof HTMLElement) || !validId(productId)) throw new TypeError('Invalid draft target');
    container.replaceChildren();
    container.classList.add('local-comment-preview');
    container.append(el('h3', '짧은 댓글 초안'));
    container.append(el('p', '이 브라우저에만 저장됩니다. 다른 사람에게 공개되지 않으며, 제품 후기나 공식 근거가 아닙니다.'));
    container.append(el('p', '개인정보를 쓰지 마세요. 암호화되지 않아 같은 브라우저 사용자도 읽을 수 있고, 사이트 데이터 삭제 시 사라집니다.', 'local-comment-privacy'));
    const label = el('label', '댓글 초안 (최대 300자)');
    const input = el('textarea');
    input.rows = 3;
    label.append(input);
    const counter = el('p', '0 / 300자', 'local-comment-counter');
    const actions = el('div', undefined, 'local-comment-actions');
    const save = el('button', '이 브라우저에 초안 저장');
    const remove = el('button', '이 제품 초안 삭제');
    save.type = remove.type = 'button';
    actions.append(save, remove);
    const status = el('p', '', 'local-comment-status');
    status.setAttribute('role', 'status');
    const saved = el('div', undefined, 'local-comment-saved');
    container.append(label, counter, actions, status, saved);
    const render = text => {
      saved.replaceChildren();
      remove.disabled = !text;
      if (text) saved.append(el('strong', '저장된 나의 로컬 초안'), el('p', text));
      else saved.append(el('p', '저장된 초안이 없습니다.'));
    };
    const count = () => {
      counter.textContent = `${length(input.value)} / ${LIMIT}자`;
      input.setAttribute('aria-invalid', String(length(input.value) > LIMIT));
    };
    input.addEventListener('input', count);
    try {
      const draft = read().find(item => item.productId === productId);
      input.value = draft ? draft.text : '';
      count();
      render(input.value);
    } catch {
      status.textContent = '저장소를 읽을 수 없거나 저장 형식이 손상되었습니다. 기존 내용을 덮어쓰지 않습니다. 브라우저 저장 설정을 확인하세요.';
      save.disabled = remove.disabled = true;
    }
    save.addEventListener('click', () => {
      const text = input.value.trim();
      if (!text || length(input.value) > LIMIT) {
        status.textContent = '1~300자로 작성해 주세요. 저장되지 않았습니다.';
        return;
      }
      try {
        const drafts = read().filter(item => item.productId !== productId);
        if (drafts.length >= MAX_PRODUCTS) {
          status.textContent = '최대 30개 제품까지 저장할 수 있습니다. 다른 제품의 초안을 먼저 삭제해 주세요.';
          return;
        }
        drafts.push({productId, text});
        localStorage.setItem(KEY, JSON.stringify({version: 1, drafts}));
        render(text);
        status.textContent = '이 브라우저에 초안을 저장했습니다. 공개되지 않았습니다.';
      } catch {
        status.textContent = '초안을 저장하지 못했습니다. 입력 내용은 이 창에 남아 있습니다.';
      }
    });
    remove.addEventListener('click', () => {
      try {
        const drafts = read().filter(item => item.productId !== productId);
        if (drafts.length) localStorage.setItem(KEY, JSON.stringify({version: 1, drafts}));
        else localStorage.removeItem(KEY);
        input.value = '';
        count();
        render('');
        status.textContent = '이 제품의 로컬 초안을 삭제했습니다.';
      } catch {
        status.textContent = '삭제하지 못했습니다. 저장된 초안은 삭제 완료로 처리하지 않았습니다.';
      }
    });
  }
  window.ConnectableLocalComments = Object.freeze({mount});
})();
