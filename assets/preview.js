'use strict';
document.querySelector('#sample-form').addEventListener('submit', event => {
  event.preventDefault();
  const input = document.querySelector('#project');
  const name = input.value.trim();
  const status = document.querySelector('#sample-status');
  if (!name) { status.textContent = '請輸入專案名稱。'; input.focus(); return; }
  status.textContent = `「${name}」已套用至本次示範。重新整理後即會清除。`;
});
